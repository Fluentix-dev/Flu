from .frontend.lexer import tokenize
from .frontend.parser import Parser
from .runtime.interpreter import evaluate
from .runtime.values import Environment, NativeFunction
import flu.runtime.builtin_functions

def execute_code(code, extension):
    global_environment = Environment()

    # normal
    global_environment.assign("show", NativeFunction("show", flu.runtime.builtin_functions.show), True)
    global_environment.assign("ask", NativeFunction("ask", flu.runtime.builtin_functions.ask), True)
    if extension == "fl":
        global_environment.assign("input", NativeFunction("input", flu.runtime.builtin_functions.ask), True)
    
    global_environment.assign("stop", NativeFunction("stop", flu.runtime.builtin_functions.stop, 1), True)

    # conversions
    global_environment.assign("tonumber", NativeFunction("tonumber", flu.runtime.builtin_functions.tonumber, 1), True)
    global_environment.assign("tostring", NativeFunction("tostring", flu.runtime.builtin_functions.tostring, 1), True)

    # math
    global_environment.assign("absolute", NativeFunction("absolute", flu.runtime.builtin_functions.absolute, 1), True)

    rt = tokenize(code, extension)
    if rt.error:
        rt.error.show_error()

    #print(f"Tokens: {rt.result}\n")

    parser = Parser(rt.result, extension)
    rt = parser.produce_ast()
    if rt.error:
        rt.error.show_error()
    
    #print(f"Tree: {rt.result}\n")

    rt = evaluate(rt.result, global_environment)
    if rt.error:
        rt.error.show_error()
    
    #print(f"Result: {rt.result}")