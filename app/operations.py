class Operation:
    def execute(self, a, b):
        raise NotImplementedError

class Add(Operation):
    def execute(self, a, b):
        return a + b

class Subtract(Operation):
    def execute(self, a, b):
        return a - b

class Multiply(Operation):
    def execute(self, a, b):
        return a * b

class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

class Power(Operation):
    def execute(self, a, b):
        return a ** b

class Root(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Cannot take 0th root.")
        return a ** (1 / b)

class Modulus(Operation):
    def execute(self, a, b):
        return a % b

class IntDivide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a // b

class Percent(Operation):
    def execute(self, a, b):
        return (a / b) * 100

class AbsDiff(Operation):
    def execute(self, a, b):
        return abs(a - b)

class OperationFactory:
    @staticmethod
    def get_operations_help():
        help_lines = []
        for name, cls in OperationFactory.operations.items():
            doc = cls.__doc__ or "Performs the operation."
            help_lines.append(f"- {name}: {doc.strip()}")
        return "\n".join(help_lines)

    operations = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntDivide,
        "percent": Percent,
        "abs_diff": AbsDiff,
    }

    @staticmethod
    def get_operation(name):
        if name not in OperationFactory.operations:
            raise ValueError(f"Unknown operation: {name}")
        return OperationFactory.operations[name]()