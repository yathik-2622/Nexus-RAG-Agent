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
    initial_sidebar_state="collapsed" # Collapsed for cleaner look
)

# --- 🎨 CUSTOM CSS FOR "WHATSAPP/CHATGPT" STYLE ---
st.markdown("""
<style>
    /* 1. Force the chat input to the bottom (Standard Streamlit behavior, but reinforced) */
    .stChatInput {
        position: fixed;
        bottom: 0;
        width: 100%;
        z-index: 1000;
    }
    
    /* 2. User Message: Align Right, Blue Background */
    [data-testid="stChatMessage"]:nth-child(odd) {
        flex-direction: row-reverse;
        text-align: right;
        background-color: #005c4b; /* WhatsApp Green-ish / Dark Blue */
        border: none;
    }
    
    /* 3. Agent Message: Align Left, Dark Gray Background */
    [data-testid="stChatMessage"]:nth-child(even) {
        flex-direction: row;
        text-align: left;
        background-color: #202c33; /* Dark Gray */
        border: none;
    }
    
    /* 4. Hide the avatars if you want a cleaner look (optional, keeping them for now) */
    /* [data-testid="chatAvatarIcon"] { display: none; } */
    
    /* 5. Adjust padding for the main container to allow scrolling */
    .block-container {
        padding-bottom: 150px; /* Space for the input box */
    }
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("⚡ Nexus Agent")

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

# --- Sidebar (Cleaned Up) ---
with st.sidebar:
    st.header("📂 Knowledge Base")
    # Cleaned up: No list of files, no "permanent path" text.
    
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt", "docx", "csv"])
    
    if uploaded_file:
        if st.button("🚀 Ingest Document", type="primary"):
            with st.spinner("Processing..."):
                try:
                    # Save silently in background
                    file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    ingest_file(file_path)
                    st.success("✅ Document added to knowledge base.")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- Helper: Streaming Effect ---
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# --- Main Layout ---
tab1, tab2 = st.tabs(["💬 Chat", "🛠️ Internals"])

# --- Tab 1: Chat Interface ---
with tab1:
    # 1. Render History first (Scrollable area)
    for message in st.session_state.messages:
        role = message["role"]
        # Custom avatars
        avatar = "👤" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

    # 2. Chat Input (Fixed at bottom)
    if prompt := st.chat_input("Type your message..."):
        # User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Assistant Message
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            
            # Status Container (The "Thinking" part)
            with st.status("🧠 **Thinking...**", expanded=True) as status:
                try:
                    final_generation = ""
                    
                    # Stream the Graph Events
                    for event in graph.stream({"question": prompt}):
                        
                        # Handle RAG Step
                        if "retrieve" in event:
                            status.update(label="📚 **Checking Documents**", state="running")
                            st.write("Reading knowledge base...")
                            st.session_state.last_step = "Retrieval"
                            st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                            
                        # Handle Weather Step
                        elif "weather_search" in event:
                            status.update(label="🌤️ **Checking Weather**", state="running")
                            st.write("Calling Weather API...")
                            st.session_state.last_step = "Weather API"
                            # For weather, the 'documents' key holds the API string response
                            st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
                            
                        # Handle Generation Step
                        elif "generate" in event:
                            status.update(label="⚡ **Synthesizing**", state="running")
                            final_generation = event["generate"]["generation"]
                    
                    # Complete
                    status.update(label="✅ **Complete**", state="complete", expanded=False)
                    
                    # Stream the final answer
                    message_placeholder.write_stream(stream_text(final_generation))
                    st.session_state.messages.append({"role": "assistant", "content": final_generation})

                except Exception as e:
                    status.update(label="❌ **Error**", state="error")
                    st.error(f"Agent failed: {e}")

# --- Tab 2: Internals (Logic Updated) ---
with tab2:
    st.header("⚙️ Execution Trace")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Routing Decision")
        if st.session_state.last_step:
            if st.session_state.last_step == "Weather API":
                st.info("The Agent chose: **WEATHER TOOL**")
            else:
                st.success("The Agent chose: **DOCUMENT RETRIEVAL**")
        else:
            st.write("No actions taken yet.")

    with col2:
        # LOGIC UPDATE: Differentiate Weather vs RAG display
        if st.session_state.last_step == "Weather API":
            st.subheader("🌤️ Weather API Response")
            # Weather tool returns a list with 1 string usually
            if st.session_state.last_retrieved_docs:
                st.code(st.session_state.last_retrieved_docs[0], language="json")
            else:
                st.caption("No data returned.")
                
        elif st.session_state.last_step == "Retrieval":
            st.subheader("📄 Retrieved Document Chunks")
            if st.session_state.last_retrieved_docs:
                for i, doc in enumerate(st.session_state.last_retrieved_docs):
                    # Handle document objects safely
                    content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                    meta = doc.metadata if hasattr(doc, 'metadata') else {}
                    source = meta.get('source', 'Uploaded Doc')
                    
                    with st.expander(f"Chunk {i+1} (Source: {os.path.basename(source)})"):
                        st.text(content)
            else:
                st.caption("No relevant documents found.")
        else:
            st.subheader("🔍 Context")
            st.write("Waiting for query...")

    st.markdown("---")
    st.subheader("📜 System Logs")
    logs = get_logs()
    st.code(logs, language="log")