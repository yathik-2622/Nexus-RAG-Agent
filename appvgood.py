# # # import streamlit as st
# # # import os
# # # import time
# # # import json
# # # from dotenv import load_dotenv
# # # import streamlit.components.v1 as components

# # # # Import our custom logic
# # # from src.components.ingestion import ingest_file
# # # from src.components.graph import build_graph
# # # from src.utils.logger import get_logs

# # # # Load environment variables
# # # load_dotenv()

# # # # --- Configuration ---
# # # RAW_DATA_DIR = "./data/raw_documents"
# # # os.makedirs(RAW_DATA_DIR, exist_ok=True)

# # # # --- Page Configuration ---
# # # st.set_page_config(
# # #     page_title="Nexus Agent",
# # #     page_icon="⚡",
# # #     layout="wide",
# # #     initial_sidebar_state="expanded"
# # # )

# # # # --- 🔄 Auto-Scroll JavaScript Helper ---
# # # def scroll_to_bottom():
# # #     js = """
# # #     <script>
# # #         var body = window.parent.document.querySelector(".main .block-container");
# # #         body.scrollTop = body.scrollHeight;
# # #     </script>
# # #     """
# # #     components.html(js, height=0)

# # # # --- 🎨 FINAL CSS (Plain Text, Split Alignment) ---
# # # st.markdown("""
# # # <style>
# # #     /* 1. Global Layout & Dark Theme */
# # #     .stApp {
# # #         background-color: #0E1117; /* Default Streamlit Dark */
# # #     }
    
# # #     .block-container {
# # #         padding-top: 6rem;
# # #         padding-bottom: 6rem;
# # #         max-width: 1000px;
# # #     }

# # #     /* 2. Fixed Header */
# # #     .fixed-header {
# # #         position: fixed;
# # #         top: 3rem;
# # #         left: 0;
# # #         right: 0;
# # #         height: 3.5rem;
# # #         background-color: #0E1117;
# # #         z-index: 99;
# # #         display: flex;
# # #         align-items: center;
# # #         padding-left: 20px;
# # #         border-bottom: 1px solid #333;
# # #     }
    
# # #     .header-text {
# # #         font-size: 1.5rem;
# # #         font-weight: 700;
# # #         background: -webkit-linear-gradient(left, #00ADB5, #00ffcc);
# # #         -webkit-background-clip: text;
# # #         -webkit-text-fill-color: transparent;
# # #     }

# # #     /* 3. Fixed Chat Input */
# # #     .stChatInput {
# # #         position: fixed;
# # #         bottom: 0px;
# # #         left: 0;
# # #         right: 0;
# # #         padding-bottom: 20px;
# # #         padding-top: 10px;
# # #         background-color: #0E1117;
# # #         z-index: 1000;
# # #         width: 100%;
# # #         display: flex;
# # #         justify-content: center;
# # #         border-top: 1px solid #333;
# # #     }
    
# # #     /* --- MESSAGE STYLING (No Backgrounds) --- */

# # #     /* Hide Avatars for cleaner look (optional, remove if you want avatars) */
# # #     [data-testid="stChatMessage"] [data-testid="stImage"] {
# # #         display: none;
# # #     }

# # #     /* 4. USER Message -> RIGHT Side, RIGHT Aligned Text */
# # #     [data-testid="stChatMessage"]:nth-child(odd) {
# # #         flex-direction: row-reverse; /* Container on right */
# # #         text-align: right; 
# # #     }
    
# # #     [data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stMarkdownContainer"] {
# # #         background-color: transparent !important; /* No background */
# # #         color: #00ADB5; /* Teal color to distinguish User */
# # #         text-align: right !important; /* Force text to right */
# # #         padding: 0;
# # #         margin-left: auto; /* Push to right */
# # #     }
    
# # #     /* Force paragraphs inside user bubble to align right */
# # #     [data-testid="stChatMessage"]:nth-child(odd) p {
# # #         text-align: right !important;
# # #     }

# # #     /* 5. AGENT Message -> LEFT Side, LEFT Aligned Text */
# # #     [data-testid="stChatMessage"]:nth-child(even) {
# # #         flex-direction: row; /* Container on left */
# # #         text-align: left;
# # #     }
    
# # #     [data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"] {
# # #         background-color: transparent !important; /* No background */
# # #         color: #ECECF1; /* Standard White/Grey */
# # #         text-align: left !important; /* Force text to left */
# # #         padding: 0;
# # #         margin-right: auto; /* Push to left */
# # #     }

# # #     /* 6. Status Widget styling */
# # #     .stStatusWidget {
# # #         background-color: #111;
# # #         border: 1px solid #333;
# # #     }
    
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # --- RENDER: Fixed Header ---
# # # st.markdown("""
# # #     <div class="fixed-header">
# # #         <span class="header-text">⚡ NEXUS AGENT</span>
# # #     </div>
# # # """, unsafe_allow_html=True)

# # # # --- Session State ---
# # # if "messages" not in st.session_state:
# # #     st.session_state.messages = []
# # # if "last_retrieved_docs" not in st.session_state:
# # #     st.session_state.last_retrieved_docs = []
# # # if "last_step" not in st.session_state:
# # #     st.session_state.last_step = None

# # # # --- Cache Graph ---
# # # @st.cache_resource
# # # def load_agent_graph():
# # #     return build_graph()
# # # graph = load_agent_graph()

# # # # --- Helper: Stream Text ---
# # # def stream_text(text):
# # #     for word in text.split(" "):
# # #         yield word + " "
# # #         time.sleep(0.02)

# # # # --- SIDEBAR ---
# # # with st.sidebar:
# # #     st.subheader("📥 Knowledge Base")
# # #     uploaded_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt", "docx"], label_visibility="collapsed")
    
# # #     if uploaded_file:
# # #         if st.button("⚡ Embed & Ingest", type="primary", use_container_width=True):
# # #             with st.spinner("Indexing..."):
# # #                 try:
# # #                     file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
# # #                     with open(file_path, "wb") as f:
# # #                         f.write(uploaded_file.getbuffer())
                    
# # #                     ingest_file(file_path)
# # #                     st.success(f"✅ **{uploaded_file.name}** indexed!")
# # #                 except Exception as e:
# # #                     st.error(f"Error: {e}")

# # # # --- MAIN TABS ---
# # # tab_chat, tab_logs = st.tabs(["💬 Chat", "🔧 Internals"])

# # # # --- TAB 1: CHAT ---
# # # with tab_chat:
# # #     # 1. History
# # #     for message in st.session_state.messages:
# # #         role = message["role"]
# # #         content = message["content"]
# # #         steps = message.get("steps", [])
        
# # #         with st.chat_message(role):
# # #             st.markdown(content)
# # #             if role == "assistant" and steps:
# # #                 with st.expander("View Process"):
# # #                     for step in steps:
# # #                         st.markdown(f"- {step}")

# # #     # 2. Input
# # #     if prompt := st.chat_input("Type your message..."):
# # #         st.session_state.messages.append({"role": "user", "content": prompt})
# # #         st.rerun()

# # #     # 3. Generation
# # #     if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
# # #         scroll_to_bottom()
# # #         with st.chat_message("assistant"):
# # #             response_placeholder = st.empty()
# # #             steps_log = [] 
            
# # #             with st.status("🧠 **Processing...**", expanded=True) as status:
# # #                 try:
# # #                     final_text = ""
# # #                     st.session_state.last_step = None
# # #                     st.session_state.last_retrieved_docs = []

# # #                     for event in graph.stream({"question": st.session_state.messages[-1]["content"]}):
                        
# # #                         if "retrieve" in event:
# # #                             status.write("📚 Searching Knowledge Base...")
# # #                             steps_log.append("Router: Selected RAG Path")
# # #                             st.session_state.last_step = "Retrieval"
# # #                             st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                            
# # #                         elif "weather_search" in event:
# # #                             status.write("🌤️ Calling Weather API...")
# # #                             steps_log.append("Router: Selected Weather Tool")
# # #                             st.session_state.last_step = "Weather API"
# # #                             st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
                            
# # #                         elif "generate" in event:
# # #                             status.write("⚡ Synthesizing Answer...")
# # #                             steps_log.append("LLM: Generating Response")
# # #                             final_text = event["generate"]["generation"]
                    
# # #                     status.update(label="✅ **Complete**", state="complete", expanded=False)
                    
# # #                     response_placeholder.write_stream(stream_text(final_text))
                    
# # #                     st.session_state.messages.append({
# # #                         "role": "assistant", 
# # #                         "content": final_text,
# # #                         "steps": steps_log
# # #                     })
# # #                     scroll_to_bottom()

# # #                 except Exception as e:
# # #                     status.update(label="❌ Failed", state="error")
# # #                     st.error(str(e))

# # # # --- TAB 2: INTERNALS ---
# # # with tab_logs:
# # #     st.subheader("🔧 System Traces")
# # #     col_tool, col_response = st.columns(2)
    
# # #     with col_tool:
# # #         st.markdown("### 📍 **Selected Tool**")
# # #         if st.session_state.last_step == "Weather API":
# # #             st.info("🌤️ Weather API")
# # #         elif st.session_state.last_step == "Retrieval":
# # #             st.success("📚 RAG (Vector DB)")
# # #         else:
# # #             st.caption("No active tool.")

# # #     with col_response:
# # #         st.markdown("### 📤 **Tool Output**")
# # #         if st.session_state.last_step == "Weather API":
# # #             if st.session_state.last_retrieved_docs:
# # #                 st.code(st.session_state.last_retrieved_docs[0], language="json")
# # #             else:
# # #                 st.caption("No data.")
        
# # #         elif st.session_state.last_step == "Retrieval":
# # #             if st.session_state.last_retrieved_docs:
# # #                 for i, doc in enumerate(st.session_state.last_retrieved_docs):
# # #                     with st.expander(f"Chunk {i+1}"):
# # #                         st.text(doc.page_content)
# # #             else:
# # #                 st.warning("No documents found.")
# # #         else:
# # #             st.caption("Waiting for response...")
    
# # #     st.divider()
# # #     with st.expander("📜 View Raw Logs"):
# # #         st.code(get_logs())



# # import streamlit as st
# # import os
# # import time
# # import json
# # from dotenv import load_dotenv
# # import streamlit.components.v1 as components

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
# #     initial_sidebar_state="expanded"
# # )

# # # --- 🔄 Auto-Scroll JavaScript Helper ---
# # def scroll_to_bottom():
# #     js = """
# #     <script>
# #         var body = window.parent.document.querySelector(".main .block-container");
# #         body.scrollTop = body.scrollHeight;
# #     </script>
# #     """
# #     components.html(js, height=0)

# # # --- 🎨 FINAL CSS (Alignment Fix) ---
# # st.markdown("""
# # <style>
# #     /* 1. Global Layout & Dark Theme */
# #     .stApp {
# #         background-color: #0E1117;
# #     }
    
# #     .block-container {
# #         padding-top: 6rem;
# #         padding-bottom: 6rem;
# #         max-width: 1000px;
# #     }

# #     /* 2. Fixed Header */
# #     .fixed-header {
# #         position: fixed;
# #         top: 3rem;
# #         left: 0;
# #         right: 0;
# #         height: 3.5rem;
# #         background-color: #0E1117;
# #         z-index: 99;
# #         display: flex;
# #         align-items: center;
# #         padding-left: 20px;
# #         border-bottom: 1px solid #333;
# #     }
    
# #     .header-text {
# #         font-size: 1.5rem;
# #         font-weight: 700;
# #         background: -webkit-linear-gradient(left, #00ADB5, #00ffcc);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #     }

# #     /* 3. Fixed Chat Input (Compact) */
# #     .stChatInput {
# #         position: fixed;
# #         bottom: 0px;
# #         left: 0;
# #         right: 0;
# #         padding-bottom: 20px;
# #         padding-top: 10px;
# #         background-color: #0E1117;
# #         z-index: 1000;
# #         width: 100%;
# #         display: flex;
# #         justify-content: center;
# #         border-top: 1px solid #333;
# #     }
    
# #     .stChatInput > div {
# #         width: 50% !important; 
# #         max-width: 600px;
# #     }
    
# #     /* --- MESSAGE STYLING (Plain Text, Strict Alignment) --- */

# #     /* Hide Avatars */
# #     [data-testid="stChatMessage"] [data-testid="stImage"] {
# #         display: none;
# #     }

# #     /* 4. USER Message (ODD) -> RIGHT Side, RIGHT Aligned */
# #     [data-testid="stChatMessage"]:nth-child(odd) {
# #         flex-direction: row-reverse; 
# #         text-align: right; 
# #     }
    
# #     [data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stMarkdownContainer"] {
# #         background-color: transparent !important; 
# #         color: #00ADB5; /* Teal */
# #         text-align: right !important; 
# #         padding: 0;
# #         margin-left: auto; 
# #     }
    
# #     [data-testid="stChatMessage"]:nth-child(odd) p {
# #         text-align: right !important;
# #     }

# #     /* 5. AGENT Message (EVEN) -> LEFT Side, LEFT Aligned */
# #     [data-testid="stChatMessage"]:nth-child(even) {
# #         flex-direction: row; 
# #         text-align: left;
# #     }
    
# #     [data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"] {
# #         background-color: transparent !important; 
# #         color: #ECECF1; /* White/Grey */
# #         text-align: left !important; 
# #         padding: 0;
# #         margin-right: auto; 
# #     }
    
# #     /* Force Left Alignment for Agent Paragraphs */
# #     [data-testid="stChatMessage"]:nth-child(even) p {
# #         text-align: left !important;
# #     }

# #     /* 6. Status Widget styling */
# #     .stStatusWidget {
# #         background-color: #111;
# #         border: 1px solid #333;
# #     }
    
# # </style>
# # """, unsafe_allow_html=True)

# # # --- RENDER: Fixed Header ---
# # st.markdown("""
# #     <div class="fixed-header">
# #         <span class="header-text">⚡ NEXUS AGENT</span>
# #     </div>
# # """, unsafe_allow_html=True)

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

# # # --- SIDEBAR ---
# # with st.sidebar:
# #     st.subheader("📥 Knowledge Base")
# #     uploaded_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt", "docx"], label_visibility="collapsed")
    
# #     if uploaded_file:
# #         if st.button("⚡ Embed & Ingest", type="primary", use_container_width=True):
# #             with st.spinner("Indexing..."):
# #                 try:
# #                     file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
# #                     with open(file_path, "wb") as f:
# #                         f.write(uploaded_file.getbuffer())
                    
# #                     ingest_file(file_path)
# #                     st.success(f"✅ **{uploaded_file.name}** indexed!")
# #                 except Exception as e:
# #                     st.error(f"Error: {e}")

# # # --- MAIN TABS ---
# # tab_chat, tab_logs = st.tabs(["💬 Chat", "🔧 Internals"])

# # # --- TAB 1: CHAT ---
# # with tab_chat:
    
# #     # --- 🟢 CONTAINER FIX: Wraps chat in a clean block to fix odd/even counting ---
# #     chat_container = st.container()
    
# #     with chat_container:
# #         # 1. History
# #         for message in st.session_state.messages:
# #             role = message["role"]
# #             content = message["content"]
# #             steps = message.get("steps", [])
            
# #             with st.chat_message(role):
# #                 st.markdown(content)
# #                 if role == "assistant" and steps:
# #                     with st.expander("View Process"):
# #                         for step in steps:
# #                             st.markdown(f"- {step}")

# #         # 2. Generation Placeholder (To ensure it stays inside container)
# #         if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
# #             scroll_to_bottom()
# #             with st.chat_message("assistant"):
# #                 response_placeholder = st.empty()
# #                 steps_log = [] 
                
# #                 with st.status("🧠 **Processing...**", expanded=True) as status:
# #                     try:
# #                         final_text = ""
# #                         st.session_state.last_step = None
# #                         st.session_state.last_retrieved_docs = []

# #                         for event in graph.stream({"question": st.session_state.messages[-1]["content"]}):
                            
# #                             if "retrieve" in event:
# #                                 status.write("📚 Searching Knowledge Base...")
# #                                 steps_log.append("Router: Selected RAG Path")
# #                                 st.session_state.last_step = "Retrieval"
# #                                 st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                                
# #                             elif "weather_search" in event:
# #                                 status.write("🌤️ Calling Weather API...")
# #                                 steps_log.append("Router: Selected Weather Tool")
# #                                 st.session_state.last_step = "Weather API"
# #                                 st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
                                
# #                             elif "generate" in event:
# #                                 status.write("⚡ Synthesizing Answer...")
# #                                 steps_log.append("LLM: Generating Response")
# #                                 final_text = event["generate"]["generation"]
                        
# #                         status.update(label="✅ **Complete**", state="complete", expanded=False)
                        
# #                         response_placeholder.write_stream(stream_text(final_text))
                        
# #                         st.session_state.messages.append({
# #                             "role": "assistant", 
# #                             "content": final_text,
# #                             "steps": steps_log
# #                         })
# #                         scroll_to_bottom()

# #                     except Exception as e:
# #                         status.update(label="❌ Failed", state="error")
# #                         st.error(str(e))

# #     # 3. Input (Outside container, but fixed position handles it)
# #     if prompt := st.chat_input("Type your message..."):
# #         st.session_state.messages.append({"role": "user", "content": prompt})
# #         st.rerun()

# # # --- TAB 2: INTERNALS ---
# # with tab_logs:
# #     st.subheader("🔧 System Traces")
# #     col_tool, col_response = st.columns(2)
    
# #     with col_tool:
# #         st.markdown("### 📍 **Selected Tool**")
# #         if st.session_state.last_step == "Weather API":
# #             st.info("🌤️ Weather API")
# #         elif st.session_state.last_step == "Retrieval":
# #             st.success("📚 RAG (Vector DB)")
# #         else:
# #             st.caption("No active tool.")

# #     with col_response:
# #         st.markdown("### 📤 **Tool Output**")
# #         if st.session_state.last_step == "Weather API":
# #             if st.session_state.last_retrieved_docs:
# #                 st.code(st.session_state.last_retrieved_docs[0], language="json")
# #             else:
# #                 st.caption("No data.")
        
# #         elif st.session_state.last_step == "Retrieval":
# #             if st.session_state.last_retrieved_docs:
# #                 for i, doc in enumerate(st.session_state.last_retrieved_docs):
# #                     with st.expander(f"Chunk {i+1}"):
# #                         st.text(doc.page_content)
# #             else:
# #                 st.warning("No documents found.")
# #         else:
# #             st.caption("Waiting for response...")
    
# #     st.divider()
# #     with st.expander("📜 View Raw Logs"):
# #         st.code(get_logs())





# import streamlit as st
# import os
# import time
# import json
# from dotenv import load_dotenv
# import streamlit.components.v1 as components

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

# # --- 🔄 Auto-Scroll JavaScript Helper ---
# def scroll_to_bottom():
#     js = """
#     <script>
#         var body = window.parent.document.querySelector(".main .block-container");
#         body.scrollTop = body.scrollHeight;
#     </script>
#     """
#     components.html(js, height=0)

# # --- 🎨 FINAL CSS (Class-Based Alignment) ---
# st.markdown("""
# <style>
#     /* 1. Global Layout & Dark Theme */
#     .stApp {
#         background-color: #0E1117;
#     }
    
#     .block-container {
#         padding-top: 6rem;
#         padding-bottom: 6rem;
#         max-width: 1000px;
#     }

#     /* 2. Fixed Header */
#     .fixed-header {
#         position: fixed;
#         top: 3rem;
#         left: 0;
#         right: 0;
#         height: 3.5rem;
#         background-color: #0E1117;
#         z-index: 99;
#         display: flex;
#         align-items: center;
#         padding-left: 20px;
#         border-bottom: 1px solid #333;
#     }
    
#     .header-text {
#         font-size: 1.5rem;
#         font-weight: 700;
#         background: -webkit-linear-gradient(left, #00ADB5, #00ffcc);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }

#     /* 3. Fixed Chat Input (Compact) */
#     .stChatInput {
#         position: fixed;
#         bottom: 0px;
#         left: 0;
#         right: 0;
#         padding-bottom: 20px;
#         padding-top: 10px;
#         background-color: #0E1117;
#         z-index: 1000;
#         width: 100%;
#         justify-content: center;
#         border-top: 1px solid #333;
#     }
    
#     .stChatInput > div {
#         width: 50% !important; 
#         max-width: 600px;
#     }
    
#     /* --- BUBBLE CONTAINER POSITIONS --- */
    
#     /* Hide Avatars */
#     [data-testid="stChatMessage"] [data-testid="stImage"] {
#         display: none;
#     }

#     /* Remove default backgrounds */
#     [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
#         background-color: transparent !important; 
#         padding: 0;
#     }

#     /* Position User Bubbles on Right */
#     [data-testid="stChatMessage"]:nth-child(odd) {
#         flex-direction: row-reverse; 
#     }
    
#     /* Position Agent Bubbles on Left */
#     [data-testid="stChatMessage"]:nth-child(even) {
#         flex-direction: row; 
#     }

#     /* --- TEXT STYLING CLASSES (Injected via Python) --- */
    
#     .user-text {
#         text-align: right !important;
#         color: #00ADB5 !important;
#         width: 100%;
#     }
    
#     .agent-text {
#         text-align: left !important;
#         color: #ECECF1 !important;
#         width: 100%;
#     }

#     /* Status Widget styling */
#     .stStatusWidget {
#         background-color: #111;
#         border: 1px solid #333;
#         margin-bottom: 1rem;
#     }
    
# </style>
# """, unsafe_allow_html=True)

# # --- RENDER: Fixed Header ---
# st.markdown("""
#     <div class="fixed-header">
#         <span class="header-text">⚡ NEXUS AGENT</span>
#     </div>
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

# # --- Helper: Stream Text with HTML Wrapper ---
# def stream_text_with_class(text, css_class):
#     """Yields text wrapped in a styled div for streaming"""
#     # We output the opening tag first
#     first = True
#     for word in text.split(" "):
#         if first:
#             yield f'<div class="{css_class}">' + word + " "
#             first = False
#         else:
#             yield word + " "
#         time.sleep(0.02)
#     yield "</div>"

# # --- SIDEBAR ---
# with st.sidebar:
#     st.subheader("📥 Knowledge Base")
#     uploaded_file = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt", "docx"], label_visibility="collapsed")
    
#     if uploaded_file:
#         if st.button("⚡ Embed & Ingest", type="primary", use_container_width=True):
#             with st.spinner("Indexing..."):
#                 try:
#                     file_path = os.path.join(RAW_DATA_DIR, uploaded_file.name)
#                     with open(file_path, "wb") as f:
#                         f.write(uploaded_file.getbuffer())
                    
#                     ingest_file(file_path)
#                     st.success(f"✅ **{uploaded_file.name}** indexed!")
#                 except Exception as e:
#                     st.error(f"Error: {e}")

# # --- MAIN TABS ---
# tab_chat, tab_logs = st.tabs(["💬 Chat", "🔧 Internals"])

# # --- TAB 1: CHAT ---
# with tab_chat:
    
#     # 1. History
#     for message in st.session_state.messages:
#         role = message["role"]
#         content = message["content"]
#         steps = message.get("steps", [])
        
#         with st.chat_message(role):
#             # INJECTION: Wrap content in specific div classes based on role
#             if role == "user":
#                 st.markdown(f'<div class="user-text">{content}</div>', unsafe_allow_html=True)
#             else:
#                 st.markdown(f'<div class="agent-text">{content}</div>', unsafe_allow_html=True)
                
#             if role == "assistant" and steps:
#                 with st.expander("View Process"):
#                     for step in steps:
#                         st.markdown(f"- {step}")

#     # 2. Input
#     if prompt := st.chat_input("Type your message..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         st.rerun()

#     # 3. Generation
#     if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
#         scroll_to_bottom()
        
#         # NOTE: We do NOT open st.chat_message() here for the status widget.
#         # This keeps the status widget completely separate from the message logic.
        
#         steps_log = []
#         final_text = ""
        
#         # A. Status Area (Separate from chat bubbles)
#         with st.status("🧠 **Processing...**", expanded=True) as status:
#             try:
#                 st.session_state.last_step = None
#                 st.session_state.last_retrieved_docs = []

#                 for event in graph.stream({"question": st.session_state.messages[-1]["content"]}):
                    
#                     if "retrieve" in event:
#                         status.write("📚 Searching Knowledge Base...")
#                         steps_log.append("Router: Selected RAG Path")
#                         st.session_state.last_step = "Retrieval"
#                         st.session_state.last_retrieved_docs = event["retrieve"].get("documents", [])
                        
#                     elif "weather_search" in event:
#                         status.write("🌤️ Calling Weather API...")
#                         steps_log.append("Router: Selected Weather Tool")
#                         st.session_state.last_step = "Weather API"
#                         st.session_state.last_retrieved_docs = event["weather_search"].get("documents", [])
                        
#                     elif "generate" in event:
#                         status.write("⚡ Synthesizing Answer...")
#                         steps_log.append("LLM: Generating Response")
#                         final_text = event["generate"]["generation"]
                
#                 status.update(label="✅ **Complete**", state="complete", expanded=False)
            
#             except Exception as e:
#                 status.update(label="❌ Failed", state="error")
#                 st.error(str(e))
        
#         # B. Result Area (The actual Agent Bubble)
#         if final_text:
#             with st.chat_message("assistant"):
#                 # Stream with the correct Agent Class
#                 st.write_stream(stream_text_with_class(final_text, "agent-text"))
            
#             # Save to history
#             st.session_state.messages.append({
#                 "role": "assistant", 
#                 "content": final_text,
#                 "steps": steps_log
#             })
#             scroll_to_bottom()

# # --- TAB 2: INTERNALS ---
# with tab_logs:
#     st.subheader("🔧 System Traces")
#     col_tool, col_response = st.columns(2)
    
#     with col_tool:
#         st.markdown("### 📍 **Selected Tool**")
#         if st.session_state.last_step == "Weather API":
#             st.info("🌤️ Weather API")
#         elif st.session_state.last_step == "Retrieval":
#             st.success("📚 RAG (Vector DB)")
#         else:
#             st.caption("No active tool.")

#     with col_response:
#         st.markdown("### 📤 **Tool Output**")
#         if st.session_state.last_step == "Weather API":
#             if st.session_state.last_retrieved_docs:
#                 st.code(st.session_state.last_retrieved_docs[0], language="json")
#             else:
#                 st.caption("No data.")
        
#         elif st.session_state.last_step == "Retrieval":
#             if st.session_state.last_retrieved_docs:
#                 for i, doc in enumerate(st.session_state.last_retrieved_docs):
#                     with st.expander(f"Chunk {i+1}"):
#                         st.text(doc.page_content)
#             else:
#                 st.warning("No documents found.")
#         else:
#             st.caption("Waiting for response...")
    
#     st.divider()
#     with st.expander("📜 View Raw Logs"):
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

# --- 🎨 FINAL CSS (Robust Class-Based Alignment) ---
st.markdown("""
<style>
    /* 1. Global Layout & Dark Theme */
    .stApp {
        background-color: #0E1117;
    }
    
    .block-container {
        padding-top: 6rem;
        padding-bottom: 6rem;
        max-width: 1000px;
    }

    /* 2. Fixed Header */
    .fixed-header {
        position: fixed;
        top: 3rem;
        left: 0;
        right: 0;
        height: 3.5rem;
        background-color: #0E1117;
        z-index: 99;
        display: flex;
        align-items: center;
        padding-left: 20px;
        border-bottom: 1px solid #333;
    }
    
    .header-text {
        font-size: 1.5rem;
        font-weight: 700;
        background: -webkit-linear-gradient(left, #00ADB5, #00ffcc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 3. Fixed Chat Input (Compact) */
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
        width: 50% !important; 
        max-width: 600px;
    }
    
    /* --- CHAT MESSAGE CONTAINERS --- */
    
    /* Hide Avatars completely */
    [data-testid="stChatMessage"] [data-testid="stImage"] {
        display: none;
    }

    /* Make container full width and transparent */
    [data-testid="stChatMessage"] {
        width: 100%;
        background-color: transparent !important;
        padding: 0px 10px;
    }
    
    /* Remove default background from Markdown container */
    [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
        background-color: transparent !important; 
        padding: 0;
        max-width: 100% !important;
    }

    /* --- TEXT STYLING CLASSES (Used in Python) --- */
    
    /* USER: Teal, Right Aligned */
    .user-text {
        text-align: right;
        color: #00ADB5;
        font-size: 1rem;
        margin-left: auto;
        display: block;
        width: 100%;
    }
    
    /* AGENT: White, Left Aligned */
    .agent-text {
        text-align: left;
        color: #ECECF1;
        font-size: 1rem;
        margin-right: auto;
        display: block;
        width: 100%;
    }

    /* Status Widget styling */
    .stStatusWidget {
        background-color: #111;
        border: 1px solid #333;
        margin-bottom: 1rem;
    }
    
</style>
""", unsafe_allow_html=True)

# --- RENDER: Fixed Header ---
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

# --- SIDEBAR ---
with st.sidebar:
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

# --- MAIN TABS ---
tab_chat, tab_logs = st.tabs(["💬 Chat", "🔧 Internals"])

# --- TAB 1: CHAT ---
with tab_chat:
    
    # 1. History
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        steps = message.get("steps", [])
        
        with st.chat_message(role):
            # INJECTION: Use div classes to control alignment/color
            if role == "user":
                st.markdown(f'<div class="user-text">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="agent-text">{content}</div>', unsafe_allow_html=True)
                
            if role == "assistant" and steps:
                with st.expander("View Process"):
                    for step in steps:
                        st.markdown(f"- {step}")

    # 2. Input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # 3. Generation
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        scroll_to_bottom()
        
        steps_log = []
        final_text = ""
        
        # A. Status Area
        with st.status("🧠 **Processing...**", expanded=True) as status:
            try:
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
            
            except Exception as e:
                status.update(label="❌ Failed", state="error")
                st.error(str(e))
        
        # B. Result Area (The actual Agent Bubble)
        if final_text:
            with st.chat_message("assistant"):
                # Create a placeholder for the streaming effect
                response_placeholder = st.empty()
                accumulated_text = ""
                
                # Manual Streaming Loop to support HTML rendering
                for word in final_text.split(" "):
                    accumulated_text += word + " "
                    # Re-render the whole HTML block with the new word
                    response_placeholder.markdown(f'<div class="agent-text">{accumulated_text}</div>', unsafe_allow_html=True)
                    time.sleep(0.02)
            
            # Save to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": final_text,
                "steps": steps_log
            })
            scroll_to_bottom()

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