from app.operations import OperationFactory
from app.history import History
from app.calculator_memento import CalculatorMemento
from app.calculator_config import CalculatorConfig
from colorama import init, Fore, Style
init(autoreset=True, convert=True)

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
        self.logger_observer.log_event("Calculator initialized.")

    def perform_operation(self, op_name, a, b):
        try:
            from app.input_validators import validate_inputs
            validate_inputs(a, b, config.max_input_value)
            operation = OperationFactory.get_operation(op_name)
            result = operation.execute(a, b)
            # Apply precision
            result = round(result, config.precision)
            # Save history before adding new calculation
            self.memento.save()
            from app.calculation import Calculation
            calculation = Calculation(op_name, a, b, result)
            self.history.add(calculation)
            self.logger_observer.log_event(f"Performed operation: {op_name}({a}, {b}) = {result}")
            print(Fore.GREEN + f"Result: {result}" + Style.RESET_ALL)
        except Exception as e:
            from app.exceptions import ValidationError, OperationError
            if isinstance(e, ValidationError):
                self.logger_observer.log_warning(f"Input Error: {e}")
                print(f"Input Error: {e}")
            elif isinstance(e, OperationError):
                self.logger_observer.log_error(f"Operation Error: {e}")
                print(Fore.RED + f"Operation Error: {e}" + Style.RESET_ALL)
            else:
                self.logger_observer.log_error(f"Unexpected Error: {e}")
                print(Fore.RED + f"Unexpected Error: {e}" + Style.RESET_ALL)

    def show_history(self):
        for entry in self.history.all():
            print(f"{entry.operation}({float(entry.val1)}, {float(entry.val2)}) = {float(entry.result)}")

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
                print("Exiting calculator. Goodbye!")
                break
            elif cmd == "help":
                print("Commands:")
                from app.operations import OperationFactory
                print(OperationFactory.get_operations_help())
                print("history, clear, undo, redo, save, load, help, exit")
            elif cmd == "history":
                self.show_history()
            elif cmd == "clear":
                self.history._history.clear()
                self.history._undo_stack.clear()
                self.history._redo_stack.clear()
                print("History cleared.")
            elif cmd == "undo":
                self.undo()
            elif cmd == "redo":
                self.redo()
            elif cmd == "save":
                # Manual save using pandas
                try:
                    from app.logger import AutoSaveObserver
                    observer = AutoSaveObserver(config.history_file)
                    observer.save_history(self.history.all())
                    print("History saved to file.")
                except Exception as e:
                    print(f"Save Error: {e}")
            elif cmd == "load":
                # Manual load using pandas
                try:
                    from app.logger import AutoSaveObserver
                    observer = AutoSaveObserver(config.history_file)
                    self.history._history.clear()
                    observer.load_history(self.history)
                    print("History loaded from file.")
                except Exception as e:
                    print(f"Load Error: {e}")
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