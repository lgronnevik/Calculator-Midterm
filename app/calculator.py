from app.operations import OperationFactory
from app.history import History
from app.calculator_memento import CalculatorMemento
from app.calculator_config import CalculatorConfig

config = CalculatorConfig()

class Calculator:
    def __init__(self):
        self.history = History(max_size=config.max_history_size)
        self.memento = CalculatorMemento(self.history)
        # Observer setup
        from app.logger import LoggingObserver, AutoSaveObserver
        import os
        log_path = os.path.join(os.getenv("CALCULATOR_LOG_DIR", "logs"), config.log_file)
        history_path = os.path.join(os.getenv("CALCULATOR_HISTORY_DIR", "history"), config.history_file)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        self.logger_observer = LoggingObserver(log_path)
        self.autosave_observer = AutoSaveObserver(history_path)
        self.history.register_observer(self.logger_observer)
        if config.auto_save:
            self.history.register_observer(self.autosave_observer)

    def perform_operation(self, op_name, a, b):
        try:
            # Input validation
            if abs(a) > config.max_input_value or abs(b) > config.max_input_value:
                print(f"Error: Input value exceeds maximum allowed ({config.max_input_value})")
                return
            operation = OperationFactory.get_operation(op_name)
            result = operation.execute(a, b)
            # Apply precision
            result = round(result, config.precision)
            # Save history before adding new calculation
            self.memento.save()
            from app.calculation import Calculation
            calculation = Calculation(op_name, a, b, result)
            self.history.add(calculation)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

    def show_history(self):
        for entry in self.history.list():
            op, a, b, result = entry
            print(f"{op}({a}, {b}) = {result}")

    def undo(self):
        snapshot = self.memento.undo()
        if snapshot is None:
            print("Nothing to undo.")
        else:
            print("Undo successful.")

    def redo(self):
        snapshot = self.memento.redo()
        if snapshot is None:
            print("Nothing to redo.")
        else:
            print("Redo successful.")

    def repl(self):
        print("Welcome to the Advanced Calculator! Type 'help' for commands.")
        while True:
            cmd = input(">> ").strip().lower()
            if cmd == "exit":
                break
            elif cmd == "help":
                print("Commands: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff, history, undo, redo, exit")
            elif cmd == "history":
                self.show_history()
            elif cmd == "undo":
                self.undo()
            elif cmd == "redo":
                self.redo()
            else:
                parts = cmd.split()
                if len(parts) != 3:
                    print("Invalid input. Format: operation operand1 operand2")
                    continue
                op_name, val1, val2 = parts
                try:
                    val1 = float(val1)
                    val2 = float(val2)
                except ValueError:
                    print("Error: Arguments must be numbers.")
                    continue
                self.perform_operation(op_name, val1, val2)

if __name__ == "__main__":
    calc = Calculator()
    calc.repl()