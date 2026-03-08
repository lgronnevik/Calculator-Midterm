import datetime

class Calculation:
    def __init__(self, operation, val1, val2, result, timestamp=None):
        self.operation = operation
        self.val1 = val1
        self.val2 = val2
        self.result = result
        self.timestamp = timestamp or datetime.datetime.now().isoformat()