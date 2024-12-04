# Submitter: cyrc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import goody
from goody import irange
import prompt
from random import choice


# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    r_dict, text = {}, list(word_at_a_time(file))
    for i in range(len(text) - (os)):
        key_tuple = tuple([text[i+x] for x in range(os)])
        r_dict.setdefault(key_tuple, list())
        if text[i+os] not in r_dict[key_tuple]: r_dict[key_tuple].append(text[i+os])
    return dict(sorted(r_dict.items()))


def corpus_as_str(corpus : {(str):[str]}) -> str:
    return "".join(f'  {x} can be followed by any of {[y for y in corpus[x]]}\n' for x in dict(sorted(corpus.items()))) + f'min/max list lengths = {(min(len(x) for x in corpus.values()))}/{(max(len(x) for x in corpus.values()))}\n'


def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    r_list, key = start.copy(), start.copy()
    for i in range(count):
        next_str = choice(corpus[tuple(key)])
        key, r_list = key[1:] + [next_str], r_list + [next_str]
        if tuple(key) not in corpus.keys(): return r_list + [None]
    return r_list



if __name__ == '__main__':
    # Write script here
    os = prompt.for_int("Specify the order statistic")
    corpus = read_corpus(os, goody.safe_open("Specify the file name representing the text to process", "r", "Invalid file"))
    print(f'Corpus\n{corpus_as_str(corpus)}\n\nSpecify {os} words starting the list')
    print(f'Random text = {produce_text(corpus, [prompt.for_string(f"Specify word {x+1}") for x in range(os)], prompt.for_int("Specify # of words to append at the end of the started list"))}')
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
    # driver.default_show_traceback = True
    # driver.default_show_exception = True
    # driver.default_show_exception_message = True
    driver.driver()
