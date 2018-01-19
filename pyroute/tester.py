from pyroute.config import Configuration
from pyroute.logger import Logger
from pyroute.errors import *


class ITester(object):

    def __init__(self, modules, methods, ambiguity_set):
        self.__config = Configuration("config/config.json")
        self.__loaded_modules = modules
        self.__loaded_methods = methods
        self.__ambiguity_set = ambiguity_set
        self.__log = Logger()

    def say(self, message):
        """
        This method sends a custom message to the Logger.
        Use this for debugging.
            `- message`: The text to be displayed.
        """
        self.__log.custom("[-I-]", message)

    def sleep(self):
        pass

    def __getitem__(self, modname):
        # Allow 'I' to be used like a dictionary to specify
        # a Module in ambiguous scenarios
        return self.__loaded_modules[(modname.upper() + "MODULE")]

    def __setattr__(self, attr, value):
        # Write-protect 'I' (bar the initial parameters)
        if attr in ("_ITester__config",
                    "_ITester__loaded_modules",
                    "_ITester__loaded_methods",
                    "_ITester__ambiguity_set",
                    "_ITester__log"):
            object.__setattr__(self, attr, value)
        else:
            # The logger will take care of this in the future
            err = "Cannot assign to '{0}'.\
                    Only use a module methods to\
                    interface with it.".format(attr)
            raise AssignmentError(err)

    def __getattr__(self, attr):
        """
        First load the method if it is available in any module. If
        two or more modules share the same method, raises an error.
        """
        if attr in self.__loaded_methods:
            return getattr(self.__loaded_methods[attr], attr)
        if attr in self.__ambiguity_set:
            err = "Two or more modules share the same method.\
                    Use the dictionary syntax to specify a module.\
                    Ex: I[module_name].{0}".format(attr)
            raise AmbiguousMethodCallError(err)
        else:
            err = "No module has a \
                    method or property called '{0}'".format(attr)
            raise AttributeError(err)
