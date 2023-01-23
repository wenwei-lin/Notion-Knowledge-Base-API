import dotenv
import os
from datetime import datetime

from notion.database import PersonDatabase, SourceDatabase, PodcastDatabase
from notion.notion import NotionManager
from logic.commands import GetSourceIDCommand, GetPersonIDCommand, CreateSourceCommand

dotenv.load_dotenv()
notion = NotionManager(os.getenv("NOTION_TOKEN"))


class TestGetSourceIDCommand:
    def setup_method(self, test_method):
        source_database = SourceDatabase(notion, os.getenv("SOURCE_DATABASE_ID"))
        self.command = GetSourceIDCommand(source_database)

    def test_source_in_database(self):
        source_id = self.command.execute(
            {
                "title": "Recovering from Emotional Immature Parents",
            }
        )
        assert source_id == "590687e0-f796-4b9b-b3de-d0004c0ffe54"

        source_id = self.command.execute(
            {
                "title": "下班后开始新的一天",
            }
        )
        assert source_id == "802fa164-d5a8-4611-84a8-e432354fbf22"

    def test_source_not_in_database(self):
        source_id = self.command.execute(
            {
                "title": "1.2 总序｜舶来的“年轻学科”如何适应中国的土壤？",
                "description": "作为引领课程开场的总序，来自北京大学社会学系的周飞舟教授和渠敬东教授，在本讲中将以对谈的形式，整体性地讲述“什么是社会学”，以及如何用社会学的眼光来理解中国问题。在某种意义上，社会学关切的并不仅仅是当下问题，更有“通古今之变”的宏大视野，让我们通过社会学，找到过去和未来之间的一个连接点，从而搭建起观察中国的另一种眼光。",
                "type": "Podcast",
                "language": "Chinese",
                "published": "2022-04-18",
                "icon_url": "http://zdimg.lifeweek.com.cn/bg/20220418/1650283872461prqui.jpg",
            }
        )
        assert source_id is not None
        notion.delete(source_id)


class TestGetPersonIDCommand:
    def setup_method(self, test_method):
        person_database = PersonDatabase(notion, os.getenv("PERSON_DATABASE_ID"))
        self.command = GetPersonIDCommand(person_database)

    def test_person_in_database(self):
        assert (
            self.command.execute({"name": "梁永安"})
            == "4990836d-1d34-46db-bf38-72421bac85d7"
        )
        assert (
            self.command.execute({"name": "斯图尔特 · 基利"})
            == "123fe817-880d-4205-a3a8-fcedef0ce36f"
        )


class TestCreateSourceCommand:
    def setup_method(self, test_method):
        person_database = PersonDatabase(notion, os.getenv("PERSON_DATABASE_ID"))
        source_database = SourceDatabase(notion, os.getenv("SOURCE_DATABASE_ID"))
        podcast_database = PodcastDatabase(notion, os.getenv("PODCAST_DATABASE_ID"))
        get_source_id_command = GetSourceIDCommand(source_database)
        get_person_id_command = GetPersonIDCommand(person_database)
        self.command = CreateSourceCommand(
            get_source_id_command, get_person_id_command, podcast_database
        )

    def testCreatePodcast(self):
        assert (
            self.command.execute(
                {
                    "title": "1.2 总序｜舶来的“年轻学科”如何适应中国的土壤？",
                    "description": "作为引领课程开场的总序，来自北京大学社会学系的周飞舟教授和渠敬东教授，在本讲中将以对谈的形式，整体性地讲述“什么是社会学”，以及如何用社会学的眼光来理解中国问题。在某种意义上，社会学关切的并不仅仅是当下问题，更有“通古今之变”的宏大视野，让我们通过社会学，找到过去和未来之间的一个连接点，从而搭建起观察中国的另一种眼光。",
                    "type": "Podcast",
                    "published": "2022-04-18",
                    "duration": 5,
                    "language": "Chinese",
                    "series": "社会学看中国",
                    "icon_url": "http://zdimg.lifeweek.com.cn/bg/20220418/1650283872461prqui.jpg",
                    "author": [
                        {
                            "name": "渠敬东",
                            "icon_url": "http://zdimg.lifeweek.com.cn/bg/20201029/1603973376905sxxkk.png",
                        },
                        {
                            "name": "周飞舟",
                            "icon_url": "http://zdimg.lifeweek.com.cn/bg/20220416/1650117821294acimg.png",
                        },
                    ],
                }
            )
            is not None
        )
