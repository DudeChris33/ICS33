# Submitter: cyrc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    g = {}
    with file as f:
        for x in f.readlines(): g[x[0]].add(x[2]) if x[0] in g.keys() else g.update({x[0]: {x[2]}})
        return g
        

def graph_as_str(graph : {str:{str}}) -> str:
    return "".join([f'  {x} -> {sorted(list(graph[x]))}\n' for x in sorted(graph)])


def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    reached_set, explore_list = set(), [start]
    while len(set(explore_list)) > 0:
        for x in explore_list[:]:
            if trace: print(f'\nreached set    = {str(reached_set)}\nexploring list = {explore_list}')
            if x != '': reached_set.add(x)
            [explore_list.append(y) for y in graph.get(x, '') if y not in reached_set and y not in explore_list]
            explore_list.remove(x)
            if trace: print(f'moving node {x} from the exploring list into the reached set\nafter adding all nodes reachable directly from {x} but not already in reached, exploring = {explore_list}')
    return reached_set


if __name__ == '__main__':
    # Write script here
    graph = read_graph(goody.safe_open(prompt_text = 'Specify the file name representing the graph', mode = 'r', error_message='Not a valid file'))
    print('\nGraph: str (one source node) -> [str] (sorted list of destination nodes)\n' + graph_as_str(graph))
    while True:
        start = input('Specify one start node (or terminate): ')
        if start == "terminate": break
        elif start in graph.keys():
            trace = prompt.for_bool('Specify choice for tracing algorithm[True]')
            print(f'From start node {start}, reachable nodes = {reachable(graph, start, trace)}\n')
        else: print(f"  Entry Error: '{start}';  Illegal: not a source node\n  Please enter a legal String\n")
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
    # driver.default_show_traceback = True
    # driver.default_show_exception = True
    # driver.default_show_exception_message = True
    driver.driver()
