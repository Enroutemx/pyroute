""" Run module

    The module 'Run' is the piece of code that is in charge of the

    set up of the configuration and the tests of the scripts the user

    wants to be tested.

     Dependencies:

     - **importlib**
     - **logging**
     - **os**
     - **pyroute.engine**
     - **pyroute.config**
     - **pyroute.logger**

    .. moduleauthor:: Enroute
"""

import importlib
import logging
import os

import pyroute.engine as Pyroute
from pyroute.config import Configuration
from pyroute.logger import Logger

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class Run(object):
    """
    Class Run is intended to set the configuration requirements, ensure the init

    of the Logger and the intitialization of a generic engine.
   """
    def __init__(self, config=None):
	"""The class loads the configuration requirements into the variables:

           - self.config
           - self.module_list
           - self.run_log

       Args:
            config (str): Path to the json file
        """
        self.config = Configuration(config)
        self.module_list = []
        self.run_log = Logger(self.config)

    def execute_tests(self):
	""" execute_test method starts a counter at the logger and initialize

	the generic engine.

	The method **self.run_log** prints a default message to the logger.

	The variable **session** is an instance of the generic engine and it

	loads the configuration requirements.
        """
        Logger.count_time()

        # Initialize Engine
        self.run_log.separate(self.config._colors['pyroute_logo'] ,"Pyroute Acceptance Testing Framework (insert logo)")
        session = Pyroute.EngineInitializer(self.config)

        # Start testing
        session.start()
