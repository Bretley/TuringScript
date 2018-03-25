import sys
""" Save some keystrokes """
R = "R"
L = "L"

class TM:
    """ The assumption is that the starting state is always 0 """
    def __init__(self, tapeInput, program, halts):
        self.tape = []
        for symbol in tapeInput:
            self.tape.append(symbol)
        self.tape.append(" ")
        self.tapePosition = 0
        self.stateNumber = 0
        self.halts = halts
        """ hash { state: hash {symbol : tuple (symbol, state, direction)} } """
        self.program = program
    def moveTapeHead(self, direction):
        if direction == "R":
            self.tapePosition += 1
        elif direction == "L":
            self.tapePosition -=1
            if self.tapePosition < 0:
                self.tape.insert(0, " ")
                self.tapePosition = 0
        else: 
            print "ERROR: Tape movement invalid: " + direction
            sys.exit()

    """ Write the symbol, move the tape head, then move to the next state """
    def transition(self,newState, symbol, direction):
        if self.tapePosition == len(self.tape)-1:
            self.tape.append(" ")
        self.tape[self.tapePosition] = str(symbol)
        self.moveTapeHead(direction)
        self.stateNumber = newState

    """ Read the symbol, then do the thing """
    def run(self):
        while True:
            if self.stateNumber in self.halts:
                print "DONE:"
                print self.stateNumber
                self.printState()
                sys.exit()
            self.printState()
            symbol = self.tape[self.tapePosition]
            newSymbol,newState, direction = self.program[self.stateNumber][symbol]
            self.transition(newState,newSymbol, direction)

    def printState(self):
        print self.stateNumber
        print "".join(self.tape)
        print " "*self.tapePosition + "^"

prog = {0: {'1': ('1', 1, 'R'), '0': ('0', 19, 'R'), 'S': ('S', 19, 'R'), 'B': ('B', 19, 'R'), 'A': ('A', 19, 'R'), ' ': (' ', 19, 'R')}, 1: {'1': ('1', 2, 'R'), '0': ('0', 2, 'R'), 'S': ('S', 2, 'R'), 'B': ('B', 2, 'R'), 'A': ('A', 2, 'R'), ' ': (' ', 2, 'R')}, 2: {'1': ('1', 3, 'R'), '0': ('0', 3, 'R'), 'S': ('S', 3, 'R'), 'B': ('B', 3, 'R'), 'A': ('A', 3, 'R'), ' ': (' ', 3, 'R')}, 3: {'1': ('1', 4, 'R'), '0': ('0', 4, 'R'), 'S': ('S', 4, 'R'), 'B': ('B', 4, 'R'), 'A': ('A', 4, 'R'), ' ': (' ', 4, 'R')}, 4: {'1': ('1', 5, 'R'), '0': ('0', 5, 'R'), 'S': ('S', 5, 'R'), 'B': ('B', 5, 'R'), 'A': ('A', 5, 'R'), ' ': (' ', 5, 'R')}, 5: {'1': ('1', 6, 'R'), '0': ('0', 6, 'R'), 'S': ('S', 6, 'R'), 'B': ('B', 6, 'R'), 'A': ('A', 6, 'R'), ' ': (' ', 6, 'R')}, 6: {'1': ('1', 7, 'R'), '0': ('0', 7, 'R'), 'S': ('S', 7, 'R'), 'B': ('B', 7, 'R'), 'A': ('A', 7, 'R'), ' ': (' ', 7, 'R')}, 7: {'1': ('1', 8, 'R'), '0': ('0', 8, 'R'), 'S': ('S', 8, 'R'), 'B': ('B', 8, 'R'), 'A': ('A', 8, 'R'), ' ': (' ', 8, 'R')}, 8: {'1': ('1', 9, 'R'), '0': ('0', 9, 'R'), 'S': ('S', 9, 'R'), 'B': ('B', 9, 'R'), 'A': ('A', 9, 'R'), ' ': (' ', 9, 'R')}, 9: {'1': ('1', 10, 'R'), '0': ('0', 10, 'R'), 'S': ('S', 10, 'R'), 'B': ('B', 10, 'R'), 'A': ('A', 10, 'R'), ' ': (' ', 10, 'R')}, 10: {'1': ('1', 11, 'R'), '0': ('0', 11, 'R'), 'S': ('S', 11, 'R'), 'B': ('B', 11, 'R'), 'A': ('A', 11, 'R'), ' ': (' ', 11, 'R')}, 11: {'1': ('1', 12, 'R'), '0': ('0', 12, 'R'), 'S': ('S', 12, 'R'), 'B': ('B', 12, 'R'), 'A': ('A', 12, 'R'), ' ': (' ', 12, 'R')}, 12: {'1': ('1', 13, 'R'), '0': ('0', 13, 'R'), 'S': ('S', 13, 'R'), 'B': ('B', 13, 'R'), 'A': ('A', 13, 'R'), ' ': (' ', 13, 'R')}, 13: {'1': ('A', 14, 'R'), '0': ('A', 14, 'R'), 'S': ('A', 14, 'R'), 'B': ('A', 14, 'R'), 'A': ('A', 14, 'R'), ' ': ('A', 14, 'R')}, 14: {'1': ('A', 15, 'R'), '0': ('A', 15, 'R'), 'S': ('A', 15, 'R'), 'B': ('A', 15, 'R'), 'A': ('A', 15, 'R'), ' ': ('A', 15, 'R')}, 15: {'1': ('A', 16, 'R'), '0': ('A', 16, 'R'), 'S': ('A', 16, 'R'), 'B': ('A', 16, 'R'), 'A': ('A', 16, 'R'), ' ': ('A', 16, 'R')}, 16: {'1': ('A', 17, 'R'), '0': ('A', 17, 'R'), 'S': ('A', 17, 'R'), 'B': ('A', 17, 'R'), 'A': ('A', 17, 'R'), ' ': ('A', 17, 'R')}, 17: {'1': ('1', 18, 'L'), '0': ('0', 18, 'L'), 'S': ('S', 18, 'L'), 'B': ('B', 18, 'L'), 'A': ('A', 18, 'L'), ' ': (' ', 18, 'L')}, 18: {'1': ('1', -1, 'R'), '0': ('0', -1, 'R'), 'S': ('S', -1, 'R'), 'B': ('B', -1, 'R'), 'A': ('A', -1, 'R'), ' ': (' ', -1, 'R')}, 19: {'1': ('B', 20, 'R'), '0': ('B', 20, 'R'), 'S': ('B', 20, 'R'), 'B': ('B', 20, 'R'), 'A': ('B', 20, 'R'), ' ': ('B', 20, 'R')}, 20: {'1': ('B', 21, 'R'), '0': ('B', 21, 'R'), 'S': ('B', 21, 'R'), 'B': ('B', 21, 'R'), 'A': ('B', 21, 'R'), ' ': ('B', 21, 'R')}, 21: {'1': ('B', 22, 'R'), '0': ('B', 22, 'R'), 'S': ('B', 22, 'R'), 'B': ('B', 22, 'R'), 'A': ('B', 22, 'R'), ' ': ('B', 22, 'R')}, 22: {'1': ('B', -1, 'R'), '0': ('B', -1, 'R'), 'S': ('B', -1, 'R'), 'B': ('B', -1, 'R'), 'A': ('B', -1, 'R'), ' ': ('B', -1, 'R')}}
tm = TM("1",prog,[-1])
tm.run()
