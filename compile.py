import sys
from parse import Branch, Instruction, Body, parse, pretty_print, pretty_print2
from instruction import NamedInstructionGenerator
from lex import lex

"""
Author: Bret A. Barkley

This is where the compiler lives. The compiler takes an array of Instruction or Branch Classes.
On the Instruction class, it will add to a
On a Branch, it compiles the True body and if there is one, the false body.
"""
L = "L"
R = "R"
alphabet = ["0","1"," ","A","B", "S"] # Just binary for now

def linearCompile(body,stateOffset):
    done = {}
    program = []
    programLen = 0
    stateCount = 0
    instructionGen = NamedInstructionGenerator(alphabet)

    for instruction in body.instructions:
        if isinstance(instruction, Instruction):
            haltState, code = instructionGen.genInstruction(instruction.name,instruction.argument.split(","))
            program.append((haltState,code))
            programLen += 1
    print program

    for index, tupleItem in enumerate(program):
        haltState, code = tupleItem
        for state in code:
            for symbol in alphabet:
                transition =  code[state][symbol]
                #if transition[1] == -1 and index < programLen-1:
                if index < programLen:
                    if transition[1] == -1 and state == haltState:
                        if index != programLen-1:
                            code[state][symbol] = (transition[0], stateOffset+haltState+1, transition[2])
                    else:
                        code[state][symbol] = (transition[0], transition[1] + stateOffset , transition[2])
                stateCount += +1

        for state in code:
            done.update({state+stateOffset: code[state]})
        stateOffset += haltState+1
    for state in done:
        print state, done[state]
    return stateOffset, done

def recursiveCompile(parseItem,depth,totalOffset):
    if isinstance(parseItem, Body):
        if parseItem.isTerminal() and len(parseItem.instructions) > 0:
            parseItem.haltState, parseItem.code = linearCompile(parseItem,totalOffset)
            totalOffset = parseItem.haltState
            return totalOffset
        else:
            for item in parseItem.instructions:
                
                totalOffset =  recursiveCompile(item, depth+1,totalOffset)
            return totalOffset
    elif isinstance(parseItem, Branch):
        branchCode = Body([Instruction("IF",parseItem.condition)], True)
        stateOffset, parseItem.branchCode = linearCompile(branchCode ,totalOffset)
        totalOffset = recursiveCompile(parseItem.trueBody, depth+1, totalOffset+1)
        if parseItem.falseBody is not None:
            jmpCode = Body([Instruction("JMP", parseItem.condition)], True)
            stateOffset, parseItem.escapeTrue = linearCompile(jmpCode, totalOffset)
            totalOffset = recursiveCompile(parseItem.falseBody, depth+1,totalOffset+2)
        return totalOffset
    return totalOffset

def link(parsedItem,totalOffset):
    program = {}
    recursiveLink(parsedItem, 0, 0, totalOffset, program)
    return program


def recursiveLink(item, depth, currentOffset, totalOffset,program):
    if isinstance(item, Body):
        if item.isTerminal() and item.code is not None:
            for state in item.code:
                for symbol in item.code[state]:
                    transition = item.code[state][symbol]
                    if transition[1] == -1 and state != totalOffset-1:
                        item.code[state][symbol] = (transition[0],state+1,transition[2])
                    program.update({state: item.code[state]})
                currentOffset += 1
        else:
            for item in item.instructions:
                currentOffset = recursiveLink(item, depth+1,currentOffset, totalOffset, program)
        return currentOffset

    elif isinstance(item, Branch):
        falsejmp = currentOffset + item.trueBody.getNumStates() + 3
        for symbol in item.branchCode[currentOffset]:
            transition = item.branchCode[currentOffset][symbol]
            if transition[1] == -1:
                item.branchCode[currentOffset][symbol] = (transition[0], falsejmp, transition[2])
        program.update(item.branchCode)
        recursiveLink(item.trueBody, depth+1, currentOffset+1,totalOffset, program)
        if item.falseBody is not None:
            print "TRUEJMP"
            trueFinalState = max(item.escapeTrue.keys())
            truejmp =  trueFinalState + item.falseBody.getNumStates() + 1
            for symbol in item.escapeTrue[trueFinalState]:
                transition = item.escapeTrue[trueFinalState][symbol]
                if truejmp < totalOffset: 
                    item.escapeTrue[trueFinalState][symbol] = (transition[0],truejmp, transition[2] )
                else:
                    item.escapeTrue[trueFinalState][symbol] = (transition[0],-1, transition[2] )
            program.update(item.escapeTrue)


            print "TRUJMP"
            print trueFinalState
            print truejmp
            currentOffest = recursiveLink(item.falseBody, depth+1, currentOffset+1,totalOffset, program)
            # for symbol in program[trueFinalState]:
                # transition = program[trueFinalState][symbol]
                # print transition

        for state in program:
            print state, program[state]
    return currentOffset


def compile(parseItem):
    parseItem.simplify()
    totalOffset = recursiveCompile(parseItem, 0,0)
    print totalOffset
    return link(parseItem,totalOffset)



code = """
IRC(5)
if (1) {
    if (1) {
    WRT("ABCD")
    }
}
else {
IRC(1)
WRT("ABCD")
}

"""


lexed = lex(code)
parsed,useless = parse(lexed, 0)
""" This is a hack, we need to not use it"""
parsed.simplify()
#print "===========================parsed========================"
#pretty_print(parsed,0)
program = compile(parsed)
print "===========================compiled====================="
print parsed.getNumStates()

print "===========================pretty2====================="
pretty_print2(parsed,0)
for state in program:
    print state, program[state]



