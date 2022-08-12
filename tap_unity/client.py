from typing import Dict, List
from datetime import timedelta
from dateutil import parser as date_parser

import requests


class UnityClient:

    BASE_URL = "https://stats.unityads.unity3d.com"

    def __init__(self, config: Dict[str, str], state: Dict[str, str]):
        self.config = config
        self.last_record: str = state.get("last_record", config.get("start_date", ""))
        self.organization_id: str = self.config.get("organization_id")
        
        self.http_session = requests.Session()
        self.http_session.headers.update({"Authorization": "Bearer " + config.get("auth_token")})


    def __build_resouce_url(self, resource_name: str) -> str:
        return f"{self.BASE_URL}/organizations/{self.organization_id}/reports/{resource_name}"
    
    
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
                    parsed_row[header[i]] = value.replace("\"", "")
            parsed_body.append(parsed_row)

        return parsed_body

    
    def make_request(self, endpoint: str, params: Dict[str, str]) -> List[Dict[str, str]]:
        response = self.http_session.get(f"{self.BASE_URL}/{endpoint}", params=params)
        parsed = self.parse_csv_body(response.content.decode("utf-8"))
        return parsed
        

    def make_acquisitions_request(self) -> List[Dict[str, str]]:
        end = date_parser.parse(self.last_record)
        start = end - timedelta(days=1)

        query_params = {
            "start": start,
            "end": end,
            "splitBy": self.config.get("split_by", "country,store"),
        }

        if self.config.get("fields"):
            query_params.update({"fields": self.config.get("fields"),})

        url = self.__build_resouce_url("acquisitions")
        response = self.http_session.get(url, params=query_params)
        parsed = self.parse_csv_body(response.content.decode("utf-8"))
        return parsed
