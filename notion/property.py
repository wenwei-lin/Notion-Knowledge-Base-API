from abc import ABC, abstractmethod

class NotionProperty(ABC):
    def __init__(self, notion_column_name, value='') -> None:
        self.name = notion_column_name
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
        return {
            self.name: {
                "Title": [
                    {
                        "text": {
                            "content": self.value
                        }
                    }
                ]
            }
        }

