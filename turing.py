import sys
from lex import lex
from parse import parser
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


prog = {0: {'1': ('1', 1, 'L'), '0': ('0', 1, 'L'), 'S': ('S', 1, 'L'), 'B': ('B', 1, 'L'), 'A': ('A', 1, 'L'), ' ': (' ', 1, 'L')}, 1: {'1': ('1', 2, 'L'), '0': ('0', 2, 'L'), 'S': ('S', 2, 'L'), 'B': ('B', 2, 'L'), 'A': ('A', 2, 'L'), ' ': (' ', 2, 'L')}, 2: {'1': ('1', 3, 'L'), '0': ('0', 3, 'L'), 'S': ('S', 3, 'L'), 'B': ('B', 3, 'L'), 'A': ('A', 3, 'L'), ' ': (' ', 3, 'L')}, 3: {'1': ('1', 4, 'L'), '0': ('0', 4, 'L'), 'S': ('S', 4, 'L'), 'B': ('B', 4, 'L'), 'A': ('A', 4, 'L'), ' ': (' ', 4, 'L')}, 4: {'1': ('1', 5, 'L'), '0': ('0', 5, 'L'), 'S': ('S', 5, 'L'), 'B': ('B', 5, 'L'), 'A': ('A', 5, 'L'), ' ': (' ', 5, 'L')}, 5: {'1': ('1', 6, 'L'), '0': ('0', 6, 'L'), 'S': ('S', 6, 'L'), 'B': ('B', 6, 'L'), 'A': ('A', 6, 'L'), ' ': (' ', 6, 'L')}, 6: {'1': ('1', 7, 'L'), '0': ('0', 7, 'L'), 'S': ('S', 7, 'L'), 'B': ('B', 7, 'L'), 'A': ('A', 7, 'L'), ' ': (' ', 7, 'L')}, 7: {'1': ('1', 8, 'L'), '0': ('0', 8, 'L'), 'S': ('S', 8, 'L'), 'B': ('B', 8, 'L'), 'A': ('A', 8, 'L'), ' ': (' ', 8, 'L')}, 8: {'1': ('1', 9, 'L'), '0': ('0', 9, 'L'), 'S': ('S', 9, 'L'), 'B': ('B', 9, 'L'), 'A': ('A', 9, 'L'), ' ': (' ', 9, 'L')}, 9: {'1': ('1', 10, 'L'), '0': ('0', 10, 'L'), 'S': ('S', 10, 'L'), 'B': ('B', 10, 'L'), 'A': ('A', 10, 'L'), ' ': (' ', 10, 'L')}, 10: {'1': ('1', 11, 'L'), '0': ('0', 11, 'L'), 'S': ('S', 11, 'L'), 'B': ('B', 11, 'L'), 'A': ('A', 11, 'L'), ' ': (' ', 11, 'L')}, 11: {'1': ('1', 12, 'L'), '0': ('0', 12, 'L'), 'S': ('S', 12, 'L'), 'B': ('B', 12, 'L'), 'A': ('A', 12, 'L'), ' ': (' ', 12, 'L')}, 12: {'1': ('1', 13, 'L'), '0': ('0', 13, 'L'), 'S': ('S', 13, 'L'), 'B': ('B', 13, 'L'), 'A': ('A', 13, 'L'), ' ': (' ', 13, 'L')}, 13: {'1': ('1', 14, 'L'), '0': ('0', 14, 'L'), 'S': ('S', 14, 'L'), 'B': ('B', 14, 'L'), 'A': ('A', 14, 'L'), ' ': (' ', 14, 'L')}, 14: {'1': ('1', 15, 'L'), '0': ('0', 15, 'L'), 'S': ('S', 15, 'L'), 'B': ('B', 15, 'L'), 'A': ('A', 15, 'L'), ' ': (' ', 15, 'L')}, 15: {'1': ('1', 16, 'L'), '0': ('0', 16, 'L'), 'S': ('S', 16, 'L'), 'B': ('B', 16, 'L'), 'A': ('A', 16, 'L'), ' ': (' ', 16, 'L')}, 16: {'1': ('1', 17, 'L'), '0': ('0', 17, 'L'), 'S': ('S', 17, 'L'), 'B': ('B', 17, 'L'), 'A': ('A', 17, 'L'), ' ': (' ', 17, 'L')}, 17: {'1': ('1', 18, 'L'), '0': ('0', 18, 'L'), 'S': ('S', 18, 'L'), 'B': ('B', 18, 'L'), 'A': ('A', 18, 'L'), ' ': (' ', 18, 'L')}, 18: {'1': ('A', 19, 'R'), '0': ('A', 19, 'R'), 'S': ('A', 19, 'R'), 'B': ('A', 19, 'R'), 'A': ('A', 19, 'R'), ' ': ('A', 19, 'R')}, 19: {'1': ('0', 20, 'R'), '0': ('0', 20, 'R'), 'S': ('0', 20, 'R'), 'B': ('0', 20, 'R'), 'A': ('0', 20, 'R'), ' ': ('0', 20, 'R')}, 20: {'1': ('0', 21, 'R'), '0': ('0', 21, 'R'), 'S': ('0', 21, 'R'), 'B': ('0', 21, 'R'), 'A': ('0', 21, 'R'), ' ': ('0', 21, 'R')}, 21: {'1': ('0', 22, 'R'), '0': ('0', 22, 'R'), 'S': ('0', 22, 'R'), 'B': ('0', 22, 'R'), 'A': ('0', 22, 'R'), ' ': ('0', 22, 'R')}, 22: {'1': ('0', 23, 'R'), '0': ('0', 23, 'R'), 'S': ('0', 23, 'R'), 'B': ('0', 23, 'R'), 'A': ('0', 23, 'R'), ' ': ('0', 23, 'R')}, 23: {'1': ('0', 24, 'R'), '0': ('0', 24, 'R'), 'S': ('0', 24, 'R'), 'B': ('0', 24, 'R'), 'A': ('0', 24, 'R'), ' ': ('0', 24, 'R')}, 24: {'1': ('0', 25, 'R'), '0': ('0', 25, 'R'), 'S': ('0', 25, 'R'), 'B': ('0', 25, 'R'), 'A': ('0', 25, 'R'), ' ': ('0', 25, 'R')}, 25: {'1': ('0', 26, 'R'), '0': ('0', 26, 'R'), 'S': ('0', 26, 'R'), 'B': ('0', 26, 'R'), 'A': ('0', 26, 'R'), ' ': ('0', 26, 'R')}, 26: {'1': ('0', 27, 'R'), '0': ('0', 27, 'R'), 'S': ('0', 27, 'R'), 'B': ('0', 27, 'R'), 'A': ('0', 27, 'R'), ' ': ('0', 27, 'R')}, 27: {'1': ('B', 28, 'R'), '0': ('B', 28, 'R'), 'S': ('B', 28, 'R'), 'B': ('B', 28, 'R'), 'A': ('B', 28, 'R'), ' ': ('B', 28, 'R')}, 28: {'1': ('0', 29, 'R'), '0': ('0', 29, 'R'), 'S': ('0', 29, 'R'), 'B': ('0', 29, 'R'), 'A': ('0', 29, 'R'), ' ': ('0', 29, 'R')}, 29: {'1': ('0', 30, 'R'), '0': ('0', 30, 'R'), 'S': ('0', 30, 'R'), 'B': ('0', 30, 'R'), 'A': ('0', 30, 'R'), ' ': ('0', 30, 'R')}, 30: {'1': ('0', 31, 'R'), '0': ('0', 31, 'R'), 'S': ('0', 31, 'R'), 'B': ('0', 31, 'R'), 'A': ('0', 31, 'R'), ' ': ('0', 31, 'R')}, 31: {'1': ('0', 32, 'R'), '0': ('0', 32, 'R'), 'S': ('0', 32, 'R'), 'B': ('0', 32, 'R'), 'A': ('0', 32, 'R'), ' ': ('0', 32, 'R')}, 32: {'1': ('0', 33, 'R'), '0': ('0', 33, 'R'), 'S': ('0', 33, 'R'), 'B': ('0', 33, 'R'), 'A': ('0', 33, 'R'), ' ': ('0', 33, 'R')}, 33: {'1': ('0', 34, 'R'), '0': ('0', 34, 'R'), 'S': ('0', 34, 'R'), 'B': ('0', 34, 'R'), 'A': ('0', 34, 'R'), ' ': ('0', 34, 'R')}, 34: {'1': ('0', 35, 'R'), '0': ('0', 35, 'R'), 'S': ('0', 35, 'R'), 'B': ('0', 35, 'R'), 'A': ('0', 35, 'R'), ' ': ('0', 35, 'R')}, 35: {'1': ('0', 36, 'R'), '0': ('0', 36, 'R'), 'S': ('0', 36, 'R'), 'B': ('0', 36, 'R'), 'A': ('0', 36, 'R'), ' ': ('0', 36, 'R')}, 36: {'1': ('1', 37, 'R'), '0': ('0', 37, 'R'), 'S': ('S', 37, 'R'), 'B': ('B', 37, 'R'), 'A': ('A', 37, 'R'), ' ': (' ', 37, 'R')}, 37: {'1': ('1', 38, 'R'), '0': ('0', 38, 'R'), 'S': ('S', 38, 'R'), 'B': ('B', 38, 'R'), 'A': ('A', 38, 'R'), ' ': (' ', 38, 'R')}, 38: {'1': ('1', 39, 'R'), '0': ('0', 39, 'R'), 'S': ('S', 39, 'R'), 'B': ('B', 39, 'R'), 'A': ('A', 39, 'R'), ' ': (' ', 39, 'R')}, 39: {'1': ('1', 40, 'R'), '0': ('0', 40, 'R'), 'S': ('S', 40, 'R'), 'B': ('B', 40, 'R'), 'A': ('A', 40, 'R'), ' ': (' ', 40, 'R')}, 40: {'1': ('1', 41, 'R'), '0': ('0', 41, 'R'), 'S': ('S', 41, 'R'), 'B': ('B', 41, 'R'), 'A': ('A', 41, 'R'), ' ': (' ', 41, 'R')}, 41: {'1': ('A', 42, 'R'), '0': ('A', 42, 'R'), 'S': ('A', 42, 'R'), 'B': ('A', 42, 'R'), 'A': ('A', 42, 'R'), ' ': ('A', 42, 'R')}, 42: {'1': ('B', 43, 'R'), '0': ('B', 43, 'R'), 'S': ('B', 43, 'R'), 'B': ('B', 43, 'R'), 'A': ('B', 43, 'R'), ' ': ('B', 43, 'R')}, 43: {'1': ('A', 44, 'R'), '0': ('A', 44, 'R'), 'S': ('A', 44, 'R'), 'B': ('A', 44, 'R'), 'A': ('A', 44, 'R'), ' ': ('A', 44, 'R')}, 44: {'1': ('B', 45, 'R'), '0': ('B', 45, 'R'), 'S': ('B', 45, 'R'), 'B': ('B', 45, 'R'), 'A': ('B', 45, 'R'), ' ': ('B', 45, 'R')}}
tm = TM("S",prog,[-1])
tm.run()