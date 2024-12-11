from ..errors import RuntimeResult, MathError, InterpreterError, DataTypeError, ModuleError
from .values import *

def evaluate_program(ast_node, environment):
    last_evaluated = None
    for statement in ast_node.body:
        rt = evaluate(statement, environment)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        last_evaluated = rt.result
    
    return RuntimeResult(last_evaluated)

def evaluate(ast_node, environment):
    match ast_node.kind.type:
        case "Program":
            rt = evaluate_program(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "Identifier":
            rt = evaluate_identifier(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "NumberLiteral":
            rt = evaluate_number_literal(ast_node)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "BooleanLiteral":
            rt = evaluate_boolean_literal(ast_node)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "NullLiteral":
            rt = evaluate_null_literal()
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "StringLiteral":
            rt = evaluate_string_literal(ast_node)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "ArrayLiteral":
            rt = evaluate_array_literal(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "CallExpression":
            rt = evaluate_call_expression(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "UnaryExpression":
            rt = evaluate_unary_expression(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "BinaryExpression":
            rt = evaluate_binary_expression(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "ComparisonExpression":
            rt = evaluate_comparison_expression(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "AssignmentStatement":
            rt = evaluate_assignment_statement(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "UpdateStatement":
            rt = evaluate_update_statement(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case "GetStatement":
            rt = evaluate_get_statement(ast_node, environment)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        case _:
            return RuntimeResult(None, InterpreterError(f"This AST node has not been setup for interpretion yet: {ast_node}", 35))

def evaluate_assignment_statement(ast_node, environment):
    rt = evaluate(ast_node.value, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    rt = environment.assign(ast_node.identifier, rt.result, ast_node.constant)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(None)

def evaluate_update_statement(ast_node, environment):
    rt = evaluate(ast_node.value, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    rt = environment.update(ast_node.identifier, rt.result)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(None)

def evaluate_get_statement(ast_node, environment):
    module = ast_node.module
    match module:
        case "conversions":
            import flu.runtime.conversions
            environment.assign("conversions", Module("conversions"), True)
            rt = environment.lookup("conversions")
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            module = rt.result
            module.assign("to_number", NativeFunction("to_number", flu.runtime.conversions.to_number, 1))
            return RuntimeResult(None)
        case _:
            return RuntimeResult(None, ModuleError(f"No module named {module}", 99)) # unexpected

def evaluate_identifier(ast_node, environment):
    rt = environment.lookup(ast_node.symbol)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    return RuntimeResult(rt.result)

def evaluate_number_literal(ast_node):
    return RuntimeResult(create_number(ast_node.value))

def evaluate_boolean_literal(ast_node):
    return RuntimeResult(Boolean(ast_node.value))

def evaluate_null_literal():
    return RuntimeResult(Null())

def evaluate_string_literal(ast_node):
    return RuntimeResult(String(ast_node.value))

def evaluate_array_literal(ast_node, environment):
    array = []
    for element in ast_node.value:
        rt = evaluate(element, environment)
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        array += [rt.result]
    
    return RuntimeResult(Array(array))

def evaluate_call_expression(ast_node, environment):
    rt = evaluate(ast_node.callee, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    if rt.result.type.type not in ("native function", "module"):
        return RuntimeResult(None, DataTypeError(f"Expected native function or module, got {rt.result.type.type}", 5))
    
    match rt.result.type.type:
        case "native function":
            callee = rt.result
            arguments = []
            for argument in ast_node.arguments:
                rt = evaluate(argument, environment)
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                arguments += [translate_fluentix_to_python(rt.result)]
            
            rt = callee.call(arguments)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(translate_python_to_fluentix(rt.result))
        case "module":
            if len(ast_node.arguments) != 1:
                return RuntimeResult(None, ArgumentError(f"Expected 1 function in '{rt.result.callee.symbol}', got {len(ast_node.arguments)}/1"))
            
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            func = ast_node.arguments[0]
            
            rt = environment.lookup(ast_node.callee.symbol)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            rt = rt.result.lookup(func.callee.symbol)
            if rt.error:
                return RuntimeResult(None, rt.error)

            func = rt.result
            arguments = []
            for argument in ast_node.arguments[0].arguments:
                rt = evaluate(argument, environment)
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                arguments += [translate_fluentix_to_python(rt.result)]
            
            rt = func.call(arguments)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(translate_python_to_fluentix(rt.result))

def evaluate_unary_expression(ast_node, environment):
    rt = evaluate(ast_node.value, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    match rt.result.type.type:
        case "number":
            if ast_node.sign == "-":
                return RuntimeResult(create_number(-rt.result.value))
            
            return RuntimeResult(rt.result)
        case _:
            return RuntimeResult(None, DataTypeError(f"Unexpected unary operation for '{rt.result.type.type}'", 2))

def evaluate_binary_expression(ast_node, environment):
    rt = evaluate(ast_node.left, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    left = rt.result
    
    rt = evaluate(ast_node.right, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    right = rt.result

    match ast_node.operator:
        case "Plus":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 42))
                    
                    return RuntimeResult(create_number(left.value + right.value))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 7))
        case "Minus":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 100))
            
            return RuntimeResult(create_number(left.value - right.value))
        case "Multiply":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 69))
            
            return RuntimeResult(create_number(left.value * right.value))
        case "Divide":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 21))
            
            if right.value == 0:
                return RuntimeResult(None, MathError(f"Cannot divide {left.value} by 0", 1))
            
            return RuntimeResult(create_number(left.value / right.value))
        case "Power":
            if left.type.type != "number" or right.type.type != "number":
                return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 16))
            
            return RuntimeResult(create_number(left.value ** right.value))

def evaluate_comparison_expression(ast_node, environment):
    rt = evaluate(ast_node.left, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    left = rt.result

    rt = evaluate(ast_node.right, environment)
    if rt.error:
        return RuntimeResult(None, rt.error)
    
    right = rt.result

    match ast_node.operator:
        case "Equals":
            if left.type.type != right.type.type:
                return RuntimeResult(Boolean("false"))
            
            if left.value == right.value:
                return RuntimeResult(Boolean("true"))
            
            return RuntimeResult(Boolean("false"))
        case "NotEquals":
            if left.type.type != right.type.type:
                return RuntimeResult(Boolean("true"))
            
            if left.value != right.value:
                return RuntimeResult(Boolean("true"))
            
            return RuntimeResult(Boolean("false"))
        case "GreaterThan":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    if left.value > right.value:
                        return RuntimeResult(Boolean("true"))

                    return RuntimeResult(Boolean("false"))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 99)) # unexpected
        case "GreaterThanOrEquals":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    if left.value >= right.value:
                        return RuntimeResult(Boolean("true"))

                    return RuntimeResult(Boolean("false"))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 99)) # unexpected
        case "SmallerThan":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    if left.value < right.value:
                        return RuntimeResult(Boolean("true"))

                    return RuntimeResult(Boolean("false"))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 99)) # unexpected
        case "SmallerThanOrEquals":
            match left.type.type:
                case "number":
                    if right.type.type != "number":
                        return RuntimeResult(None, DataTypeError(f"Unexpected operation between number and {right.type.type}", 99)) # unexpected
                    
                    if left.value <= right.value:
                        return RuntimeResult(Boolean("true"))

                    return RuntimeResult(Boolean("false"))
                case _:
                    return RuntimeResult(None, DataTypeError(f"Unexpected operation between {left.type.type} and {right.type.type}", 99)) # unexpected