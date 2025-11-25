# Import Streamlit for the UI
import streamlit as st
# Import os to manage file paths
import os
# Import dotenv to load API keys
from dotenv import load_dotenv

# Import our custom logic
from src.components.ingestion import ingest_file
from src.components.graph import build_graph
from src.utils.logger import get_logs

# Load environment variables (API keys)
load_dotenv()

# --- Configuration ---
RAW_DATA_DIR = "./data/raw_documents"
# Ensure the directory exists
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# --- Page Configuration ---
st.set_page_config(
    page_title="Nexus Agent: RAG & Weather",
    page_icon="🤖",
    layout="wide"
)

# --- Title and Header ---
st.title("🤖 Nexus Agent: RAG + Weather")
st.markdown(
    """
    **Intelligent Routing:** Automatically switches between:
    - 🌤️ **Weather API** (Real-time data)
    - 📚 **Local Knowledge Base** (Your uploaded docs)
    """
)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_retrieved_docs" not in st.session_state:
    st.session_state.last_retrieved_docs = []

if "last_step" not in st.session_state:
    st.session_state.last_step = None

# --- Cache the Graph ---
@st.cache_resource
def load_agent_graph():
    return build_graph()

graph = load_agent_graph()

# --- Sidebar: Knowledge Base ---
with st.sidebar:
    st.header("📂 Knowledge Base (Admin)")
    st.info(f"Files are saved permanently to:\n`{RAW_DATA_DIR}/`")
    
    # File uploader widget
    uploaded_file = st.file_uploader("Upload New Document", type=["pdf", "txt", "docx", "csv"])
    
    # Process the file if uploaded
    if uploaded_file:
        if st.button("Save & Ingest Document"):
            with st.spinner("Saving file and indexing..."):
                try:
                    # 1. Define permanent path
                    file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
                    
                    # 2. Save the file to disk (Permanent Storage)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # 3. Ingest into Qdrant
                    ingest_file(file_path)
                    
                    st.success(f"✅ Saved to {uploaded_file.name} & Indexed!")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### 🗃️ Stored Files")
    # Simple Admin View: List files in the directory
    if os.path.exists(RAW_DATA_DIR):
        files = os.listdir(RAW_DATA_DIR)
        if files:
            for f in files:
                st.caption(f"📄 {f}")
        else:
            st.caption("No files uploaded yet.")

# --- Main Layout: Tabs ---
tab1, tab2 = st.tabs(["💬 Chat Interface", "⚙️ Internals & Logs"])

# --- Tab 1: Chat Interface ---
with tab1:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask about weather or documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = graph.invoke({"question": prompt})
                    final_answer = response.get("generation", "No response generated.")
                    
                    # Update State for Debugging
                    st.session_state.last_step = response.get("step", "unknown")
                    st.session_state.last_retrieved_docs = response.get("documents", [])
                    
                    st.markdown(final_answer)
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# --- Tab 2: Internals (Logs) ---
with tab2:
    st.header("🔧 System Internals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Decision Logic")
        if st.session_state.last_step:
            st.info(f"Last Route: **{st.session_state.last_step.upper()}**")
        else:
            st.write("No actions taken yet.")

    with col2:
        st.subheader("Retrieved Context")
        if st.session_state.last_retrieved_docs:
            for i, doc in enumerate(st.session_state.last_retrieved_docs):
                content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                with st.expander(f"Chunk {i+1}"):
                    st.write(content)
        else:
            st.caption("No context retrieved.")

    st.subheader("📝 Live System Logs")
    logs = get_logs()
    st.code(logs, language="log")