from abc import ABC, abstractmethod
import logging

from persistence.notion import NotionManager

log = logging.getLogger(__name__)


class PersistenceLayer(ABC):
    def __init__(self, notion: NotionManager, database_id):
        self.notion = notion
        self.database_id = database_id

        log.info(
            f"Create a {self.__class__.__name__} object: database_id={database_id}"
        )

    @abstractmethod
    def _format_one_property(self, name, value):
        raise NotImplementedError(
            "PersistenceLayer class should implement the _format_one_property method."
        )

    def _format_properties(self, data: dict):
        log.info(f"Format data into Notion property values: {data}")

        properties = dict()

        for property_name in data.keys():
            # Invoke _format_one_property() method only if property value is not empty
            property = (
                self._format_one_property(property_name, data[property_name])
                if data[property_name]
                else None
            )
            if property:
                properties.update(property)
        log.info(f"Properties after formatting: {properties}")
        
        return properties

    def _construct_page_object(self, data: dict):
        log.info(f"Format a Notion page object for: {data}")

        properties = self._format_properties(data)

        page_object = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }

        # Add optional attributes
        if data.get("icon"):
            page_object["icon"] = {"emoji": data["icon"]}
        if data.get("icon_url"):
            page_object["icon"] = {"external": {"url": data["icon_url"]}}
        if data.get("cover"):
            page_object["cover"] = {"external": {"url": data["cover"]}}
        log.info(f"Construct a Notion page object: {page_object}")

        return page_object

    def create_page(self, data):
        log.info(f"Create a page in Notion for: {data}")

        page_object = self._construct_page_object()
        response = self.notion.create(page_object)
        log.info("Page created.")

        return response

    def update_page_property(self, page_id, data: dict):
        log.info(f"Update page {page_id} into: {data}")

        properties = self._format_properties(data)
        payload = {"properties": properties}
        response = self.notion.update(page_id, payload)
        log.info("Page updated.")

        return response

    def delete_page(self, page_id):
        log.info(f"Delete page: {page_id}")

        self.notion.delete(page_id)
        log.info("Page deleted.")

        return True

    def query_pages(self, filter):
        log.info(f'Query database({self.database_id}) for: {filter}')

        response = self.notion.query(self.database_id, payload=filter)
        log.info('Query successfully.')

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


class SourceDatabase(PersistenceLayer):
    def _format_one_property(self, name, value):
        formats = {
            "title": {"Title": {"title": [{"text": {"content": value}}]}},
            "type": {"Type": {"select": {"name": value}}},
            "description": {
                "Description": {
                    "rich_text": [{"type": "text", "text": {"content": value}}]
                }
            },
            "language": {"Language": {"select": {"name": value}}},
            "published": {"Published": {"date": {"start": value}}},
        }
        return formats.get(name)


class PodcastDatabase(PersistenceLayer):
    def _format_one_property(self, name, value):
        if isinstance(value, list):
            value = [{"id": id} for id in value]

        formats = {
            "title": {"Title": {"title": [{"text": {"content": value}}]}},
            "author": {"Author": {"relation": value}},
            "duration": {"Duration": {"number": value}},
            "series": {"Series": {"select": {"name": value}}},
            "source_id": {"Source": {"relation": [{"id": value}]}},
        }

        return formats.get(name)
