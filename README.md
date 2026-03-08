# Calculator Midterm Project

## Project Description
A command-line calculator supporting advanced operations, history management, undo/redo, logging, auto-save, and configuration via .env. Features include:
- Arithmetic operations (add, subtract, multiply, divide, power, root, modulus, integer division, percent, absolute difference)
- History with undo/redo (Memento pattern)
- Observer pattern for logging and auto-save
- Configuration management with .env and python-dotenv
- Serialization and persistence with pandas
- Unit tests with pytest and coverage
- CI/CD with GitHub Actions

## Installation Instructions
1. Clone the repository:
	 ```
	 git clone https://github.com/your-username/your-repo-name.git
	 cd your-repo-name
	 ```
2. Create and activate a virtual environment:
	 ```
	 python -m venv venv
	 venv\Scripts\activate   # Windows
	 source venv/bin/activate  # Mac/Linux
	 ```
3. Install dependencies:
	 ```
	 pip install -r requirements.txt
	 ```

## Configuration Setup
- Create a `.env` file in the project root with:
	```
	CALCULATOR_LOG_DIR=logs
	CALCULATOR_HISTORY_DIR=history
	CALCULATOR_MAX_HISTORY_SIZE=100
	CALCULATOR_AUTO_SAVE=true
	CALCULATOR_PRECISION=2
	CALCULATOR_MAX_INPUT_VALUE=1000000
	CALCULATOR_DEFAULT_ENCODING=utf-8
	```

## Usage Guide
- Start the calculator:
	```
	python -m app.calculator
	```
- Supported commands:
	- `add`, `subtract`, `multiply`, `divide`, `power`, `root`, `modulus`, `int_divide`, `percent`, `abs_diff`
	- `history`, `clear`, `undo`, `redo`, `save`, `load`, `help`, `exit`

## Testing Instructions
- Run all tests:
	```
	pytest --cov=app
	```
- Check coverage (aim for 90%+):
	```
	pytest --cov=app --cov-report=html
	```

## CI/CD Information
- GitHub Actions workflow runs tests and enforces 90% coverage on every push/pull request to main.
- See `.github/workflows/python-app.yml` for details.

## Code Documentation
- Code is documented with comments and docstrings.
- See `.env` setup and logging configuration in README and code.
