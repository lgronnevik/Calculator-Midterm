# app/calculator_config.py
import os
from dotenv import load_dotenv

class CalculatorConfig:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env if it exists

        # Base directories / file paths
        self.log_file = os.getenv("CALCULATOR_LOG_FILE", "calculator.log")
        self.history_file = os.getenv("CALCULATOR_HISTORY_FILE", "history.csv")

        # History settings
        self.max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", 100))
        self.auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"

        # Calculation settings
        self.precision = int(os.getenv("CALCULATOR_PRECISION", 2))
        self.max_input_value = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", 1e6))
        self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")