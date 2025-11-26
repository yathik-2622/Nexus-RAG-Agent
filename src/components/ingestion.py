
# Import List for type hinting
from typing import List

# Import Document class from LangChain
from langchain_core.documents import Document
# Import HuggingFace embeddings
from langchain_huggingface import HuggingFaceEmbeddings
# Import the NEW QdrantVectorStore
from langchain_qdrant import QdrantVectorStore
# Import Qdrant Client explicitly
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# Import os for environment variables
import os

# Load environment variables from .env file
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

# Import text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import specific loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader
)

# Import our custom logger
from src.utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Define constants
QDRANT_PATH = os.getenv("QDRANT_PATH")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
EMBEDDING_DIMENSION = os.getenv("EMBEDDING_DIMENSION")

def get_loader(file_path: str):
    """Factory function to select the correct loader based on file extension."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    logger.info(f"Detected file extension: {ext}")

    if ext == ".pdf":
        return PyPDFLoader(file_path)
    elif ext == ".txt":
        return TextLoader(file_path)
    elif ext == ".csv":
        return CSVLoader(file_path)
    elif ext == ".docx":
        return Docx2txtLoader(file_path)
    elif ext in [".xlsx", ".xls"]:
        return UnstructuredExcelLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def ingest_file(file_path: str):
    """Process a file and store it in Qdrant using QdrantVectorStore."""
    try:
        logger.info(f"Starting ingestion for file: {file_path}")

        # 1. Load Documents
        loader = get_loader(file_path)
        raw_docs = loader.load()
        logger.info(f"Loaded {len(raw_docs)} raw documents/pages from source file.")

        # 2. Split Text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(raw_docs)
        logger.info(f"Split documents into {len(chunks)} chunks.")

        # 3. Initialize Embeddings
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        logger.info("Loaded HuggingFace Embeddings model.")

        # 4. Initialize Qdrant Client
        client = QdrantClient(path=QDRANT_PATH)

        # 5. Recreate Collection (Force fresh start for this assignment)
        if client.collection_exists(COLLECTION_NAME):
            client.delete_collection(COLLECTION_NAME)
            logger.info(f"Deleted existing collection: {COLLECTION_NAME}")
        
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSION, distance=Distance.COSINE)
        )
        logger.info(f"Created new collection: {COLLECTION_NAME}")

        # 6. Add to Vector Store using the new class
        # Note: parameter is 'embedding' (singular) in the new class
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding=embeddings,
        )
        vector_store.add_documents(chunks)
        
        logger.info(f"Successfully stored vectors in local Qdrant at {QDRANT_PATH}")
        return vector_store.as_retriever()

    except Exception as e:
        logger.error(f"Error during ingestion: {str(e)}")
        raise e

def get_retriever():
    """Get the retriever connecting to the existing local Qdrant DB."""
    
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    client = QdrantClient(path=QDRANT_PATH)
    
    # Connect using the new QdrantVectorStore
    vector_store = QdrantVectorStore(
        client=client, 
        collection_name=COLLECTION_NAME, 
        embedding=embeddings
    )
    
    return vector_store.as_retriever()