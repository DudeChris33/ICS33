# Submitter: cyrc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import prompt
import goody

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    p_dict = {}
    for line in open_file.readlines():
        line = line.rstrip()
        line = line.split(";")
        if line[0] not in p_dict.keys(): p_dict[line[0]] = [None, [x for x in line[1:]]]
    return p_dict


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    return "".join([f'  {x} -> {d[x]}\n' for x in sorted(d.keys(), key=key, reverse=reverse)])


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    return p1 if order.index(p1) < order.index(p2) else p2


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return set([tuple([x, men[x][0]]) for x in men])    


def make_match(men : {str:[str,[str]]}, women : {str :[str,[str]]}, trace : bool = False) -> {(str,str)}:
    men_copy = men.copy()
    unmatched_men = set([x for x in men.keys()])
    if trace: print("\nWomen Preferences (unchanging)\n" + dict_as_str(women), end='')
    while True:
        if len(unmatched_men) == 0: break
        if trace: print("\nMen Preferences (current)\n" + dict_as_str(men_copy) + "\nunmatched men = " + str(unmatched_men))
        for i in unmatched_men: man_name = i
        unmatched_men.remove(man_name)
        top_pick = men_copy[man_name][1].pop(0)
        if women[top_pick][0] == None:
            men_copy[man_name][0], women[top_pick][0] = top_pick, man_name
            print(f"\n{man_name} proposes to {top_pick}, who is currently unmatched, accepting proposal")
        else:
            if who_prefer(women[top_pick][1], man_name, women[top_pick][0]) == man_name:
                unmatched_men.add(women[top_pick][0])
                men[women[top_pick][0]][0] = None
                men_copy[man_name][0], women[top_pick][0] = top_pick, man_name
                print(f"\n{man_name} proposes to {top_pick}, who is currently matched, accepting the proposal (likes new match better)")
            else:
                unmatched_men.add(man_name)
                print(f"\n{man_name} proposes to {top_pick}, who is currently matched, rejecting the proposal (likes current match better)")
    return extract_matches(men_copy)


if __name__ == '__main__':
    # Write script here
    m_dict = read_match_preferences(goody.safe_open(prompt_text = 'Specify the file name representing the preferences for men', mode = 'r', error_message='Not a valid file'))
    w_dict = read_match_preferences(goody.safe_open(prompt_text = 'Specify the file name representing the preferences for women', mode = 'r', error_message='Not a valid file'))
    print('\nMen Preferences\n' + dict_as_str(m_dict))
    print('Women Preferences\n' + dict_as_str(w_dict))
    trace = prompt.for_bool("Specify choice for tracing algorithm[True]")
    print(f'\nThe final matches: {make_match(m_dict, w_dict, trace)}')
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
    # driver.default_show_traceback = True
    # driver.default_show_exception = True
    # driver.default_show_exception_message = True
    driver.driver()
