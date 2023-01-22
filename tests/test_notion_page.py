import pytest
from notion.property import *
from notion.page import NotionPage


class TestNotionPage:
    def test_page_with_no_property(self):
        with pytest.raises(AssertionError):
            NotionPage("aaa", [])

    def test_page_with_only_properties(self):
        page = NotionPage(
            database_id="12345",
            properties=[
                Title("Title", "学会提问"),
                Relation("Author", ["author_id"]),
                RichText("Description", ""),
                Select("Type", ""),
            ],
        )
        assert page.format_page_to_notion() == {
            "parent": {"database_id": "12345"},
            "properties": {
                "Title": {"title": [{"text": {"content": "学会提问"}}]},
                "Author": {"relation": [{"id": "author_id"}]},
            },
        }

    def test_page_with_cover(self):
        page = NotionPage(
            database_id="12345",
            cover_url="cover_url",
            properties=[
                Title("Title", "学会提问"),
                Relation("Author", ["author_id"]),
                RichText("Description", ""),
                Select("Type", ""),
            ],
        )
        assert page.format_page_to_notion() == {
            "parent": {"database_id": "12345"},
            "cover": {"external": {"url": "cover_url"}},
            "properties": {
                "Title": {"title": [{"text": {"content": "学会提问"}}]},
                "Author": {"relation": [{"id": "author_id"}]},
            },
        }

    def test_page_with_emoji_icon(self):
        page = NotionPage(
            database_id="12345",
            icon_emoji="🍉",
            properties=[
                Title("Title", "学会提问"),
                Relation("Author", ["author_id"]),
                RichText("Description", ""),
                Select("Type", ""),
            ],
        )
        assert page.format_page_to_notion() == {
            "parent": {"database_id": "12345"},
            "icon": {"emoji": "🍉"},
            "properties": {
                "Title": {"title": [{"text": {"content": "学会提问"}}]},
                "Author": {"relation": [{"id": "author_id"}]},
            },
        }

    def test_page_with_url_icon(self):
        page = NotionPage(
            database_id="12345",
            icon_emoji="🍉",
            properties=[
                Title("Title", "学会提问"),
                Relation("Author", ["author_id"]),
                RichText("Description", ""),
                Select("Type", ""),
            ],
        )
        assert page.format_page_to_notion() == {
            "parent": {"database_id": "12345"},
            "icon": {"emoji": "🍉"},
            "properties": {
                "Title": {"title": [{"text": {"content": "学会提问"}}]},
                "Author": {"relation": [{"id": "author_id"}]},
            },
        }

    def test_page_with_both_emoji_and_url_icon(self):
        page = NotionPage(
            database_id="12345",
            icon_emoji="🍉",
            icon_url="icon_url",
            properties=[
                Title("Title", "学会提问"),
                Relation("Author", ["author_id"]),
                RichText("Description", ""),
                Select("Type", ""),
            ],
        )
        assert page.format_page_to_notion() == {
            "parent": {"database_id": "12345"},
            "icon": {"external": {"url": "icon_url"}},
            "properties": {
                "Title": {"title": [{"text": {"content": "学会提问"}}]},
                "Author": {"relation": [{"id": "author_id"}]},
            },
        }

    def test_page_with_both_cover_and_emoji(self):
        page = NotionPage(
            database_id="12345",
            icon_url="icon_url",
            cover_url="cover_url",
            properties=[
                Title("Title", "学会提问"),
                Relation("Author", ["author_id"]),
                RichText("Description", ""),
                Select("Type", ""),
            ],
        )
        assert page.format_page_to_notion() == {
            "parent": {"database_id": "12345"},
            "icon": {"external": {"url": "icon_url"}},
            "cover": {"external": {"url": "cover_url"}},
            "properties": {
                "Title": {"title": [{"text": {"content": "学会提问"}}]},
                "Author": {"relation": [{"id": "author_id"}]},
            },
        }
