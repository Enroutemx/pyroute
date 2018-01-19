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
        Logger.count_time()
        
        # Initialize Engine
        self.run_log.separate("Pyroute Acceptance Testing Framework (insert logo)")
        session = Pyroute.EngineInitializer(self.config)

        # Start testing
        session.start()
