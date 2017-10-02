import importlib
import logging
import pytest
import os

from pyroute import I
from pyroute.config import Configuration

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class Run(object):

    def __init__(self, config=None):
        self.config = Configuration(config)
        self.module_list = []

    def execute_tests(self):
        ########################################
        # TODO: we need to finish this process #
        #       of executing a test.           #
        ########################################
        # initialize modules
        modules = self.__load_modules()

        I(self.module_list)

        # Load tests
        tests = self.__load_tests()
        # Inject modules to I object

        ######################################
        # TODO: Expose I object with modules #
        #       found in config.json         #
        ######################################
        # Execute found tests
        pytest.main(tests)

    def __load_tests(self):
        #################################################################
        # TODO: make different scenarios with                           #
        # "path": [                                                     #
        #     "tests/sprint01_features", -> file                        #
        #     "tests/sprint02_features", -> file                        #
        #     "tests/other_fetaure/sprint01_features", -> file          #
        #     "tests/other_fetaure/sprint02_features", -> file          #
        #     "tests/whole_feature/" -> folder,                         #
        #                            discover sub folders and files.    #
        #     ],                                                        #
        #################################################################
        try:
            _real_test_path = []
            for test in self.config._tests['path']:
                _real_test_path.append(os.getcwd() + "/" + test + ".py")
            print(_real_test_path)
            return _real_test_path

        except Exception as e:
            print(e)

    def __load_modules(self):
        try:
            print(self.config._modules)
            for module in self.config._modules:
                # I._init(module)
                dir_path = os.path.dirname(os.path.realpath(__file__)) + \
                    "/modules/{0}.py".format(module)

                spec = importlib.util.spec_from_file_location(module, dir_path)

                mod_ = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(mod_)

                ###################################################
                # TODO: we need to make this case insensitive.    #
                ###################################################
                class_ = getattr(mod_, module.capitalize())

                self.module_list.append(class_)
        except Exception as e:
            logger.exception(e)
