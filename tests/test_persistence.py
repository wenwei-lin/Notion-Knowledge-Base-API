import unittest
import dotenv
import os

from persistence.database import PersonDatabase
from persistence.notion import NotionManager

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
        self.assertEquals(page_id, "4990836d-1d34-46db-bf38-72421bac85d7")


if __name__ == "__main__":
    unittest.main()
