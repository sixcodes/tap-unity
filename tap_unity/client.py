import requests

class UnityClient:

    def __init__(self, config):
        organization_id = config.get("organization_id")
        
        self.http_session = requests.Session()
        self.base_url = f"https://stats.unityads.unity3d.com/organizations/{organization_id}/reports/acquisitions"

        self.http_session.headers.update({"Authorization": "Bearer " + config.get("bearer")})

    
    def make_request(self) -> str:
        query_params = {
            "start": "2021-06-01T00:00:00.000Z",
            "end": "2021-12-31T00:00:00.000Z",
            "splitBy": "store,country",
            "fields": "starts,timestamp,campaign"
        }

        response = self.http_session.get(self.base_url, params=query_params)
        return response.content.decode("utf-8")
