from parser import parser
from parser import StackMoveType
from itertools import zip_longest

STATE_WIDTH = 9
POINTER_WIDTH = 2
STACK_WIDTH = 1

def get_ID(state, stack, pointer, word):
    """
    Prints the instantaneous description given the state, stack, position and word.
    Shows the entire stack (stacked vertically) and the configuration ontop of the stack.

    inputs:
    - current state
    - current stack
    - current position in string
    - the string

    outputs:
    - returns a representation of the above information
    """
    # configuration at the top of the stack
    res = "({:{STATE_WIDTH}.{STATE_WIDTH}}, {:{POINTER_WIDTH}.{POINTER_WIDTH}}, {:{STACK_WIDTH}.{STACK_WIDTH}})\n".format(state, str(pointer), stack[-1], \
        STACK_WIDTH = STACK_WIDTH, POINTER_WIDTH = POINTER_WIDTH, STATE_WIDTH = STATE_WIDTH)

    # builds up stack layer by later
    for symbol in reversed(stack):
        res += "_" * (STATE_WIDTH + POINTER_WIDTH + STACK_WIDTH + 6) + "\n"
        res += "|{:^{width}}|\n".format(symbol, width = STATE_WIDTH + POINTER_WIDTH + STACK_WIDTH + 4)
    res += "_" * (STATE_WIDTH + POINTER_WIDTH + STACK_WIDTH + 6) + "\n"
    
    return res

def print_stack_series(ls, write_file):
    """
    Given a series of string representations of stacks in a list, print them horizontally
    , bottom aligned

    inputs:
    - list of strings representations of stacks

    output:
    - prints them horizontally, bottom aligned
    """
    f = open(write_file, "a")
    lines = [reversed(ls[i].splitlines()) for i in range(len(ls))]
    next = zip_longest(*lines, fillvalue = " " * (STATE_WIDTH + POINTER_WIDTH + STACK_WIDTH + 6))
    next = list(next)
    next.reverse()

    for l in next:
        f.write("".join(l))
        f.write("\n")
    
    f.close()

def print_word_position(pointer, word, write_file):
    """
    Given a word and a pointer position, print a diagramatic representation of this

    inputs:
    - word (str)
    - pointer position (int)

    outputs:
    - prints diagramatic representation
    """
    f = open(write_file, "a")

    f.write("          " + ((pointer) * " ") + "|\n")
    f.write("          " + ((pointer) * " ") + "V\n")
    f.write("Position: {}\n".format(word))

    f.close()

def two_dpda_simulator(filename, word, write_file, show = False, debug = False):
    """
    Runs the given word on the given 2DPDA defined in the given file. Returns
    whether or not the the word is accepted (i.e. ends up with a z_0 on stack + in q_f)
    Note that the computation may not halt.

    inputs: 
    - filename where the 2DPDA is defined
    - word which is to be run on 2DPDA
    - write_file will write the output to file aswell
    - show == True will print the stack, state and pointer at each step
    - debug == True will prompt the user for input before progressing to next step

    outputs:
    - boolean depending on whether word is accepted or not
    """
    # adding left and right delimiters
    word = "$" + word + "%"

    # intialise starting state/stack/pointer
    q_0, q_f, z_0, transition = parser(filename)
    current_state = q_0
    stack = [z_0]
    pointer = 1
    visualiser = []
    if show:
        # flush the contents
        f = open(write_file, "w")
        f.close()

        visualiser.append(get_ID(current_state, stack, pointer, word))
        print_stack_series(visualiser, write_file)
        print_word_position(pointer, word, write_file)

        print(stack, end = " ")
        print("({}, {}, {})".format(current_state, pointer, stack[-1]))

    while not (current_state == q_f and len(stack) == 1):
        if len(stack) == 0:
            return False

        current_config = (current_state, word[pointer], stack[-1])
        if debug:
            input()

        # if transition isn't defined for current configuration, reject
        if current_config not in transition:
            return False
        next = transition[current_config]

        # use transition function
        pointer += next[0].value
        current_state = next[2]
        # change stack depending on the move used
        if next[1].type_move is StackMoveType.POP:
            stack.pop()
        elif next[1].type_move is StackMoveType.NOOP:
            pass
        else:
            stack.append(next[1].char)

        if show:
            visualiser.append(get_ID(current_state, stack, pointer, word))
            print_stack_series(visualiser, write_file)
            print_word_position(pointer, word, write_file)

            print(stack, end = " ")
            print("({}, {}, {})".format(current_state, pointer, stack[-1]))


    return True

if __name__ == "__main__":
    res = two_dpda_simulator("pattern_match.txt", "abababababbaabbabbaabab#abbaabbabba", "output.txt", True, False)
    print(res)