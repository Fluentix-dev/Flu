import sys
from ..errors import RuntimeResult, DataTypeError, SyntaxError
from .values import translate_python_to_fluentix

def show(arguments, newline=True):
    sys.stdout.write(" ".join([translate_python_to_fluentix(argument).__repr__() for argument in arguments]))
    if newline:
        sys.stdout.write("\n")

    return RuntimeResult(None)

def ask(arguments):
    show(arguments, False)
    return RuntimeResult(sys.stdin.readline()[0:-1])

def stop(arguments):
    sys.exit(arguments[0])

def tonumber(arguments):
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
    

def tostring(arguments):
    if isinstance(arguments[0], bool):
        return RuntimeResult(str(arguments[0]).lower())
    
    if isinstance(arguments[0], (int, float)):
        return RuntimeResult(str(arguments[0]))

    if isinstance(arguments[0], str):
        return RuntimeResult(arguments[0])
    
    if arguments[0] == None:
        return RuntimeResult("null")
    
    if isinstance(arguments[0], (list, tuple, set)):
        return RuntimeResult(str([tostring([element]) for element in arguments[0]]))
    

def absolute(arguments):
    value = arguments[0]
    if isinstance(value, (int, float)):
        return RuntimeResult(abs(value))

    elif isinstance(value, str):
        try:
            return RuntimeResult(abs(float(value)))
        except:
            pass
    return RuntimeResult(None, DataTypeError(f"Absolute value '{value}' must be a number.", 99)) # unexpec


