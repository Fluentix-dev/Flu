from ..errors import *
import flu.runtime.values as v
from ..frontend.lexer import tokenize
from ..frontend.parser import Parser
import sys
import flu.runtime.builtin_functions

sys.setrecursionlimit(10**9)

FILE_EXTENSION = None

def evaluate_program(ast_node, environment, in_function, in_loop, return_env):
    last_evaluated = None
    for statement in ast_node.body:
        rt = evaluate(statement, environment, in_function, in_loop, return_env)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        last_evaluated = rt.result
        if isinstance(last_evaluated, v.Return):
            return RuntimeResult(last_evaluated)
        
        if isinstance(last_evaluated, v.Stop):
            return RuntimeResult(last_evaluated)
    
    return RuntimeResult(last_evaluated)

def evaluate(ast_node, environment, in_function, in_loop, return_env):
    match ast_node.kind.type:
        case "Program":
            rt = evaluate_program(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "Identifier":
            rt = evaluate_identifier(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "NumberLiteral":
            rt = evaluate_number_literal(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "BooleanLiteral":
            rt = evaluate_boolean_literal(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "NullLiteral":
            rt = evaluate_null_literal(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "StringLiteral":
            rt = evaluate_string_literal(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "ArrayLiteral":
            rt = evaluate_array_literal(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "CallExpression":
            rt = evaluate_call_expression(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "UnaryExpression":
            rt = evaluate_unary_expression(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "BinaryExpression":
            rt = evaluate_binary_expression(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "ComparisonExpression":
            rt = evaluate_comparison_expression(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "AssignmentStatement":
            rt = evaluate_assignment_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "UpdateStatement":
            rt = evaluate_update_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "GetStatement":
            rt = evaluate_get_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "IfUnlessElseStatement":
            rt = evaluate_if_unless_else_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "FunctionDeclarationStatement":
            rt = evaluate_function_declaration_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "ReturnStatement":
            rt = evaluate_return_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)

            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "UntilStatement":
            rt = evaluate_until_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "StopStatement":
            rt = evaluate_stop_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "ForeverStatement":
            rt = evaluate_forever_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "IncludeStatement":
            rt = evaluate_include_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)

            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case "ExcludeStatement":
            rt = evaluate_exclude_statement(ast_node, environment, in_function, in_loop, return_env)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if return_env:
                return RuntimeResult((rt.result, environment))
            
            return RuntimeResult(rt.result)
        case _:
            return RuntimeResult(None, InterpreterError(f"This AST node has not been setup for interpretion yet: {ast_node}", 35))

def evaluate_assignment_statement(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.value, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    rt = environment.assign(ast_node.identifier, rt.result, ast_node.constant)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(None)

def evaluate_update_statement(ast_node, environment, in_function, in_loop, return_env):
    match ast_node.identifier.kind.type:
        case "Identifier":
            rt = evaluate(ast_node.value, environment, in_function, in_loop, False)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            rt = environment.update(ast_node.identifier.symbol, rt.result)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(None)
        case "CallExpression":
            callee = ast_node.identifier.callee
            rt = evaluate(callee, environment, in_function, in_loop, False)
            if rt.error:
                return RuntimeResult(None, rt.error)

            if rt.result.type.type != "array":
                return RuntimeResult(None, DataTypeError(f"Expected array, got {rt.result.type.type}"))
            
            array = rt.result
            rt = evaluate(ast_node.identifier.arguments[0], environment, in_function, in_loop, False)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if rt.result.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Expected number, got {rt.result.type.type}", 99)) # unexpected
            
            if rt.result.value % 1 > 0:
                return RuntimeResult(None, ValueError(f"Expected integer, got remainder {rt.result.value % 1}/1", 99)) # unexpected

            if rt.result.value > len(array.value):
                return RuntimeResult(None, ValueError(f"Expected a number smaller than or equals{len(array)}, got {rt.result.value}", 99)) # unexpected
            
            if rt.result.value < 1:
                return RuntimeResult(None, ValueError(f"Expected a number larger than 0, got {rt.result.value}", 99)) # unexpected

            index = rt.result.value - 1
            rt = evaluate(ast_node.value, environment, in_function, in_loop, False)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            array.value[index] = rt.result
            return RuntimeResult(None)

def evaluate_get_statement(ast_node, environment, in_function, in_loop, return_env):
    module = ast_node.module
    match module:
        # import module
        case "math":
            import flu.runtime.math2 as math2
            module = v.Module("math")
            module.assign("sqrt", v.NativeFunction("sqrt", math2.square_root, 1))
            module.assign("cbrt", v.NativeFunction("cbrt", math2.cube_root, 1))
            module.assign("pi", v.Number(math2.pi))
            rt = environment.assign("math", module, True)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(None)
        case _:
            code = None
            extension = None
            global_environment = v.Environment(FILE_EXTENSION)

            try:
                with open(f"{module}.flu") as file:
                    code = file.read()
                    extension = "flu"
            except FileNotFoundError:
                try:
                    with open(f"{module}.fl") as file:
                        code = file.read()
                        extension = "fl"
                except FileNotFoundError:
                    return RuntimeResult(None, ModuleError(f"No module named {module}", 99)) # unexpected
            
            rt = tokenize(code, extension)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            parser = Parser(rt.result, extension)
            rt = parser.produce_ast()
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            rt = evaluate(rt.result, global_environment, in_function, in_loop, True)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            module = v.Module(module)
            module.table = rt.result[1].table
            rt = environment.assign(module.name, module, True)
            if rt.error:
                return RuntimeResult(None, rt.error)

            return RuntimeResult(None)

def evaluate_if_unless_else_statement(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.condition, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)

    if rt.result.type.type == "boolean" and rt.result.value == "true":
        rt = evaluate(ast_node.body, environment, in_function, in_loop, False)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        return RuntimeResult(rt.result)

    if not ast_node.next:
        return RuntimeResult(None, rt.error)
    
    rt = evaluate_if_unless_else_statement(ast_node.next, environment, in_function, in_loop, return_env)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(rt.result)

def evaluate_function_declaration_statement(ast_node, environment, in_function, in_loop, return_env):
    environment.assign(ast_node.func_name, v.DefinedFunction(ast_node.func_name, ast_node.body, ast_node.arguments), True)
    return RuntimeResult(None)

def evaluate_return_statement(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.value, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(v.Return(rt.result))

def evaluate_until_statement(ast_node, environment, in_function, in_loop, return_env):
    while True:
        rt = evaluate(ast_node.condition, environment, in_function, True, False)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if rt.result.type.type == "boolean" and rt.result.value == "true":
            return RuntimeResult(None)

        rt = evaluate(ast_node.body, environment, in_function, True, False)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if isinstance(rt.result, v.Return):
            if not in_function:
                return RuntimeResult(None, ReturnError("Cannot return outside of function", 99)) # unexpected

            return RuntimeResult(rt.result)
        
        if isinstance(rt.result, v.Stop):
            return RuntimeResult(None)

def evaluate_stop_statement(ast_node, environment, in_function, in_loop, return_env):
    return RuntimeResult(v.Stop())

def evaluate_forever_statement(ast_node, environment, in_function, in_loop, return_env):
    while True:
        rt = evaluate(ast_node.body, environment, in_function, True, False)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if isinstance(rt.result, v.Return):
            if not in_function:
                return RuntimeResult(None, ReturnError("Cannot return outside of function", 99)) # unexpected

            return RuntimeResult(rt.result)
        
        if isinstance(rt.result, v.Stop):
            return RuntimeResult(None)

def evaluate_include_statement(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.array, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    if rt.result.type.type not in ("array",):
        return RuntimeResult(None, DataTypeError(f"Expected array, got {rt.result.type.type}"))
    
    array = rt.result
    if ast_node.index:
        rt = evaluate(ast_node.index, environment, in_function, in_loop, False)
        if rt.error:
            return RuntimeResult(None, rt.error)

        if rt.result.type.type != "number":
            return RuntimeResult(None, DataTypeError(f"Expected number, got {rt.result.type.type}", 99)) # unexpected
        
        if rt.result.value % 1 > 0:
            return RuntimeResult(None, ValueError(f"Expected integer, got remainder {rt.result.value % 1}/1", 99)) # unexpected

        if rt.result.value > len(array.value):
            return RuntimeResult(None, ValueError(f"Expected a number smaller than or equals{len(array)}, got {rt.result.value}", 99)) # unexpected
        
        if rt.result.value < 1:
            return RuntimeResult(None, ValueError(f"Expected a number larger than 0, got {rt.result.value}", 99)) # unexpected

        index = rt.result.value
    else:
        index = len(array.value)

    rt = evaluate(ast_node.element, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    element = rt.result
    array.value.insert(index, element)
    return RuntimeResult(None)

def evaluate_exclude_statement(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.array, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    if rt.result.type.type not in ("array",):
        return RuntimeResult(None, DataTypeError(f"Expected array, got {rt.result.type.type}"))

    array = rt.result
    rt = evaluate(ast_node.index, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)

    if rt.result.type.type != "number":
        return RuntimeResult(None, DataTypeError(f"Expected number, got {rt.result.type.type}", 99)) # unexpected
    
    if rt.result.value % 1 > 0:
        return RuntimeResult(None, ValueError(f"Expected integer, got remainder {rt.result.value % 1}/1", 99)) # unexpected

    if rt.result.value > len(array.value):
        return RuntimeResult(None, ValueError(f"Expected a number smaller than or equals{len(array)}, got {rt.result.value}", 99)) # unexpected
    
    if rt.result.value < 1:
        return RuntimeResult(None, ValueError(f"Expected a number larger than 0, got {rt.result.value}", 99)) # unexpected

    index = rt.result.value
    array.value.pop(index)
    return RuntimeResult(None)

def evaluate_identifier(ast_node, environment, in_function, in_loop, return_env):
    rt = environment.lookup(ast_node.symbol)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(rt.result)

def evaluate_number_literal(ast_node, environment, in_function, in_loop, return_env):
    return RuntimeResult(v.create_number(ast_node.value))

def evaluate_boolean_literal(ast_node, environment, in_function, in_loop, return_env):
    return RuntimeResult(v.Boolean(ast_node.value))

def evaluate_null_literal(ast_node, environment, in_function, in_loop, return_env):
    return RuntimeResult(v.Null())

def evaluate_string_literal(ast_node, environment, in_function, in_loop, return_env):
    return RuntimeResult(v.String(ast_node.value))

def evaluate_array_literal(ast_node, environment, in_function, in_loop, return_env):
    array = []
    for element in ast_node.value:
        rt = evaluate(element, environment, in_function, in_loop, False)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        array += [rt.result]
    
    return RuntimeResult(v.Array(array))

def evaluate_call_expression(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.callee, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    if rt.result.type.type not in ("native function", "defined function", "module", "array"):
        return RuntimeResult(None, DataTypeError(f"Expected native function, defined function, array or module, got {rt.result.type.type}", 5))
    
    match rt.result.type.type:
        case "native function":
            callee = rt.result
            arguments = []
            for argument in ast_node.arguments:
                rt = evaluate(argument, environment, in_function, in_loop, False)
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                arguments += [v.translate_fluentix_to_python(rt.result)]

            rt = callee.call(arguments)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(v.translate_python_to_fluentix(rt.result))
        case "defined function":
            callee = rt.result
            arguments = []
            for argument in ast_node.arguments:
                rt = evaluate(argument, environment, in_function, in_loop, False)
                if rt.error:
                    return RuntimeResult(None, rt.error)

                arguments += [rt.result]
            
            rt = callee.call(arguments, environment, in_loop)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "module":
            if len(ast_node.arguments) != 1:
                return RuntimeResult(None, ArgumentError(f"Expected 1 function in '{rt.result.name}', got {len(ast_node.arguments)}/1", 99)) # unexpected

            rt = environment.lookup(rt.result.name)
            if rt.error:
                return RuntimeResult(None, rt.error)

            match ast_node.arguments[0].kind.type:
                case "CallExpression":
                    rt = evaluate_call_expression(ast_node.arguments[0], rt.result, in_function, in_loop, False)
                    if rt.error:
                        return RuntimeResult(None, rt.error)
                    
                    return RuntimeResult(rt.result)
                case "Identifier":
                    rt = evaluate_identifier(ast_node.arguments[0], rt.result, in_function, in_loop, False)
                    if rt.error:
                        return RuntimeResult(None, rt.error)

                    return RuntimeResult(rt.result)
                case _:
                    return RuntimeResult(None, SyntaxError("Invalid Syntax!", 99)) # unexpected
        case "array":
            array = rt.result
            if len(ast_node.arguments) != 1:
                return RuntimeResult(None, ArgumentError(f"Expected 1 number in '{rt.result.callee.symbol}, got {len(ast_node.arguments)}/1", 99)) # unexpected

            rt = evaluate(ast_node.arguments[0], environment, in_function, in_loop, False)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            if rt.result.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Expected number, got {rt.result.type.type}", 99)) # unexpected
            
            if rt.result.value % 1 > 0:
                return RuntimeResult(None, ValueError(f"Expected integer, got remainder {rt.result.value % 1}/1", 99)) # unexpected

            if rt.result.value > len(array.value):
                return RuntimeResult(None, ValueError(f"Expected a number smaller than or equals to {len(array.value)}, got {rt.result.value}", 99)) # unexpected
            
            if rt.result.value < 1:
                return RuntimeResult(None, ValueError(f"Expected a number larger than 0, got {rt.result.value}", 99)) # unexpected

            return RuntimeResult(array.value[rt.result.value-1])

def evaluate_unary_expression(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.value, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    match rt.result.type.type:
        case "number":
            if ast_node.sign == "-":
                return RuntimeResult(v.create_number(-rt.result.value))
            
            return RuntimeResult(rt.result)
        case _:
            return RuntimeResult(None, DataTypeError(f"Unexpected unary operation for '{rt.result.type.type}'", 2))

def evaluate_binary_expression(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.left, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    left = rt.result
    
    rt = evaluate(ast_node.right, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    right = rt.result

    match ast_node.operator:
        case "Plus":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 42))
                    
                    return RuntimeResult(v.create_number(left.value + right.value))
                case "string":
                    if right.type.type != "string":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    return RuntimeResult(v.String(left.value + right.value))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 7))
        case "Minus":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 100))
            
            return RuntimeResult(v.create_number(left.value - right.value))
        case "Multiply":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 69))
            
            return RuntimeResult(v.create_number(left.value * right.value))
        case "Divide":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 21))
            
            if right.value == 0:
                return RuntimeResult(None, MathError(f"Cannot divide {left.value} by 0", 1))
            
            return RuntimeResult(v.create_number(left.value / right.value))
        case "Power":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 16))
            
            return RuntimeResult(v.create_number(left.value ** right.value))

def evaluate_comparison_expression(ast_node, environment, in_function, in_loop, return_env):
    rt = evaluate(ast_node.left, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    left = rt.result

    rt = evaluate(ast_node.right, environment, in_function, in_loop, False)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    right = rt.result

    match ast_node.operator:
        case "Equals":
            if left.type.type != right.type.type:
                return RuntimeResult(v.Boolean("false"))
            
            if left.value == right.value:
                return RuntimeResult(v.Boolean("true"))
            
            return RuntimeResult(v.Boolean("false"))
        case "NotEquals":
            if left.type.type != right.type.type:
                return RuntimeResult(v.Boolean("true"))
            
            if left.value != right.value:
                return RuntimeResult(v.Boolean("true"))
            
            return RuntimeResult(v.Boolean("false"))
        case "GreaterThan":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    if left.value > right.value:
                        return RuntimeResult(v.Boolean("true"))

                    return RuntimeResult(v.Boolean("false"))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 99)) # unexpected
        case "GreaterThanOrEquals":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    if left.value >= right.value:
                        return RuntimeResult(v.Boolean("true"))

                    return RuntimeResult(v.Boolean("false"))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 99)) # unexpected
        case "SmallerThan":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    if left.value < right.value:
                        return RuntimeResult(v.Boolean("true"))

                    return RuntimeResult(v.Boolean("false"))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 99)) # unexpected
        case "SmallerThanOrEquals":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    if left.value <= right.value:
                        return RuntimeResult(v.Boolean("true"))

                    return RuntimeResult(v.Boolean("false"))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 99)) # unexpected