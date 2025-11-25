# Import the logging module to handle log messages
import logging
# Import StringIO to capture log output into a string buffer
from io import StringIO

# Create a stream buffer to hold logs in memory
log_stream = StringIO()

def get_logger(name):
    # Function to create and configure a custom logger
    
    # Get a logger instance with the specified name
    logger = logging.getLogger(name)
    
    # Set the logging level to INFO (captures info, warning, error)
    logger.setLevel(logging.INFO)
    
    # Check if the logger already has handlers to prevent duplicate logs
    if not logger.handlers:
        # Create a StreamHandler that writes to our in-memory log_stream
        handler = logging.StreamHandler(log_stream)
        
        # Define the format of the log messages (Time - Level - Message)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Apply the formatter to the handler
        handler.setFormatter(formatter)
        
        # Add the handler to the logger
        logger.addHandler(handler)
        
    # Return the configured logger object
    return logger

def get_logs():
    # Function to retrieve all captured logs as a string
    
    # Get the current value from the string buffer
    return log_stream.getvalue()