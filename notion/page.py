from notion.property import NotionProperty


class NotionPage:
    def __init__(
        self, database_id, properties: list, cover_url="", icon_emoji="", icon_url=""
    ):
        assert (
            len(properties) > 0
        ), "Notion Page should contain at least one property(Title)."
        self.database_id = database_id
        self.cover_url = cover_url
        self.icon_emoji = icon_emoji
        self.icon_url = icon_url
        self.properties = properties

    def _format_cover(self):
        cover = None
        if self.cover_url:
            cover = {"cover": {"external": {"url": self.cover_url}}}

        return cover

    def _format_icon(self):
        icon = None
        if self.icon_url:
            icon = {"icon": {"external": {"url": self.icon_url}}}
        elif self.icon_emoji:
            icon = {"icon": {"emoji": self.icon_emoji}}

        return icon

    def _format_properties(self):
        properties = {}
        for property_object in self.properties:
            assert isinstance(property_object, NotionProperty)
            property_dict = property_object.get_dict()
            if property_dict:
                properties.update(property_dict)

        return properties

    def format_page_to_notion(self):
        properties = self._format_properties()
        cover = self._format_cover()
        icon = self._format_icon()

        page_object = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
        }

        if cover:
            page_object.update(cover)
        if icon:
            page_object.update(icon)

        return page_object
