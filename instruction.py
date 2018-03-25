R = "R"
L = "L"
class NamedInstructionGenerator():
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.instructions = {   "IRC": self.genIgnoreRightCount, 
                                "ILC": self.genIgnoreLeftCount,
                                "WRT": self.genWrite,
                                "IRU": self.genIgnoreRightUntil,
                                "ILU": self.genIgnoreLeftUntil,
                                "IF": self.genBranch,
                                "JMP": self.genUnconditionalJump,

                            }
    def genInstruction(self, name,arg):
        return self.instructions[name](arg[0])

    def genUnconditionalJump(self, arg):
        code = {0:{}, 1:{}}
        for symbol in self.alphabet:
            code[0].update({symbol: (symbol, 1, L)})
            code[1].update({symbol: (symbol, -1, R)})
        return 0, code

    def genBranch(self, condition):
        if condition != '1' and condition != '0':
            print "ERR: invalid conditional: " + str(condition)

        code = {0:{}}
        for symbol in self.alphabet:
            if symbol != condition:
                code[0].update({symbol: (symbol, -1, R)})
            else:
                code[0].update({symbol: (symbol, 1, R)})
        return 0, code

    def genIgnoreLeftUntil(self, char):
        char = char.replace("\"","")
        code = {0:{}}
        count = 0
        for symbol in self.alphabet:
            if symbol != char:
                code[0].update({symbol: (symbol, 0, L)})
        code[0].update({char: (char, 1, R)})
        return count, code

    def genIgnoreRightUntil(self, char):
        char = char.replace("\"","")
        code = {0:{}}
        count = 0
        for symbol in self.alphabet:
            if symbol != char:
                code[0].update({symbol: (symbol, 0, R)})
        code[0].update({char: (char, -1, R)})
        return count, code

    def genIgnoreRightCount(self, count):
        count = int(count)-1
        code = {}
        if count < 0:
            print "ERR: count < 0"
        for state in range(0, count+1):
            code.update({state: {}})
        for state in range(0,count):
            for symbol in self.alphabet:
                code[state].update({symbol: (symbol, state+1, R)})
        for symbol in self.alphabet: 
            code[count].update({symbol: (symbol, -1, R)})
        return count, code

    def genIgnoreLeftCount(self, count):
        count = int(count)-1
        code = {}
        if count <= 0:
            print "ERR: count < 0"
        for state in range(0, count+1):
            code.update({state: {}})
        for state in range(0,count):
            for symbol in self.alphabet:
                code[state].update({symbol: (symbol, state+1, L)})
        for symbol in self.alphabet: 
            code[count].update({symbol: (symbol, -1, L)})
        return count, code

    def genWrite(self, string):
        string = string.replace("\"","")
        count = len(string)
        code = {}
        if count == 0:
            print "ERR, no args supplied"
        for state in range(count):
            code.update({state: {}})
        for state in range(count-1):
            for symbol in self.alphabet:
                code[state].update({symbol: (string[state], state+1, R)})
        for symbol in self.alphabet:
            code[count-1].update({symbol: (string[count-1], -1, R)})
        return count-1, code


