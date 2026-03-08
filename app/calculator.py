# app/calculator.py
from app.operations import OperationFactory
from app.history import History
from app.calculator_memento import CalculatorMemento

CALCULATOR_MAX_HISTORY_SIZE = 100  # you can make this configurable later

class Calculator:
    def __init__(self):
        self.history = History(max_size=CALCULATOR_MAX_HISTORY_SIZE)
        self.memento = CalculatorMemento(self.history)
        # Observer setup
        from app.logger import LoggingObserver, AutoSaveObserver
        self.logger_observer = LoggingObserver("calculator.log")
        self.autosave_observer = AutoSaveObserver("history.csv")
        self.history.register_observer(self.logger_observer)
        self.history.register_observer(self.autosave_observer)

    def perform_operation(self, op_name, a, b):
        try:
            operation = OperationFactory.get_operation(op_name)
            result = operation.execute(a, b)
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