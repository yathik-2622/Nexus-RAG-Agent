import streamlit as st
import os
import time
from dotenv import load_dotenv

# Import our custom logic
from src.components.ingestion import ingest_file
from src.components.graph import build_graph
from src.utils.logger import get_logs

# Load environment variables
load_dotenv()

# --- Configuration ---
RAW_DATA_DIR = "./data/raw_documents"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# --- Page Configuration ---
st.set_page_config(
    page_title="Nexus Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "LangSmith-like" Feel ---
st.markdown("""
<style>
    /* Remove top padding */
    .block-container {
        padding-top: 2rem;
    }
    /* Chat bubbles */
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #41444C;
    }
    /* Status indicators */
    .stStatusWidget {
        background-color: #0E1117;
        border: 1px solid #41444C;
    }
</style>
""", unsafe_allow_html=True)

# --- Title and Header ---
st.title("⚡ Nexus Agent")
st.caption("Orchestrated by **LangGraph** | Powered by **Groq** | Memory by **Qdrant**")

# --- Session State ---
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

# --- Sidebar ---
with st.sidebar:
    st.header("🗂️ Knowledge Base")
    st.info(f"Storage: `{RAW_DATA_DIR}/`")
    
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt", "docx", "csv"])
    
    if uploaded_file:
        if st.button("🚀 Ingest Document", type="primary"):
            with st.spinner("Processing & Embedding..."):
                try:
                    file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    ingest_file(file_path)
                    st.toast(f"✅ Indexed {uploaded_file.name} successfully!", icon="🎉")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("### 💾 Stored Files")
    if os.path.exists(RAW_DATA_DIR):
        files = os.listdir(RAW_DATA_DIR)
        if files:
            for f in files:
                st.caption(f"📄 {f}")
        else:
            st.caption("Empty repository.")

# --- Helper: Typewriter Effect Generator ---
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# --- Main Layout ---
tab1, tab2 = st.tabs(["💬 Conversation", "🛠️ Internals & Traces"])

# --- Tab 1: Chat ---
with tab1:
    # Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask about the weather or your docs..."):
        # User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant Message (with Streaming Status)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # The "Gemini-like" Status Container
            with st.status("🧠 **Thinking...**", expanded=True) as status:
                
                try:
                    st.write("🔄 Analyzing intent...")
                    
                    # Run Graph in Stream Mode
                    # We use graph.stream to get events as they happen
                    final_generation = ""
                    
                    for event in graph.stream({"question": prompt}):
                        
                        # Event: Decision / Routing
                        if "retrieve" in event:
                            status.update(label="📚 **Routing to Knowledge Base**", state="running")
                            st.write("🔍 Searching vector database for context...")
                            st.session_state.last_step = "Retrieval"
                            st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                            
                        elif "weather_search" in event:
                            status.update(label="🌤️ **Routing to Weather Tool**", state="running")
                            st.write("🌍 Connecting to OpenWeatherMap API...")
                            st.session_state.last_step = "Weather API"
                            
                        elif "generate" in event:
                            status.update(label="⚡ **Generating Answer**", state="running")
                            st.write("✏️ Synthesizing response...")
                            final_generation = event["generate"]["generation"]
                    
                    # Final Update
                    status.update(label="✅ **Complete**", state="complete", expanded=False)
                    
                    # Show the final answer with typewriter effect
                    message_placeholder.write_stream(stream_text(final_generation))
                    
                    # Save to history
                    st.session_state.messages.append({"role": "assistant", "content": final_generation})

                except Exception as e:
                    status.update(label="❌ **Error**", state="error")
                    st.error(f"Agent failed: {e}")

# --- Tab 2: Internals ---
with tab2:
    st.header("⚙️ Execution Trace")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Decision Path")
        if st.session_state.last_step:
            if st.session_state.last_step == "Weather API":
                st.info("Route: **WEATHER API**")
            else:
                st.success("Route: **RAG RETRIEVAL**")
        else:
            st.write("No traces yet.")

    with col2:
        st.subheader("Retrieved Context (RAG)")
        if st.session_state.last_retrieved_docs:
            for i, doc in enumerate(st.session_state.last_retrieved_docs):
                # Handle different document types
                content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                with st.expander(f"📄 Chunk {i+1} (Source: {doc.metadata.get('source', 'unknown') if hasattr(doc, 'metadata') else 'API'})"):
                    st.code(content)
        else:
            st.caption("No documents retrieved for this query.")

    st.markdown("---")
    st.subheader("📜 System Logs")
    logs = get_logs()
    st.code(logs, language="log")