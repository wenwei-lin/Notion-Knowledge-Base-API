import pytest

from notion.property import *


class TestTitle:
    def test_value_is_empty(self):
        assert Title("Title").get_dict() is None
        assert Title("Title", "").get_dict() is None
        assert Title("Title", None).get_dict() is None

    def test_value_is_not_empty(self):
        assert Title("Title", "学会提问").get_dict() == {
            "Title": {"title": [{"text": {"content": "学会提问"}}]}
        }
        assert Title("Name", "梁永安").get_dict() == {
            "Name": {"title": [{"text": {"content": "梁永安"}}]}
        }
        assert Title("标题", "学会提问").get_dict() == {
            "标题": {"title": [{"text": {"content": "学会提问"}}]}
        }

    def test_value_is_invalid(self):
        with pytest.raises(AssertionError):
            Title("Title", 8).get_dict()


class TestRichText:
    def test_value_is_empty(self):
        assert RichText("Description").get_dict() is None
        assert RichText("Description", "").get_dict() is None
        assert RichText("Description", None).get_dict() is None

    def test_value_is_not_empty(self):
        assert RichText("Description", "现代发展").get_dict() == {
            "Description": {
                "rich_text": [{"type": "text", "text": {"content": "现代发展"}}]
            }
        }
        assert RichText("Description", "现代发展 ").get_dict() == {
            "Description": {
                "rich_text": [{"type": "text", "text": {"content": "现代发展 "}}]
            }
        }
        assert RichText("描述", "现代发展").get_dict() == {
            "描述": {"rich_text": [{"type": "text", "text": {"content": "现代发展"}}]}
        }

    def test_value_is_invalid(self):
        with pytest.raises(AssertionError):
            RichText("Page", 9.0).get_dict()


class TestNumber:
    def test_value_is_empty(self):
        assert Number("Page").get_dict() is None
        assert Number("Page", "").get_dict() is None
        assert Number("Page", None).get_dict() is None

    def test_value_is_not_empty(self):
        assert Number("Page", 9).get_dict() == {"Page": {"number": 9}}
        assert Number("Page", 9.9).get_dict() == {"Page": {"number": 9.9}}

    def test_value_is_invalid(self):
        with pytest.raises(AssertionError):
            Number("Page", "9.0").get_dict()


class TestSelect:
    def test_value_is_empty(self):
        assert Select("Type").get_dict() is None
        assert Select("Type", "").get_dict() is None
        assert Select("Type", None).get_dict() is None

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestStatus:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestMultiSelect:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestDate:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestRelation:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestFiles:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestCheckbox:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestURL:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestEmail:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass


class TestPhoneNumber:
    def test_value_is_empty(self):
        pass

    def test_value_is_not_empty(self):
        pass

    def test_value_is_invalid(self):
        pass
