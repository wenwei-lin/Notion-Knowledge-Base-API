from abc import ABC, abstractmethod
import logging

from notion.notion import NotionManager
from notion.property import *
from notion.page import NotionPage

log = logging.getLogger(__name__)


class PersistenceLayer(ABC):
    def __init__(self, notion: NotionManager, database_id):
        self.notion = notion
        self.database_id = database_id

        log.info(
            f"Create a {self.__class__.__name__} object: database_id={database_id}"
        )

    @abstractmethod
    def _turn_to_notion_property(self, property_name, property_value) -> NotionProperty:
        raise NotImplementedError(
            "PersistenceLayer class should implement the _turn_to_notion_property method."
        )

    def _turn_to_notion_property_list(self, data: dict):
        log.info(f"Format data into Notion property values: {data}")

        properties = []

        for property_name, property_value in data.items():
            property_object = self._turn_to_notion_property(
                property_name, property_value
            )
            if property_object:
                properties.append(property_object)

        log.info(f"Properties after formatting: {properties}")

        return properties

    def create_page(self, data: dict):
        log.info(f"Create a page in Notion for: {data}")

        properties = self._turn_to_notion_property_list(data)
        page_object = NotionPage(
            self.database_id,
            properties,
            cover_url=data.get("cover_url"),
            icon_emoji=data.get("icon_emoji"),
            icon_url=data.get("icon_url"),
        )
        response = self.notion.create(page_object.get_notion_page_object())

        log.info("Page created.")

        return response

    def update_page_property(self, page_id, data: dict):
        log.info(f"Update page {page_id} into: {data}")

        property_list = self._turn_to_notion_property_list()
        properties = {}
        for property_object in property_list:
            assert isinstance(property_object, NotionProperty)
            property_dict = property_object.get_dict()
            if property_dict:
                properties.update(property_dict)

        response = self.notion.update(page_id, {"properties": properties})
        log.info("Page updated.")

        return response

    def delete_page(self, page_id):
        log.info(f"Delete page: {page_id}")

        self.notion.delete(page_id)
        log.info("Page deleted.")

        return True

    def query_pages(self, filter):
        log.info(f"Query database({self.database_id}) for: {filter}")

        response = self.notion.query(self.database_id, payload=filter)
        log.info("Query successfully.")

        return response


class PersonDatabase(PersistenceLayer):
    def _turn_to_notion_property(self, property_name, property_value) -> NotionProperty:
        formats = {
            "name": Title("Name", property_value),
            "description": RichText("Description", property_value),
            "original_name": RichText("Original Name", property_value),
            "country_id": Relation("Country", [property_value]),
        }
        return formats.get(property_name)


class SourceDatabase(PersistenceLayer):
    def _turn_to_notion_property(self, property_name, property_value) -> NotionProperty:
        formats = {
            "title": Title("Title", property_value),
            "type": Select("Type", property_value),
            "description": RichText("Description", property_value),
            "language": Select("Language", property_value),
            "published": Date("Published", property_value),
        }

        return formats.get(property_name)


class PodcastDatabase(PersistenceLayer):
    def _turn_to_notion_property(self, property_name, property_value) -> NotionProperty:
        formats = {
            "title": Title("Title", property_value),
            "author": Relation("Author", property_value),
            "duration": Number("Duration", property_value),
            "series": Select("Series", property_value),
            "source_id": Relation("Source", [property_value]),
        }
        return formats.get(property_name)


class BookDatabase(PersistenceLayer):
    def _turn_to_notion_property(self, property_name, property_value) -> NotionProperty:
        formats = {
            "title": Title("Title", property_value),
            "original_title": RichText("Original Title", property_value),
            "author": Relation("Author", property_value),
            "translator": Relation("Translator", property_value),
            "pages": Number("Pages", property_value),
            "publisher": Select("Publisher", property_value),
            "isbn": RichText("ISBN", property_value),
            "douban": URL("Douban", property_value),
            "source_id": Relation("Source", [property_value]),
        }
