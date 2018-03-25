class Body:
    def __init__(self,instructions,terminal):
        self.instructions = instructions
        self.terminal = terminal
        self.code = None
        self.haltState = None
        
    def simplify(self):
        for item in self.instructions:
            if isinstance(item, Body):
                item.simplify()

            elif isinstance(item, Branch):
                item.simplify()

            if len(self.instructions) == 1 and isinstance(self.instructions[0], Body):
                self.instructions[0].simplify()
                self.instructions = self.instructions[0].instructions

    def isTerminal(self):
        return self.terminal

    def getNumStates(self):
        if self.isTerminal() and self.code is not None:
            size = len(self.code)
        else:
            size = 0
            for item in self.instructions:
                size += item.getNumStates()
        return size

class Instruction:
    def __init__(self,name,arg):
        self.name = name
        self.argument = arg
        self.next = None
        self.code = None

    def __str__(self):
        return self.name + "(" + self.argument + ")"

class Branch:
    def __init__(self,condition):
        self.branchCode = None
        self.escapeTrue = None
        self.condition = condition
        self.trueBody = None
        self.falseBody = None
    
    def isTerminal(self):
        if self.falseBody is None:
            return self.trueBody.isTerminal()
        else:
            return (self.trueBody.isTerminal() and self.falseBody.isTerminal())

    def simplify(self):
        self.trueBody.simplify()
        if self.falseBody is not None:
            self.falseBody.simplify()

    def getNumStates(self):
        # Branches are only one state (for now?)
        size = 1 # Maybe fix later if adding optimization for multibody if
        size += self.trueBody.getNumStates()
        if self.falseBody is not None:
            size += self.falseBody.getNumStates()
        return size

def parse(lexed,depth):
    parsed = []
    terminal = True
    inBranch = False
    bodyOpened = False
    bodyClosed = False
    while len(lexed) > 0:
        lexType, item= lexed[0]
        if lexType == 'keyword':
            if item == 'if':
                if len(lexed) >= 6:
                    if lexed[1][0] == 'Lparen' and lexed[2][0] == 'number' and lexed[3][0] == 'Rparen' and lexed[4][0] == 'Lbrace':
                        if len(parsed) > 0:
                            parsed = [Body(parsed, terminal)]
                        parsed.append(Branch(lexed[2][1]))
                        terminal = False
                        inBranch = True
                        lexed = lexed[4:]
                        parsed[-1].trueBody, lexed = parse(lexed,depth+1)
                        continue
                else:
                    print "Not enough symbols left to form valid If"
            elif lexed[0][1] == 'else':
                if not inBranch:
                    print "Error, Else without if"
                else:
                    if len(lexed) >= 3:
                        if lexed[1][0] == "Lbrace":
                            lexed = lexed[1:]
                            parsed[-1].falseBody,lexed = parse(lexed,depth+1)
                            continue
        elif lexType == 'Lbrace':
            bodyOpened = True
        elif lexType == 'Rbrace':
            if bodyOpened:
                lexed = lexed[1:]
                return Body(parsed, terminal), lexed
        elif lexType == 'instruction':
            if len(lexed) >= 4:
                if lexed[1][0] == 'Lparen' and (lexed[2][0] == 'string' or lexed[2][0] == 'number') and lexed[3][0] == 'Rparen':
                    if len(parsed) > 0:
                        if isinstance(parsed[-1], Branch):
                            parsed.append(Body([Instruction(item, lexed[2][1])], True))
                        else:
                            parsed[-1].instructions.append(Instruction(item, lexed[2][1]))
                    else:
                            parsed.append(Body([Instruction(item, lexed[2][1])], True))
                    lexed = lexed[3:]
        lexed = lexed[1:]
    return Body(parsed, terminal),lexed

def pretty_print(parsed,depth):
    if isinstance(parsed, Body):
        for item in parsed.instructions:
            if isinstance(item,Instruction):
                print "\t"*depth + str(item)
            elif isinstance(item, Branch):
                print "\t"*depth + "if(" + str(item.condition) + ")"
                print "\t"*depth + "{"
                pretty_print(item.trueBody,depth+1)
                print "\t"*depth + "}"
                if item.falseBody is not None:
                    print "\t"*depth + "else"
                    print "\t"*depth + "{"
                    print "False"
                    pretty_print(item.falseBody,depth+1)
                    print "\t"*depth + "}"
            elif isinstance(item, Body):
                pretty_print(item,depth)

def pretty_print2(item, depth):
    if isinstance(item, Body):
        if item.code is not None:
            for x in item.instructions:
                print "\t"*depth + str(x)
            for x in item.code:
                print str(x) + ": " + str(item.code[x])
        for item in item.instructions:
            if isinstance(item, Branch):
                if item.branchCode is not None:
                    print item.branchCode
                    pretty_print2(item.branchCode,depth+1)
                print "\t"*depth + "if(" + str(item.condition) + ")"
                print "\t"*depth + "{"
                pretty_print2(item.trueBody,depth+1)
                if item.escapeTrue is not None: 
                    for x in item.escapeTrue:
                        print x, item.escapeTrue[x]
                    pass
                    
                print "\t"*depth + "}"
                if item.falseBody is not None:
                    print "\t"*depth + "else"
                    print "\t"*depth + "{"
                    pretty_print2(item.falseBody,depth+1)
                    print "\t"*depth + "}"
            elif isinstance(item, Body):
                pretty_print2(item,depth)





