from .frontend.lexer import tokenize
from .frontend.parser import Parser
import flu.runtime.interpreter as interpreter
from .runtime.values import Environment, NativeFunction, Return, Stop
from .errors import ReturnError, StopError
import sys
import flu.runtime.builtin_functions

def execute_code(code, extension):
    try:
        interpreter.FILE_EXTENSION = extension
        global_environment = Environment(extension=interpreter.FILE_EXTENSION)

        rt = tokenize(code, extension)
        if rt.error:
            rt.error.show_error()

        #print(f"Tokens: {rt.result}\n")

        parser = Parser(rt.result, extension)
        rt = parser.produce_ast()
        if rt.error:
            rt.error.show_error()
        
        #print(f"Tree: {rt.result}\n")

        rt = interpreter.evaluate(rt.result, global_environment, False, False, False)
        if rt.error:
            rt.error.show_error()
        
        #print(f"Result: {rt.result}")

        if isinstance(rt.result, Return):
            error = ReturnError("Cannot return outside of function", 99) # unexpected
            error.show_error()
        
        if isinstance(rt.Result, Stop):
            error = StopError("Cannot break outside of loop", 99) # unexpected
            error.show_error()
    except KeyboardInterrupt:
        sys.stdout.write("\n[INFO] Process force quitted")

def execute_cmd():
    interpreter.FILE_EXTENSION = "fl"
    global_environment = Environment(extension=interpreter.FILE_EXTENSION)

    sys.stdout.write("flu >> ")
    sys.stdout.flush()
    while True:
        try:
            code = sys.stdin.readline()[0:-1]
            if code == "exit":
                break
            rt = tokenize(code, "fl")
            if rt.error:
                rt.error.show_error()

            #print(f"Tokens: {rt.result}\n")

            parser = Parser(rt.result, "fl")
            rt = parser.produce_ast()
            if rt.error:
                rt.error.show_error()
            
            #print(f"Tree: {rt.result}\n")

            rt = interpreter.evaluate(rt.result, global_environment)
            if rt.error:
                rt.error.show_error()
            
            #print(f"Result: {rt.result}")

            if isinstance(rt.result, Return):
                error = ReturnError("Cannot return outside of function", 99) # unexpected
                error.show_error()
            
            sys.stdout.write("flu >> ")
            sys.stdout.flush()
        except KeyboardInterrupt:
            sys.stdout.write("\n[INFO] Forced exiting terminal...")
            sys.exit()
