"""
NutriAI Telegram Bot
A bot that provides nutritional analysis and advice through Telegram.
"""

from .modules.telegram import TelegramBot
from .modules.nutritionist_agent import Nutritionist
from .modules.food_image_analyser import FoodImageAnalyserTool

__version__ = "1.0.0"
__author__ = "Seu Nome"

# Expose main classes for easier imports
__all__ = [
    "TelegramBot",
    "Nutritionist",
    "FoodImageAnalyserTool"
]

# Configure logging for the entire application
import logging
import os

def setup_logging():
    """Configure logging for the application"""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console handler
            logging.FileHandler(  # File handler
                filename='app.log',
                mode='a',
                encoding='utf-8'
            )
        ]
    )
    
    # Suppress noisy loggers
    logging.getLogger('azure').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

setup_logging()