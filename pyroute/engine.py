import os

from pyroute.tester import ITester
from pyroute.logger import Logger
from pyroute.utils import PyrouteImporter, Utils


class ModuleEngine(object):
    """
    This class implements the Module loading specifics.
    """

    def __init__(self, config):
        self.config = config
        self.modules_config = config._modules
        self.loaded_modules = {}
        self.loaded_methods = None
        self.module_log = Logger(self.config)
        self.start_up()

    def start_up(self):
        loaded = self.module_log.process(self.config._colors['loading_modules'], "Loading modules", self.load_modules)
        self.loaded_methods = self.load_methods()
        self.module_log.custom("[{:0>3}]".format(loaded), "Modules loaded", self.config._colors['modules_loaded'])

    def get_module_classes(self, loaded, name):
        # Get valid Module classes, a valid module class ends with "Module"
        mod_dict = vars(loaded)
        name = name.upper()
        mod_ = ((k, v) for k, v in mod_dict.items()
                if name in k.upper() and "MODULE" in k.upper())
        return tuple(mod_)[0]

    def load_modules(self):
        config = self.config._modules
        path = os.path.dirname(os.path.realpath(__file__)) + "/modules/"
        dir_contents = Utils.clean_filenames(os.listdir(path))
        modules = set(self.config._modules).intersection(dir_contents)

        for module in modules:
            dir_path = path + module + ".py"
            loaded_mod_ = PyrouteImporter.load(module, dir_path)
            mod_ = self.get_module_classes(loaded_mod_, module)
            instance_ = mod_[1](config[module])
            self.loaded_modules[mod_[0].upper()] = instance_

        loaded = len(self.loaded_modules.keys())
        return loaded

    def load_methods(self):
        """
        This method loads all methods from the modules, and filters out
        the common ones (between modules)
        """
        modules = self.loaded_modules
        methods = Utils.get_methods(modules)
        ambiguous_attrs = Utils.get_shared_attrs(modules)
        for attr in ambiguous_attrs:
            methods.pop(attr, None)
        return (modules, methods, ambiguous_attrs, self.config)


class EngineInitializer(object):
    """
    This is the generic "starter". If there is a module that
    implements its own engine, that will be used, otherwise
    Pyroute's default engine will be used. This enables support
    for alternative testing platforms and technologies, like
    Gherkin or Python's classic unittest.
    """

    def __init__(self, config):
        self.config = config
        self.module_engine = ModuleEngine(config)

    def start(self):
        for module in self.module_engine.loaded_modules:
            if hasattr(module, "_start_engine"):
                module._start_engine()
                return
        PYT = PyrouteTestEngine(self.config, self.module_engine)
        PYT._start_engine()


class PyrouteTestEngine(object):
    """
    Pyroute's default engine "PYT", runs every test listed in config.
    Check the documentation for more details about the test format.
    """
    def __init__(self, config, module_engine):
        self.config = config
        self.module_engine = module_engine
        self.loaded_methods = self.module_engine.loaded_methods
        self.I = ITester(*self.loaded_methods)
        self.engine_log = Logger(self.config)

    def get_tests(self):
        """
        Test finder allows the user to specify tests with
        and without a '.py' and also allows the user to
        specify a directory path with and without "/" if
        there's a file and a folder with the same name,
        the file and the folder and its files will be
        loaded.
        """
        tests_path = []
        for test in self.config._tests['path']:
            test_path = '{}/{}'.format(os.getcwd(),test)
            py_file = '{}.py'.format(test_path)
            if os.path.isdir(test_path):
                folder = os.listdir(test_path)
                files =[os.path.join(test_path, file) for\
                file in folder if file.endswith(".py")]
                [tests_path.append(file) for file in files]
            if os.path.isfile(py_file):
                tests_path.append(py_file)
            else:
                tests_path.append(test_path)
        return tests_path

    def load_tests(self):
        """
        Loads tests. Self explanatory. This method uses PyrouteImporter,
        the same mechanism behind the module system, to load them. More
        details in 'utils.py'
        """
        paths = self.get_tests()
        loaded_tests = {}
        for testpath in paths:
            testfile = os.path.basename(testpath)
            testname = str(testfile)[:-3]  # Name without the '.py' extension
            loaded = PyrouteImporter.load(testfile, testpath)
            loaded_tests[testname] = loaded
        return loaded_tests

    def get_test_cases(self, test):
        """
        Comprehension to filter the test cases we are interested in.
        Before this, the test object has some properties we don't case about,
        thus we filter them out. We also filter out those tests that don't
        start with the preffix specified in the configuration file.
        """
        cases = (case_name for case_name in dir(test)
                 if not case_name.startswith("__") and
                 case_name.startswith(self.config._tests['preffix']))
        return cases

    def run_cases(self, test_name, test, cases):
        """
        Runs cases, self explanatory. The process method is explained in
        the Logger, but basically it acts as a wrapper.
        """
        for case in cases:
            message = "Running test: {0} - Case: {1}".format(test_name, case)
            self.engine_log.process(self.config._colors['running_test'], message, getattr(test, case), self.I)

    def _start_engine(self):
        """
        This function is called by the EngineInitializer.
        For now, it counts the passed tests, and runs each case, per test.
        The Logger here does nothing, it is intended to run the background
        tracer to deal with errors.
        """
        passed = 0
        loaded_tests = self.engine_log.process(self.config._colors['loading_tests'], "Loading tests", self.load_tests)
        loaded = len(loaded_tests.keys())
        self.engine_log.custom("[{:0>3}]".format(loaded), "Tests loaded", self.config._colors['tests_loaded'])
        for name, test in loaded_tests.items():
            cases = self.get_test_cases(test)
            self.run_cases(name, test, cases)
            message_end = "Test: {0} --- Finished".format(name)
            self.engine_log.custom("[-O-]", message_end, self.config._colors['finished_test'])
            passed += 1
        self.finish(passed)

    # This function runs at the end of all tests, anything done at that time goes here
    def finish(self, passed_tests):
        self.engine_log.custom("[>:D]", "All tests completed", self.config._colors['tests_completed'])
        self.engine_log.separate(self.config._colors['passed_time'], "<<<< {0} Passed in {1:.3}s >>>>".format(passed_tests, Logger.elapsed_time()))
