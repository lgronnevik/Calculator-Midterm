import pytest
from app.operations import OperationFactory

@pytest.mark.parametrize("op_name,a,b,expected", [
	("add", 2, 3, 5),
	("subtract", 5, 2, 3),
	("multiply", 4, 5, 20),
	("divide", 10, 2, 5),
	("power", 2, 3, 8),
	("root", 8, 3, 2),
	("modulus", 10, 3, 1),
	("int_divide", 10, 3, 3),
	("percent", 50, 200, 25),
	("abs_diff", 5, 12, 7),
])
def test_operations(op_name, a, b, expected):
	op = OperationFactory.get_operation(op_name)
	result = op.execute(a, b)
	if op_name == "root":
		assert round(result, 6) == round(expected, 6)
	else:
		assert result == expected

def test_divide_by_zero():
	op = OperationFactory.get_operation("divide")
	with pytest.raises(ValueError):
		op.execute(5, 0)

def test_int_divide_by_zero():
	op = OperationFactory.get_operation("int_divide")
	with pytest.raises(ValueError):
		op.execute(5, 0)

def test_root_zero():
	op = OperationFactory.get_operation("root")
	with pytest.raises(ValueError):
		op.execute(8, 0)
