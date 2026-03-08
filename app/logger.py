import logging
import pandas as pd

class LoggingObserver:
    def __init__(self, log_file):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # Remove all handlers if they exist
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def update(self, calculation):
        # Accepts either a Calculation object or a list of Calculation objects
        if isinstance(calculation, list):
            for c in calculation:
                self.logger.info(f"Calculation: {c.operation}({c.val1}, {c.val2}) = {c.result}")
        else:
            self.logger.info(f"Calculation: {calculation.operation}({calculation.val1}, {calculation.val2}) = {calculation.result}")

    def log_event(self, message):
        self.logger.info(f"Event: {message}")

    def log_warning(self, message):
        self.logger.warning(f"Warning: {message}")

    def log_error(self, message):
        self.logger.error(f"Error: {message}")

class AutoSaveObserver:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def update(self, calculation):
        # Accepts either a Calculation object or a list of Calculation objects
        if isinstance(calculation, list):
            self.save_history(calculation)
        else:
            self.save_history([calculation])

    def save_history(self, history):
        if not history:
            return
        try:
            import pandas as pd
            df = pd.DataFrame([{
                "operation": c.operation,
                "val1": c.val1,
                "val2": c.val2,
                "result": c.result
            } for c in history])
            df.to_csv(self.csv_file, index=False)
        except Exception as e:
            print(f"AutoSave Error: {e}")

    def load_history(self, history):
        import os, pandas as pd
        if not os.path.exists(self.csv_file):
            return
        df = pd.read_csv(self.csv_file)
        history.clear()
        for _, row in df.iterrows():
            from app.calculation import Calculation
            calc = Calculation(row["operation"], row["val1"], row["val2"], row["result"])
            history.add(calc)