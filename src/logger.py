import logging
import sys

class ColorFormatter(logging.Formatter):
    """
    Custom formatter to color log messages based on their level.
    """
    
    # Define ANSI escape codes for colors and bold text
    COLORS = {
        'DEBUG': '\033[1;34m',   # Bold Blue
        'INFO': '\033[1;32m',    # Bold Green
        'WARNING': '\033[1;33m', # Bold Yellow
        'ERROR': '\033[1;31m',   # Bold Red
        'CRITICAL': '\033[1;41m' # Bold White on Red Background
    }
    
    RESET = '\033[0m'  # Reset ANSI color

    def format(self, record):
        # Get the log level and corresponding color
        log_color = self.COLORS.get(record.levelname, self.RESET)
        
        # Apply color and bold formatting to the log message
        log_message = f"{log_color}{record.levelname}{self.RESET}: {record.message}"
        
        # Format the complete log message with color
        formatted_message = f"{log_color}{record.asctime} - {record.name} - {record.levelname}{self.RESET}: {log_message}"
        
        return formatted_message

def create_logger(log_level=logging.DEBUG, log_file='app.log'):
    """
    Creates a comprehensive logger with both stdout and file handlers.
    Args:
        log_level: The initial logging level (default is DEBUG).
        log_file: The file to log to (default is 'app.log').
    Returns:
        logger: Configured logger instance.
    """
    
    # Create a logger instance
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Formatter for file logs (plain, no color)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Color formatter for console logs
    color_formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console (stdout) handler with color
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(color_formatter)

    # File handler for comprehensive logging to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
