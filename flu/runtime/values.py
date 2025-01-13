from ..errors import RuntimeResult, VariableError, DataTypeError, ArgumentError, StopError
import flu.runtime.interpreter as interpreter
import flu.runtime.builtin_functions

class Environment:
    def __init__(self, extension, parent=None):
        self.table = {}
        self.parent = parent
        self.constants = set()
        self.extension = extension

        if not self.parent:
            # normal
            self.assign("show", NativeFunction("show", flu.runtime.builtin_functions.show), True)
            self.assign("ask", NativeFunction("ask", flu.runtime.builtin_functions.ask), True)
            if self.extension == "fl":
                self.assign("input", NativeFunction("input", flu.runtime.builtin_functions.ask), True)
            
            self.assign("stop", NativeFunction("stop", flu.runtime.builtin_functions.stop, 1), True)

            # conversions
            self.assign("tonumber", NativeFunction("tonumber", flu.runtime.builtin_functions.tonumber, 1), True)
            self.assign("tostring", NativeFunction("tostring", flu.runtime.builtin_functions.tostring, 1), True)

            # math
            self.assign("absolute", NativeFunction("absolute", flu.runtime.builtin_functions.absolute, 1), True)
    
    def lookup(self, var_name):
        if var_name not in self.table:
            if not self.parent:
                return RuntimeResult(None, VariableError(f"Cannot get the value of variable {var_name} because it does not exist.", 35))

            rt = self.parent.lookup(var_name)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result, None)
        
        return RuntimeResult(self.table[var_name], None)

    def update(self, var_name, value):
        if var_name not in self.table:
            return RuntimeResult(None, VariableError(f"Cannot update variable {var_name} because it does not exist.", 41))
        
        if var_name in self.constants:
            return RuntimeResult(None, VariableError(f"Cannot update variable {var_name} because it is a constant.", 80))

        self.table[var_name] = value
        return RuntimeResult(None, None)
    
    def assign(self, var_name, value, constant):
        if var_name in self.table:
            return RuntimeResult(None, VariableError(f"Cannot assign variable {var_name} because it exists.", 5))
        
        self.table.update({var_name: value})
        if constant:
            self.constants.add(var_name)

        return RuntimeResult(None, None)
    
    def copy(self):
        env = Environment(extension=self.extension)
        env.parent = self
        return env

class ValueType:
    def __init__(self, type):
        self.type = type

class RuntimeValue:
    def __init__(self, type):
        self.type = type

# unrelated but useful runtime values
class Return(RuntimeValue):
    def __init__(self, value):
        super().__init__(ValueType("Return"))
        self.value = value

    def __repr__(self):
        return f"<return {self.value}>"

class Stop(RuntimeValue):
    def __init__(self):
        pass

    def __repr__(self):
        return "<stop>"

class Module(RuntimeValue):
    def __init__(self, name):
        super().__init__(ValueType("module"))
        self.name = name
        self.table = {}
    
    def assign(self, var_name, value):
        if var_name in self.table:
            return RuntimeResult(None, VariableError(f"Cannot assign variable {var_name} because it exists.", 5))
            
        self.table.update({var_name: value})
        return RuntimeResult(None)
    
    def lookup(self, var_name):
        if var_name not in self.table:
            return RuntimeResult(None, VariableError(f"Cannot get the value of variable {var_name} because it does not exist.", 35))
        
        return RuntimeResult(self.table[var_name])
    
    def __repr__(self):
        return f"<module {self.name}>"

class Number(RuntimeValue):
    def __init__(self, value):
        super().__init__(ValueType("number"))
        self.value = value
    
    def __repr__(self):
        return str(self.value)

class Boolean(RuntimeValue):
    def __init__(self, value):
        super().__init__(ValueType("boolean"))
        self.value = value
    
    def __repr__(self):
        return self.value

class Null(RuntimeValue):
    def __init__(self):
        super().__init__(ValueType("null"))
    
    def __repr__(self):
        return "null"

class String(RuntimeValue):
    def __init__(self, value):
        super().__init__(ValueType("string"))
        self.value = value
    
    def __repr__(self):
        return self.value

class Array(RuntimeValue):
    def __init__(self, value):
        super().__init__(ValueType("array"))
        self.value = value
    
    def __repr__(self):
        return f"[{'; '.join([element.__repr__() for element in self.value])}]"

class NativeFunction(RuntimeValue):
    def __init__(self, name, value, arguments=None):
        super().__init__(ValueType("native function"))
        self.name = name
        self.value = value
        self.arguments = arguments
    
    def call(self, arguments):
        if self.arguments == None:
            return self.value(arguments)
        
        if len(arguments) != self.arguments:
            return RuntimeResult(None, ArgumentError(f"Expected {self.arguments} argument in {self.name}, got {len(arguments)}/{self.arguments}", 39))

        return self.value(arguments)

    def __repr__(self):
        return f"<function {self.name}>"

class DefinedFunction(RuntimeValue):
    def __init__(self, name, value, arguments):
        super().__init__(ValueType("defined function"))
        self.name = name
        self.value = value
        self.arguments = arguments
    
    def call(self, arguments, environment, in_loop):
        if len(arguments) != len(self.arguments):
            return RuntimeResult(None, ArgumentError(f"Expected {len(self.arguments)} arguments in {self.name}, got {len(arguments)}/{len(self.arguments)}", 39))

        env = environment.copy()
        for i, argument in enumerate(arguments):
            env.table.update({self.arguments[i]: argument})
            if self.arguments[i] in env.constants:
                env.constants.remove(self.arguments[i])
        
        rt = interpreter.evaluate(self.value, env, True, in_loop, False)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if isinstance(rt.result, Stop):
            if not in_loop:
                return RuntimeResult(None, StopError("Cannot break outside of loop", 99)) # unexpected
            
            return RuntimeResult(None)

        if isinstance(rt.result, Return):
            return RuntimeResult(rt.result.value)
        
        return RuntimeResult(rt.result)
    
    def __repr__(self):
        return f"<function {self.name}>"

def create_number(value):
    return Number(int(value) if value % 1 == 0 else value)

def translate_fluentix_to_python(value):
    match value.type.type:
        case "number":
            return value.value
        case "boolean":
            if value.value == "true":
                return True
            
            return False
        case "null":
            return None
        case "string":
            return value.value
        case "array":
            new = []
            for element in value.value:
                new += [translate_fluentix_to_python(element)]
            
            return new
        case "defined function":
            return value
        case "native function":
            return value

def translate_python_to_fluentix(value):
    if isinstance(value, bool):
        if value:
            return Boolean("true")
        
        return Boolean("false")
    
    if isinstance(value, (int, float)):
        return create_number(value)
    
    if value == None:
        return Null()
    
    if isinstance(value, str):
        return String(value)
    
    if isinstance(value, (list, tuple, set)):
        new = []
        for element in value:
            new += [translate_python_to_fluentix(element)]

        return Array(new)
    
    if isinstance(value, (DefinedFunction, NativeFunction)):
        return value
    
    return RuntimeResult(None, DataTypeError(f"Invalid data type in Python not translated to Fluentix: {type(value)}", 15))