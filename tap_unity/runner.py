import os
import json
import singer

from tap_unity.utils import get_abs_path
from tap_unity.client import UnityClient


LOGGER = singer.get_logger()


class TapUnityRunner:

    def __init__(self, config):
        self.config = config
        self.unity_client = UnityClient(config)


    def load_schemas(self):
        """ Load schemas from schemas folder """
        schemas = {}
        for filename in os.listdir(get_abs_path('schemas')):
            path = get_abs_path('schemas') + '/' + filename
            file_raw = filename.replace('.json', '')
            with open(path) as file:
                schemas[file_raw] = json.load(file)
        return schemas


    def sync(self):
        """
        Sync data from tap source
        """
        LOGGER.info('Starting sync')

        # Load schemas
        schemas = self.load_schemas()
        response = self.unity_client.make_request()
        
        singer.write_schema("acquisitions", schemas["acquisitions"], "timestamp")
        
        for row in response:
            singer.write_record("acquisitions", row)

        return
