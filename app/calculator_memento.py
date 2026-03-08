# app/calculator_memento.py
class CalculatorMemento:
    def __init__(self, history):
        self.history = history

    def save(self):
        # Save a snapshot of history
        self.history._undo_stack.append(self.history.all()[:])
        self.history._redo_stack.clear()

    def undo(self):
        if self.history.undo():
            return self.history.all()
        return None

    def redo(self):
        if self.history.redo():
            return self.history.all()
        return None