import importlib
import logging
import pytest
import os

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
