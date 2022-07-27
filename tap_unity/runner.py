import os
import json
import singer
from tap_unity.streams import AVAILABLE_STREAMS

from tap_unity.utils import get_abs_path
from tap_unity.client import UnityClient


LOGGER = singer.get_logger()


class TapUnityRunner:

    def __init__(self, config, state):
        self.config = config
        self.state = state
        self.unity_client = UnityClient(self.config, self.state)
        self.streams = [Stream(state, self.unity_client) for Stream in AVAILABLE_STREAMS]


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

        schemas = self.load_schemas()

        for stream in self.streams:
            stream.set_schema(schemas.get(stream.STREAM_NAME))
            stream.do_sync()    

        return
