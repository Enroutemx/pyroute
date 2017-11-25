import threading as T
import importlib
import re

# All functions and classes that could be useful for Pyroute internals go here.

class Threaded(object):
    
    """
    Decorator class to make a function threaded.
    The threads will be kept in a list given as its single argument
    Like so:
    
        ```
        @Threaded(<a_thread_list>)
        def function_to_wrap...
        ```
    The wrap_up method joins all pending threads on a given list:

        ```
        Threaded.wrap_up(<a_thread_list)
        ```
    If the need arises, a resource lock queue will be implemented as well,
    but for basic I/O, this should be enough.
    """

    def __init__(self, thread_list):
        self.thread_list = thread_list

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            thread = T.Thread(target=fn, args=args, kwargs=kwargs)
            thread.daemon = True
            thread.start()
            self.thread_list.append(thread)
        return wrapper
         
    @classmethod
    def wrap_up(cls, thread_list):
        for t in thread_list:
            t.join()

class PyrouteImporter(object):
    """
    Static class used to load tests and modules, it reads a spec,
    makes sure the module class is loaded case-insensitively, etc.
    
    Internally, the attributes look as follows
    Pyroute Module class: class MODULENAME
    Pyroute Module names: modulename or module_name
    Pyroute Test Case:    <preffix>name 
    Pyroute Test Name:    testname or test_name

    Loading the source directly is most likely not a good solution, if
    someone comes up with a safer and better solution, replace this.
    """
    @classmethod
    def load(cls, name, path):
        
        mod_dict = {}
        spec = importlib.util.spec_from_file_location(name, path)
        src = spec.loader.get_source(name)

        # Pyroute handles uppercased names, regardless of how they're written
        # Not the prettiest and more pythonic option, but it works
        regex = re.compile(r"(?:^class)\s*([a-zA-Z]*)\(Module\)", re.M)
         
        for match in regex.finditer(src):
            src = regex.sub("class {0}(Module)".format(name.upper()), src)
        
        mod = spec.loader.source_to_code(src, path)
        
        exec(mod, mod_dict)
        
        return mod_dict
