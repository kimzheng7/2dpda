from re import S
from parser import parser
from parser import StackMoveType
from itertools import zip_longest

STATE_WIDTH = 9
POINTER_WIDTH = 2
STACK_WIDTH = 1

def terminator_table(filename, word, write_file):
    """
    Takes in the 2DPDA specified in filename and the word, and returns
    the terminator table when cook's theorem is run on the intial state

    inputs:
    - filename with 2DPDA defined
    - inputs word

    output:
    - terminator table of configurations (dictionary)
    - a list containing the current symbols in the stack
    """
    f = open(write_file, "w")
    f.close()

    word = "$" + word + "%"
    q_0, q_f, z_0, transition = parser(filename)
    table = {}
    stack = [z_0]
    visualiser = []
    initial_config = (q_0, 1, z_0)
    terminator(initial_config, table, word, transition, stack, visualiser, write_file)

    return table, stack

def config_step(config, transition, word):
    """
    Given a configuration and a transition function, find the step from the current
    configuration under the transition function
    """
    state, index, stack = config
    curr = (state, word[index], stack)
    
    if curr in transition:
        return transition[curr]
    else:
        return None

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

def terminator(config, table, word, transition, stack, visualiser, write_file):
    """
    Runs cook's theorem to find the terminator of the current configuration, 
    filling in the table given (which will be a dictionary). This is done on the
    input word.
    """
    visualiser.append(get_ID(config[0], stack, config[1], word))
    print_stack_series(visualiser, write_file)
    print_word_position(config[1], word, write_file)

    print(stack, end = " ")
    print(config)

    if config in table:
        if table[config] == True:
            table[config] = None
            return None
        else:
            visualiser.append("->")
            visualiser.append(get_ID(table[config][0], stack, table[config][1], word))
            print_stack_series(visualiser, write_file)
            print_word_position(table[config][1], word, write_file)

            print("|\nV")
            print(stack, end = " ")
            print(table[config])


            return table[config]

    # mark the entry in table, to show its been seen
    table[config] = True
    
    # find what the transition function does on configuration
    step = config_step(config, transition, word)

    # case 0: no transitions defined outgoing, hence is terminator
    if step is None:
        table[config] = config
        return config

    mov, stack_move, new_state = step

    # case 1: config is no-op
    if stack_move.type_move == StackMoveType.NOOP:
        next_config = (new_state, config[1] + mov.value, config[2])
        res = terminator(next_config, table, word, transition, stack, visualiser, write_file)

    # case 2: config is push
    elif stack_move.type_move == StackMoveType.PUSH:
        # step up and get terminator
        upper_config = (new_state, config[1] + mov.value, step[1].char)

        stack.append(step[1].char)
        intermediate = terminator(upper_config, table, word, transition, stack, visualiser, write_file)

        if intermediate is None:
            table[config] = None
            return None
        else:
            # step down and get terminator
            step = config_step(intermediate, transition, word)
            if step is None:
                table[config] = None
                return None
            mov, stack_move, new_state = step

            stack.pop()
            lower_config = (new_state, intermediate[1] + mov.value, config[2])
            res = terminator(lower_config, table, word, transition, stack, visualiser, write_file)

    # case 3: config is pop
    elif stack_move.type_move == StackMoveType.POP:
        res = config

    table[config] = res
    return res


if __name__ == "__main__":
    table, stack = terminator_table("pattern_match.txt", "abababababbaabbabbaabab#abbaabbabba", "cook_output.txt")
