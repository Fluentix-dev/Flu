import sys

class RuntimeResult:
    def __init__(self, result, error=None):
        self.result = result
        self.error = error

class ErrorType:
    def __init__(self, type):
        self.type = type

class Error:
    def __init__(self, error, reason, error_code):
        self.error = error
        self.error_code = error_code
        self.reason = reason
    
    def show_error(self):
        print(f"{self.error.type}#{self.error_code}: {self.reason}\nLearn more at https://docs.fluentix.dev/code/")
        sys.exit(self.error_code)

class SyntaxError(Error):
    def __init__(self, reason, error_code):
        super().__init__(ErrorType("SyntaxError"), reason, error_code)

class DataTypeError(Error):
    def __init__(self, reason, error_code):
        super().__init__(ErrorType("DataTypeError"), reason, error_code)

class MathError(Error):
    def __init__(self, reason, error_code):
        super().__init__(ErrorType("MathError"), reason, error_code)

class VariableError(Error):
    def __init__(self, reason, error_code):
        super().__init__(ErrorType("VariableError"), reason, error_code)

class InterpreterError(Error):
    def __init__(self, reason, error_code):
        super().__init__(ErrorType("InterpreterError"), reason, error_code)

class ArgumentError(Error):
    def __init__(self, reason, error_code):
        super().__init__(ErrorType("ArgumentError"), reason, error_code)

class ModuleError(Error):
    def __init__(self, reason, error_code):
        super().__init__(ErrorType("ModuleError"), reason, error_code)