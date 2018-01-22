from pyroute.module import Module
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    logger.exception("You need to install `requests` library")


class RestModule(Module):

    def __init__(self, config):
        # Default values
        self.defaults = {
            'endpoint': ''
        }
        self.config_data = super().\
            __init__(config=config, defaults=self.defaults)
        self.module_configuration = self.config_data['defaults']

    def send_get_request(self, url, **kwargs):
        # This should only receive headers, but use kwargs in case of expansion
        return requests.get(url=self.__build_url(url), **kwargs)

    def send_post_request(self, url, **kwargs):
        # Should receive payload and headers as named parameter
        return requests.post(url=self.__build_url(url), **kwargs)

    def send_patch_request(self, url, **kwargs):
        return requests.patch(url=self.__build_url(url), **kwargs)

    def send_put_request(self, url, **kwargs):
        return requests.put(url=self.__build_url(url), **kwargs)

    def send_delete_request(self, url, **kwargs):
        return requests.delete(url=self.__build_url(url), **kwargs)

    def __build_url(self, url):
        return self.module_configuration['endpoint'] + url
