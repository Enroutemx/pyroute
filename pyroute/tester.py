import os
import importlib
from pyroute.config import Configuration


class ITester(object):

    def __init__(self):
        self.config = Configuration("config/config.json")
        self.__loaded_modules = {}
        self.__load_modules()

    def __getitem__(self, modname):
        return self.__loaded_modules[modname]

    def __getattr__(self, attr):
        for module in self.__loaded_modules:
            try:
                return getattr(self.__loaded_modules[module], attr)
            except AttributeError:
                next

        # The logger will take care of this in the future
        err = "No module has a method or property called '{0}'".format(attr)
        raise AttributeError(err)

    def __load_modules(self):
        for module in self.config._modules:
            dir_path = os.path.dirname(os.path.realpath(__file__)) + \
                "/modules/{0}.py".format(module)

            spec = importlib.util.spec_from_file_location(module, dir_path)

            mod_ = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(mod_)

            ###################################################
            # TODO: we need to make this case insensitive.    #
            ###################################################
            class_ = getattr(mod_, module.capitalize())
            instance_ = class_(self.config._modules[module])
            self.__loaded_modules[module] = instance_


I = ITester()
# class Decorators(object):
#     pass
