import pytz
from typing import Dict, List
from datetime import timedelta, datetime
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

    
    def __get_start_end(self):
        start = date_parser.parse(self.last_record) - timedelta(days=1)
        end = min(
            (datetime.today() - timedelta(1)).replace(tzinfo=pytz.UTC), 
            (date_parser.parse(self.last_record) + timedelta(30)).replace(tzinfo=pytz.UTC)
        )
        return start, end
    
    
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
        start, end = self.__get_start_end()        
        query_params = {
            "start": start,
            "end": end,
            "scale": self.config.get("granularity"),
            "adTypes":  "video,playable",
            "stores": "apple,google",
            "splitBy": self.config.get("split_by", "store,country,campaignSet,creativePack,adType,campaign,target,sourceAppId,platform,reachExtension,skadConversionValue"),
        }

        if self.config.get("fields"):
            query_params.update({"fields": self.config.get("fields"),})
        else:
            all_fields = "timestamp,campaignSet,creativePack,adType,campaign,target,sourceAppId,store,country,platform,starts,views,clicks,installs,spend,skadInstalls,skadCpi,skadConversion"
            query_params.update({"fields": all_fields })
        url = self.__build_resouce_url("acquisitions")
        print(f"---------URL: {url}, query: {query_params}")
        response = self.http_session.get(url, params=query_params)
        parsed = self.parse_csv_body(response.content.decode("utf-8"))
        return parsed
