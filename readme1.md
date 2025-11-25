# 🤖 Intelligent Agentic RAG & Weather Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange)
![Qdrant](https://img.shields.io/badge/Vector_DB-Qdrant_(Local)-red)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-green)

An intelligent agent capable of routing user queries between **real-time weather data** and **document-based knowledge** (RAG). Built with **LangGraph** for orchestration, **Groq** for high-speed inference, and **Qdrant** for local vector storage.

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [🏗️ System Architecture](#️-system-architecture)
- [⚙️ Tech Stack](#️-tech-stack)
- [🚀 Installation & Setup](#-installation--setup)
- [🔑 Configuration](#-configuration)
- [💻 Usage](#-usage)
- [🧪 Testing](#-testing)
- [📊 Evaluation (LangSmith)](#-evaluation-langsmith)

---

## ✨ Features

* **🧠 Intelligent Routing:** A specialized LangGraph node (powered by Groq) analyzes user intent to decide whether to call the `Weather Tool` or the `RAG Retriever`.
* **🌦️ Real-Time Weather:** Integration with OpenWeatherMap API to fetch live weather data for any city.
* **📚 Retrieval-Augmented Generation (RAG):** Ingests PDF documents, generates embeddings via HuggingFace, and stores them in a local Qdrant instance for accurate QA.
* **🕷️ Agentic Workflow:** Uses a graph-based state machine (LangGraph) to manage conversation history and tool execution.
* **👀 Observability:** Full integration with **LangSmith** for tracing LLM inputs, outputs, and latency.
* **🖥️ Interactive UI:** A clean Streamlit interface to chat with the agent and view the decision-making process.

---

## 🏗️ System Architecture

The agent operates on a graph workflow:
1.  **Start Node:** Receives user query.
2.  **Router Node:** LLM classifies intent -> `Weather` OR `Document`.
3.  **Tool Nodes:**
    * *Weather Path:* Calls OpenWeatherMap API.
    * *RAG Path:* Queries Qdrant Vector DB for relevant chunks.
4.  **Generator Node:** LLM synthesizes the tool output into a natural language response.

*(Optional: Add a screenshot of your LangGraph visualization here)*

---

## ⚙️ Tech Stack

* **LLM:** Groq (`llama-3.1-70b-versatile`)
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
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
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
OPENWEATHERMAP_API_KEY="..."

# LangSmith Configuration (For Evaluation)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGCHAIN_API_KEY="lsv2_..."
LANGCHAIN_PROJECT="Agentic-RAG-Assignment"







