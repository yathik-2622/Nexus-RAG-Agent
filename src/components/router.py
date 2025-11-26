# Import Literal for type safety in routing
from typing import Literal
# Import Pydantic BaseModel/Field for structured output
from pydantic import BaseModel, Field # Use standard Pydantic import
# Import ChatGroq for the LLM
from langchain_groq import ChatGroq

# Import os for environment variables
import os

# Load environment variables from .env file
from dotenv import load_dotenv


# Initialize environment variables
load_dotenv()

# Import our logger
from src.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Define the structure for the router's output
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    
    # The 'datasource' field must be either 'vectorstore' or 'weather_api'
    datasource: Literal["vectorstore", "weather_api"] = Field(
        ...,
        description="Given a user question choose to route it to weather_api or a vectorstore.",
    )

def get_router_chain():
    # Function to create the routing chain
    
    # Initialize the Groq LLM
    # temperature=0 ensures deterministic (consistent) routing
    groq_model = os.getenv("GROQ_MODEL_NAME", "")
    llm = ChatGroq(model=groq_model, temperature=0)
    
    # Bind the structured output model to the LLM
    # This forces the LLM to return strictly the RouteQuery format
    structured_llm_router = llm.with_structured_output(RouteQuery)
    
    # Log that the router is ready
    logger.info("Router chain initialized with Groq Llama-3.")
    
    # Return the runnable chain
    return structured_llm_router