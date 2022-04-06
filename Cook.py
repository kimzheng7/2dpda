from re import S
from parser import parser
from parser import StackMoveType

def terminator_table(filename, word):
    """
    Takes in the 2DPDA specified in filename and the word, and returns
    the terminator table when cook's theorem is run on the intial state

    inputs:
    - filename with 2DPDA defined
    - inputs word

    output:
    - terminator table of configurations (dictionary)
    """

    word = "$" + word + "%"

    q_0, q_f, z_0, transition = parser(filename)
    table = {}
    initial_config = (q_0, 1, z_0)
    terminator(initial_config, table, word, transition)

    return table

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

def terminator(config, table, word, transition):
    """
    Runs cook's theorem to find the terminator of the current configuration, 
    filling in the table given (which will be a dictionary). This is done on the
    input word.
    """
    print(table)
    if config in table:
        if table[config] == True:
            table[config] = None
            return None
        else:
            return table[config]

    # mark the entry in table, to show its been seen
    table[config] = True
    
    # find what the transition function does on configuration
    step = config_step(config, transition, word)
    # no transitions defined outgoing
    if step is None:
        table[config] = None
        return None

    mov, stack_move, new_state = step

    # case 1: config is no-op
    if stack_move.type_move == StackMoveType.NOOP:
        next_config = (new_state, config[1] + mov.value, config[2])
        res = terminator(next_config, table, word, transition)

    # case 2: config is push
    elif stack_move.type_move == StackMoveType.PUSH:
        # step up and get terminator
        upper_config = (new_state, config[1] + mov.value, step[1].char)
        intermediate = terminator(upper_config, table, word, transition)
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
            lower_config = (new_state, intermediate[1] + mov.value, config[2])
            res = terminator(lower_config, table, word, transition)

    # case 3: config is pop
    elif stack_move.type_move == StackMoveType.POP:
        res = config

    table[config] = res
    return res


if __name__ == "__main__":
    table = terminator_table("pattern_match.txt", "aabbaa#bb")
    print(table)