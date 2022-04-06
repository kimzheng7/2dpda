from parser import parser
from parser import StackMoveType

def print_ID(state, stack, pointer, word):
    """
    Prints the instantaneous description given the state, stack, position and word

    inputs:
    - current state
    - current stack
    - current position in string
    - the string

    outputs:
    - prints a representation of the above information
    """

    print("State: {}".format(state))
    print("Stack: {}".format(stack))
    print("          " + ((pointer) * " ") + "|")
    print("          " + ((pointer) * " ") + "V")
    print("Position: {}".format(word))
    print()

def two_dpda_simulator(filename, word, show = False, debug = False):
    """
    Runs the given word on the given 2DPDA defined in the given file. Returns
    whether or not the the word is accepted (i.e. ends up with a z_0 on stack + in q_f)
    Note that the computation may not halt.

    inputs: 
    - filename where the 2DPDA is defined
    - word which is to be run on 2DPDA
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
    if show:
        print_ID(current_state, stack, pointer, word)

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
            print_ID(current_state, stack, pointer, word)
    return True

if __name__ == "__main__":
    res = two_dpda_simulator("pattern_match.txt", "aabbaa#bb", True, True)
    print(res)