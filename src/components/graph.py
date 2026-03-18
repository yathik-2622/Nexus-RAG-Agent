# Import TypedDict for the state definition
from typing import TypedDict, List
# Import LangGraph components
from langgraph.graph import END, StateGraph
# Import LangChain message types
from langchain_core.messages import HumanMessage, AIMessage
# Import ChatGroq for the generation step
from langchain_groq import ChatGroq
# Import string output parser
from langchain_core.output_parsers import StrOutputParser
# Import the prompt template
from langchain_core.prompts import PromptTemplate
# Import os for environment variables
import os

# Load environment variables from .env file
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

# Import our custom components
from src.components.ingestion import get_retriever
from src.components.tools import get_weather_data
from src.components.router import get_router_chain
from src.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# --- 1. Define the Agent State ---
class AgentState(TypedDict):
    # The question asked by the user
    question: str
    # The generated answer
    generation: str
    # The list of retrieved documents (if RAG is used)
    documents: List[str]
    # The decision made by the router (for debugging/UI)
    step: str

# --- 2. Define the Nodes ---

def retrieve(state: AgentState):
    # Node: Retrieve documents from Qdrant
    
    logger.info("---NODE: RETRIEVE---")
    question = state["question"]
    
    try:
        # Get the retriever connected to local Qdrant
        retriever = get_retriever()
        # Fetch relevant documents
        documents = retriever.invoke(question)
        
        # Log the number of docs found
        logger.info(f"Retrieved {len(documents)} documents from Qdrant.")
        
        # Return the updated state
        return {"documents": documents, "step": "retrieval"}
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        return {"documents": [], "step": "retrieval_failed"}

def weather_search(state: AgentState):
    # Node: Fetch weather data
    
    logger.info("---NODE: WEATHER SEARCH---")
    question = state["question"]
    
    # Extract city using a simple heuristic or LLM (Here assuming city is in query)
    # For a robust production app, we'd use an extraction chain. 
    # For this assignment, we pass the whole query or extraction logic.
    # Let's use the LLM to extract the city for better accuracy.
    groq_model = os.getenv("GROQ_MODEL_NAME", "")
    llm = ChatGroq(model=groq_model, temperature=0)
    
    # Prompt to extract city name only
    system_prompt = "Extract only the city name from the user's query about weather. Return nothing else."
    city_extraction = llm.invoke([("system", system_prompt), ("user", question)]).content.strip()
    
    logger.info(f"Extracted city: {city_extraction}")
    
    # Call the tool
    weather_result = get_weather_data(city_extraction)
    
    # Return result wrapped as a Document-like string for the generator to consume
    return {"documents": [weather_result], "step": "weather_api"}

def generate(state: AgentState):
    # Node: Generate the final answer using retrieved data
    
    logger.info("---NODE: GENERATE---")
    question = state["question"]

    # FIX: Use .get() to avoid the 'documents' KeyError
    # If the key is missing (like in general chat), it defaults to an empty list []
    documents = state.get("documents", [])
    # documents = state["documents"]
    
    # Initialize the LLM
    groq_model = os.getenv("GROQ_MODEL_NAME", "")
    llm = ChatGroq(model=groq_model, temperature=0)
    
    # Define the RAG prompt
    # prompt = PromptTemplate(
    #     template="""You are the 'Rystudios Nexus Agent', a helpful and professional AI assistant.
        
    #     Capabilities:
    #     - You can answer general questions and greetings.
    #     - You can fetch real-time weather using your weather tool.
    #     - You can search through uploaded documents to provide specific answers.
        
    #     If the user asks who you are or what you can do, explain these capabilities.
    #     Use the following context to answer if available. If no context exists and it's not a greeting, say you don't know.
        
    #     Context: {context} 
    #     Question: {question} 
    #     Answer:""",
    #     input_variables=["question", "context"],
    # )
    prompt = PromptTemplate(
        template="""You are the 'RyStudios Nexus Agent', a helpful and professional AI assistant.
        
        Capabilities:
        - You can answer general questions, greet users, and explain who you are.
        - You can fetch real-time weather for any city.
        - You can analyze uploaded documents to answer specific questions.
        
        If the user asks for your name or what you can do, introduce yourself as RyStudios Nexus Agent and list your capabilities clearly.
        
        Use the following context to answer if relevant. If no context exists and it's not a general greeting, say you don't know.
        
        Context: {context}
        Question: {question}
        Answer:""",
        input_variables=["question", "context"],
    )
    # prompt = PromptTemplate(
    #     template="""You are an assistant for question-answering tasks. 
    #     Use the following pieces of retrieved context to answer the question. 
    #     If you don't know the answer, just say that you don't know. 
        
    #     Question: {question} 
        
    #     Context: {context} 
        
    #     Answer:""",
    #     input_variables=["question", "context"],
    # )
    
    # Create the chain
    rag_chain = prompt | llm | StrOutputParser()
    
    # Run the chain
    generation = rag_chain.invoke({"context": documents, "question": question})
    
    logger.info("Generated final response.")
    return {"generation": generation}

# --- 3. Define the Routing Logic ---

def route_question(state: AgentState):
    # Conditional Edge: Decides where to go next
    
    logger.info("---DECISION: ROUTING---")
    question = state["question"]
    
    # Get the router chain
    router = get_router_chain()
    # Predict the route
    source = router.invoke(question)
    
    logger.info(f"Router decided to route to: {source.datasource}")
    
    # Return the node name to visit next
    if source.datasource == "weather_api":
        return "weather_search"
    elif source.datasource == "vectorstore":
        return "retrieve"
    else:
        # For general chat or unrecognized, we can default to generation without context
        return "generate"

# --- 4. Build the Graph ---

def build_graph():
    # Initialize the StateGraph
    workflow = StateGraph(AgentState)

    # Add the nodes
    workflow.add_node("weather_search", weather_search)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)

    # Add the Conditional Entry Point (The Router)
    # The flow starts at the router, which points to either 'weather_search' or 'retrieve'
    workflow.set_conditional_entry_point(
        route_question,
        {
            "weather_search": "weather_search",
            "retrieve": "retrieve",
            "generate": "generate",  # For general chat or fallback
        },
    )

    # Add edges from tools to the generator
    # After getting data (weather or docs), go to generate
    workflow.add_edge("weather_search", "generate")
    workflow.add_edge("retrieve", "generate")
    
    # End the workflow after generation
    workflow.add_edge("generate", END)

    # Compile the graph
    app = workflow.compile()
    
    logger.info("LangGraph compiled successfully.")
    return app