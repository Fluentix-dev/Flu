import sys
from ..errors import RuntimeResult, DataTypeError

def to_number(arguments):
    if isinstance(arguments[0], bool):
        return RuntimeResult(int(arguments[0]))
    
    if isinstance(arguments[0], (int, float)):
        return RuntimeResult(arguments[0])

    if isinstance(arguments[0], str):
        try:
            return RuntimeResult(float(arguments[0]))
        except ValueError:
            return RuntimeResult(None, DataTypeError(f"Cannot convert string '{arguments[0]}' to a number", 99)) # unexpected
    
    if arguments[0] == None:
        return RuntimeResult(0)
    
    if isinstance(arguments[0], (list, tuple, set)):
        return RuntimeResult(None, DataTypeError("Cannot convert array to a number"), 99) # unexpected