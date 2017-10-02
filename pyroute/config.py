import json
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class Configuration(object):

    def __init__(self, config_path):
        config = self.load_configs(config_path)
        self._tests = config['tests']
        self._modules = config['modules']

    def load_configs(self, config_path):
        """
        Loads configuration from a json file.
        """
        logger.info('Start loading config file')
        logger.debug('config_path=%s', config_path)
        try:
            with open(config_path) as data_file:
                return json.load(data_file)
        except IOError:
            logger.exception("File doesn't exist in %s", config_path)
