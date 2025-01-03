from ..errors import RuntimeResult, MathError
import math

def square_root(arguments):
    if arguments[0] < 0:
        return RuntimeResult(None, MathError("Can't get square root of a negative number", 99)) # unexpected
    
    return RuntimeResult(math.sqrt(arguments[0]))

def cube_root(arguments):
    return RuntimeResult(arguments[0] ** (1/3))

pi = math.pi