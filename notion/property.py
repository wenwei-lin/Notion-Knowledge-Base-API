from abc import ABC, abstractmethod
import numbers


class NotionProperty(ABC):
    def __init__(self, notion_column_name, value="") -> None:
        self.notion_column_name = notion_column_name
        self.value = value

    def set_value(self, value):
        self.value = value

    @abstractmethod
    def _format_to_notion_property_value(self) -> dict:
        raise NotImplementedError(
            "Classes inherit Property should implement a _format_to_notion_property_values() method."
        )

    def get_dict(self):
        if self.value:
            return self._format_to_notion_property_value()
        else:
            return None


class Title(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, str), "The value of Title should be a str."
        return {self.notion_column_name: {"title": [{"text": {"content": self.value}}]}}


class RichText(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, str), "The value of RichText should be a str."
        value = self.value[0:2000] if len(self.value) > 2000 else self.value
        return {
            self.notion_column_name: {
                "rich_text": [{"type": "text", "text": {"content": value}}]
            }
        }


class Number(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(
            self.value, numbers.Number
        ), "The value of Number should be a number."
        return {self.notion_column_name: {"number": self.value}}


class Select(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, str), "The value of Select should be a str."
        return {self.notion_column_name: {"select": {"name": self.value}}}


class Status(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, str), "The value of Status should be a str."
        return {self.notion_column_name: {"Status": {"name": self.value}}}


class MultiSelect(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(
            self.value, list
        ), "The value of MultiSelect should be a list."
        return {
            self.notion_column_name: {
                "multi_select": [{"name": name} for name in self.value]
            }
        }


class Date(NotionProperty):
    def __init__(self, notion_column_name, start="", end="", timezone="") -> None:
        super().__init__(notion_column_name, start)
        self.end = end
        self.timezone = timezone

    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, str), "The start of Date should be a str."
        property_dict = {self.notion_column_name: {"date": {"start": self.value}}}

        if self.end:
            assert isinstance(self.end, str), "The end of Date should be a str."
            property_dict[self.notion_column_name]["date"].update({"end": self.end})
        if self.timezone:
            assert isinstance(
                self.timezone, str
            ), "The timezone of Date should be a str."
            property_dict[self.notion_column_name]["date"].update(
                {"timezone": self.timezone}
            )

        return property_dict


class Relation(NotionProperty):
    """
    The value of Relation object should be a list of Notion page id.
    """

    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, list), "The value of Relation should be a list."
        return {
            self.notion_column_name: {"relation": [{"id": id} for id in self.value]}
        }


class Files(NotionProperty):
    """
    The value of Files object should be a list of {name: "", url: ""}
    """

    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, list), "The value of Files should be a list."
        return {
            self.notion_column_name: {
                "files": [
                    {
                        "type": "external",
                        "name": file["name"],
                        "external": {"url": file["url"]},
                    }
                    for file in self.value
                ]
            }
        }


class Checkbox(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, bool), "The values of Checkbox should be a bool."
        return {self.notion_column_name: {"checkbox": self.value}}


class URL(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, str), "The value of URL should be a str."
        return {self.notion_column_name: {"url": self.value}}


class Email(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, str), "The value of URL should be a str."
        return {self.notion_column_name: {"email": self.value}}


class PhoneNumber(NotionProperty):
    def _format_to_notion_property_value(self) -> dict:
        assert isinstance(self.value, str), "The value of PhoneNumber should be a str."
        return {self.notion_column_name: {"phone_number": self.value}}
