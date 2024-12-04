# Submitter: cyrdc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)  
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

import re, traceback, keyword, copy


def pnamedtuple(type_name, field_names, mutable = False,  defaults = {}):
    def show_listing(s):
        for line_number, line_text in enumerate(s.split('\n'),1):           
            print(f' {line_number: >3} {line_text.rstrip()}')
    
    def filters(arg):
        return True if re.match('([A-Z|a-z])\w*', arg) and not keyword.iskeyword(arg) else False
    
    try:
        if type(field_names) == list: names_field = copy.deepcopy(field_names)
        elif type(field_names) == str: names_field = re.split('[, ]+', field_names)
        else: raise SyntaxError('Not a list or string')
        
        if not filters(type_name): raise SyntaxError("Invalid type_name")
        if type(names_field) == list:
            for i in names_field:
                if not filters(i): raise SyntaxError("Invalid field_names")
        else: raise SyntaxError('Not a string or list')
        if defaults:
            if not all([filters(i) if i in names_field else False for i in defaults.keys()]): raise SyntaxError("Invalid default keys")
    except TypeError: raise SyntaxError("Something went wrong")
    
    def args():
        return str(names_field)[1:-1].replace("'", "")

    def init():
        return '\n'.join([f'        self.{i} = {i}' for i in names_field])

    def repr1():
        return ','.join([f'{i}=' + "{" + f'{i}' + "}" for i in names_field])
    
    def repr2():
        return ','.join([f'{i}=self.{i}' for i in names_field])
    
    def get():
        return '\n\n'.join([f'    def get_{i}(self):\n        return self.{i}' for i in names_field])
    
    def getitem():
        r_str = '        if type(index) == int:\n            '
        r_str += '\n            '.join([f'elif index == {i}:\n                return self.get_{names_field[i]}()' for i in range(len(names_field))])[2:]
        r_str += '\n            else: raise IndexError("Invalid int index")'
        r_str += '\n        elif type(index) == str:'
        r_str += '\n            if index in self._fields: return eval("self.get_" + index + "()")'
        r_str += '\n            else: raise IndexError("Invalid str index")'
        r_str += '\n        else: raise IndexError("Invalid type")'
        return r_str

    def eq():
        return f'return True if type(self) == type(right) and all(self[i] == right[i] for i in range(len({names_field}))) else False'

    def asdict():
        return f'return dict(zip(self._fields, [self[x] for x in self._fields]))'
    
    def make():
        return f'return {type_name}(*iterable)'
    
    def replace():
        r_str =     '        for i in kargs.keys():'
        r_str +=  '\n            if i not in self._fields: raise TypeError("Illegal field name")'
        r_str +=  '\n        if self._mutable:'
        r_str +=  '\n            for i, j in kargs.items(): self.i = j'
        r_str +=  '\n            return None'
        r_str +=  '\n        else:'
        r_str +=  '\n            from copy import deepcopy'
        r_str +=  '\n            new_fields = deepcopy(self._fields)'
        r_str +=  '\n            for x in range(len(new_fields)):'
        r_str +=  '\n                if new_fields[x] in kargs.keys(): new_fields[x] = kargs[new_fields[x]]'
        r_str +=  '\n                else: new_fields[x] = self[new_fields[x]]'
        r_str += f'\n            return {type_name}._make(new_fields)'
        return r_str


    function_template = '''\
    _fields = {fields}
    _mutable = {mutable}
    
    def __init__(self, {args}):
{init}

    def __repr__(self):
        return '{type_name}({repr1})'.format({repr2})
    
{get}

    def __getitem__(self, index):
{getitem}
    
    def __eq__(self, right):
        {eq}

    def _asdict(self):
        {dict}
    
    def _make(iterable):
        {make}
    
    def _replace(self, **kargs):
{replace}
'''  

    function_definition = function_template.format(\
    type_name = type_name,\
    fields = names_field,\
    mutable = mutable,\
    args = args(),\
    init = init(),\
    repr1 = repr1(),\
    repr2 = repr2(),\
    get = get(),\
    getitem = getitem(),\
    eq = eq(),\
    dict = asdict(),\
    make = make(),\
    replace = replace()
    )


#     if decorate:
#         function_definition += "    return '-->'+result+'<--'"
#     else:
#         function_definition += "    return result"

    class_definition = f'class {type_name}():\n{function_definition}'
    # Debug help: uncomment next line, which prints source code for the class
    show_listing(class_definition)
    
    # Execute the class_definition's str in name_space; next bind its
    #   source_code attribute to this class_definition; following try+except
    #   return the class object created; if there are any syntax errors, show
    #   the class and also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )                    
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):                        
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    #driver tests
    import driver  
    driver.default_file_name = 'bscp3S22.txt'
    driver.default_show_exception_message = True
    driver.default_show_traceback = True
    driver.driver()
