

class UnityBase:
    """
    Stram base class
    """

    STREAM_NAME = ""

    def __init__(self, config, state, unity_client):
        self.config = config
        self.state = state
        self.unity_client = unity_client

    def set_schema(self, schema):
        self.schema = schema

    def do_sync(self):
        """
        Sync data from tap source
        """
        raise NotImplementedError()
