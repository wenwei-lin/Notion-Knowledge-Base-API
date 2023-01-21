import unittest
import dotenv
import os
from datetime import datetime

from notion.database import PersonDatabase, SourceDatabase, PodcastDatabase
from notion.notion import NotionManager

dotenv.load_dotenv()


class PersonDatabaseTester(unittest.TestCase):
    def setUp(self):
        notion = NotionManager(os.getenv("NOTION_TOKEN"))
        self.person_database = PersonDatabase(notion, os.getenv("PERSON_DATABASE_ID"))

    def testAddPerson_01(self):
        person = {"name": "啊哈哈哈", "icon": "🧑\u200d🏫"}
        page_id = self.person_database.create_page(person)
        self.assertIsNotNone(page_id)
        self.assertTrue(self.person_database.delete_page(page_id))

    def testAddPerson_02(self):
        person = {
            "name": "嘿嘿嘿",
            "country_id": "cf1073dbe4634ee789c6833982fe3fdf",
            "icon": "🧑\u200d🏫",
        }
        page_id = self.person_database.create_page(person)
        self.assertIsNotNone(page_id)
        self.assertTrue(self.person_database.delete_page(page_id))

    def testQueryPerson_01(self):
        filter = {"filter": {"property": "Name", "rich_text": {"equals": "梁永安"}}}
        page_id = self.person_database.query_pages(filter)[0]["id"]
        self.assertEqual(page_id, "4990836d-1d34-46db-bf38-72421bac85d7")


class SourceDatabaseTester(unittest.TestCase):
    def setUp(self) -> None:
        notion = NotionManager(os.getenv("NOTION_TOKEN"))
        self.source_database = SourceDatabase(notion, os.getenv("SOURCE_DATABASE_ID"))

    def testAddSource_01(self):
        data = {
            "title": "Psychology",
            "type": "Book",
            "language": "English",
            "icon": "📘",
            "description": "Peter Gray's evolutionary perspective and emphasis on critical thinking have made his rigorous yet accessible introduction to psychology a widely respected classroom favorite, edition after edition. Now thoroughly revised, with the help of new co-author David Bjorklund, This text invites and stimulates students to investigate the big ideas in psychological science",
            "published": "2021-05-11",
        }
        page_id = self.source_database.create_page(data)
        self.assertIsNotNone(page_id)
        self.assertTrue(self.source_database.delete_page(page_id))

class PodcastDatabaseTester(unittest.TestCase):
    def setUp(self) -> None:
        notion = NotionManager(os.getenv("NOTION_TOKEN"))
        self.podcast_database = PodcastDatabase(notion, os.getenv('PODCAST_DATABASE_ID'))
    
    def testAddPodcast(self):
        data = {
            "title": """你的“报复性熬夜”，也许能创造更多价值""",
            "author": ["4990836d1d3446dbbf3872421bac85d7"],
            "duration": 47,
            "series": "梁永安的播客",
            "source_id": "00fa6eeeb1404ffba814c4776be86f82"
        }
        page_id = self.podcast_database.create_page(data)
        self.assertIsNotNone(page_id)
        self.assertTrue(self.podcast_database.delete_page(page_id))


if __name__ == "__main__":
    unittest.main()
