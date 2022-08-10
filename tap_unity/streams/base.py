from typing import Dict
import singer
from tap_unity.client import UnityClient
from tap_unity.utils import SchemaNotSetError


class UnityBase:
    """
    Stram base class
    """

    STREAM_NAME = ""
    ENDOINT = ""

    def __init__(self, config, state, unity_client):
        self.config: Dict[str, str] = config
        self.state: Dict[str, str] = state
        self.unity_client: UnityClient = unity_client

    
    def set_schema(self, schema):
        self.schema = schema


    def do_sync(self):
        """
        Sync data from tap source
        """
        if not self.schema:
            raise SchemaNotSetError()

        response = self.unity_client.make_request(endpoint=self.ENDOINT, params={})
        singer.write_schema(
            self.STREAM_NAME, 
            self.schema, 
            "timestamp")
        
        for row in response:
            if row.get("timestamp") is not None:
                singer.write_record(self.STREAM_NAME, row)

        if "last_record" not in self.state:
            self.state["last_record"] = self.config.get("start_date", "")
        
        singer.write_state(self.state)

