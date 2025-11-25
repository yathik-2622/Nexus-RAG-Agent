# # import streamlit as st
# # import os
# # import time
# # import json
# # from dotenv import load_dotenv

# # # Import our custom logic
# # from src.components.ingestion import ingest_file
# # from src.components.graph import build_graph
# # from src.utils.logger import get_logs

# # # Load environment variables
# # load_dotenv()

# # # --- Configuration ---
# # RAW_DATA_DIR = "./data/raw_documents"
# # os.makedirs(RAW_DATA_DIR, exist_ok=True)

# # # --- Page Configuration ---
# # st.set_page_config(
# #     page_title="Nexus Agent",
# #     page_icon="⚡",
# #     layout="wide",
# #     initial_sidebar_state="collapsed"
# # )

# # # --- 🎨 MODERN CHAT STYLING ---
# # st.markdown("""
# # <style>
# #     /* 1. Remove top padding */
# #     .block-container { padding-top: 1rem; padding-bottom: 10rem; }
    
# #     /* 2. Chat Input Styling */
# #     .stChatInput {
# #         position: fixed;
# #         bottom: 20px;
# #         z-index: 1000;
# #         width: 80%; /* Make it slightly narrower to look like an app */
# #         left: 50%;
# #         transform: translateX(-50%);
# #     }
    
# #     /* 3. User Message (Right, Green) */
# #     [data-testid="stChatMessage"]:nth-child(odd) {
# #         flex-direction: row-reverse;
# #         text-align: right;
# #         background-color: #005c4b;
# #         border: none;
# #         margin-left: auto; /* Push to right */
# #         max-width: 70%;
# #     }
    
# #     /* 4. Agent Message (Left, Gray) */
# #     [data-testid="stChatMessage"]:nth-child(even) {
# #         flex-direction: row;
# #         text-align: left;
# #         background-color: #202c33;
# #         border: none;
# #         margin-right: auto; /* Push to left */
# #         max-width: 80%;
# #     }
    
# #     /* 5. The Attachment Popover Button */
# #     [data-testid="stPopover"] {
# #         position: fixed;
# #         bottom: 35px;
# #         left: 10%; /* Position to the left of the chat input */
# #         z-index: 1001;
# #     }
    
# #     /* 6. Headers */
# #     h1 { text-align: center; color: #ECECF1; font-size: 1.5rem; margin-bottom: 0.5rem; }
# # </style>
# # """, unsafe_allow_html=True)

# # # --- Title ---
# # st.title("NEXUS AGENT ⚡")

# # # --- Session State ---
# # if "messages" not in st.session_state:
# #     st.session_state.messages = []
# # if "last_retrieved_docs" not in st.session_state:
# #     st.session_state.last_retrieved_docs = []
# # if "last_step" not in st.session_state:
# #     st.session_state.last_step = None

# # # --- Cache Graph ---
# # @st.cache_resource
# # def load_agent_graph():
# #     return build_graph()
# # graph = load_agent_graph()

# # # --- Helper: Stream Text ---
# # def stream_text(text):
# #     for word in text.split(" "):
# #         yield word + " "
# #         time.sleep(0.02)

# # # --- Main Tabs ---
# # tab_chat, tab_logs = st.tabs(["💬 Chat", "⚙️ Internals"])

# # with tab_chat:
# #     # 1. Display History
# #     if not st.session_state.messages:
# #         st.markdown("<div style='text-align: center; color: #888; margin-top: 20vh;'>👋 Hi! Ask me about the weather or upload a doc.</div>", unsafe_allow_html=True)

# #     for message in st.session_state.messages:
# #         role = message["role"]
# #         with st.chat_message(role, avatar="👤" if role == "user" else "⚡"):
# #             st.markdown(message["content"])

# #     # 2. The "Attachment" Popover (Acts like the + button)
# #     with st.popover("📎", use_container_width=False):
# #         st.markdown("### 📤 Upload Knowledge")
# #         uploaded_file = st.file_uploader("Choose a file...", type=["pdf", "txt", "docx"], label_visibility="collapsed")
        
# #         if uploaded_file:
# #             if st.button("Upload & Embed", type="primary", use_container_width=True):
# #                 # --- STREAMING UPLOAD UX ---
                
# #                 # A. User sees the command
# #                 st.session_state.messages.append({"role": "user", "content": f"📎 Uploading file: `{uploaded_file.name}`"})
# #                 st.rerun() # Force refresh to show user message first

# #     # 3. Handle Ingestion Logic (If triggered by rerun)
# #     # We check the last message to see if we need to trigger the ingestion agent response
# #     if st.session_state.messages and "Uploading file:" in st.session_state.messages[-1]["content"] and len(st.session_state.messages) % 2 != 0:
        
# #         last_filename = st.session_state.messages[-1]["content"].split("`")[1]
        
# #         with st.chat_message("assistant", avatar="⚡"):
# #             status_placeholder = st.empty()
            
# #             # Simulate "Agent Thinking/Processing" for Upload
# #             with st.status("⚙️ **Processing Document...**", expanded=True) as status:
# #                 try:
# #                     st.write("📂 Saving file to secure storage...")
# #                     time.sleep(0.8)
                    
# #                     # Actual Logic
# #                     file_path = os.path.join(RAW_DATA_DIR, last_filename)
# #                     # We need to seek the file from the uploader in the popover 
# #                     # (Streamlit complexity: direct file access across reruns is tricky, 
# #                     # so we assume the file is re-available or we save it immediately in the popover.
# #                     # For this UI demo, we assume the file object is accessible or we re-prompt if lost.
# #                     # To make it robust, we usually save immediately in the popover logic.
# #                     # FIX: Let's handle save inside the popover for robustness, but show status here.
                    
# #                     st.write("🧠 Generating Embeddings (HuggingFace)...")
# #                     time.sleep(1) # UX Pause
                    
# #                     st.write("💾 Indexing into Qdrant Vector DB...")
# #                     # Simulate ingestion call (since we can't easily pass the file object across rerun boundary without session state hacks)
# #                     # For the assignment, we can actually just do the logic inside the popover and print the result there, 
# #                     # BUT you asked for chat streaming.
                    
# #                     status.update(label="✅ **Knowledge Base Updated!**", state="complete", expanded=False)
# #                     response_text = f"I have successfully ingested **{last_filename}**. You can now ask questions about it."
# #                     st.markdown(response_text)
# #                     st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
# #                 except Exception as e:
# #                     status.update(label="❌ Error", state="error")
# #                     st.error(str(e))

# #     # 4. Chat Input
# #     if prompt := st.chat_input("Type a message..."):
# #         # User Message
# #         st.session_state.messages.append({"role": "user", "content": prompt})
# #         st.rerun() # Rerun to display user message immediately

# #     # 5. Handle Response Generation
# #     if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
# #         with st.chat_message("assistant", avatar="⚡"):
# #             prompt = st.session_state.messages[-1]["content"]
            
# #             # Status Container (Gemini Style)
# #             with st.status("🧠 **Thinking...**", expanded=True) as status:
# #                 try:
# #                     final_generation = ""
# #                     for event in graph.stream({"question": prompt}):
                        
# #                         # RAG Path
# #                         if "retrieve" in event:
# #                             status.update(label="📘 **Consulting Knowledge Base**", state="running")
# #                             st.write("🔍 Searching vector store...")
# #                             st.session_state.last_step = "Retrieval"
# #                             st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                            
# #                         # Weather Path
# #                         elif "weather_search" in event:
# #                             status.update(label="🌤️ **Checking Live Weather**", state="running")
# #                             st.write("🌍 Calling OpenWeatherMap API...")
# #                             st.session_state.last_step = "Weather API"
# #                             st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
                            
# #                         # Generator Path
# #                         elif "generate" in event:
# #                             status.update(label="⚡ **Synthesizing Response**", state="running")
# #                             final_generation = event["generate"]["generation"]
                    
# #                     status.update(label="✅ **Complete**", state="complete", expanded=False)
                    
# #                     # Streaming Output
# #                     message_placeholder = st.empty()
# #                     message_placeholder.write_stream(stream_text(final_generation))
# #                     st.session_state.messages.append({"role": "assistant", "content": final_generation})

# #                 except Exception as e:
# #                     status.update(label="❌ Error", state="error")
# #                     st.error(f"System Error: {e}")

# # # --- Internals Tab (Strict Separation) ---
# # with tab_logs:
# #     st.subheader("🔧 Execution Trace")
    
# #     if st.session_state.last_step:
# #         # Dynamic Header based on decision
# #         if st.session_state.last_step == "Weather API":
# #             st.info("📍 **Route:** Weather Tool (External API)")
# #             st.markdown("### 🌤️ Weather API Payload")
            
# #             # Strict: Show Raw API Data
# #             if st.session_state.last_retrieved_docs:
# #                 raw_data = st.session_state.last_retrieved_docs[0]
# #                 # Try to format as JSON if possible, else string
# #                 try:
# #                     # If it's a string representation of dict
# #                     st.code(raw_data, language="json") 
# #                 except:
# #                     st.code(raw_data, language="text")
# #             else:
# #                 st.warning("API call executed but returned no data.")

# #         elif st.session_state.last_step == "Retrieval":
# #             st.success("📍 **Route:** RAG (Vector Store)")
# #             st.markdown("### 📄 Retrieved Document Chunks")
            
# #             # Strict: Show Chunks
# #             if st.session_state.last_retrieved_docs:
# #                 for i, doc in enumerate(st.session_state.last_retrieved_docs):
# #                     # Handle string vs Document object
# #                     content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
# #                     source = doc.metadata.get('source', 'Unknown') if hasattr(doc, 'metadata') else 'Index'
                    
# #                     with st.expander(f"Chunk {i+1} | Source: {os.path.basename(source)}"):
# #                         st.markdown(f"**Content:**\n{content}")
# #             else:
# #                 st.warning("Search executed but found no matching documents.")
# #     else:
# #         st.markdown("*waiting for first query...*")

# #     st.markdown("---")
# #     with st.expander("📜 View System Logs"):
# #         st.code(get_logs(), language="log")








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
#     initial_sidebar_state="expanded"
# )

# # --- 🎨 CSS STYLING (WhatsApp Style + Compact Header) ---
# st.markdown("""
# <style>
#     /* 1. Main Container Padding */
#     .block-container { padding-top: 1rem; padding-bottom: 10rem; }
    
#     /* 2. Compact Header Styling */
#     .header-container {
#         padding: 0.5rem;
#         margin-bottom: 1rem;
#         text-align: center;
#         border-bottom: 1px solid #333;
#     }
#     .header-title {
#         font-size: 1.2rem; /* Smaller font */
#         font-weight: 700;
#         color: #ECECF1;
#         letter-spacing: 1px;
#         margin: 0;
#     }
    
#     /* 3. Chat Input Styling (Fixed Bottom) */
#     .stChatInput {
#         position: fixed;
#         bottom: 20px;
#         z-index: 1000;
#         width: 75%;
#         left: 50%;
#         transform: translateX(-45%);
#     }
    
#     /* 4. User Message (Right, Green) */
#     [data-testid="stChatMessage"]:nth-child(odd) {
#         flex-direction: row-reverse;
#         text-align: right;
#         background-color: #005c4b;
#         border: none;
#         margin-left: auto;
#         max-width: 70%;
#         border-radius: 10px;
#     }
    
#     /* 5. Agent Message (Left, Gray) */
#     [data-testid="stChatMessage"]:nth-child(even) {
#         flex-direction: row;
#         text-align: left;
#         background-color: #202c33;
#         border: none;
#         margin-right: auto;
#         max-width: 80%;
#         border-radius: 10px;
#     }
    
#     /* 6. Steps Expander Styling (In Chat) */
#     .streamlit-expanderHeader {
#         font-size: 0.8rem;
#         color: #aaa;
#     }
# </style>
# """, unsafe_allow_html=True)

# # --- Header ---
# st.markdown("""
# <div class="header-container">
#     <div class="header-title">⚡ NEXUS AGENT</div>
# </div>
# """, unsafe_allow_html=True)

# # --- Session State ---
# if "messages" not in st.session_state:
#     st.session_state.messages = [] # Stores dicts: {role, content, steps}
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

# # --- Sidebar (Restored) ---
# with st.sidebar:
#     st.markdown("### 📤 Knowledge Base")
#     uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt", "docx"], label_visibility="collapsed")
    
#     if uploaded_file:
#         if st.button("Ingest File", type="primary", use_container_width=True):
#             with st.spinner("Processing..."):
#                 try:
#                     file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
#                     with open(file_path, "wb") as f:
#                         f.write(uploaded_file.getbuffer())
                    
#                     ingest_file(file_path)
#                     st.success(f"✅ **{uploaded_file.name}** added to brain!")
#                 except Exception as e:
#                     st.error(f"Error: {e}")
    
#     st.markdown("---")
#     st.info("💡 **Tip:** Upload a PDF to enable RAG, or ask directly for Weather.")

# # --- Main Tabs ---
# tab_chat, tab_logs = st.tabs(["💬 Chat", "⚙️ Internals"])

# with tab_chat:
#     # 1. Display Chat History (With Persistent Steps)
#     for message in st.session_state.messages:
#         role = message["role"]
#         content = message["content"]
#         steps = message.get("steps", []) # Retrieve stored steps
        
#         with st.chat_message(role, avatar="👤" if role == "user" else "⚡"):
#             st.markdown(content)
            
#             # If it's an assistant message and has steps, show them
#             if role == "assistant" and steps:
#                 with st.expander("🔍 View Process Steps"):
#                     for step in steps:
#                         st.caption(f"• {step}")

#     # 2. Chat Input
#     if prompt := st.chat_input("Type a message..."):
#         # User Message
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(prompt)

#         # Assistant Message
#         with st.chat_message("assistant", avatar="⚡"):
#             message_placeholder = st.empty()
#             steps_taken = [] # List to capture steps for history
            
#             # Status Container (Active Stream)
#             with st.status("🧠 **Thinking...**", expanded=True) as status:
#                 try:
#                     final_generation = ""
                    
#                     # Stream Graph Events
#                     for event in graph.stream({"question": prompt}):
                        
#                         # RAG Path
#                         if "retrieve" in event:
#                             label = "📘 **Checking Knowledge Base**"
#                             status.update(label=label, state="running")
#                             st.write("Searching vector store for context...")
                            
#                             # Update State & Log
#                             st.session_state.last_step = "Retrieval"
#                             st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
#                             steps_taken.append("Retrieved context from Qdrant")
                            
#                         # Weather Path
#                         elif "weather_search" in event:
#                             label = "🌤️ **Checking Live Weather**"
#                             status.update(label=label, state="running")
#                             st.write("Querying OpenWeatherMap API...")
                            
#                             # Update State & Log
#                             st.session_state.last_step = "Weather API"
#                             st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
#                             steps_taken.append("Called OpenWeatherMap API")
                            
#                         # Generator Path
#                         elif "generate" in event:
#                             label = "⚡ **Synthesizing Response**"
#                             status.update(label=label, state="running")
                            
#                             final_generation = event["generate"]["generation"]
#                             steps_taken.append("LLM Generated Final Answer")
                    
#                     # Completion
#                     status.update(label="✅ **Complete**", state="complete", expanded=False)
                    
#                     # Streaming Output
#                     message_placeholder.write_stream(stream_text(final_generation))
                    
#                     # SAVE TO HISTORY (Content + Steps)
#                     st.session_state.messages.append({
#                         "role": "assistant", 
#                         "content": final_generation,
#                         "steps": steps_taken
#                     })

#                 except Exception as e:
#                     status.update(label="❌ Error", state="error")
#                     st.error(f"System Error: {e}")

# # --- Internals Tab (Strict Separation) ---
# with tab_logs:
#     st.subheader("🔧 Execution Trace")
    
#     col1, col2 = st.columns([1, 2])
    
#     with col1:
#         st.markdown("**Routing Decision**")
#         if st.session_state.last_step:
#             if st.session_state.last_step == "Weather API":
#                 st.info("📍 Tool Selected: **WEATHER**")
#             elif st.session_state.last_step == "Retrieval":
#                 st.success("📍 Tool Selected: **RAG (DOCS)**")
#         else:
#             st.caption("Waiting for query...")

#     with col2:
#         st.markdown("**Tool Output**")
        
#         if st.session_state.last_step == "Weather API":
#             st.caption("Raw API Response (JSON)")
#             if st.session_state.last_retrieved_docs:
#                 try:
#                     # Try to parse string as JSON for pretty printing
#                     # Often comes as a string representation of a dict
#                     raw_text = st.session_state.last_retrieved_docs[0]
#                     st.code(raw_text, language="json")
#                 except:
#                     st.code(st.session_state.last_retrieved_docs[0], language="text")
#             else:
#                 st.warning("No data returned.")

#         elif st.session_state.last_step == "Retrieval":
#             st.caption("Retrieved Text Chunks")
#             if st.session_state.last_retrieved_docs:
#                 for i, doc in enumerate(st.session_state.last_retrieved_docs):
#                     content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
#                     meta = doc.metadata if hasattr(doc, 'metadata') else {}
#                     source = os.path.basename(meta.get('source', 'Unknown'))
                    
#                     with st.expander(f"📄 Chunk {i+1} | {source}"):
#                         st.text(content)
#             else:
#                 st.warning("No relevant documents found.")
#         else:
#             st.caption("No tool output generated yet.")

#     st.markdown("---")
#     with st.expander("📜 Full System Logs"):
#         st.code(get_logs(), language="log")







import streamlit as st
import os
import time
import json
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

# --- 🎨 PRECISE CSS STYLING ---
st.markdown("""
<style>
    /* 1. Main Layout */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 8rem;
        max-width: 950px;
    }
    
    /* 2. Header */
    .header-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ECECF1;
        margin-bottom: 1rem;
    }
    
    /* 3. Chat Input */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 70%;
        z-index: 1000;
    }
    
    /* 4. USER Message Styling (Right Side, Auto Width) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        flex-direction: row-reverse; /* Avatar on right */
        background-color: transparent;
        border: none;
    }
    
    /* Target the specific text container for the User */
    [data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stMarkdownContainer"] {
        background-color: #005c4b; /* WhatsApp Green */
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px; /* Rounded corners */
        text-align: left; /* Text inside is normal */
        margin-left: auto; /* Push to right */
        width: fit-content; /* Auto-size */
        max-width: 80%;
        display: block;
    }

    /* 5. AGENT Message Styling (Left Side, Transparent, Streaming) */
    [data-testid="stChatMessage"]:nth-child(even) {
        flex-direction: row; /* Avatar on left */
        background-color: transparent;
        border: none;
    }
    
    /* Target the specific text container for Agent */
    [data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"] {
        background-color: transparent;
        color: #ECECF1;
        padding: 0;
        margin-right: auto;
        width: 100%; /* Full width for reading */
        text-align: left;
    }
    
    /* 6. Thinking Process Box */
    .stStatusWidget {
        background-color: #121212;
        border: 1px solid #333;
        border-radius: 8px;
        margin-bottom: 10px;
        max-width: 100%;
    }
    
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header-title">⚡ NEXUS AGENT</div>', unsafe_allow_html=True)

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

# --- Sidebar (Restored) ---
with st.sidebar:
    st.subheader("📥 Knowledge Base")
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt", "docx"], label_visibility="visible")
    
    if uploaded_file:
        if st.button("Ingest File", type="primary", use_container_width=True):
            with st.spinner("Processing..."):
                try:
                    file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    ingest_file(file_path)
                    st.success(f"✅ **{uploaded_file.name}** added to brain!")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    st.divider()
    st.info("💡 **Modes:**\n1. **Weather:** Ask for cities.\n2. **RAG:** Upload a PDF and ask questions.")

# --- Main Tabs ---
tab_chat, tab_logs = st.tabs(["💬 Chat", "⚙️ Internals"])

with tab_chat:
    # 1. Render Chat History
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role, avatar="👤" if role == "user" else "⚡"):
            st.markdown(content)

    # 2. Chat Input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # 3. Agent Response Generation
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant", avatar="⚡"):
            response_container = st.empty()
            
            # "Thinking" Status (Gemini Style)
            with st.status("🧠 **Thought Process**", expanded=True) as status:
                try:
                    final_text = ""
                    # Reset state for new query
                    st.session_state.last_retrieved_docs = []
                    st.session_state.last_step = None
                    
                    for event in graph.stream({"question": st.session_state.messages[-1]["content"]}):
                        
                        if "retrieve" in event:
                            status.update(label="📚 **Searching Knowledge Base**", state="running")
                            st.write("Accessing Qdrant vector store...")
                            st.session_state.last_step = "Retrieval"
                            st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                            
                        elif "weather_search" in event:
                            status.update(label="🌤️ **Connecting to Weather API**", state="running")
                            st.write("Fetching real-time data...")
                            st.session_state.last_step = "Weather API"
                            st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
                            
                        elif "generate" in event:
                            status.update(label="⚡ **Synthesizing**", state="running")
                            final_text = event["generate"]["generation"]
                    
                    status.update(label="✅ **Complete**", state="complete", expanded=False)
                    
                    # Stream the final text
                    response_container.write_stream(stream_text(final_text))
                    
                    # Save to history
                    st.session_state.messages.append({"role": "assistant", "content": final_text})

                except Exception as e:
                    status.update(label="❌ **Error**", state="error")
                    st.error(str(e))

# --- Internals Tab (Correct Naming) ---
with tab_logs:
    st.subheader("🔧 System Traces")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Last Route**")
        if st.session_state.last_step == "Weather API":
            st.info("🌤️ Weather Tool")
        elif st.session_state.last_step == "Retrieval":
            st.success("📚 RAG (Docs)")
        else:
            st.caption("Waiting for query...")

    with col2:
        # DYNAMIC HEADER based on tool
        if st.session_state.last_step == "Weather API":
            st.markdown("**🌤️ OpenWeatherMap API Response**")
            if st.session_state.last_retrieved_docs:
                st.code(st.session_state.last_retrieved_docs[0], language="json")
            else:
                st.caption("No data returned.")
                
        elif st.session_state.last_step == "Retrieval":
            st.markdown("**📄 RAG Document Chunks**")
            if st.session_state.last_retrieved_docs:
                for i, doc in enumerate(st.session_state.last_retrieved_docs):
                    # Safe metadata extraction
                    source = "Unknown"
                    if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                        source = os.path.basename(doc.metadata['source'])
                        
                    content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                    
                    with st.expander(f"Chunk {i+1} (Source: {source})"):
                        st.text(content)
            else:
                st.warning("No relevant context found in documents.")
        else:
            st.markdown("**waiting for tool output...**")

    st.divider()
    with st.expander("📜 View Full Logs"):
        st.code(get_logs())