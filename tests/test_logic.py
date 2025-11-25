# Import necessary components for testing
import pytest
import os
from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage

# Import functions from our source code
from src.components.tools import get_weather_data
from src.components.router import get_router_chain, RouteQuery
from src.components.ingestion import ingest_file

# Setup: Define fixture for Groq API key (ensures key is set for testing)
@pytest.fixture(scope="session", autouse=True)
def set_env_vars():
    # Set dummy API keys for testing
    os.environ['GROQ_API_KEY'] = 'test_groq_key'
    os.environ['OPENWEATHERMWAP_API_KEY'] = 'test_weather_key'

# --- 1. Test API Handling (OpenWeatherMap) ---
def test_weather_api_success():
    # Test case for successful weather API response
    
    # Define a mock JSON response for London
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'weather': [{'description': 'clear sky'}],
        'main': {'temp': 15.0, 'humidity': 70}
    }

    # Use patch to mock the requests.get call
    with patch('requests.get', return_value=mock_response) as mock_get:
        # Call the function
        result = get_weather_data("London")
        
        # Assert that the API was called
        assert mock_get.called
        # Assert the result string is correctly formatted
        assert "Weather in London: clear sky, Temperature: 15.0°C, Humidity: 70%" in result

def test_weather_api_failure():
    # Test case for failed weather API response (e.g., 404)
    
    # Define a mock 404 response
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {}

    # Use patch to mock the requests.get call
    with patch('requests.get', return_value=mock_response):
        # Call the function
        result = get_weather_data("InvalidCity")
        
        # Assert the result indicates failure
        assert "Failed to get weather. Status: 404" in result

# --- 2. Test LLM Processing/Routing Logic ---

def test_router_chain_creation():
    # Test the router chain initialization
    
    # Get the router chain
    router_chain = get_router_chain()
    
    # Assert that the chain object exists
    assert router_chain is not None
    # Check if it has an invoke method (validating it's a Runnable)
    assert hasattr(router_chain, 'invoke')

def test_router_chain_predict_weather():
    # Test if the router correctly predicts 'weather_api'
    
    # We patch the ChatGroq class itself in the router module
    with patch('src.components.router.ChatGroq') as MockChatGroq:
        # Create a mock for the chain
        mock_chain = MagicMock()
        
        # Mock the return value to be a valid RouteQuery object
        mock_chain.invoke.return_value = RouteQuery(datasource="weather_api")
        
        # Connect our mock chain to the LLM mock
        MockChatGroq.return_value.with_structured_output.return_value = mock_chain
        
        # Get the router
        router_chain = get_router_chain()
        
        # Run the chain
        result = router_chain.invoke("What's the temperature in Tokyo?")
        
        # Assert the predicted route is correct
        assert result.datasource == "weather_api"

# --- 3. Test Retrieval Logic (Qdrant & Embeddings) ---

# We now patch the NEW classes we are using in ingestion.py
@patch('src.components.ingestion.QdrantVectorStore')
@patch('src.components.ingestion.QdrantClient')
@patch('src.components.ingestion.HuggingFaceEmbeddings')
def test_ingest_file_logic(mock_embeddings, mock_client, mock_vector_store):
    # Test the ingestion function logic
    
    # Create a dummy file for the loader to find
    test_filename = "temp_test_file.txt"
    with open(test_filename, "w") as f:
        f.write("Test content for retrieval.")
        
    try:
        # Setup the mock instance that the constructor returns
        mock_vs_instance = mock_vector_store.return_value
        
        # Run the ingestion function
        retriever = ingest_file(test_filename)
        
        # Assert that the Client was initialized
        assert mock_client.called
        # Assert that the VectorStore was initialized
        assert mock_vector_store.called
        # Assert that documents were added
        assert mock_vs_instance.add_documents.called
        # Assert that we got a retriever back
        assert retriever == mock_vs_instance.as_retriever.return_value
        
    finally:
        # Clean up the mock file
        if os.path.exists(test_filename):
            os.remove(test_filename)