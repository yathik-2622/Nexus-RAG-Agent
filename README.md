# ⚡ Nexus Agent: Intelligent Agentic RAG & Weather Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange)
![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant_(Local)-red)
![Streamlit](https://img.shields.io/badge/UI-Streamlit_Chat-green)

**Nexus Agent** is an advanced AI assistant capable of intelligently routing user queries between **real-time weather data** and **document-based knowledge** (RAG).

Built with a focus on **observability and user experience**, it features real-time token streaming, a transparent thought process display, and a modern "App-like" dark mode interface.

---

## 📋 Table of Contents
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#-system-architecture)
- [⚙️ Tech Stack](#-tech-stack)
- [🚀 Installation & Setup](#-installation--setup)
- [💻 Usage Guide](#-usage-guide)
- [🧪 Testing](#-testing)
- [📊 Evaluation (LangSmith)](#-evaluation-langsmith)
- [📂 Project Structure](#-project-structure)

---

## ✨ Key Features

### 🧠 Intelligent Core
* **Agentic Identity:** Explicitly programmed to identify as the `RyStudios Nexus Agent`, explaining its own capabilities and purpose.
* **Smart Routing:** A **LangGraph** router (powered by **Groq**) dynamically decides whether to call the `Weather Tool` or the `RAG Retriever` based on user intent , or `General Chat`.
* **Agentic Workflow:** Uses a state-based graph to manage conversation history and tool execution steps.

### 🎨 Modern User Experience (UI/UX)
* **⚡ Real-Time Streaming:** Responses flow token-by-token (Typewriter effect), just like ChatGPT/Gemini.
* **💭 Transparent Thought Process:** Every agent response includes a collapsible **"Thought Process"** section, allowing users to inspect the exact steps taken (e.g., "Router decided X", "Tool returned Y").
* **📱 App-Like Interface:** Custom CSS implementation for:
    * **Sticky Header:** Persistent navigation bar.
    * **Message Alignment:** User (Right/Transparent) vs. Agent (Left/Transparent).
    * **Clean Layout:** Fixed chat input at the bottom for a seamless feel.

### 📚 Retrieval-Augmented Generation (RAG)
* **Local Vector Store:** Ingests PDF, TXT, and DOCX files into a local **Qdrant** instance.
* **HuggingFace Embeddings:** Uses `sentence-transformers/all-MiniLM-L6-v2` for high-quality retrieval.

### 👀 Observability
* **Live Internals Tab:** A split-screen view showing the **Active Tool** on the left and the **Raw Data Payload** (JSON/Text) on the right.
* **LangSmith Integration:** Full tracing of latency, token usage, and decision paths.

---

## 🏗️ System Architecture

The agent follows a modular, state-driven directed graph workflow:

* **Entry Point:** The user query is received and stored in the AgentState.
* **Router Node (The Brain):** The Groq LLM analyzes the query and selects one of three paths:
* **Weather Path:** Triggered by queries about temperature or conditions.
* **Vectorstore Path:** Triggered when the user asks about uploaded documents.
* **General Chat Path:** Triggered for greetings, identity questions ("Who are you?"), or general knowledge.

# Execution Nodes:

* **weather_search:** Fetches data via OpenWeatherMap API.
* **retrieve:** Queries the Qdrant Cloud collection.
* **generate:** Always runs last. It synthesizes the tool output (or uses internal knowledge for general chat) into a branded final response.
* **State Management:** The AgentState ensures that even if a tool is skipped, the system defaults to an empty context to prevent processing errors.

---

## ⚙️ Tech Stack

* **LLM:** Groq (`llama-3.3-70b-versatile`)
* **Orchestration:** LangChain & LangGraph
* **Vector Database:** Qdrant (Embedded/Local mode)
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **UI Framework:** Streamlit (with Custom CSS)
* **Testing:** Pytest
* **Evaluation:** LangSmith

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.9+
* Git
* Qdrant Cloud Cluster URL & API Key

### Steps

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yathik-2622/Nexus-RAG-Agent.git](https://github.com/yathik-2622/Nexus-RAG-Agent.git)
    cd Nexus-RAG-Agent
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Create a `.env` file in the root directory:
    ```ini
    GROQ_API_KEY="gsk_..."
    OPENWEATHERMWAP_API_KEY="..."
    QDRANT_URL="https://your-cluster-url.aws.cloud.qdrant.io"
    QDRANT_API_KEY="your_cloud_api_key"
    
    # LangSmith (Optional but recommended)
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_API_KEY="lsv2_..."
    ```


# 💻 Usage
1. Run the Streamlit App
# Launch the user interface:
### 1. Launch the App
```bash
streamlit run app.py
```


# 2. Interaction Modes
🌤️ Weather Mode
Ask: "What is the current temperature in New York?"

# Observe:
* The chat will show a "🧠 Processing Query..." status box.
* Once complete, the answer streams in.
* Check the "Internals" tab to see the raw JSON response from OpenWeatherMap.

# 📚 RAG (Document) Mode
* Open the Sidebar.
* Upload a PDF or TXT file.
* Click "⚡ Embed & Ingest".
* Ask: "Summarize the document" or "What are the key findings?"
* Inspect: Click the "View Thought Process" expander under the answer to see that the agent chose the "Retrieval" path.

# 🧪 Testing
Run the automated test suite to verify API connectivity and router logic:

```bash
pytest tests/test_logic.py -v
(or)
pytest -m tests/test_logic.py -v
```
# Coverage:
* test_weather_api: Validates real connectivity to OpenWeatherMap.
* test_router: Ensures the LLM correctly classifies intents.
* test_ingest: Verifies Qdrant ingestion pipeline.
### ✅ Test Results
![Unit Test Results](assets/Testcases.png)

## 📊 Evaluation (LangSmith)

This project is fully integrated with **LangSmith** for evaluation.
* **Traces:** Every interaction is logged to monitor latency and token usage.
* **Decision Making:** The screenshot below shows the agent correctly routing queries.

![LangSmith Dashboard](assets/langsmith_dashboard.png)
![LangSmith Trace View -> Weather API](assets/langsmith_trace_view_Weather_1.png)
![LangSmith Trace View -> RAG](assets/langsmith_trace_view_RAG_1.png)


# 📂 Repository Structure :
```bash
Nexus-RAG-Agent/
├── data/                   # Local Qdrant storage (gitignored)
├── src/
│   ├── components/
│   │   ├── ingestion.py    # Qdrant & Embedding logic
│   │   ├── router.py       # Classification Logic
│   │   ├── tools.py        # Weather API Tool
│   │   └── graph.py        # LangGraph State Machine
│   ├── utils/
│   │   └── logger.py       # Custom UI Logging
├── tests/                  # Unit Tests
├── app.py                  # Main Streamlit UI
├── requirements.txt        # Dependencies
└── .env                    # Secrets

# for theme Use .streamlit/ folder
```

# DEMO UI:
![DEMO UI 1](assets/demo_1.png)
![DEMO UI 2](assets/demo_2.png)

