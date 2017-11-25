import os

from pyroute.config import Configuration
from pyroute.logger import Logger
from pyroute.utils import PyrouteImporter
from pyroute.errors import *

class ITester(object):

    __loaded_modules = {}

    def __init__(self):
        self.__all_loaded = False
        self.__config = Configuration("config/config.json")
        self.__load_modules()
        self.__log = Logger()
    
    def say(self, message):
        """
        This method sends a custom message to the Logger. Use this for debugging.
            `- message`: The text to be displayed.
        """
        self.__log.custom("[-I-]", message)
    
    def __getitem__(self, modname):
        # Allow 'I' to be used like a dictionary to specify a Module in ambiguous
        # scenarios
        return ITester.__loaded_modules[modname.lower()]

    def __setattr__(self, attr, value):
        # Write-protect 'I' (bar the initial parameters)
        if attr in ("_ITester__all_loaded",\
                "_ITester__config",
                "_ITester__loaded_modules",
                "_ITester__log"):
            object.__setattr__(self, attr, value)
        else:
            # The logger will take care of this in the future
            err = "Cannot assign to '{0}'. Only use a module methods to interface with it.".format(attr)
            raise AssignmentError(err)

    def __getattr__(self, attr):
        """
        Module method finder algorithm. This will be replaced with a cache-based
        lookup in the next version/commit.
        """
        for module in ITester.__loaded_modules:
            try:
                return getattr(ITester.__loaded_modules[module], attr)
            except AttributeError:
                next

        # The logger will take care of this in the future
        err = "No module has a method or property called '{0}'".format(attr)
        raise AttributeError(err)

    def __load_modules(self):
        """
        Loads instances of each module in a list. Rather than using dependency
        injection directly, an object dispatcher is used. See above for the 
        current implementation of this dispatcher
        """
        for module in self.__config._modules:
            dir_path = os.path.dirname(os.path.realpath(__file__)) + \
                "/modules/{0}.py".format(module)

            mod_ = PyrouteImporter.load(module, dir_path)
            instance_ = mod_[module.upper()]
            instance_ = instance_(self.__config._modules[module])
            ITester.__loaded_modules[module] = instance_
