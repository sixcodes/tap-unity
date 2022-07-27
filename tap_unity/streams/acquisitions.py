from tap_unity.streams.base import UnityBase
import singer

from tap_unity.utils import SchemaNotSetError


class AcquisitionsStream(UnityBase):
    STREAM_NAME = "acquisitions"

    def do_sync(self):
        if not self.schema:
            raise SchemaNotSetError()

        response = self.unity_client.make_request()
        singer.write_schema(
            self.STREAM_NAME, 
            self.schema, 
            "timestamp")
        
        for row in response:
            if row.get("timestamp") is not None:
                singer.write_record(self.STREAM_NAME, row)

        singer.write_state(self.state)
