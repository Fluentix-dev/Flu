import sys
from ..errors import RuntimeResult
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