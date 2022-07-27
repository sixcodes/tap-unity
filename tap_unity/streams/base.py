

class UnityBase:
    """
    Stram base class
    """

    # BASE_URL = ""
    STREAM_NAME = ""

    def __init__(self, state, unity_client):
        self.state = state
        self.unity_client = unity_client

    def set_schema(self, schema):
        self.schema = schema

    def do_sync(self):
        """
        Sync data from tap source
        """
        raise NotImplementedError()
