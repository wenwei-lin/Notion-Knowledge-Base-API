import os
from abc import ABC, abstractmethod
import json

from persistence.notion import NotionManager


class PersistenceLayer:
    def __init__(self, notion: NotionManager, database_id):
        self.notion = notion
        self.database_id = database_id

    @abstractmethod
    def _format_one_property(self, name, value):
        raise NotImplementedError(
            "PersistenceLayer class should implement the _format_one_property method."
        )

    def _format_properties(self, data: dict):
        properties = dict()

        for property_name in data.keys():
            property = self._format_one_property(property_name, data[property_name])
            if property:
                properties.update(property)

        return properties

    def create_page(self, data):
        properties = self._format_properties(data)

        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }

        if data.get("icon"):
            payload["icon"] = {"emoji": data["icon"]}

        if data.get("icon_url"):
            payload["icon"] = {"external": {"url": data["icon_url"]}}

        if data.get("cover"):
            payload["cover"] = {"external": {"url": data["cover"]}}

        response = self.notion.create(payload)
        page_id = response["id"]

        return page_id

    def update_page_property(self, page_id, data: dict):
        properties = self._format_properties(data)
        payload = {"properties": properties}

        response = self.notion.update(page_id, payload)
        page_id = response["id"]

        return page_id

    def delete_page(self, page_id):
        response = self.notion.delete(page_id)
        return True

    def query_pages(self, filter):
        response = self.notion.query(self.database_id, payload=filter)
        return response


class PersonDatabase(PersistenceLayer):
    def _format_one_property(self, name, value):
        formats = {
            "name": {"Name": {"title": [{"text": {"content": value}}]}},
            "original_name": {
                "Original Name": {"rich_text": [{"type": "text", "content": value}]}
            },
            "country_id": {"Country": {"relation": [{"id": value}]}},
        }
        return formats.get(name, None)
