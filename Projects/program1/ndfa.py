# Submitter: cyrc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming


import goody


def read_ndfa(file : open) -> {str:{str:{str}}}:
    r_dict = {}
    for line in file.readlines():
        line = line.rstrip().split(';')
        function = line.pop(0)
        r_dict[function], keys, values = {}, line[::2], line[1::2]
        assert len(keys) == len(values)
        for index in range(len(keys)):
            if keys[index] not in r_dict[function].keys(): r_dict[function][keys[index]] = set()
            r_dict[function][keys[index]].add(values[index])
    return dict(sorted(r_dict.items()))


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    return "".join([f'  {x} transitions: {[(y, sorted(z)) for (y, z) in sorted(ndfa[x].items())]}\n' for x in sorted(ndfa)])

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    r_list, current_states, next_states = [state], {state}, set()
    for i in inputs:
        for current_state in current_states:
            if i in ndfa[current_state].keys(): next_states.update(set([j for j in ndfa[current_state][i]]))
        else:
            r_list.append((i, next_states))
            if len(next_states) == 0: break
            current_states = next_states
            next_states = set()
            continue
        break
    return r_list


def interpret(result : [None]) -> str:
    return f"Start state = {result.pop(0)}\n" + "".join([f'  Input = {x[0]}; new possible states = {sorted(list(x[1]))}\n' for x in result if x[1] != None]) + f"Stop state(s) = {sorted(list(result[-1][1]))}\n"




if __name__ == '__main__':
    # Write script here
    ndfa = read_ndfa(goody.safe_open('Specify the file name representing the Non-Deterministic Finite Automaton', "r", "Invalid file"))
    print(f"\nSpecified details of this Non-Deterministic Finite Automaton\n{ndfa_as_str(ndfa)}")
    fa_inputs = goody.safe_open('Specify the file name representing multiple start-states and their inputs', "r", "Invalid file").readlines()
    for i in range(len(fa_inputs)): fa_inputs[i] = fa_inputs[i].rstrip().split(";")
    for j in fa_inputs: print(f"Computed NDFA trace from its start-state\n{interpret(process(ndfa, j.pop(0), j))}")
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
    # driver.default_show_traceback = True
    # driver.default_show_exception = True
    # driver.default_show_exception_message = True
    driver.driver()
