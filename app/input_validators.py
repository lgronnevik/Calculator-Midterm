# app/input_validators.py
from app.exceptions import ValidationError

def validate_inputs(a, b, max_value):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValidationError("Inputs must be numbers.")
    if abs(a) > max_value or abs(b) > max_value:
        raise ValidationError(f"Inputs cannot exceed {max_value}.")