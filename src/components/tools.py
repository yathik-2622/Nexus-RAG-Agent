# Import requests to make HTTP calls to the weather API
import requests
# Import os to retrieve the API key from environment variables
import os
# Import our custom logger
from src.utils.logger import get_logger

# Initialize the logger
logger = get_logger(__name__)

def get_weather_data(city: str) -> str:
    # Function to fetch real-time weather for a specific city
    
    # Retrieve the API key from the environment
    api_key = os.getenv("OPENWEATHERMWAP_API_KEY")
    
    # Check if the API key is missing
    if not api_key:
        # Log an error and return a helpful message
        logger.error("Weather API key not found in environment variables.")
        return "Error: Weather API key missing."

    # Construct the API URL with the city and key
    # units=metric ensures we get Celsius
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        # Log the attempt to fetch weather
        logger.info(f"Fetching weather for city: {city}")
        
        # Make the GET request to OpenWeatherMap
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract key details to keep the context clean for the LLM
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            
            # Create a summary string
            result = f"Weather in {city}: {weather_desc}, Temperature: {temp}°C, Humidity: {humidity}%"
            
            # Log the successful retrieval
            logger.info(f"Weather data retrieved: {result}")
            return result
        else:
            # Handle API errors (e.g., city not found)
            error_msg = f"Failed to get weather. Status: {response.status_code}"
            logger.warning(error_msg)
            return error_msg

    except Exception as e:
        # Catch network or parsing errors
        logger.error(f"Exception in weather tool: {str(e)}")
        return f"Error occurred: {str(e)}"