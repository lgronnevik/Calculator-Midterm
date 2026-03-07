from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.calculator_config import CalculatorConfig
from app.history import History
from app.operations import OperationFactory
from app.logger import LoggingObserver, AutoSaveObserver

CALCULATOR_LOG_FILE = "calculator.log"
CALCULATOR_HISTORY_FILE = "history.csv"

class Calculator:
    def __init__(self):
        self.config = CalculatorConfig()
        self.history = History()
        self.memento = CalculatorMemento(self.history)
        self.observers = []
        self.register_observers()

    def register_observers(self):
        self.observers.append(LoggingObserver(CALCULATOR_LOG_FILE))
        self.observers.append(AutoSaveObserver(CALCULATOR_HISTORY_FILE))

    def perform_operation(self, operation_name, val1, val2):
        self.memento.save()
        op = OperationFactory.get_operation(operation_name)
        result = op.execute(val1, val2)
        calc = Calculation(operation_name, val1, val2, result)
        self.history.add(calc)
        for observer in self.observers:
            observer.update(calc)
        print(f"Result: {result}")

    def repl(self):
        print("Welcome to the Advanced Calculator! Type 'help' for commands.")
        while True:
            cmd = input(">> ").strip().split()
            if not cmd:
                continue
            action = cmd[0].lower()
            args = cmd[1:]
            if action == "exit":
                break
            elif action == "help":
                print("Commands: add, subtract, multiply, divide, power, root, "
                      "modulus, int_divide, percent, abs_diff, history, undo, redo, save, load, exit")
            elif action in ["add","subtract","multiply","divide","power","root",
                            "modulus","int_divide","percent","abs_diff"]:
                if len(args) != 2:
                    print("Error: Two numeric arguments required.")
                    continue
                try:
                    val1, val2 = float(args[0]), float(args[1])
                    self.perform_operation(action, val1, val2)
                except ValueError:
                    print("Error: Arguments must be numbers.")
            elif action == "history":
                self.history.show()
            elif action == "undo":
                self.memento.undo()
            elif action == "redo":
                self.memento.redo()
            elif action == "save":
                for observer in self.observers:
                    if isinstance(observer, AutoSaveObserver):
                        observer.save_history(self.history)
            elif action == "load":
                for observer in self.observers:
                    if isinstance(observer, AutoSaveObserver):
                        observer.load_history(self.history)
            else:
                print(f"Unknown command: {action}")

def repl():
    calc = Calculator()
    calc.repl()

if __name__ == "__main__":
    repl()