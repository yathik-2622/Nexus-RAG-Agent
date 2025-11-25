# Import Streamlit for the UI
import streamlit as st
# Import os to manage file paths
import os
# Import tempfile to handle uploaded files safely
import tempfile
# Import dotenv to load API keys
from dotenv import load_dotenv

# Import our custom logic
from src.components.ingestion import ingest_file
from src.components.graph import build_graph
from src.utils.logger import get_logs

# Load environment variables (API keys)
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Agent: RAG & Weather",
    page_icon="🤖",
    layout="wide"  # Use wide mode to have space for logs
)

# --- Title and Header ---
st.title("🤖 Intelligent Agent: RAG + Weather")
st.markdown(
    """
    This agent uses **LangGraph** to decide between tools:
    - **OpenWeatherMap** for real-time weather.
    - **Local RAG (Qdrant)** for document questions.
    """
)

# --- Session State Initialization ---
# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize state to track retrieved documents for display
if "last_retrieved_docs" not in st.session_state:
    st.session_state.last_retrieved_docs = []

# Initialize state to track the last agent step/decision
if "last_step" not in st.session_state:
    st.session_state.last_step = None

# --- Cache the Graph ---
# We use cache_resource so we don't rebuild the graph on every UI interaction
@st.cache_resource
def load_agent_graph():
    return build_graph()

# Load the graph
graph = load_agent_graph()

# --- Sidebar: File Ingestion ---
with st.sidebar:
    st.header("📂 Knowledge Base")
    st.info("Upload a document (PDF, TXT, DOCX) to enable RAG.")
    
    # File uploader widget
    uploaded_file = st.file_uploader("Upload File", type=["pdf", "txt", "docx", "csv"])
    
    # Process the file if uploaded
    if uploaded_file:
        # Create a button to trigger ingestion
        if st.button("Ingest Document"):
            with st.spinner("Ingesting and Embedding..."):
                try:
                    # Save uploaded file to a temporary file on disk
                    # This is necessary because LangChain loaders need a file path
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Run the ingestion logic
                    ingest_file(tmp_path)
                    
                    # Clean up the temp file
                    os.remove(tmp_path)
                    
                    st.success("✅ File ingested into Local Qdrant DB!")
                except Exception as e:
                    st.error(f"Error ingesting file: {e}")

# --- Main Layout: Tabs ---
# Create two tabs: one for the conversation, one for debugging/logs
tab1, tab2 = st.tabs(["💬 Chat", "⚙️ Internals (Logs & Steps)"])

# --- Tab 1: Chat Interface ---
with tab1:
    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask about the weather or your document..."):
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Invoke the LangGraph agent
                    # The input state matches the AgentState definition in graph.py
                    response = graph.invoke({"question": prompt})
                    
                    # Extract the generation (final answer)
                    final_answer = response.get("generation", "No response generated.")
                    
                    # Extract internal state for visualization in Tab 2
                    st.session_state.last_step = response.get("step", "unknown")
                    st.session_state.last_retrieved_docs = response.get("documents", [])
                    
                    # Display the answer
                    st.markdown(final_answer)
                    
                    # Add assistant response to history
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# --- Tab 2: Internals (Logs & Debugging) ---
with tab2:
    st.header("🔧 Agent Diagnostics")
    
    # Section 1: Agent Decision Path
    st.subheader("1️⃣ Decision Logic")
    if st.session_state.last_step:
        st.info(f"Last Route Taken: **{st.session_state.last_step.upper()}**")
        if st.session_state.last_step == "weather_api":
             st.markdown("👉 The Agent decided this was a **Weather** query.")
        elif st.session_state.last_step == "retrieval":
             st.markdown("👉 The Agent decided this was a **Document** query.")
    else:
        st.write("No actions taken yet.")

    # Section 2: Retrieved Context (RAG only)
    st.subheader("2️⃣ Retrieved Context (RAG)")
    if st.session_state.last_retrieved_docs:
        # If documents exist, show them in an expander
        for i, doc in enumerate(st.session_state.last_retrieved_docs):
            # Check if it's a Document object (RAG) or string (Weather)
            content = doc.page_content if hasattr(doc, 'page_content') else doc
            with st.expander(f"Chunk {i+1}"):
                st.write(content)
    else:
        st.write("No documents retrieved for the last query.")

    # Section 3: Live System Logs
    st.subheader("3️⃣ System Logs")
    # Fetch logs from the memory buffer
    logs = get_logs()
    # Display logs in a code block for readability
    st.code(logs, language="log")