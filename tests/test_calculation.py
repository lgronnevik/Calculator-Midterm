from app.calculation import Calculation

def test_calculation():
	calc = Calculation("add", 2, 3, 5)
	assert calc.operation == "add"
	assert calc.val1 == 2
	assert calc.val2 == 3
	assert calc.result == 5
