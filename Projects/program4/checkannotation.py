# Submitter: cyrdc(Cyr, Christopher)
# Partner  : justisl9(Lee, Justin)  
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
 
from goody import type_as_str
import inspect
from collections.abc import Iterable

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # We start by binding the class attribute to True meaning checking can occur
    #   (but only when the function's self._checking_on is also bound to True)
    checking_on  = True
  
    # For checking the decorated function, bind its self._checking_on as True
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    def check(self,param,annot,value,check_history=''):
        '''
        Check whether param's annot is correct for value, adding to check_history if recurs;
        defines many local function which use it parameters.
        Params:
        param is a string that specifies the name of the parameter being checked
        annot is a data structure that specifies the annotation
        value is the value of param that the annotation should be checked against
        check_history is a string that embodies the history of checking the annotation for the parameter to here
        '''    
        def check_list(check_history):
            assert isinstance(value, list), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {str(type(value))[8:-2]} ...should be type {str(type(annot))[8:-2]}{check_history}"
            if len(annot) == 0: pass
            elif len(annot) == 1:
                for x in value:
                    if isinstance(x, Iterable): self.check(param, annot[0], x, check_history)
                    elif not isinstance(x, annot[0]):
                        check_history += f'\nlist[{value.index(x)}] check: {type(value)}'
                        assert False, f"'{param}' failed annotation check(wrong type): value = {x}\n  was type {str(type(x))[8:-2]} ...should be type {str(type(annot[0]))[8:-2]}{check_history}"
            else:
                assert len(value) == len(annot), f"'{param}' failed annotation check(wrong number of elements): value = {value}\n  annotation had {len(annot)} elements{annot}"
                for x, y in zip(value, annot):
                    if isinstance(x, Iterable): self.check(param, y, x, check_history)
                    elif not isinstance(x, y):
                        check_history += f'\nlist[{value.index(x)}] check: {y}'
                        assert False, f"'{param}' failed annotation check(wrong type): value = {x}\n  was type {str(type(x))[8:-2]} ...should be type {str(y)[8:-2]}{check_history}"
        
        def check_tuple(check_history):
            assert isinstance(value, tuple), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {str(type(value))[8:-2]} ...should be type {str(type(annot))[8:-2]}{check_history}"
            if len(annot) == 0: pass
            elif len(annot) == 1:
                for x in value:
                    if isinstance(x, Iterable): self.check(param, annot[0], x, check_history)
                    elif not isinstance(x, annot[0]):
                        check_history += f'\ntuple[{value.index(x)}] check: {type(value)}'
                        assert False, f"'{param}' failed annotation check(wrong type): value = {x}\n  was type {str(type(x))[8:-2]} ...should be type {str(type(annot[0]))[8:-2]}{check_history}"
            else:
                assert len(value) == len(annot), f"'{param}' failed annotation check(wrong number of elements): value = {value}\n  annotation had {len(annot)} elements{annot}{check_history}"
                for x, y in zip(value, annot):
                    if isinstance(x, Iterable): self.check(param, y, x, check_history)
                    elif not isinstance(x, y):
                        check_history += f'\ntuple[{value.index(x)}] check: {y}'
                        assert False, f"'{param}' failed annotation check(wrong type): value = {x}\n  was type {str(type(x))[8:-2]} ...should be type {str(y)[8:-2]}{check_history}"
        
        def check_dict(check_history):
            assert isinstance(value, dict), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {str(type(value))[8:-2]} ...should be type {str(type(annot))[8:-2]}{check_history}"
            if len(annot) == 0: pass
            elif len(annot) == 1:
                for x, y in value.items():
                    if not isinstance(x, list(annot.keys())[0]):
                        check_history += f'\ndict key check: {list(annot.keys())[0]}'
                        assert False, f"'{param}' failed annotation check(wrong type): value = {x}\n  was type {str(type(x))[8:-2]} ...should be type {str(list(annot.keys())[0])[8:-2]}{check_history}"
                    if not isinstance(y, list(annot.values())[0]):
                        check_history += f'\ndict value check: {list(annot.values())[0]}'
                        assert False, f"'{param}' failed annotation check(wrong type): value = {y}\n  was type {str(type(y))[8:-2]} ...should be type {str(list(annot.values())[0])[8:-2]}{check_history}"
            else: assert False, f"'{param}' annotation inconsistency: dict should have 1 item but had {len(annot)}\n  annotation = {annot}{check_history}"
                
        def check_set(check_history):
            assert isinstance(value, set), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {str(type(value))[8:-2]} ...should be type {str(type(annot))[8:-2]}{check_history}"
            if len(annot) == 0: pass
            elif len(annot) == 1:
                for x in value:
                    if not isinstance(x, list(annot)[0]):
                        check_history += f'\nset[{x}] check: {list(annot)[0]}'
                        assert False, f"'{param}' failed annotation check(wrong type): value = {x}\n  was type {str(type(x))[8:-2]} ...should be type {str(type(annot[0]))[8:-2]}{check_history}"
            else: assert False, f"'{param}' annotation inconsistency: set should have 1 item but had {len(annot)}\n  annotation = {annot}{check_history}"
            
        def check_frozenset(check_history):
            assert isinstance(value, frozenset), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {str(type(value))[8:-2]} ...should be type {str(type(annot))[8:-2]}{check_history}"
            if len(annot) == 0: pass
            elif len(annot) == 1:
                for x in value:
                    if not isinstance(x, list(annot)[0]):
                        check_history += f'\nfrozenset[{x}] check: {list(annot)[0]}'
                        assert False, f"'{param}' failed annotation check(wrong type): value = {x}\n  was type {str(type(x))[8:-2]} ...should be type {str(type(annot[0]))[8:-2]}{check_history}"
            else: assert False, f"'{param}' annotation inconsistency: frozenset should have 1 item but had {len(annot)}\n  annotation = {annot}{check_history}"
            
        def check_callable(check_history):
            try:
                if type(value) != int:
                    if type(annot) != list:
                        if not all([annot(x) for x in value]): assert False
                    else:
                        if not all([annot[0](x) for x in value]): assert False
                else: 
                    if not annot(value): assert False
            except:
                assert False

        # We start by comparing check's function annotation to its arguments
        # print()
        # print('param', param)
        # print('annot', annot)
        # print('value', value)
        # print()
        if annot is None: return
        elif isinstance(annot, type): assert isinstance(value, annot), f"'{param}' failed annotation check(wrong type): value = {value}\n  was type {str(type(value))[8:-2]} ...should be type {str(annot)[8:-2]}"
        elif isinstance(annot, list) and 'lambda' not in str(annot): check_list(check_history)
        elif isinstance(annot, tuple): check_tuple(check_history)
        elif isinstance(annot, dict): check_dict(check_history)
        elif isinstance(annot, set): check_set(check_history)
        elif isinstance(annot, frozenset): check_frozenset(check_history)
        elif 'lambda' in str(annot): check_callable(check_history)
        else: raise NotImplemented

        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        '''
        Returns the parameter->argument bindings as an OrderedDict, derived
        from dict, binding the function header's parameters in order
        '''

        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        if not self._checking_on or not self.checking_on: return self._f(*args, **kargs)
        
        try:
            bindings = param_arg_bindings()
            annots = inspect.OrderedDict(self._f.__annotations__.items())
            if args and not kargs:
                # print(args)
                for x in bindings.keys():
                    self.check(x, annots[x], bindings[x])
            elif kargs and not args:
                # print(kargs)
                for x in bindings.keys():
                    self.check(x, annots[x], bindings[x])
            # If 'return' is in the annotation, check it
            if 'return' in annots.keys(): assert isinstance(self._f(*args), annots['return']), "Invalid return type"
            # Return the decorated answer
            return annots
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            # print(80*'-')
            # for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #     print(l.rstrip())
            # print(80*'-')
            raise




  
if __name__ == '__main__':     
#Extra Credit Check: String (with Eval)
#c-->def f(x : 'x>=0'): pass
#c-->f = ca(f)
#c-->f(1)
#^-->f(-1)-->AssertionError
#^-->f('a')-->AssertionError
#c-->def f(x,y : 'x<y'): pass
#c-->f = ca(f)
#c-->f(3,5)
#^-->f(5,3)-->AssertionError
#^-->f(3,'a')-->AssertionError
               
    #driver tests
    import driver
    driver.default_file_name = 'bscp4S22.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
