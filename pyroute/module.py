from abc import ABCMeta, abstractmethod

import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# class Module(type, metaclass=ABCMeta):
class Module(metaclass=ABCMeta):

    # @abstractmethod
    def __init__(self, config, **kwargs):
        self.config = config
        if "defaults" in kwargs:
            kwargs['defaults'] = self.__load_options(kwargs['defaults'])
        return kwargs

    def log(self):
        return logger

    def __load_options(self, options):
        for option in options:
            try:
                if self.config[option]:
                    options[option] = self.config[option]
            except KeyError:
                msg = \
                    "config.json doesn't contain info about '{}', " \
                    "setting default value to '{}'".format(option,
                                                           options[option])
                logger.info(msg)
        for config in self.config:
            if config not in options:
                options[config] = self.config[config]
        return options

    def _init(self):
        pass

    def _before_init(self):
        pass

    def _after_init(self):
        pass

    def _check_requirements():
        pass
