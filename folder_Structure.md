ai_agent_assignment/
├── data/                   # Folder to store local Qdrant DB files
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── ingestion.py    # Handles file loading (PDF, TXT, etc.) & Qdrant indexing
│   │   ├── tools.py        # Weather API and RAG Retrieval definitions
│   │   ├── router.py       # Groq-based Decision making logic
│   │   └── graph.py        # LangGraph construction (Nodes & Edges)
│   ├── utils/
│   │   ├── logger.py       # Custom logging config for UI redirection
│   │   └── helpers.py      # Env var loading and text splitters
│   └── ui/
│       └── layout.py       # Streamlit helper functions
├── tests/                  # Unit tests for API and Logic [cite: 13]
├── app.py                  # Main Streamlit entry point
├── requirements.txt
├── README.md
└── .env                    # API Keys (Groq, OpenWeather, LangSmith)