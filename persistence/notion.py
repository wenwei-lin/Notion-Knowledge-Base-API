import requests
import json


class NotionAPIException(Exception):
    pass


class NotionManager:
    def __init__(self, token):
        self.header = {
            "Accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def create(self, payload: dict):
        endpoint = "https://api.notion.com/v1/pages"
        response = requests.post(
            endpoint, json.dumps(payload), headers=self.header
        ).json()
        
        if response["object"] == "error":
            raise NotionAPIException(
                f"Response {response['status']}: {response['code']}. {response['message']}"
            )

        return response

    def update(self, page_id, payload):
        endpoint = f"https://api.notion.com/v1/pages/{page_id}"
        response = requests.patch(
            endpoint, json.dumps(payload), headers=self.header
        ).json()

        return response

    def delete(self, page_id):
        endpoint = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"archived": True}
        response = requests.patch(endpoint, json.dumps(payload), headers=self.header).json()

        return response

    def query(self, database_id, payload):
        endpoint = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.post(endpoint, json.dumps(payload), headers=self.header).json()

        if response["object"] == "error":
            raise NotionAPIException(
                f"Response {response['status']}: {response['code']}. {response['message']}"
            )

        return response['results']
