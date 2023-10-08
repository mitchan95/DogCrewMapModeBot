# logging_setup.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Set up the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Format for the logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Rotating File Handler - keeps 5 backup log files, each log file is up to 1MB
    file_handler = RotatingFileHandler('bot.log', maxBytes=1e6, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Also print logs to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
