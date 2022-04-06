from enum import Enum

class Move(Enum):
    LEFT = -1
    STAY = 0
    RIGHT = 1

class StackMoveType(Enum):
    POP = -1
    NOOP = 0
    PUSH = 1

class StackMove:
    def __init__(self, type_move, char = None):
        self.type_move = type_move
        self.char = char

def parser(filename):
    """Parses the 2DPDA in the given filename
    Each line in the file is either:
    - the first line, which is the alphabet of letters on the input tape (each separated by ", ")-
    includes $ and % the left and right delimiters of the input string
    - the second line, which is the alphabet of stack symbols (each separated by ", ")- 
    includes Z_0 the bottom stack symbol
    - the 3rd line, which is the initial state
    - the 4th line, which is the final state
    - the 5th line, which is the symbol at the bottom of the stack
    - a comment which starts with ; (to be ignored)
    - An empty line (to be ignored)
    - Otherwise, it is of the form:
        - q_start, a, alpha, move, stack, q_next
        - where a is an alphabet symbol, alpha is a stack symbol
          move is in {-1, 0, 1}, stack is in {pop, push-"letter", noop}
    which describes a transition from q_start to q_next after reading a from the
    tape and alpha from the stack. It does the move and stack operation too.
    - The following shortcuts can be used:
        - "!" can be used in place of a to signify that the transition occurs for
        all letters
        - "!" can be used in place of alpha to signify that the transition occurs for
        all stack symbols
        - these shortcuts should be written first for a given state, since any subsequent rules
        with the same state will overwrite the ones defined using the above shortcuts


    input: filename where the 2DPDA is defined
    returns: a triple which contains
    - the initial state name
    - the final state name
    - the bottom stack symbol
    - the transition function: a dictionary where keys are tuples (q, a, alpha) and values are (move, stackmove, qnext)
    """
    delta = {}
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    for i, line in enumerate(lines):
        line = line.strip()

        # handling first 5 lines
        if i == 0:
            alphabet = line.split(", ")
            continue
        if i == 1:
            stack_alphabet = line.split(", ")
            continue
        if i == 2:
            q_0 = line
            continue
        if i == 3:
            q_f = line
            continue
        if i == 4:
            z_0 = line
            continue

        # comment lines are ignored
        if line == "" or line[0] == ";":
            continue

        elems = line.split()
        # assigning move with corresponding enum value
        if elems[3] == "-1":
            move = Move.LEFT
        elif elems[3] == "0":
            move = Move.STAY
        else:
            move = Move.RIGHT

        # assigning stackmove with corresponding enum value
        if elems[4] == "pop":
            stack_move = StackMove(StackMoveType.POP)
        elif "push" in elems[4]:
            # need to store the character which comes with it
            stack_move = StackMove(StackMoveType.PUSH, elems[4][-1])
        else:
            stack_move = StackMove(StackMoveType.NOOP)

        # adding entries into transition function 
        value = (move, stack_move, elems[5])
        # deals with shortcut
        if elems[1] == "!" and elems[2] == "!":
            for a in alphabet:
                for alpha in stack_alphabet:
                    delta[(elems[0], a, alpha)] = value
        elif elems[1] == "!":
            for a in alphabet:
                delta[(elems[0], a, elems[2])] = value
        elif elems[2] == "!": 
            for alpha in stack_alphabet:
                delta[(elems[0], elems[1], alpha)] = value
        else:
            # deals with normal case
            key = (elems[0], elems[1], elems[2])
            delta[key] = value
    
    return (q_0, q_f, z_0, delta)
