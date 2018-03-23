"""
Convert the thing into a tree
"""

class Instruction:
    def __init__(self,name,arg):
        self.name = name
        self.argument = arg
        self.next = None

    def __str__(self):
        return self.name + "(" + self.argument + ")"

class Branch:
    def __init__(self,condition):
        self.condition = condition
        self.trueBody = None
        self.falseBody = None
        self.done = None
        pass

lexed = [('keyword', 'if'), ('Lparen', '('), ('number', '1234'), ('Rparen', ')'), ('Lbrace', '{'), ('keyword', 'if'), ('Lparen', '('), ('number', '1'), ('Rparen', ')'), ('Lbrace', '{'), ('instruction', 'IRC'), ('Lparen', '('), ('number', '7'), ('Rparen', ')'), ('Rbrace', '}'), ('keyword', 'else'), ('Lbrace', '{'), ('instruction', 'IRU'), ('Lparen', '('), ('string', '"A"'), ('Rparen', ')'), ('Rbrace', '}'), ('instruction', 'WRT'), ('Lparen', '('), ('string', '"8"'), ('Rparen', ')'), ('Rbrace', '}'), ('keyword', 'else'), ('Lbrace', '{'), ('keyword', 'if'), ('Lparen', '('), ('number', '1'), ('Rparen', ')'), ('Lbrace', '{'), ('instruction', 'IRC'), ('Lparen', '('), ('number', '7'), ('Rparen', ')'), ('Rbrace', '}'), ('instruction', 'IRU'), ('Lparen', '('), ('string', '"C"'), ('Rparen', ')'), ('Rbrace', '}')]

print """if(1234)
{
    if(1234)
    {
    IRU(7)
    }
WRT("8")
}
else{
if (1) {  irc(7) } else { WRT("A"")}
IRU("C")
}
"""

def parse(lexed,depth):
    parsed = []
    inBranch = False
    bodyOpened = False
    bodyClosed = False
    while len(lexed) > 0:
        lexType, item= lexed[0]
        if lexType == 'keyword':
            if item == 'if':
                if len(lexed) >= 6:
                    if lexed[1][0] == 'Lparen' and lexed[2][0] == 'number' and lexed[3][0] == 'Rparen' and lexed[4][0] == 'Lbrace':
                        parsed.append(Branch(lexed[2][1]))
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
                return parsed, lexed
        elif lexType == 'instruction':
            if len(lexed) >= 4:
                if lexed[1][0] == 'Lparen' and (lexed[2][0] == 'string' or lexed[2][0] == 'number') and lexed[3][0] == 'Rparen':
                    parsed.append(Instruction(item, lexed[2][1]))
                    lexed = lexed[3:]
        if depth == 0:
            break
        lexed = lexed[1:]
    return parsed,lexed

parsed, poop  = parse(lexed,0)


def pretty_print(parsed,depth):
    for item in parsed:
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
                pretty_print(item.falseBody,depth+1)
                print "\t"*depth + "}"
pretty_print(parsed, 0)



    





