from abc import ABCMeta, abstractmethod


class Module(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _init(self):
        pass

    def _before_init(self):
        pass

    def _after_init(self):
        pass

    @abstractmethod
    def _check_requirements(self):
        pass
