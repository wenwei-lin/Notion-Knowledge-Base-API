from extractor.douban import DoubanBookExtractor
import dotenv
import os
from datetime import datetime

from notion.database import PersonDatabase, SourceDatabase, BookDatabase
from notion.notion import NotionManager
from logic.commands import GetSourceIDCommand, GetPersonIDCommand, CreateSourceCommand

dotenv.load_dotenv()
notion = NotionManager(os.getenv("NOTION_TOKEN"))


class TestDoubanBookExtractor:
    def setup_method(self, test_method):
        self.extractor = DoubanBookExtractor()

        person_database = PersonDatabase(notion, os.getenv("PERSON_DATABASE_ID"))
        source_database = SourceDatabase(notion, os.getenv("SOURCE_DATABASE_ID"))
        book_database = BookDatabase(notion, os.getenv("BOOK_DATABASE_ID"))
        get_source_id_command = GetSourceIDCommand(source_database)
        get_person_id_command = GetPersonIDCommand(person_database)
        self.command = CreateSourceCommand(
            get_source_id_command, get_person_id_command, book_database
        )

    def test_match(self):
        assert self.extractor.match("9787111680925")
        assert self.extractor.match("9787115564672")
        assert self.extractor.match("http://") == False

    def test_get_forwarding_url(self):
        assert (
            self.extractor._get_douban_url("9787111680925")
            == "https://book.douban.com/subject/35513147/"
        )
        assert (
            self.extractor._get_douban_url("9787115564672")
            == "https://book.douban.com/subject/35503571/"
        )
    
    def test_no_forwarding_url(self):
        assert(
            self.extractor._get_douban_url("9780593418239")
            == None
        )

    def test_extract_data(self):
        book_data = self.extractor.extract("9787521704693")
        page = self.command.execute(book_data)
        assert page["id"] is not None
