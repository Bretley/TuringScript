import sys
""" This is where the implementation of what I'd call macros or micro-instructions lives. """





""" This is where we're going to start abstracting the language.
    Believe it or not, thinking in terms of return oriented programming 
    is probably a benefit here. The goal is to ultimately construct a chain of 
    'gadgets' that would enable the emulation of an assembly like language
""" 
L = "L"
R = "R"
alphabet = ["0","1"," ","A","B", "S"] # Just binary for now
""" Compiling:
    Well, to be honest I don't know too much about compiling, but it seems like at this small of a level,
    the only thing we need to do is link the states together. Figuring out how to name states and how to link control-flow
    is going to be a fun one.
"""

"""
IFF(symbol): q_branch: symbol -> (symbol, q_true, R)
                       not_symbol -> (not_symbol, q_false, R)
"""

def genIgnoreLeftUntil(char):
    code = {0:{}}
    count = 0
    """Ignore Right Until X= On any symbol not X, continue Right. On X, Go right one and Write X.
    IRightUntil(untilSymbol)= { q_right: [symbol in alphabet] -> (symbol, repeat-state, Right ), untilSymbol -> (untilSymbol, next-state, Right) }"""
    for symbol in alphabet:
        if symbol != char:
            code[0].update({symbol: (symbol, 0, L)})
    code[0].update({char: (char, 1, R)})
    return count, code

def genIgnoreRightUntil(char):
    code = {0:{}}
    count = 0
    """Ignore Right Until X= On any symbol not X, continue Right. On X, Go right one and Write X.
    IRightUntil(untilSymbol)= { q_right: [symbol in alphabet] -> (symbol, repeat-state, Right ), untilSymbol -> (untilSymbol, next-state, Right) }"""
    for symbol in alphabet:
        if symbol != char:
            code[0].update({symbol: (symbol, 0, R)})
    code[0].update({char: (char, -1, R)})
    return count, code


def genIgnoreRightCount(count):
    count = int(count)-1
    code = {}
    if count < 0:
        print "ERR: count < 0"
    for state in range(0, count+1):
        code.update({state: {}})
    for state in range(0,count):
        for symbol in alphabet:
            code[state].update({symbol: (symbol, state+1, R)})
    for symbol in alphabet: 
        code[count].update({symbol: (symbol, -1, R)})
    return count, code

def genIgnoreLeftCount(count):
    print count
    count = int(count)-1
    code = {}
    if count <= 0:
        print "ERR: count < 0"
    for state in range(0, count+1):
        code.update({state: {}})
    for state in range(0,count):
        for symbol in alphabet:
            code[state].update({symbol: (symbol, state+1, L)})
    for symbol in alphabet: 
        code[count].update({symbol: (symbol, -1, L)})
    return count, code


def genWrite(string):
    count = len(string)
    code = {}
    if count == 0:
        print "ERR, no args supplied"
    for state in range(count):
        code.update({state: {}})
    for state in range(count-1):
        for symbol in alphabet:
            code[state].update({symbol: (string[state], state+1, R)})
    for symbol in alphabet:
        code[count-1].update({symbol: (string[count-1], -1, R)})
    return count-1, code


namedInstructionGenerator = {"IRC": genIgnoreRightCount, 
        "ILC": genIgnoreLeftCount,
        "WRT": genWrite,
        "IRU": genIgnoreRightUntil,
        "ILU": genIgnoreLeftUntil,
}
initRegisterA8bit= """IFF(1)
{
IRC(8)
}
ELS
{
A
}
"""

def linearCompile(description):
    instList = []
    program = []
    done = {}
    """God help me"""
    """Parse input"""
    for line in description.split("\n"):
        if line != '':
            instList.append(line)

    for instruction in instList:
        instName = instruction[0:3]
        generator = namedInstructionGenerator[instName]
        args = instruction[4:-1].split(",")
        haltState, code = generator(*args)
        program.append((haltState,code))
        print code

    """ We have to stitch together the halt states to the start states """
    fullProg = {}
    stateCount = 0
    progCount = 0
    stateOffset = 0

    """ Get the number of the halting state, and the bits of code """
    for haltState, code  in program:
        """ First thing we should do is... count states?"""
        for stateNum in code:
            print code
            print stateOffset, stateCount, stateNum
            for symbol in code[stateNum]:
                transition = code[stateNum][symbol]
                """ Link to next instruction in chain """
                if transition[1] == -1:
                    code[stateNum][symbol] = (transition[0], stateOffset+haltState+1, transition[2])
                else: 
                    code[stateNum][symbol] = (transition[0], stateOffset+transition[1], transition[2])

                print code[stateNum][symbol]
            done.update({stateCount:code[stateNum]})
            stateCount+=1


        progCount+=1
        stateOffset += haltState+1
    return stateCount, done

def branchCompile(instList,recurCount):
    program = []
    done = {}
    index = 0
    while index<len(instList):
        instruction = instList[index]
        if recurCount == 0: 
            print instruction
        if instruction == "{":
            branchHalt, code, index =  branchCompile(instList[index+1:],recurCount+1)
            #print str(num) + ": " +"\t"*num+ "}"
        elif instruction == "}":
            return 0, None, index+1
        else:
            pass
            #print str(num) + ": " + "\t"*num + instruction
        index+=1




def checkSemantics(description):
    print description
    numIf = 0
    numElse = 0
    numRightBrace = 0
    numLeftBrace = 0

    instList = []
    program = []
    done = {}
    for line in description.split("\n"):
        if line != '':
            instList.append(line)

    for instruction in instList:
        if instruction.startswith("IFF"):
            numIf+=1
        if instruction.startswith("ELS"):
            numElse+=1
        if instruction == "{":
            numLeftBrace +=1
        if instruction == "}":
            numRightBrace +=1

    if numElse > numIf:
        print "Tscript Error, More ELSE than IF"
        sys.exit(1)
    if numIf > numRightBrace or numIf > numLeftBrace:
        print "Tscript Error, More Braces than IFs"
        sys.exit(1)

    if numRightBrace != numLeftBrace:
        print "Tscript Error, mismatched braces"
        sys.exit(1)

    branchCompile(instList,0)




checkSemantics(initRegisterA8bit)

""" 
...
IFF(1)
{
    ...
}
ELS
{
    ...
}
(done)
...
"""


""" Ignore-count instructions
    
    Basic Idea: Being able to move the tape head any number of directions would be nice.
    However, turing machines don't really have the capability to do so, at least at a very low level.
    As such, we want to maybe be able to move 8 or 9 in any direction.

    ILeftCount(count) = { q_[1-9]: [symbol in alphabet] -> (symbol, countstate-1, Left), 
                          q_0: [symbol in alphabet] -> (symbol, next-state, Left)
"""


""" Ignore-until instructions

    Basic idea:  Ignore Left-until and Ignore Right-until instructions.
    Ignore Left and Ignore Right until instructions are going to simplify
    things quite a bit. There might be some special cases with whitespaces.

    Ignore Right Until X= On any symbol not X, continue Right. On X, Go right one and Write X.

    IRightUntil(untilSymbol)= { q_right: [symbol in alphabet] -> (symbol, repeat-state, Right ), untilSymbol -> (untilSymbol, next-state, Right) }
"""


