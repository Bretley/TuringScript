"""
This is the lexer for the Turing Machine
micro-langauge
"""

def lex(code):
    instructions = ["ILC","WRT","IRU","ILU","IRC"]
    lexed = []
    code = "".join(code.split())
    inNumber = False
    inString = False
    currentLexItem = ""
    while len(code) > 0:
        char = code[0]
        if inString:
            if char == "\"":
                currentLexItem += "\""
                lexed.append(("string", currentLexItem))
                currentLexItem = ""
                inString = False
            else:
                currentLexItem += char
        elif inNumber:
            if char.isdigit():
                currentLexItem += char
                if len(code) > 0 and (code[1].isdigit()):
                    pass
                else:
                    lexed.append(("number",currentLexItem))
                    currentLexItem = ""
                    inNumber = False
        else:
            if char == "\"":
                currentLexItem += "\""
                inString = True
            elif char.isdigit():
                if len(code) > 0 and (code[1].isdigit()):
                    inNumber = True
                    currentLexItem += char
                else:
                    lexed.append(('number',char))
                    currentLexItem = ""
                    inNumber = False

            elif char == "i" or char == "I":
                if len(code) > 0 and (code[1] == "F" or code[1] == "f"):
                    lexed.append(("keyword","if"))
                    code = code[1:]
            elif char == "(":
                lexed.append(("Lparen",char))
            elif char == ")":
                lexed.append(("Rparen",char))
            elif char == "{":
                lexed.append(("Lbrace",char))
            elif char == "}":
                lexed.append(("Rbrace",char))
            elif code.startswith("else"):
                lexed.append(('keyword',"else"))
                code = code[2:]
            for inst in instructions:
                if code.startswith(inst):
                    lexed.append(("instruction",inst))
                    code = code[len(inst)-2:]
        code = code[1:]
    return lexed



