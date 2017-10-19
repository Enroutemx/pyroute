import os
import importlib
from pyroute.config import Configuration

class ITester(object):

    __module_list = []

    def __init__(self):
        self.config = Configuration("config/config.json")
        self.__load_modules()

    def __getattr__(self, attr):
        for module in ITester.__module_list:
            method = getattr(module, attr)
            if hasattr(method, "__call__"):
                return self.__MethodWrapper(method)
            else: next
        return method

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
            ITester.__module_list.append(instance_)

    class __MethodWrapper(object):
        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            try:
                self.func(*args, **kwargs)
            except AttributeError:
                ITester.__module_list[self.func.__name__](*args, **kwargs)

I = ITester()
# class Decorators(object):
#     pass
