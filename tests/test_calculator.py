def test_repl_help(monkeypatch, capsys):
	calc = Calculator()
	inputs = iter(["help", "exit"])
	monkeypatch.setattr("builtins.input", lambda _: next(inputs))
	calc.repl()
	captured = capsys.readouterr()
	assert "Commands:" in captured.out

def test_repl_history(monkeypatch, capsys):
	calc = Calculator()
	calc.perform_operation("add", 2, 3)
	inputs = iter(["history", "exit"])
	monkeypatch.setattr("builtins.input", lambda _: next(inputs))
	calc.repl()
	captured = capsys.readouterr()
	assert "add(2.0, 3.0) = 5.0" in captured.out

def test_repl_clear(monkeypatch, capsys):
	calc = Calculator()
	calc.perform_operation("add", 2, 3)
	inputs = iter(["clear", "exit"])
	monkeypatch.setattr("builtins.input", lambda _: next(inputs))
	calc.repl()
	captured = capsys.readouterr()
	assert "History cleared." in captured.out
	assert len(calc.history.all()) == 0

def test_repl_save_load(monkeypatch, tmp_path, capsys):
	calc = Calculator()
	calc.perform_operation("add", 2, 3)
	csv_file = tmp_path / "history.csv"
	# Patch config.history_file to use temp file
	import app.calculator_config
	app.calculator_config.CalculatorConfig.history_file = str(csv_file)
	inputs = iter(["save", "clear", "load", "exit"])
	monkeypatch.setattr("builtins.input", lambda _: next(inputs))
	calc.repl()
	captured = capsys.readouterr()
	assert "History saved to file." in captured.out
	assert "History loaded from file." in captured.out
	assert len(calc.history.all()) == 1
def test_logger_edge_cases(tmp_path):
	log_file = tmp_path / "edge.log"
	logger = LoggingObserver(str(log_file))
	# Log empty event
	logger.log_event("")
	logger.log_warning("")
	logger.log_error("")
	# Log None
	logger.log_event(None)
	logger.log_warning(None)
	logger.log_error(None)
	with open(log_file, "r", encoding="utf-8") as f:
		content = f.read()
	assert "Event" in content
	assert "Warning" in content
	assert "Error" in content

def test_perform_operation_unexpected_error(monkeypatch):
	calc = Calculator()
	# Monkeypatch OperationFactory to raise unexpected error
	monkeypatch.setattr("app.operations.OperationFactory.get_operation", lambda name: (_ for _ in ()).throw(Exception("Unexpected!")))
	result = None
	try:
		calc.perform_operation("add", 2, 3)
	except Exception as e:
		result = str(e)
	assert result is None  # Error handled internally
from app.calculator_memento import CalculatorMemento

def test_invalid_command(monkeypatch):
	calc = Calculator()
	inputs = iter(["foobar", "exit"])
	monkeypatch.setattr("builtins.input", lambda _: next(inputs))
	calc.repl()
	# Should print invalid input message and not add to history
	assert len(calc.history.all()) == 0

def test_undo_redo_edge_cases():
	calc = Calculator()
	# Undo with no history
	calc.undo()
	# Redo with no history
	calc.redo()
	# Should not raise exceptions
	assert True

def test_memento_edge_cases():
	calc = Calculator()
	memento = CalculatorMemento(calc.history)
	# Undo/redo with empty stacks
	assert memento.undo() is None
	assert memento.redo() is None
from app.calculation import Calculation
import io
import sys
from app.exceptions import ValidationError, OperationError
from app.input_validators import validate_inputs
from app.history import History
from app.logger import LoggingObserver, AutoSaveObserver
import pandas as pd

def test_error_handling_divide_by_zero():
	calc = Calculator()
	result = None
	try:
		calc.perform_operation("divide", 5, 0)
	except Exception as e:
		result = str(e)
	assert result is None  # Error handled internally

def test_error_handling_invalid_input():
	calc = Calculator()
	result = None
	try:
		calc.perform_operation("add", "a", 5)
	except Exception as e:
		result = str(e)
	assert result is None  # Error handled internally

def test_clear_history():
	calc = Calculator()
	calc.perform_operation("add", 2, 3)
	calc.history._history.clear()
	assert len(calc.history.all()) == 0

def test_undo_redo():
	calc = Calculator()
	calc.perform_operation("add", 2, 3)
	calc.perform_operation("subtract", 5, 2)
	calc.undo()
	assert len(calc.history.all()) == 1
	calc.redo()
	assert len(calc.history.all()) == 2

def test_save_load(tmp_path):
	calc = Calculator()
	calc.perform_operation("add", 2, 3)
	csv_file = tmp_path / "history.csv"
	observer = AutoSaveObserver(str(csv_file))
	observer.save_history(calc.history.all())
	calc.history._history.clear()
	observer.load_history(calc.history)
	assert len(calc.history.all()) == 1
	assert calc.history.all()[0].operation == "add"

def test_logger(tmp_path):
	log_file = tmp_path / "test.log"
	logger = LoggingObserver(str(log_file))
	logger.log_event("Test event")
	logger.log_warning("Test warning")
	logger.log_error("Test error")
	logger.update([Calculation("add", 2, 3, 5)])
	with open(log_file, "r", encoding="utf-8") as f:
		content = f.read()
	assert "Test event" in content
	assert "Test warning" in content
	assert "Test error" in content
	assert "Calculation: add(2, 3) = 5" in content

def test_input_validators():
	validate_inputs(2, 3, 10)
	with pytest.raises(ValidationError):
		validate_inputs("a", 3, 10)
	with pytest.raises(ValidationError):
		validate_inputs(100, 3, 10)

def test_observer_pattern():
	history = History()
	class DummyObserver:
		def __init__(self):
			self.called = False
		def update(self, h):
			self.called = True
	observer = DummyObserver()
	history.register_observer(observer)
	history.add(Calculation("add", 2, 3, 5))
	assert observer.called
import pytest
from app.calculator import Calculator

def test_calculator_add(monkeypatch):
	calc = Calculator()
	inputs = iter(["add 2 3", "exit"])
	monkeypatch.setattr("builtins.input", lambda _: next(inputs))
	calc.repl()
	assert any(entry.operation == "add" and entry.result == 5 for entry in calc.history.all())

def test_calculator_invalid_input(monkeypatch):
	calc = Calculator()
	inputs = iter(["add a 5", "exit"])
	monkeypatch.setattr("builtins.input", lambda _: next(inputs))
	calc.repl()
	assert len(calc.history.all()) == 0
