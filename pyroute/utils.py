""" Utils Module
    ============

    All functions and classes that are useful for Pyroute internals.

    Dependencies:

    - **threading**
    - **os**
    - **importlib**

"""
import threading as T
import importlib
import os


class Threaded(object):
    """
    Decorator class to make a function threaded.
        The threads will be kept in a list given as its single argument::

            @Threaded(<a_thread_list>)
            def function_to_wrap...

        *If the need arises, a resource lock queue will be implemented as well,
        but for basic I/O, this should be enough.*
    """
    def __init__(self, thread_list):
        """
        The class loads the thread list into:

        - self.thread_list

        :param thread_list: List of threads wrapped
        :type thread_list: List

        """
        self.thread_list = thread_list

    def __call__(self, fn):
        """
        The __call__ method is used to call on the wrapper function\
        outside the class:

        :param fn: List of
        :type fn: List <Thread>
        :returns wrapper: The thread of the function
        """
        def wrapper(*args, **kwargs):
            """
            The wrapper function creates the thread to be handled.

            :param fn: A list with threads
            :type fn: List <Thread>
            :returns wrapper: The thread of the function in which @Threaded
            is implemented
            """
            thread = T.Thread(target=fn, args=args, kwargs=kwargs)
            thread.daemon = True
            thread.start()
            self.thread_list.append(thread)
        return wrapper

    @classmethod
    def wrap_up(cls, thread_list):
        """
        The wrap_up method joins all pending threads on a given list::

            Threaded.wrap_up(<a_thread_list)

        :param thread_list: A list with the threads
        :type thread_list: List <Thread>
        """
        for t in thread_list:
            t.join()


class PyrouteImporter(object):
    """
    Used to load tests and modules.

    Internally, the attributes look as follows:

        * Pyroute Module names: **MODULENAME**
        * Pyroute Test Case:    **<preffix>** name
        * Pyroute Test Name:    **testname** or **test_name**

    *Loading the source directly is most likely not a good solution, if
    someone comes up with a safer and better solution, anyone is welcome
    to contribute.*
    """
    @classmethod
    def load(cls, name, path):
        """
        Loads the tests and modules.

        :param name: The name of the modules
        :type name: String
        :param path: The path of the module to loads
        :type path: String
        :returns loaded: The module loaded
        :type loaded: Python Module
        """
        spec = importlib.util.spec_from_file_location(name, path)
        loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
        return loaded


class Utils(object):
    """
    General useful functions used in Pyroute, not necessarily related to
    one another.
    """
    @staticmethod
    def get_shared_attrs(objs):
        """
        This method takes a dictionary of objects and returns their shared
        attributes. This method is useful to find conflicting attributes
        between objects.

        :param objs: The objects to be processed
        :type objs: Dictionary
        :returns shared: Dictionary
        """
        methods = list(map(dir, objs.values()))
        if len(methods) <= 1:
            return set()
        shared = set(Utils.clear_dunders(methods[0])).intersection(*methods)
        return shared

    @staticmethod
    def get_methods(objs):
        """
        This method takes a dictionary of objects and returns their
        methods in a dictionary.

        If two or more objects share the same method, only one will
        be loaded.

        :param objs: The objects to be processed
        :type objs: Dictionary
        :returns shared: Dictionary
        """
        return {method: obj for obj in objs.values()
                for method in Utils.clear_dunders(dir(obj))
                if callable(getattr(obj, method))}

    @staticmethod
    def clean_filenames(filenames):
        """
        This method takes a list of filenames and gets rid of their
        extensions.

        :param filenames: A List of filenames to be processed_func
        :type filenames: List <String>
        :returns set: Set of Methods
        """
        return set(map(lambda x: os.path.splitext(x)[0], filenames))

    @staticmethod
    def clear_dunders(methods):
        """
        This method takes a list of methods and filters out those
        that are Python's 'dunder' methods.

        :param methods: A list of Methods and Filters
        :type methods: List <String>
        :returns List: A list of non-dunder methods
        """
        return list(filter(lambda n: not n.startswith("_"), methods))

    @staticmethod
    def overridable(methods):
        """
        This decorator allows the decorated function to be replaced
        (overriden) by another with the same name, from a list of methods.
        This decorator is useful to define functions that can be redefined
        elsewhere (ex: *from a module*).

        :param methods: List of methods to be overriden
        :type methods: List <String>
        :returns processed_func: Function
        """
        def processed_func(fn):
            def wrapper(*args, **kwargs):
                if fn.__name__ in methods:
                    return getattr(methods[fn.__name__], fn.__name__)(
                        *args, **kwargs)
                else:
                    return fn(*args, **kwargs)
            return wrapper
        return processed_func
