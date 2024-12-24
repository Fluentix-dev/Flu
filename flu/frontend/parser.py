from .abstract_syntax_tree import *
from ..errors import RuntimeResult, SyntaxError
from .lexer import Token, TokenType

class Parser:
    def __init__(self, tokens, extension):
        self.tokens = tokens
        self.extension = extension
    
    def at(self):
        return self.tokens[0]

    def skip_tab(self):
        while self.at().type.type == "Tab":
            self.tokens.pop(0)

    def eat(self):
        self.skip_tab()
        return self.tokens.pop(0)

    def expect(self, *expected, error):
        token = self.eat()
        if token.type.type not in expected:
            if self.in_end(token):
                return RuntimeResult(None, error)
            
            return RuntimeResult(None, SyntaxError(f"{error.reason}, got '{token.value}'", error.error_code))
        
        return RuntimeResult(token)

    def in_end(self, token):
        return token.type.type in ("EOF", "Newline")

    def in_whitespace(self, token):
        return token.type.type in ("Newline", "Tab")

    def not_eof(self):
        return self.at().type.type != "EOF"

    def produce_ast(self):
        program = Program([])
        while self.not_eof():
            while self.at().type.type == "Newline":
                self.eat()

            if self.at().type.type == "EOF":
                return RuntimeResult(program)

            rt = self.parse_statement()
            if rt.error:
                return RuntimeResult(None, rt.error)

            program.body += [rt.result]

        return RuntimeResult(program)

    def parse_statement(self):
        match self.at().type.type:
            case "Variable":
                rt = self.parse_variable_keyword_assignment()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Let":
                rt = self.parse_let_keyword_assignment()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Constant":
                rt = self.parse_constant_keyword_assignment()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Create":
                if self.extension == "fl":
                    rt = self.parse_create_statement()
                    if rt.error:
                        return RuntimeResult(None, rt.error)
                    
                    return RuntimeResult(rt.result)
            case "If":
                rt = self.parse_if_unless_else()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Get":
                rt = self.parse_get_statement()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Define":
                rt = self.parse_function_declaration()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Return":
                rt = self.parse_return_statement()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)

        rt = self.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if self.at().type.type == "Is":
            rt = self.parse_update_statement(rt.result)
            if rt.error:
                return RuntimeResult(None, rt.error)
            
        return RuntimeResult(rt.result)

    def parse_variable_keyword_assignment(self):
        self.eat()
        rt = self.expect("Identifier", error=SyntaxError("Expected identifier", 65))
        if rt.error:
            return RuntimeResult(None, rt.error)

        identifier = rt.result.value
        
        rt = self.expect("Is", error=SyntaxError("Expected 'is'", 15))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if not self.in_end(self.at()):
            return RuntimeResult(None, SyntaxError(f"Expected newline or nothing, got '{self.at().value}'", 61))
        
        return RuntimeResult(AssignmentStatement(identifier, rt.result))
    
    def parse_let_keyword_assignment(self):
        self.eat()
        rt = self.expect("Identifier", error=SyntaxError("Expected identifier", 57))
        if rt.error:
            return RuntimeResult(None, rt.error)

        identifier = rt.result.value
        
        rt = self.expect("Be", error=SyntaxError("Expected 'be'", 34))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if not self.in_end(self.at()):
            return RuntimeResult(None, SyntaxError(f"Expected newline or nothing, got '{self.at().value}'", 98))
        
        return RuntimeResult(AssignmentStatement(identifier, rt.result))

    def parse_constant_keyword_assignment(self):
        self.eat()
        rt = self.expect("Identifier", error=SyntaxError("Expected identifier", 19))
        if rt.error:
            return RuntimeResult(None, rt.error)

        identifier = rt.result.value
        
        rt = self.expect("Is", error=SyntaxError("Expected 'is'", 68))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if not self.in_end(self.at()):
            return RuntimeResult(None, SyntaxError(f"Expected newline or nothing, got '{self.at().value}'", 37))
        
        return RuntimeResult(AssignmentStatement(identifier, rt.result, True))

    def parse_create_statement(self):
        self.eat()
        rt = self.expect("Colon", error=SyntaxError("Expected ':'", 80))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.expect("Variable", "Constant", "Changeable", "Unchangeable", error=SyntaxError("Expected 'variable', 'constant', 'changeable' or 'unchangeable'", 97))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        self.tokens = [rt.result] + self.tokens
        match rt.result.type.type:
            case "Variable":
                rt = self.parse_variable_keyword_assignment()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Constant":
                rt = self.parse_constant_keyword_assignment()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Changeable":
                rt = self.parse_variable_keyword_assignment()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)
            case "Unchangeable":
                rt = self.parse_constant_keyword_assignment()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(rt.result)

    def parse_update_statement(self, identifier):
        self.eat()
        rt = self.expect("Now", error=SyntaxError(f"Expected 'now', got '{self.at().value}'", 92))
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if not self.in_end(self.at()):
            return RuntimeResult(None, SyntaxError(f"Expected newline or nothing, got '{self.at().value}'", 67))
        
        return RuntimeResult(UpdateStatement(identifier, rt.result))

    def parse_get_statement(self):
        self.eat()
        rt = self.expect("Colon", error=SyntaxError("Expected ':'", 99)) # unexpected
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.expect("Module", error=SyntaxError("Expected 'module'", 99)) # unexpected
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.expect("Identifier", error=SyntaxError("Expected module name", 99)) # unexpected
        if rt.error:
            return RuntimeResult(None, rt.error)

        if not self.in_end(self.at()):
            return RuntimeResult(None, SyntaxError(f"Expected newline or nothing, got '{self.at().value}'", 99)) # unexpected

        return RuntimeResult(GetStatement(rt.result.value))

    def parse_if_unless_else(self):
        # Consume the "if" token
        self.eat()  # Eat "if"/"unless"

        # Parse the "if" condition
        condition_tokens = []
        while not self.in_end(self.at()):
            condition_tokens += [self.eat()]

        # Parse the condition expression
        condition_parser = Parser(condition_tokens + [Token(TokenType("EOF"), "EOF")], self.extension)
        rt = condition_parser.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)

        condition = rt.result

        body = []
        while self.not_eof():
            while self.at().type.type == "Newline":
                body += [self.tokens.pop(0)]
            
            if self.at().type.type != "Tab":
                break
            
            self.tokens.pop(0)
            while not self.in_end(self.at()):
                body += [self.tokens.pop(0)]
        
        parser = Parser(body + [Token(TokenType("EOF"), "EOF")], self.extension)
        rt = parser.produce_ast()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        body = rt.result
        match self.at().type.type:
            case "Unless":
                rt = self.parse_if_unless_else()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(IfUnlessElseStatement(condition, body, rt.result))
            case "Else":
                self.eat()
                else_body = []
                while self.not_eof():
                    while self.at().type.type == "Newline":
                        else_body += [self.tokens.pop(0)]
                    
                    # check for tab
                    if self.at().type.type != "Tab":
                        break
                    
                    self.tokens.pop(0)
                    while not self.in_end(self.at()):
                        else_body += [self.tokens.pop(0)]
                
                parser = Parser(else_body + [Token(TokenType("EOF"), "EOF")], self.extension)
                rt = parser.produce_ast()
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                else_body = rt.result
                return RuntimeResult(IfUnlessElseStatement(condition, body, IfUnlessElseStatement(TrueLiteral(), else_body)))
            case _:
                return RuntimeResult(IfUnlessElseStatement(condition, body)) # next is reserved for unless/else

    def parse_function_declaration(self):
        self.eat()
        rt = self.expect("Identifier", error=SyntaxError("Expected identifier", 99)) # unexpected
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        func_name = rt.result.value
        rt = self.expect("With", error=SyntaxError("Expected 'with'", 99)) # unexpected
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        rt = self.expect("Colon", error=SyntaxError("Expected ':'", 99)) # unexpected
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        arguments = []
        while not self.in_end(self.at()):
            rt = self.expect("Identifier", error=SyntaxError("Expected 'identifier'", 99)) # unexpected
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            arguments += [rt.result.value]
            if self.in_end(self.at()):
                break

            rt = self.expect("Semi", error=SyntaxError("Expected ';'", 99)) # unexpected
            if rt.error:
                return RuntimeResult(None, rt.error)
        
        body = []
        while self.not_eof():
            while self.at().type.type == "Newline":
                body += [self.tokens.pop(0)]
            
            if self.at().type.type != "Tab":
                break
            
            self.tokens.pop(0)
            while not self.in_end(self.at()):
                body += [self.tokens.pop(0)]
        
        parser = Parser(body + [Token(TokenType("EOF"), "EOF")], self.extension)
        rt = parser.produce_ast()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        body = rt.result
        return RuntimeResult(FunctionDeclarationStatement(func_name, arguments, body))

    def parse_return_statement(self):
        self.eat()
        if self.in_end(self.at()):
            return RuntimeResult(ReturnStatement(NullLiteral()))
        
        parser = Parser(self.tokens + [Token(TokenType("EOF"), "EOF")], self.extension)
        rt = parser.parse_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        return RuntimeResult(ReturnStatement(rt.result))

    def parse_expression(self):
        rt = self.parse_comparison_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        return RuntimeResult(rt.result)
    
    def parse_comparison_expression(self):
        left = self.parse_additive_expression()
        if left.error:
            return RuntimeResult(None, left.error)
        
        left = left.result
        while self.at().type.type in ("Equals", "NotEquals", "GreaterThan", "GreaterThanOrEquals", "SmallerThan", "SmallerThanOrEquals"):
            operator = self.eat()
            right = self.parse_additive_expression()
            if right.error:
                return RuntimeResult(None, right.error)

            left = ComparisonExpression(left, right.result, operator.type.type)
        
        return RuntimeResult(left)

    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        if left.error:
            return RuntimeResult(None, left.error)
        
        left = left.result
        while self.at().type.type in ("Plus", "Minus"):
            operator = self.eat()
            right = self.parse_multiplicative_expression()
            if right.error:
                return RuntimeResult(None, right.error)
            
            left = BinaryExpression(left, operator.type.type, right.result)
        
        return RuntimeResult(left)
    
    def parse_multiplicative_expression(self):
        left = self.parse_exponentation_expression()
        if left.error:
            return RuntimeResult(None, left.error)
        
        left = left.result
        while self.at().type.type in ("Multiply", "Divide"):
            operator = self.eat()
            right = self.parse_exponentation_expression()
            if right.error:
                return RuntimeResult(None, right.error)
            
            left = BinaryExpression(left, operator.type.type, right.result)
        
        return RuntimeResult(left)
    
    def parse_exponentation_expression(self):
        rt = self.parse_unary_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        elements = [rt.result]
        while self.at().type.type == "Power":
            self.eat()
            rt = self.parse_unary_expression()
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            elements += [rt.result]
        
        elements = elements[::-1]
        left = None
        for element in elements:
            if left:
                left = BinaryExpression(element, "Power", left)
            else:
                left = element
        
        return RuntimeResult(left)

    def parse_unary_expression(self):
        if self.at().type.type not in ("Plus", "Minus"):
            rt = self.parse_call_expression()
            if rt.error:
                return RuntimeResult(None, rt.error)
            
            return RuntimeResult(rt.result)
        
        sign = "+"
        while self.at().type.type in ("Plus", "Minus"):
            operator = self.eat()
            if operator.type.type == "Minus":
                sign = "-" if sign == "+" else "-"
        
        rt = self.parse_call_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        return RuntimeResult(UnaryExpression(sign, rt.result))
    
    def parse_call_expression(self):
        rt = self.parse_primary_expression()
        if rt.error:
            return RuntimeResult(None, rt.error)
        
        if self.at().type.type != "Colon":
            return RuntimeResult(rt.result)
        
        callee = rt.result

        inside = []
        stack = []
        self.eat()
        while not self.in_end(self.at()):
            if self.at().type.type in ("OpenBracket", "OpenParen"):
                stack += [self.at().type.type]
            elif self.at().type.type == "CloseParen":
                if not stack:
                    break
                
                if stack[0] != "OpenParen":
                    return RuntimeResult(None, SyntaxError("Unexpected ')'", 42))

                stack.pop(0)
            elif self.at().type.type == "CloseBracket":
                if not stack:
                    break
                
                if stack[0] != "OpenBracket":
                    return RuntimeResult(None, SyntaxError("Unexpected ']'", 69))

                stack.pop(0)
            
            inside += [self.eat()]
        
        elements = []
        element = []
        stack = []
        for token in inside:
            if token.type.type == "Semi" and not stack:
                if element:
                    elements += [element]
                    element = []
            else:
                element += [token]
            
            if token.type.type in ("OpenBracket", "OpenParen"):
                stack += [token.type.type]
            elif token.type.type == "CloseParen":
                if "OpenParen" not in stack:
                    return RuntimeResult(None, SyntaxError("Unexpected ')'", 63))
                
                if stack[0] != "OpenParen":
                    return RuntimeResult(None, SyntaxError("Unexpected ')'", 84))

                stack.pop(0)
            elif token.type.type == "CloseBracket":
                if "OpenBracket" not in stack:
                    return RuntimeResult(None, SyntaxError("Unexpected ']'", 17))
                
                if stack[0] != "OpenBracket":
                    return RuntimeResult(None, SyntaxError("Unexpected ']'", 27))

                stack.pop(0)
        
        if element:
            elements += [element]
        
        new = []
        for element in elements:
            parser = Parser(element + [Token(TokenType("EOF"), "EOF")], self.extension)
            rt = parser.parse_expression()
            if rt.error:
                return RuntimeResult(None, rt.error)

            new += [rt.result]
        
        return RuntimeResult(CallExpression(callee, new))

    def parse_primary_expression(self):
        match self.at().type.type:
            case "Identifier":
                return RuntimeResult(Identifier(self.eat().value))
            case "Number":
                return RuntimeResult(NumberLiteral(float(self.eat().value)))
            case "True":
                self.eat()
                return RuntimeResult(TrueLiteral())
            case "False":
                self.eat()
                return RuntimeResult(FalseLiteral())
            case "Null":
                self.eat()
                return RuntimeResult(NullLiteral())
            case "String":
                return RuntimeResult(StringLiteral(self.eat().value.encode().decode('unicode_escape')))
            case "OpenParen":
                self.eat()
                expression = self.parse_expression()
                if expression.error:
                    return RuntimeResult(None, expression.error)
                
                rt = self.expect("CloseParen", error=SyntaxError("Expected ')'", 99))
                if rt.error:
                    return RuntimeResult(None, rt.error)
                
                return RuntimeResult(expression.result)
            case "OpenBracket":
                self.eat()
                inside = []
                stack = []
                while (self.at().type.type != "CloseBracket" or stack) and self.at().type.type != "EOF":
                    token = self.eat()
                    if token.type.type in ("OpenBracket", "OpenParen"):
                        stack += [token.type.type]
                    elif token.type.type == "CloseParen":
                        if "OpenParen" not in stack:
                            return RuntimeResult(None, SyntaxError("Unexpected ')'", 89))
                        
                        if stack[0] != "OpenParen":
                            return RuntimeResult(None, SyntaxError("Unexpected ')'", 6))

                        stack.pop(0)
                    elif token.type.type == "CloseBracket":
                        if "OpenBracket" not in stack:
                            return RuntimeResult(None, SyntaxError("Unexpected ']'", 8))
                        
                        if stack[0] != "OpenBracket":
                            return RuntimeResult(None, SyntaxError("Unexpected ']'", 23))

                        stack.pop(0)
                    
                    inside += [token]
                
                if self.at().type.type == "EOF":
                    return RuntimeResult(None, SyntaxError("Unexpected ']'", 25))

                self.eat()
                
                elements = []
                element = []
                stack = []
                for token in inside:
                    if token.type.type == "Semi" and not stack:
                        if element:
                            elements += [element]
                            element = []
                    elif not self.in_end(token):
                        element += [token]
                    
                    if token.type.type in ("OpenBracket", "OpenParen"):
                        stack += [token.type.type]
                    elif token.type.type == "CloseParen":
                        if "OpenParen" not in stack:
                            return RuntimeResult(None, SyntaxError("Unexpected ')'", 63))
                        
                        if stack[0] != "OpenParen":
                            return RuntimeResult(None, SyntaxError("Unexpected ')'", 84))

                        stack.pop(0)
                    elif token.type.type == "CloseBracket":
                        if "OpenBracket" not in stack:
                            return RuntimeResult(None, SyntaxError("Unexpected ']'", 17))
                        
                        if stack[0] != "OpenBracket":
                            return RuntimeResult(None, SyntaxError("Unexpected ']'", 27))

                        stack.pop(0)
                
                if element:
                    elements += [element]

                new = []
                for element in elements:
                    parser = Parser(element + [Token(TokenType("EOF"), "EOF")], self.extension)
                    rt = parser.parse_expression()
                    if rt.error:
                        return RuntimeResult(None, rt.error)
                    
                    new += [rt.result]
                
                return RuntimeResult(ArrayLiteral(new))
            case _:
                return RuntimeResult(None, SyntaxError(f"Unexpected token found: '{self.at()}'", 11))