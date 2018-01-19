import threading as T
import importlib
import os

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
    Pyroute Module names: MODULENAME or MODULENAME
    Pyroute Test Case:    <preffix>name 
    Pyroute Test Name:    testname or test_name

    Loading the source directly is most likely not a good solution, if
    someone comes up with a safer and better solution, replace this.
    """
    @classmethod
    def load(cls, name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
        return loaded

class Utils(object):
    """
    General useful functions used in Pyroute, not necessarily related to 
    one another
    """
    @staticmethod
    def get_shared_attrs(objs):
        """
        This method takes a dictionary of objects of the form:
            - {object_name: object_instance}
        and returns their shared attributes, that is, the attributes
        the objects have in common.
        This method is useful to find conflicting attributes between 
        objects. (Returns an empty set if there is only a single object)
        """
        methods = list(map(dir, objs.values()))
        if len(methods) <= 1:
            return set()
        shared = set(Utils.clear_dunders(methods[0])).intersection(*methods)
        return shared

    @staticmethod
    def get_methods(objs):
        """
        This method takes a dictionary of objects of the form:
            - {object_name: object_instance}
        and returns their methods, in a dictionary of the form:
            - {method_name: object_instance}
        If two or more objects share the same method, only one will
        be loaded.        
        """
        return {method: obj for obj in objs.values() 
                for method in Utils.clear_dunders(dir(obj))
                if callable(getattr(obj, method))}

    @staticmethod
    def clean_filenames(filenames):
        """
        This method takes a list of filenames and gets rid of their
        extensions
        """
        return set(map(lambda x: os.path.splitext(x)[0], filenames))

    @staticmethod
    def clear_dunders(methods):
        """
        This method takes a list of methods and filters out those 
        that are Python's 'dunder' methods
        """
        return list(filter(lambda n: not n.startswith("_"), methods))

    @staticmethod
    def overridable(methods):
        """
        This decorator allows the decorated function to be replaced
        (overriden) by another with the same name, from a list of methods.
        This decorator is useful to define functions that can be redefined
        elsewhere (ex: from a module)
        """
        def processed_func(fn):
            def wrapper(*args, **kwargs):
                if fn.__name__ in methods:
                    return getattr(methods[fn.__name__], fn.__name__)(*args, **kwargs)
                else:
                    return fn(*args, **kwargs)
            return wrapper
        return processed_func
