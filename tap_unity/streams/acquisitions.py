from tap_unity.streams.base import UnityBase
import singer

from tap_unity.utils import SchemaNotSetError


class AcquisitionsStream(UnityBase):
    STREAM_NAME = "acquisitions"

    def make_request(self, endpoint=None, params=None):
        return self.unity_client.make_acquisitions_request()
        
