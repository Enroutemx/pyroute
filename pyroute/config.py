"""The config module loads the framework modules specified by the user, 
user's tests and settings from the default config.json, unless a different
file is choosen by the user.

When **pryoute run** is used, the default config.json will be loaded.

.. code-block:: console

   $ pyroute run 

Below is shown how to use a specific json file.

.. code-block:: console

   $ pyroute run --config=/users/path/to_json_file

.. moduleauthor:: Enroute
"""

import json
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class Configuration(object):

    def __init__(self, config_path):
        """The class loads the json file into the variables:

        - self._tests
        - self._modules
        - self._colors

        Args:
            config_path (str): Relative path to the json file
        """
        config = self.load_configs(config_path)
        self._tests = config['tests']
        self._modules = config['modules']
        self._colors = config['colors']

    def load_configs(self, config_path):
        """This method takes the config_path and load the configuration from a json file.

        :param config_path: Relative path to the json file.
        :type config_path: str.
        :returns: dict
        """
        logger.info('Start loading config file')
        logger.debug('config_path=%s', config_path)
        try:
            with open(config_path) as data_file:
                return json.load(data_file)
        except IOError:
            logger.exception("File doesn't exist in %s", config_path)
