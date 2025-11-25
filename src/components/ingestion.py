# # # Import os to handle file paths and environment variables
# # import os
# # # Import List type hint for type safety
# # from typing import List

# # # Import Document class from LangChain to handle text data
# # from langchain_core.documents import Document
# # # Import HuggingFace embeddings (Sentence Transformers) as requested
# # from langchain_huggingface import HuggingFaceEmbeddings
# # # Import Qdrant vector store for local storage
# # from langchain_community.vectorstores import Qdrant
# # # Import text splitter to break large docs into chunks
# # from langchain_text_splitters import RecursiveCharacterTextSplitter

# # # Import specific loaders for different file types
# # from langchain_community.document_loaders import (
# #     PyPDFLoader,
# #     TextLoader,
# #     CSVLoader,
# #     Docx2txtLoader,
# #     UnstructuredExcelLoader
# # )

# # # Import our custom logger
# # from src.utils.logger import get_logger

# # # Initialize the logger for this module
# # logger = get_logger(__name__)

# # # Define the path where Qdrant will store data locally
# # QDRANT_PATH = "./data/local_qdrant"
# # # Define the name of the collection in Qdrant
# # COLLECTION_NAME = "agent_docs"

# # def get_loader(file_path: str):
# #     # Function to select the correct loader based on file extension
    
# #     # Extract the file extension from the path
# #     _, ext = os.path.splitext(file_path)
# #     # Convert extension to lowercase for consistent comparison
# #     ext = ext.lower()

# #     # Log which file extension we are processing
# #     logger.info(f"Detected file extension: {ext}")

# #     # Return the appropriate loader class based on extension
# #     if ext == ".pdf":
# #         return PyPDFLoader(file_path)
# #     elif ext == ".txt":
# #         return TextLoader(file_path)
# #     elif ext == ".csv":
# #         return CSVLoader(file_path)
# #     elif ext == ".docx":
# #         return Docx2txtLoader(file_path)
# #     elif ext in [".xlsx", ".xls"]:
# #         return UnstructuredExcelLoader(file_path)
# #     else:
# #         # Raise an error if the file type is not supported
# #         raise ValueError(f"Unsupported file type: {ext}")

# # def ingest_file(file_path: str):
# #     # Main function to process a file and store it in Qdrant
    
# #     try:
# #         # Log the start of the ingestion process
# #         logger.info(f"Starting ingestion for file: {file_path}")

# #         # Get the appropriate loader for this file
# #         loader = get_loader(file_path)
        
# #         # Load the raw documents from the file
# #         raw_docs = loader.load()
# #         # Log how many raw pages/documents were loaded
# #         logger.info(f"Loaded {len(raw_docs)} raw documents.")

# #         # Initialize the text splitter
# #         # chunk_size=1000: roughly 1000 chars per chunk
# #         # chunk_overlap=200: keeps context between chunks
# #         text_splitter = RecursiveCharacterTextSplitter(
# #             chunk_size=1000, 
# #             chunk_overlap=200
# #         )
        
# #         # Split the documents into smaller chunks
# #         chunks = text_splitter.split_documents(raw_docs)
# #         # Log the number of chunks created
# #         logger.info(f"Split documents into {len(chunks)} chunks.")

# #         # Initialize HuggingFace Embeddings
# #         # model_name: Using the standard efficient sentence-transformer
# #         embeddings = HuggingFaceEmbeddings(
# #             model_name="sentence-transformers/all-MiniLM-L6-v2"
# #         )
# #         # Log that embeddings model is loaded
# #         logger.info("Loaded HuggingFace Embeddings model.")

# #         # Create/Update the Qdrant vector store
# #         # path=QDRANT_PATH: Ensures it runs LOCALLY on disk
# #         # force_recreate=True: Overwrites old collection for this demo
# #         qdrant = Qdrant.from_documents(
# #             chunks,
# #             embeddings,
# #             path=QDRANT_PATH,
# #             collection_name=COLLECTION_NAME,
# #             force_recreate=True
# #         )
        
# #         # Log success message
# #         logger.info(f"Successfully stored vectors in local Qdrant at {QDRANT_PATH}")
        
# #         # Return the retriever interface for the graph to use later
# #         return qdrant.as_retriever()

# #     except Exception as e:
# #         # Log any errors that occur during ingestion
# #         logger.error(f"Error during ingestion: {str(e)}")
# #         # Re-raise the error so the UI knows something failed
# #         raise e

# # def get_retriever():
# #     # Helper function to get the retriever without re-ingesting data
    
# #     # Initialize the same embedding model
# #     embeddings = HuggingFaceEmbeddings(
# #         model_name="sentence-transformers/all-MiniLM-L6-v2"
# #     )
    
# #     # Connect to the existing local Qdrant database
# #     client = Qdrant(
# #         client=None, 
# #         collection_name=COLLECTION_NAME, 
# #         embeddings=embeddings
# #     )
# #     # Load the client explicitly with the path
# #     # Note: LangChain's Qdrant wrapper handles connection details slightly differently
# #     # but for local, we usually reload from the path via the client.
# #     # For simplicity in this specific version, we return a new instance pointing to path.
# #     doc_store = Qdrant.from_existing_collection(
# #         embedding=embeddings,
# #         path=QDRANT_PATH,
# #         collection_name=COLLECTION_NAME
# #     )
    
# #     # Return the retriever object
# #     return doc_store.as_retriever()








# import os
# from typing import List

# # Import Document class from LangChain
# from langchain_core.documents import Document
# # Import HuggingFace embeddings
# from langchain_huggingface import HuggingFaceEmbeddings
# # Import Qdrant vector store
# # from langchain_community.vectorstores import Qdrant
# from langchain_qdrant import Qdrant, QdrantVectorStore
# # Import Qdrant Client explicitly for robust connection handling
# from qdrant_client import QdrantClient
# from qdrant_client.http.models import Distance, VectorParams

# # Import text splitter
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # Import specific loaders
# from langchain_community.document_loaders import (
#     PyPDFLoader,
#     TextLoader,
#     CSVLoader,
#     Docx2txtLoader,
#     UnstructuredExcelLoader
# )

# # Import our custom logger
# from src.utils.logger import get_logger

# # Initialize logger
# logger = get_logger(__name__)

# # Define constants
# QDRANT_PATH = "./data/local_qdrant"
# COLLECTION_NAME = "agent_docs"
# EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# EMBEDDING_DIMENSION = 384  # Dimension for all-MiniLM-L6-v2

# def get_loader(file_path: str):
#     """Factory function to select the correct loader based on file extension."""
#     _, ext = os.path.splitext(file_path)
#     ext = ext.lower()
#     logger.info(f"Detected file extension: {ext}")

#     if ext == ".pdf":
#         return PyPDFLoader(file_path)
#     elif ext == ".txt":
#         return TextLoader(file_path)
#     elif ext == ".csv":
#         return CSVLoader(file_path)
#     elif ext == ".docx":
#         return Docx2txtLoader(file_path)
#     elif ext in [".xlsx", ".xls"]:
#         return UnstructuredExcelLoader(file_path)
#     else:
#         raise ValueError(f"Unsupported file type: {ext}")

# def ingest_file(file_path: str):
#     """Process a file and store it in Qdrant (Robust Version)."""
#     try:
#         logger.info(f"Starting ingestion for file: {file_path}")

#         # 1. Load Documents
#         loader = get_loader(file_path)
#         raw_docs = loader.load()
#         logger.info(f"Loaded {len(raw_docs)} raw documents.")

#         # 2. Split Text
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000, 
#             chunk_overlap=200
#         )
#         chunks = text_splitter.split_documents(raw_docs)
#         logger.info(f"Split documents into {len(chunks)} chunks.")

#         # 3. Initialize Embeddings
#         embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
#         logger.info("Loaded HuggingFace Embeddings model.")

#         # 4. Initialize Qdrant Client Explicitly
#         # We handle the client creation to avoid LangChain's internal argument errors
#         client = QdrantClient(path=QDRANT_PATH)

#         # 5. Recreate Collection
#         # We manually create the collection to ensure strict control over params
#         if client.collection_exists(COLLECTION_NAME):
#             client.delete_collection(COLLECTION_NAME)
#             logger.info(f"Deleted existing collection: {COLLECTION_NAME}")
        
#         client.create_collection(
#             collection_name=COLLECTION_NAME,
#             vectors_config=VectorParams(size=EMBEDDING_DIMENSION, distance=Distance.COSINE)
#         )
#         logger.info(f"Created new collection: {COLLECTION_NAME}")

#         # 6. Add to Vector Store
#         qdrant = Qdrant(
#             client=client,
#             collection_name=COLLECTION_NAME,
#             embeddings=embeddings,
#         )
#         qdrant.add_documents(chunks)
        
#         logger.info(f"Successfully stored vectors in local Qdrant at {QDRANT_PATH}")
#         return qdrant.as_retriever()

#     except Exception as e:
#         logger.error(f"Error during ingestion: {str(e)}")
#         raise e

# def get_retriever():
#     """Get the retriever connecting to the existing local Qdrant DB."""
    
#     embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
#     # Initialize client connecting to the same local path
#     client = QdrantClient(path=QDRANT_PATH)
    
#     # Return the LangChain wrapper around the existing client
#     doc_store = QdrantVectorStore(
#         client=client, 
#         collection_name=COLLECTION_NAME, 
#         embeddings=embeddings
#     )
    
#     return doc_store.as_retriever()






import os
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
QDRANT_PATH = "./data/local_qdrant"
COLLECTION_NAME = "agent_docs"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

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
        logger.info(f"Loaded {len(raw_docs)} raw documents.")

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