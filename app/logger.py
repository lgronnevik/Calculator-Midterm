import logging
import pandas as pd

class LoggingObserver:
    def __init__(self, log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO)
        self.logger = logging.getLogger()

    def update(self, calculation):
        # Accepts either a Calculation object or a list of Calculation objects
        if isinstance(calculation, list):
            for c in calculation:
                self.logger.info(f"{c.operation}({c.val1}, {c.val2}) = {c.result}")
        else:
            self.logger.info(f"{calculation.operation}({calculation.val1}, {calculation.val2}) = {calculation.result}")

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
        df = pd.DataFrame([{
            "operation": c.operation,
            "val1": c.val1,
            "val2": c.val2,
            "result": c.result
        } for c in history])
        df.to_csv(self.csv_file, index=False)

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