from string import ascii_letters, digits
from ..errors import RuntimeResult, SyntaxError

class TokenType:
    def __init__(self, type):
        self.type = type
    
    def __repr__(self):
        return f"(TOKEN TYPE {self.type})"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"(TOKEN with token type {self.type.__repr__()} and value {self.value})"

def define_keywords(extension):
    KEYWORDS = {
        "variable": TokenType("Variable"),
        "let": TokenType("Let"),
        "constant": TokenType("Constant"),
        "is": TokenType("Is"),
        "be": TokenType("Be"),
        "now": TokenType("Now"),
        "true": TokenType("True"),
        "false": TokenType("False"),
        "null": TokenType("Null"),
        "get": TokenType("Get"),
        "module": TokenType("Module"),
        "if": TokenType("If"),
        "unless": TokenType("Unless"),
        "else": TokenType("Else"),
        "define": TokenType("Define"),
        "with": TokenType("With")
    }

    if extension == "fl":
        KEYWORDS.update({"create": TokenType("Create"), "changeable": TokenType("Changeable"), "unchangeable": TokenType("Unchangeable")})
    
    return KEYWORDS

DIGITS = digits + "."
LETTERS = ascii_letters + "_"
LEGALS = DIGITS + LETTERS
QUOTES = "'\""

def tokenize(code, extension):
    KEYWORDS = define_keywords(extension)
    src = list(code)
    tokens = []
    while src:
        match src[0]:
            case "\t":
                tokens += [Token(TokenType("Tab"), src.pop(0))]
            case "\n":
                tokens += [Token(TokenType("Newline"), src.pop(0))]
            case "+":
                tokens += [Token(TokenType("Plus"), src.pop(0))]
            case "-":
                tokens += [Token(TokenType("Minus"), src.pop(0))]
            case "*":
                tokens += [Token(TokenType("Multiply"), src.pop(0))]
            case "/":
                tokens += [Token(TokenType("Divide"), src.pop(0))]
            case "^":
                tokens += [Token(TokenType("Power"), src.pop(0))]
            case "(":
                tokens += [Token(TokenType("OpenParen"), src.pop(0))]
            case ")":
                tokens += [Token(TokenType("CloseParen"), src.pop(0))]
            case "[":
                tokens += [Token(TokenType("OpenBracket"), src.pop(0))]
            case "]":
                tokens += [Token(TokenType("CloseBracket"), src.pop(0))]
            case ":":
                tokens += [Token(TokenType("Colon"), src.pop(0))]
            case ";":
                tokens += [Token(TokenType("Semi"), src.pop(0))]
            case "=":
                tokens += [Token(TokenType("Equals"), src.pop(0))]
            case "!":
                src.pop(0)
                if not src:
                    return RuntimeResult(None, SyntaxError("Expected '='", 99)) # not decided
                
                if src.pop(0) != "=":
                    return RuntimeResult(None, SyntaxError("Expected '='", 99)) # not decided
                
                tokens += [Token(TokenType("NotEquals"), "!=")]
            case ">":
                src.pop(0)
                if not src:
                    tokens += [Token(TokenType("GreaterThan"), ">")]
                    continue

                if src[0] != "=":
                    tokens += [Token(TokenType("GreaterThan"), ">")]
                    continue

                tokens += [Token(TokenType("GreaterThanOrEquals"), ">=")]
                src.pop(0)
            case "<":
                src.pop(0)
                if not src:
                    tokens += [Token(TokenType("SmallerThan"), "<")]
                    continue

                if src[0] != "=":
                    tokens += [Token(TokenType("SmallerThan"), "<")]
                    continue

                tokens += [Token(TokenType("SmallerThanOrEquals"), "<=")]
                src.pop(0)
            case _:
                if src[0:4] == [" "] * 4:
                    tokens += [Token(TokenType("Tab"), "    ")]
                    for i in range(4):
                        src.pop(0)
                    
                    continue

                if src[0] == " ":
                    src.pop(0)
                    continue

                if src[0] in DIGITS:
                    number = ""
                    dot_count = 0
                    while src[0] in DIGITS:
                        if src[0] == ".":
                            dot_count += 1
                        
                        number += src.pop(0)
                        if not src:
                            break
                    
                    if dot_count > 1:
                        return RuntimeResult(None, SyntaxError(f"Expected 0 or 1 '.' in a number, got {dot_count}/1", 36))
                    
                    tokens += [Token(TokenType("Number"), number)]
                    continue

                if src[0] in LETTERS:
                    identifier = ""
                    while src[0] in LEGALS:
                        identifier += src.pop(0)
                        if not src:
                            break

                    if identifier in KEYWORDS:
                        tokens += [Token(KEYWORDS[identifier], identifier)]
                        continue

                    tokens += [Token(TokenType("Identifier"), identifier)]
                    continue

                if src[0] in QUOTES:
                    quote = src.pop(0)
                    string = ""
                    flag = True
                    while src:
                        if src[0] == quote:
                            flag = False
                            break

                        string += src[0]
                        if src[0] == "\\":
                            src.pop(0)
                            if not src:
                                break

                            string += src.pop(0)
                        
                        src.pop(0)
                    
                    if flag:
                        return RuntimeResult(None, SyntaxError(f"Expected '{quote}'", 83))
                    
                    tokens += [Token(TokenType("String"), string)]
                    src.pop(0)
                    continue

                return RuntimeResult(None, SyntaxError(f"Unexpected character: '{src[0]}'", 47))
            
    return RuntimeResult(tokens + [Token(TokenType("EOF"), "EOF")])

