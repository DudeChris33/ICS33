# Submitter: cyrc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming


import goody


def read_fa(file : open) -> {str:{str:str}}:
    r_dict = {}
    for line in file.readlines():
        line = line.rstrip().split(';')
        r_dict.setdefault(line.pop(0), dict(zip(line[::2], line[1::2])))
    return dict(sorted(r_dict.items()))


def fa_as_str(fa : {str:{str:str}}) -> str:
    return "".join([f'  {x} transitions: {[(y, z) for (y, z) in sorted(fa[x].items())]}\n' for x in sorted(fa)])


def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    r_list = [state]
    for i in inputs:
        if state in fa.keys() and i in fa[state].keys():
            state = fa[state][i]
            r_list.append((i, state))
        else:
            r_list.append((i, None))
            break
    return r_list


def interpret(fa_result : [None]) -> str:
    r_str = f"Start state = {fa_result.pop(0)}\n"
    r_str += "".join([f'  Input = {x[0]}; new state = {x[1]}\n' for x in fa_result if x[1] != None])
    if fa_result[-1][1] == None: r_str += f"  Input = {fa_result[-1][0]}; illegal input: simulation terminated\n"
    r_str += f"Stop state = {fa_result[-1][1]}\n"
    return r_str


if __name__ == '__main__':
    # Write script here
    fa = read_fa(goody.safe_open('Specify the file name representing the Finite Automaton', "r", "Invalid file"))
    print(f"\nSpecified details of this Finite Automaton\n{fa_as_str(fa)}")
    fa_inputs = goody.safe_open('Specify the file name representing multiple start-states and their inputs', "r", "Invalid file").readlines()
    for i in range(len(fa_inputs)): fa_inputs[i] = fa_inputs[i].rstrip().split(";")
    for j in fa_inputs: print(f"Computed FA trace from its start-state\n{interpret(process(fa, j.pop(0), j))}")
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
    # driver.default_show_traceback = True
    # driver.default_show_exception = True
    # driver.default_show_exception_message = True    
    driver.driver()
