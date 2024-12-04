# Submitter: cyrc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programmingfrom collections import defaultdict

from collections import defaultdict
from goody import type_as_str

class Bag:
    def __init__(self, contents=[]):
        self.bag = defaultdict(int)
        for i in contents: self.bag[i] += 1
    
    def __repr__(self):
        return f'Bag({sum([[i for _j in range(j)] for i, j in self.bag.items()], [])})'
        
    def __str__(self):
        return "Bag(" + "".join([f'{i}[{j}]' for i, j in self.bag.items()]) + ")"
    
    def __len__(self):
        return sum([x for x in self.bag.values()])
    
    def unique(self):
        return len(self.bag.keys())
    
    def __contains__(self, arg):
        return arg in self.bag.keys()
    
    def count(self, arg):
        return self.bag[arg] if arg in self.bag.keys() else 0
    
    def add(self, arg):
        self.bag[arg] += 1

    def __add__(self, bag2):
        if type(bag2) != type(self): raise TypeError
        r_bag = []
        for bag1 in sum([[i for _count in range(j)] for i, j in self.bag.items()], []): r_bag.append(bag1)
        for bag3 in sum([[i for _count in range(j)] for i, j in bag2.bag.items()], []): r_bag.append(bag3)
        return Bag(r_bag)
    
    def remove(self, arg):
        if arg in self.bag.keys(): self.bag[arg] -= 1
        else: raise ValueError
        if self.bag[arg] == 0: del self.bag[arg]
    
    def __eq__(self, bag2):
        if type(bag2) == type(self):
            for i in self.bag.keys():
                if i not in bag2.bag.keys() or self.bag[i] != bag2.bag[i]: return False
            return True
        else: return False
    
    def __iter__(self):
        return iter(sum([[i for _count in range(j)] for i, j in self.bag.items()], []))




if __name__ == '__main__':
    #driver tests
    import driver
    driver.default_file_name = 'bsc21S22.txt'
    # driver.default_show_exception= True
    # driver.default_show_exception_message= True
    # driver.default_show_traceback= True
    driver.driver()
