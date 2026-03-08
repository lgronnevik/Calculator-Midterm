# app/history.py
from copy import deepcopy

class History:
    def __init__(self, max_size=100):
        self._history = []
        self._undo_stack = []
        self._redo_stack = []
        self.max_size = max_size
        self._observers = []

    # Observer methods
    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._history)

    # History management
    def add(self, calculation):
        if len(self._history) >= self.max_size:
            self._history.pop(0)
        self._history.append(calculation)
        self._undo_stack.append(deepcopy(self._history))
        self._redo_stack.clear()
        self.notify_observers()

    def undo(self):
        if len(self._undo_stack) > 1:
            self._redo_stack.append(self._undo_stack.pop())
            self._history = deepcopy(self._undo_stack[-1])
            self.notify_observers()
            return True
        return False

    def redo(self):
        if self._redo_stack:
            self._undo_stack.append(self._redo_stack.pop())
            self._history = deepcopy(self._undo_stack[-1])
            self.notify_observers()
            return True
        return False

    def all(self):
        return self._history