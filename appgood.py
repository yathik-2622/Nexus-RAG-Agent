# import streamlit as st
# import os
# import time
# import json
# from dotenv import load_dotenv

# # Import our custom logic
# from src.components.ingestion import ingest_file
# from src.components.graph import build_graph
# from src.utils.logger import get_logs

# # Load environment variables
# load_dotenv()

# # --- Configuration ---
# RAW_DATA_DIR = "./data/raw_documents"
# os.makedirs(RAW_DATA_DIR, exist_ok=True)

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="Nexus Agent",
#     page_icon="⚡",
#     layout="wide",
#     initial_sidebar_state="expanded" # FORCED OPEN
# )

# # --- 🎨 FINAL CSS FIXES ---
# st.markdown("""
# <style>
#     /* 1. Header Bar Styling (Fixed Top) */
#     .fixed-header {
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 3.5rem;
#         background-color: #0E1117; /* Match App BG */
#         border-bottom: 1px solid #262730;
#         z-index: 9999;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
#     .header-text {
#         font-size: 1.5rem;
#         font-weight: 700;
#         color: #ECECF1;
#         letter-spacing: 1px;
#         margin: 0;
#     }
    
#     /* Push content down so it doesn't hide behind header */
#     .block-container {
#         padding-top: 4rem; 
#         padding-bottom: 6rem;
#     }

#     /* 2. Chat Input (Fixed Bottom) */
#     .stChatInput {
#         position: fixed;
#         bottom: 20px;
#         left: 50%;
#         transform: translateX(-50%);
#         width: 70%;
#         z-index: 1000;
#     }

#     /* 3. USER Message: RIGHT ALIGN | NO BACKGROUND */
#     [data-testid="stChatMessage"]:nth-child(odd) {
#         flex-direction: row-reverse; /* Icon on right */
#         background-color: transparent !important;
#         border: none;
#     }
#     [data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stMarkdownContainer"] {
#         text-align: right;
#         background-color: transparent !important;
#         color: #ECECF1;
#     }

#     /* 4. AGENT Message: LEFT ALIGN | NO BACKGROUND */
#     [data-testid="stChatMessage"]:nth-child(even) {
#         flex-direction: row; /* Icon on left */
#         background-color: transparent !important;
#         border: none;
#     }
#     [data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"] {
#         text-align: left;
#         background-color: transparent !important;
#         color: #ECECF1;
#     }

#     /* 5. Hide default Streamlit header */
#     header {visibility: hidden;}
    
#     /* 6. Thinking Process Box */
#     .stStatusWidget {
#         background-color: #121212;
#         border: 1px solid #333;
#         width: 100%;
#     }
    
#     /* 7. Avatar Styling */
#     .stChatMessage .stAvatar {
#         background-color: #333;
#     }

# </style>
# """, unsafe_allow_html=True)

# # --- Custom Header Render ---
# st.markdown("""
# <div class="fixed-header">
#     <div class="header-text">⚡ NEXUS AGENT</div>
# </div>
# """, unsafe_allow_html=True)

# # --- Session State ---
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "last_retrieved_docs" not in st.session_state:
#     st.session_state.last_retrieved_docs = []
# if "last_step" not in st.session_state:
#     st.session_state.last_step = None

# # --- Cache Graph ---
# @st.cache_resource
# def load_agent_graph():
#     return build_graph()
# graph = load_agent_graph()

# # --- Helper: Stream Text ---
# def stream_text(text):
#     for word in text.split(" "):
#         yield word + " "
#         time.sleep(0.02)

# # --- SIDEBAR (Explicitly defined) ---
# with st.sidebar:
#     st.markdown("### 📥 Knowledge Base")
#     uploaded_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt", "docx"], label_visibility="collapsed")
    
#     if uploaded_file:
#         if st.button("Embed & Ingest", type="primary", use_container_width=True):
#             with st.spinner("Processing..."):
#                 try:
#                     file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
#                     with open(file_path, "wb") as f:
#                         f.write(uploaded_file.getbuffer())
                    
#                     ingest_file(file_path)
#                     st.success("Indexed successfully!")
#                 except Exception as e:
#                     st.error(f"Error: {e}")
    
#     st.divider()
#     st.caption("System Status: Online 🟢")

# # --- MAIN TABS ---
# tab_chat, tab_logs = st.tabs(["💬 Chat Stream", "🔧 System Internals"])

# with tab_chat:
#     # 1. History
#     for message in st.session_state.messages:
#         role = message["role"]
#         content = message["content"]
#         steps = message.get("steps", [])
        
#         with st.chat_message(role, avatar="👤" if role == "user" else "⚡"):
#             st.markdown(content)
#             if role == "assistant" and steps:
#                 with st.expander("Process Completed (View Steps)"):
#                     for step in steps:
#                         st.markdown(f"- {step}")

#     # 2. Input
#     if prompt := st.chat_input("Ask a question..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         st.rerun()

#     # 3. Generation
#     if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
#         with st.chat_message("assistant", avatar="⚡"):
#             response_placeholder = st.empty()
#             steps_log = [] 
            
#             # Status (Thinking...)
#             with st.status("🧠 **Processing Query...**", expanded=True) as status:
#                 try:
#                     final_text = ""
#                     st.session_state.last_step = None
#                     st.session_state.last_retrieved_docs = []

#                     for event in graph.stream({"question": st.session_state.messages[-1]["content"]}):
                        
#                         if "retrieve" in event:
#                             status.write("📚 Searching Knowledge Base...")
#                             steps_log.append("Router: Selected RAG Path")
#                             st.session_state.last_step = "Retrieval"
#                             st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                            
#                         elif "weather_search" in event:
#                             status.write("🌤️ Calling Weather API...")
#                             steps_log.append("Router: Selected Weather Tool")
#                             st.session_state.last_step = "Weather API"
#                             st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
                            
#                         elif "generate" in event:
#                             status.write("⚡ Synthesizing Answer...")
#                             steps_log.append("LLM: Generating Response")
#                             final_text = event["generate"]["generation"]
                    
#                     status.update(label="✅ **Process Completed**", state="complete", expanded=False)
                    
#                     # Stream Text Left-to-Right
#                     response_placeholder.write_stream(stream_text(final_text))
                    
#                     # Save
#                     st.session_state.messages.append({
#                         "role": "assistant", 
#                         "content": final_text,
#                         "steps": steps_log
#                     })

#                 except Exception as e:
#                     status.update(label="❌ Failed", state="error")
#                     st.error(str(e))

# # --- INTERNALS TAB ---
# with tab_logs:
#     st.subheader("System Internals")
    
#     if st.session_state.last_step == "Weather API":
#         st.info("Route: **Weather API**")
#         st.markdown("#### 🌤️ OpenWeatherMap Response")
#         if st.session_state.last_retrieved_docs:
#             st.code(st.session_state.last_retrieved_docs[0], language="json")
    
#     elif st.session_state.last_step == "Retrieval":
#         st.success("Route: **RAG (Vector DB)**")
#         st.markdown("#### 📚 RAG Document Chunks")
#         if st.session_state.last_retrieved_docs:
#             for i, doc in enumerate(st.session_state.last_retrieved_docs):
#                 with st.expander(f"Chunk {i+1}"):
#                     st.text(doc.page_content)
#     else:
#         st.caption("No active logs.")

#     st.divider()
#     with st.expander("Raw Logs"):
#         st.code(get_logs())


import streamlit as st
import os
import time
import json
from dotenv import load_dotenv
import streamlit.components.v1 as components

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

# --- 🔄 Auto-Scroll JavaScript Helper ---
def scroll_to_bottom():
    js = """
    <script>
        var body = window.parent.document.querySelector(".main .block-container");
        body.scrollTop = body.scrollHeight;
    </script>
    """
    components.html(js, height=0)

# --- 🎨 FINAL CSS (WhatsApp Style + Visible Header) ---
st.markdown("""
<style>
    /* 1. Global Layout */
    .block-container {
        padding-top: 5rem; /* Space for the new Fixed Header */
        padding-bottom: 5rem; /* Space for Fixed Input */
        max-width: 1000px;
    }

    /* 2. Fixed 'Contact Bar' Header (The Title) */
    .fixed-header {
        position: fixed;
        top: 3rem; /* Sits just below the Streamlit native top bar */
        left: 0;
        right: 0;
        width: 100%;
        height: 3.5rem;
        background-color: #0E1117; /* Matches background */
        z-index: 99;
        border-bottom: 1px solid #333;
        display: flex;
        align-items: center;
        padding-left: 5rem; /* Align with text */
    }
    
    .header-text {
        font-size: 1.2rem;
        font-weight: 700;
        color: #00ADB5; /* Teal accent color */
        margin-left: 20px;
    }

    /* 3. Chat Input (Fixed Bottom) */
    .stChatInput {
        position: fixed;
        bottom: 0px;
        left: 0;
        right: 0;
        padding-bottom: 20px;
        padding-top: 10px;
        background-color: #0E1117;
        z-index: 1000;
        width: 100%;
        display: flex;
        justify-content: center;
        border-top: 1px solid #333;
    }
    
    .stChatInput > div {
        width: 70% !important; 
        max-width: 800px;
    }

    /* 4. WHATSAPP STYLE - USER (Right Side) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        flex-direction: row-reverse;
        background-color: transparent;
        margin-bottom: 10px;
    }
    
    [data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stMarkdownContainer"] {
        background-color: #2F2F2F; /* Dark Grey */
        color: white;
        padding: 10px 16px;
        border-radius: 15px 15px 0 15px; /* Rounded top-left, top-right, bottom-left */
        text-align: left;
        margin-left: auto;
        width: fit-content;
        max-width: 75%;
        border: 1px solid #444;
    }

    /* 5. WHATSAPP STYLE - AGENT (Left Side) */
    [data-testid="stChatMessage"]:nth-child(even) {
        flex-direction: row;
        background-color: transparent;
        margin-bottom: 10px;
    }
    
    [data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"] {
        background-color: #1A1A1A; /* Black/Darker Grey */
        color: #ECECF1;
        padding: 10px 16px;
        border-radius: 0 15px 15px 15px; /* Rounded top-right, bottom-right, bottom-left */
        margin-right: auto;
        width: fit-content;
        max-width: 85%;
        border: 1px solid #333;
    }

    /* 6. Status Widget Tweaks */
    .stStatusWidget {
        background-color: #111;
        border: 1px solid #333;
        max-width: 85%; /* Match agent bubble width roughly */
    }
    
</style>
""", unsafe_allow_html=True)

# --- RENDER: Fixed Header (HTML) ---
st.markdown("""
    <div class="fixed-header">
        <span class="header-text">⚡ NEXUS AGENT</span>
    </div>
""", unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_retrieved_docs" not in st.session_state:
    st.session_state.last_retrieved_docs = []
if "last_step" not in st.session_state:
    st.session_state.last_step = None

# --- Cache Graph ---
@st.cache_resource
def load_agent_graph():
    return build_graph()
graph = load_agent_graph()

# --- Helper: Stream Text ---
def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# --- SIDEBAR ---
with st.sidebar:
    # Also put title here for completeness
    st.title("⚡ Nexus Agent")
    st.markdown("---")
    st.subheader("📥 Knowledge Base")
    uploaded_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt", "docx"], label_visibility="collapsed")
    
    if uploaded_file:
        if st.button("⚡ Embed & Ingest", type="primary", use_container_width=True):
            with st.spinner("Indexing..."):
                try:
                    file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    ingest_file(file_path)
                    st.success(f"✅ **{uploaded_file.name}** indexed!")
                except Exception as e:
                    st.error(f"Error: {e}")
    st.divider()
    st.info("System ready.")

# --- MAIN TABS ---
tab_chat, tab_logs = st.tabs(["💬 Chat Stream", "🔧 System Internals"])

# --- TAB 1: CHAT ---
with tab_chat:
    # 1. History
    if not st.session_state.messages:
        # Placeholder text in the middle
        st.markdown("<div style='text-align: center; color: #555; margin-top: 100px;'>How can I help you today?</div>", unsafe_allow_html=True)

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        steps = message.get("steps", [])
        avatar = "👤" if role == "user" else "⚡"
        
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)
            if role == "assistant" and steps:
                with st.expander("View Thought Process"):
                    for step in steps:
                        st.markdown(f"- {step}")

    # 2. Input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # 3. Generation
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        
        scroll_to_bottom() # Scroll down on new message
        
        with st.chat_message("assistant", avatar="⚡"):
            response_placeholder = st.empty()
            steps_log = [] 
            
            with st.status("🧠 **Processing...**", expanded=True) as status:
                try:
                    final_text = ""
                    st.session_state.last_step = None
                    st.session_state.last_retrieved_docs = []

                    for event in graph.stream({"question": st.session_state.messages[-1]["content"]}):
                        
                        if "retrieve" in event:
                            status.write("📚 Searching Knowledge Base...")
                            steps_log.append("Router: Selected RAG Path")
                            st.session_state.last_step = "Retrieval"
                            st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                            
                        elif "weather_search" in event:
                            status.write("🌤️ Calling Weather API...")
                            steps_log.append("Router: Selected Weather Tool")
                            st.session_state.last_step = "Weather API"
                            st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
                            
                        elif "generate" in event:
                            status.write("⚡ Synthesizing Answer...")
                            steps_log.append("LLM: Generating Response")
                            final_text = event["generate"]["generation"]
                    
                    status.update(label="✅ **Complete**", state="complete", expanded=False)
                    
                    response_placeholder.write_stream(stream_text(final_text))
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": final_text,
                        "steps": steps_log
                    })
                    
                    scroll_to_bottom() # Scroll down after finish

                except Exception as e:
                    status.update(label="❌ Failed", state="error")
                    st.error(str(e))

# --- TAB 2: INTERNALS ---
with tab_logs:
    st.subheader("🔧 System Traces")
    col_tool, col_response = st.columns(2)
    
    with col_tool:
        st.markdown("### 📍 **Selected Tool**")
        if st.session_state.last_step == "Weather API":
            st.info("🌤️ Weather API")
        elif st.session_state.last_step == "Retrieval":
            st.success("📚 RAG (Vector DB)")
        else:
            st.caption("No active tool.")

    with col_response:
        st.markdown("### 📤 **Tool Output**")
        if st.session_state.last_step == "Weather API":
            if st.session_state.last_retrieved_docs:
                st.code(st.session_state.last_retrieved_docs[0], language="json")
            else:
                st.caption("No data.")
        
        elif st.session_state.last_step == "Retrieval":
            if st.session_state.last_retrieved_docs:
                for i, doc in enumerate(st.session_state.last_retrieved_docs):
                    with st.expander(f"Chunk {i+1}"):
                        st.text(doc.page_content)
            else:
                st.warning("No documents found.")
        else:
            st.caption("Waiting for response...")

    st.divider()
    with st.expander("📜 View Raw Logs"):
        st.code(get_logs())