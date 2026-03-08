# app/calculator_memento.py
class CalculatorMemento:
    def __init__(self, history):
        self.history = history
        self.undo_stack = []
        self.redo_stack = []

    def save(self):
        # Save a snapshot of history
        self.undo_stack.append(self.history.list()[:])
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return None
        snapshot = self.undo_stack.pop()
        self.redo_stack.append(self.history.list()[:])
        self.history.clear()
        for item in snapshot:
            self.history.add(item)
        return snapshot

    def redo(self):
        if not self.redo_stack:
            return None
        snapshot = self.redo_stack.pop()
        self.undo_stack.append(self.history.list()[:])
        self.history.clear()
        for item in snapshot:
            self.history.add(item)
        return snapshot