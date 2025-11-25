# 🤖 Intelligent Agentic RAG & Weather Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange)
![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant_(Local)-red)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-green)

An intelligent AI agent capable of routing user queries between **real-time weather data** and **document-based knowledge** (RAG). Built with **LangGraph** for orchestration, **Groq** for high-speed inference, and **Qdrant** for local vector storage.

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [🏗️ System Architecture](#-system-architecture)
- [⚙️ Tech Stack](#-tech-stack)
- [🚀 Installation & Setup](#-installation--setup)
- [🔑 Configuration](#-configuration)
- [💻 Usage](#-usage)
- [🧪 Testing](#-testing)
- [📊 Evaluation (LangSmith)](#-evaluation-langsmith)
- [📂 Repository Structure](#-repository-structure)

---

## ✨ Features

* **🧠 Intelligent Routing:** A specialized **LangGraph** node (powered by Groq) analyzes user intent to decide whether to call the `Weather Tool` or the `RAG Retriever`.
* **🌦️ Real-Time Weather:** Integration with **OpenWeatherMap API** to fetch live weather data for any city.
* **📚 Retrieval-Augmented Generation (RAG):** Ingests PDF, TXT, and DOCX documents, generates embeddings via **HuggingFace**, and stores them in a local **Qdrant** instance.
* **🕷️ Agentic Workflow:** Uses a state-based graph to manage conversation history, routing logic, and tool execution.
* **👀 Observability:** Full integration with **LangSmith** for tracing LLM inputs, outputs, and latency.
* **🖥️ Interactive UI:** A clean **Streamlit** interface with real-time logging, decision visualization, and retrieved context inspection.

---

## 🏗️ System Architecture

The agent operates on a directed graph workflow:

1.  **Start Node:** Receives user query.
2.  **Router Node:** LLM classifies intent $\rightarrow$ `Weather` OR `Document`.
3.  **Tool Nodes:**
    * *Weather Path:* Calls OpenWeatherMap API.
    * *RAG Path:* Queries Qdrant Vector DB for relevant chunks.
4.  **Generator Node:** LLM synthesizes the tool output into a natural language response.
5.  **End Node:** Returns the final response to the UI.

---

## ⚙️ Tech Stack

* **LLM:** Groq (`llama-3.3-70b-versatile`)
* **Orchestration:** LangChain & LangGraph
* **Vector Database:** Qdrant (Local mode)
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **UI Framework:** Streamlit
* **Testing:** Pytest
* **Evaluation:** LangSmith

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.9+
* Git

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

---

## 🔑 Configuration

Create a `.env` file in the root directory and add the following API keys:

```ini
# Core API Keys
GROQ_API_KEY="gsk_..."
OPENWEATHERMWAP_API_KEY="..."

# LangSmith Configuration (For Evaluation)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGCHAIN_API_KEY="lsv2_..."
LANGCHAIN_PROJECT="AI_Agent_Assignment"





💻 Usage
1. Run the Streamlit App
# Launch the user interface:

```bash
streamlit run app.py
```


# 2. How to Interact
## Weather Queries: 
Ask questions like "What's the weather in Tokyo?" or "Is it raining in London?"
Check the "Internals" tab to see the Router choose the Weather API.

## Document Queries:

Use the sidebar to Upload a document (PDF, TXT, CSV).
Click "Ingest Document" to process and index the file into Qdrant.

Ask questions like "Summarize the document" or "What are the key requirements?"
Check the "Internals" tab to see the retrieved text chunks.




# 🧪 Testing
This project includes a suite of unit tests for API connectivity, router logic, and retrieval accuracy.
Run the tests using pytest:

``` bash
pytest tests/test_logic.py -v

```


# Test Coverage:

test_weather_api_success: Validates OpenWeatherMap connection.
test_router_chain: Ensures the LLM correctly routes "weather" vs "doc" queries.
test_ingest_file_logic: Verifies that Qdrant ingestion and retrieval logic works.


# 📊 Evaluation (LangSmith)
We use LangSmith to evaluate the agent's performance and decision-making.

1.**Tracing**: Every interaction via the UI is traced.
2.**Metrics**: We monitor latency, token usage, and tool selection accuracy.
3.**Results**: Logs can be viewed in the LangSmith dashboard under project AI_Agent_Assignment.


# 📂 Repository Structure
ai_agent_assignment/
├── data/                   # Local Qdrant storage (gitignored)
├── src/
│   ├── components/
│   │   ├── ingestion.py    # File loading & Vector DB logic
│   │   ├── router.py       # LLM Decision classification
│   │   ├── tools.py        # OpenWeatherMap API tool
│   │   └── graph.py        # LangGraph workflow definition
│   ├── utils/
│   │   └── logger.py       # Custom in-memory logging for UI
├── tests/                  # Pytest unit tests
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── .env                    # API Keys config