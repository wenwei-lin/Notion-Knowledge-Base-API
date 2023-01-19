import requests
import json
import logging
log = logging.getLogger(__name__)

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

        log.info("Create a NotionManager object.")

    def create(self, payload: dict):
        endpoint = "https://api.notion.com/v1/pages"

        log.info(f"Send a HTTP request to {endpoint} for creating a page. Payload is: {payload}")
        response = requests.post(
            endpoint, json.dumps(payload), headers=self.header
        ).json()
        log.info(f'Receive HTTP response from {endpoint}: {response}')
        
        if response["object"] == "error":
            raise NotionAPIException(
                f"Response {response['status']}: {response['code']}. {response['message']}"
            )

        return response

    def update(self, page_id, payload):
        endpoint = f"https://api.notion.com/v1/pages/{page_id}"

        log.info(f"Send a HTTP request to {endpoint} for updating a page. Payload is: {payload}")
        response = requests.patch(
            endpoint, json.dumps(payload), headers=self.header
        ).json()
        log.info(f'Receive HTTP response from {endpoint}: {response}')

        return response

    def delete(self, page_id):
        endpoint = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"archived": True}

        log.info(f"Send a HTTP request to {endpoint} for deleting a page. Payload is: {payload}")
        response = requests.patch(endpoint, json.dumps(payload), headers=self.header).json()
        log.info(f'Receive HTTP response from {endpoint}: {response}')

        return response

    def query(self, database_id, payload):
        endpoint = f"https://api.notion.com/v1/databases/{database_id}/query"

        log.info(f"Send a HTTP request to {endpoint} for query pages. Payload is: {payload}")
        response = requests.post(endpoint, json.dumps(payload), headers=self.header).json()
        log.info(f'Receive HTTP response from {endpoint}: {response}')

        if response["object"] == "error":
            raise NotionAPIException(
                f"Response {response['status']}: {response['code']}. {response['message']}"
            )

        return response['results']
