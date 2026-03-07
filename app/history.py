class History:
    def __init__(self):
        self._entries = []

    def add(self, calculation):
        self._entries.append(calculation)

    def show(self):
        if not self._entries:
            print("No history.")
            return
        for i, c in enumerate(self._entries, 1):
            print(f"{i}: {c.operation}({c.val1}, {c.val2}) = {c.result}")

    def get_all(self):
        return self._entries[:]

    def clear(self):
        self._entries = []