class CalculatorMemento:
    def __init__(self, history):
        self.history = history
        self.undo_stack = []
        self.redo_stack = []

    def save(self):
        self.undo_stack.append(self.history.get_all())

    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo.")
            return
        self.redo_stack.append(self.history.get_all())
        previous = self.undo_stack.pop()
        self.history._entries = previous
        print("Undo performed.")

    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo.")
            return
        self.undo_stack.append(self.history.get_all())
        next_state = self.redo_stack.pop()
        self.history._entries = next_state
        print("Redo performed.")