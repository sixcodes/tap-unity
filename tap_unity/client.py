from typing import Dict, List
from datetime import timedelta, datetime

import requests


class UnityClient:

    def __init__(self, config):
        organization_id = config.get("organization_id")
        
        self.http_session = requests.Session()
        self.base_url = f"https://stats.unityads.unity3d.com/organizations/{organization_id}/reports/acquisitions"

        self.http_session.headers.update({"Authorization": "Bearer " + config.get("auth_token")})

    
    def parse_csv_body(self, csv_body: str) -> list:
        splited_body = csv_body.split("\n")
        header = [attr.replace("\ufeff", "").replace(" ", "_") for attr in splited_body[0].split(",")]

        parsed_body = []

        for row in splited_body[1:]:
            row_splited = row.split(",")
            parsed_row = {}
            for i, value in enumerate(row_splited):
                if value == "":
                    parsed_row[header[i]] = None
                else: 
                    parsed_row[header[i]] = value
            parsed_body.append(parsed_row)

        return parsed_body
        

    def make_request(self) -> List[Dict[str, str]]:
        end = datetime.today()
        start = end - timedelta(days=1)

        query_params = {
            "start": start,
            "end": end,
            "splitBy": "store,country",
            "fields": "timestamp,target,creativePack,campaign,country,starts,views,clicks,installs,spend",
        }

        response = self.http_session.get(self.base_url, params=query_params)
        parsed = self.parse_csv_body(response.content.decode("utf-8"))
        return parsed
