# Submitter: cyrc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programmingfrom goody import type_as_str  # Useful for some exceptions

from copy import deepcopy

class DictList:
    def __init__(self, *args):
        assert len(args) > 0 and all(type(arg) == dict for arg in args) and all(len(arg) > 0 for arg in args), "Cannot initialize: invalid input"
        self.dl = list(args)
    
    
    def __len__(self):
        return len(set(sum([[x for x in y.keys()] for y in self.dl], [])))
    
    
    def __bool__(self):
        return False if len(self.dl) == 1 else True
    
    
    def __repr__(self):
        return f'DictList({", ".join(str(x) for x in self.dl)})'
    
    
    def __contains__(self, key):
        return True if key in sum([list(x.keys()) for x in self.dl], []) else False
    
    
    def __getitem__(self, key):
        if key not in set(sum([[x for x in y.keys()] for y in self.dl], [])): raise KeyError("Cannot get: invalid input")
        for x in self.dl:
            for y in x.keys():
                if y == key: z = x[y]
        return z


    def __setitem__(self, key, value):
        if key not in set(sum([[x for x in y.keys()] for y in self.dl], [])): self.dl.append({key: value})
        else:
            for x in self.dl:
                for y in x.keys():
                    if y == key: z = self.dl.index(x)
            self.dl[z][key] = value
    
    
    def __delitem__(self, key):
        if key not in set(sum([[x for x in y.keys()] for y in self.dl], [])): raise KeyError("Cannot delete: invalid input")
        else:
            for x in self.dl:
                for y in x.keys():
                    if y == key: z = self.dl.index(x)
            del self.dl[z][key]
            if len(self.dl[z]) == 0: self.dl.pop(z)
    
    
    def __call__(self, key):
        r_list = []
        if key in set(sum([[x for x in y.keys()] for y in self.dl], [])):
            for x in self.dl:
                for y in x.keys():
                    if y == key: r_list.append((self.dl.index(x), x[y]))
        return r_list
    
    
    def __iter__(self):
        r_list = []
        for x in range(len(self.dl)-1, -1, -1):
            for y in sorted(list(self.dl[x].keys())):
                if y not in r_list: r_list.append(y)
        return iter(r_list)


    def items(self):
        r_list, added = [], []
        for x in range(len(self.dl)-1, -1, -1):
            for y in sorted(list(self.dl[x].keys())):
                if y not in added:
                    r_list.append((y, self.dl[x][y]))
                    added.append(y)
        return iter(r_list)
    
    
    def collapse(self):
        r_dict, added = {}, []
        for x in range(len(self.dl)-1, -1, -1):
            for y in sorted(list(self.dl[x].keys())):
                if y not in added:
                    r_dict.setdefault(y, self.dl[x][y])
                    added.append(y)
        return dict(sorted(r_dict.items()))

    
    def __eq__(self, dict2):
        if type(dict2) in (type(self), dict):
            i = sorted(list(set(sum([[x for x in y.keys()] for y in self.dl], []))))
            j = sorted(list(set(sum([[x for x in y.keys()] for y in dict2.dl], [])))) if type(dict2) == type(self) else sorted(dict2.keys())
            if i == j:
                for x in i:
                    if self[x] == dict2[x]: continue
                    else: return False
                return True
            else:
                return False
        else: raise TypeError("Cannot compare =: not a dict")
    
    
    def __lt__(self, dict2):
        if type(dict2) in (type(self), dict):
            i = sorted(list(set(sum([[x for x in y.keys()] for y in self.dl], []))))
            j = sorted(list(set(sum([[x for x in y.keys()] for y in dict2.dl], [])))) if type(dict2) == type(self) else sorted(dict2.keys())
            if len(i) < len(j):
                for x in i:
                    if self[x] == dict2[x]: continue
                    else: return False
                return True
            else:
                return False
        else: raise TypeError("Cannot compare <: not a dict")


    def __gt__(self, dict2):
        if type(dict2) in (type(self), dict):
            i = sorted(list(set(sum([[x for x in y.keys()] for y in self.dl], []))))
            j = sorted(list(set(sum([[x for x in y.keys()] for y in dict2.dl], [])))) if type(dict2) == type(self) else sorted(dict2.keys())
            if len(i) > len(j):
                for x in j:
                    if dict2[x] == self[x]: continue
                    else: return False
                return True
            else:
                return False
        else: raise TypeError("Cannot compare >: not a dict")


    def __add__(self, dict2):
        if type(dict2) in (type(self), dict):
            dl_list = []
            dl_copy = deepcopy(self.dl)
            dict2_copy = deepcopy(dict2.dl) if type(dict2) == type(self) else [deepcopy(dict2)]
            for x in dl_copy: dl_list.append(x)
            for x in dict2_copy: dl_list.append(x)
            return DictList(*dl_list)
        else: raise TypeError("Cannot add: not a dict")
    


    def __radd__(self, dict2):
        if type(dict2) in (type(self), dict):
            dl_list = []
            dl_copy = deepcopy(self.dl)
            dict2_copy = deepcopy(dict2.dl) if type(dict2) == type(self) else [deepcopy(dict2)]
            for x in dict2_copy: dl_list.append(x)
            for x in dl_copy: dl_list.append(x)
            return DictList(*dl_list)
        else: raise TypeError("Cannot add: not a dict")
    
    
    def __setattr__(self, name, value):
        if str(name) == "dl" and type(value) == list: super().__setattr__(name, value)
        else: raise AssertionError("Cannot store new values")
        
        
            
if __name__ == '__main__':
    #Simple tests before running driver
    #Put your own test code here to test DictList before doing bsc tests

    # d = DictList(dict(a=1,b=2), dict(b=12,c=13))
    # print('len(d): ', len(d))
    # print('bool(d):', bool(d))
    # print('repr(d):', repr(d))
    # print(', '.join("'"+x+"'" + ' in d = '+str(x in d) for x in 'abcx'))
    # print("d['a']:", d['a'])
    # print("d['b']:", d['b'])
    # print("d('b'):", d('b'))
    # print('iter results:', ', '.join(i for i in d))
    # print('item iter results:', ', '.join(str(i) for i in d.items()))
    # print('d.collapse():', d.collapse())
    # print('d==d:', d==d)
    # print('d+d:', d+d)
    # print('(d+d).collapse():', (d+d).collapse())
    
    print()
    import driver
    driver.default_file_name = 'bsc22S22.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
