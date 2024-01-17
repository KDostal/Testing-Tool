from elasticsearch import Elasticsearch
import config

class Client:
    def __init__(self, is_dev=True):
        self.user = config.ES_USER
        self.password = config.ES_PW_DEV if is_dev else config.ES_PW_TEST
        self.url = config.ES_URL_DEV if is_dev else config.ES_URL_TEST

    def initialize_client(self):
        client = Elasticsearch(
            self.url, basic_auth=(self.user, self.password), verify_certs=False
        )
        return client