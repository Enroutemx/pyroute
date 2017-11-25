import os
import sys
import importlib
import traceback

from pyroute.tester import ITester
from pyroute.logger import Logger
from pyroute.utils import PyrouteImporter

class TestEngine(object):
    def __init__(self, config):
        self.__loaded_tests = {}
        self.config = config
        self.TElog = Logger()
        self.I = ITester()

    def get_tests(self):
        """
        Test finder, for now it just allows the user to specify tests
        with and without a '.py' extension.
        """
        tests_path = []
        for test in self.config._tests['path']:
            test_path = os.getcwd() + "/" + test
            if not test_path.endswith(".py"):
                test_path = "".join([test_path, ".py"])
            tests_path.append(test_path)
        return tests_path
    
    #@Logger.on_error("log")
    def load_tests(self):
        """
        Loads tests. Self explanatory. This method uses PyrouteImporter, 
        the same mechanism behind the module system, to load them. More
        details in 'utils.py'
        """
        paths = self.get_tests()
        loaded = 0
        for testpath in paths:
            testfile = os.path.basename(testpath)
            testname = str(testfile)[:-3] # Name without the '.py' extension.
            loaded_test = PyrouteImporter.load(testfile, testpath)
            self.__loaded_tests[testname] = loaded_test
            loaded += 1
        return loaded

    #@Logger.on_error("log")
    def get_test_cases(self, test):
        """
        Comprehension to filter the test cases we are interested in.
        Before this, the test object has some properties we don't case about,
        thus we filter them out. We also filter out those tests that don't start 
        with the preffix specified in the configuration file.
        """
        cases = (case_name for case_name in test.keys() 
                if not case_name.startswith("__") and 
                case_name.startswith(self.config._tests['preffix']))
        return cases

    #@Logger.on_error("log")
    def run_cases(self, test_name, test, cases):
        """
        Runs cases, self explanatory. The process method is explained in 
        the Logger, but basically it acts as a wrapper.
        """
        for case in cases:
            message = "Running test: {0} - Case: {1}".format(test_name, case)
            self.TElog.process(message, test[case], self.I)

    def start(self):
        """
        This function is called from run.py, once a TestEngine object,
        has been initialized.
        For now, it counts the passed tests, and runs each case, per test.
        The Logger here does nothing, it is intended to run the background 
        tracer to deal with errors.
        """
        passed = 0
        Logger.start_tracing()
        for name, test in self.__loaded_tests.items():
            cases = self.get_test_cases(test)
            self.run_cases(name, test, cases)
            message_end = "Test: {0} --- Finished".format(name)
            self.TElog.custom("[-O-]", message_end)
            passed += 1
        self.finish(passed)
    
    #This function runs at the end of all tests, anything done at that time goes here
    def finish(self, passed_tests):
        self.TElog.custom("[>:D]", "All tests completed")
        self.TElog.separate("<<<< {0} Passed in {1:.3}s >>>>".format(passed_tests, Logger.elapsed_time()))
