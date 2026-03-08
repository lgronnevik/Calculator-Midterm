# app/history.py
from collections import deque

class History:
    def __init__(self, max_size=100):
        self._history = deque(maxlen=max_size)

    def add(self, calculation):
        self._history.append(calculation)

    def undo(self):
        if not self._history:
            return None
        return self._history.pop()

    def list(self):
        return list(self._history)

    def clear(self):
        self._history.clear()