from typing import Dict
import singer
from tap_unity.client import UnityClient
from tap_unity.utils import SchemaNotSetError


LOGGER = singer.get_logger()

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

        self.bookmark_date = singer.get_bookmark(
            state=state, 
            tap_stream_id=self.STREAM_NAME, 
            key="last_record"
        )

        if not self.bookmark_date:
            self.bookmark_date = self.state.get(
                "last_record", 
                self.config.get("start_date", "")
            )

    
    def set_schema(self, schema):
        self.schema = schema


    def make_request(self, endpoint=None, params=None):
        if endpoint is None:
            endpoint = self.ENDOINT

        if params is None:
            params = {}
        
        return self.unity_client.make_request(endpoint=endpoint, params=params)


    def sync(self):
        singer.write_schema(self.STREAM_NAME,  self.schema, "timestamp")
        self.do_sync()
        singer.write_state(self.state)


    def do_sync(self):
        """
        Sync data from tap source
        """
        if not self.schema:
            raise SchemaNotSetError()

        response = self.make_request()
       
        new_bookmark_date = self.bookmark_date
        LOGGER.info(f"Start bookmark: {new_bookmark_date}")
        with singer.metrics.Counter("record_count", {"endpoint": self.STREAM_NAME}) as counter:
            for row in response:
                if row.get("timestamp") is not None:
                    new_bookmark_date = max(new_bookmark_date, row["timestamp"])
                    singer.write_message(singer.RecordMessage(
                        stream=self.STREAM_NAME,
                        record=row
                    ))

            counter.increment()
        self.state = singer.write_bookmark(self.state, self.STREAM_NAME, "last_record", new_bookmark_date)
        LOGGER.warning(f"state: {self.state}")

