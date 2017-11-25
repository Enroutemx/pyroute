import importlib
import logging
import os

import pyroute.engine as Pyroute
from pyroute.config import Configuration
from pyroute.logger import Logger

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class Run(object):

    def __init__(self, config=None):
        self.config = Configuration(config)
        self.module_list = []
        self.run_log = Logger()

    def execute_tests(self):
        ########################################
        # TODO: we need to finish this process #
        #       of executing a test.           #
        ########################################
        
        Logger.count_time()
        # Initialize Engine
        self.run_log.separate("Pyroute Acceptance Testing Framework (insert logo)")
        session = Pyroute.TestEngine(self.config)

        # Load tests
        load_message = "Loading tests"
        loaded = self.run_log.process(load_message, session.load_tests)
        self.run_log.custom("[{:0>3}]".format(loaded), "Tests loaded")

        ######################################
        # TODO: Expose I object with modules #
        #       found in config.json         #
        ######################################
        
        # Execute found tests
        session.start()

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
