from abc import ABC, abstractmethod
import logging

from notion.database import (
    SourceDatabase,
    PersonDatabase,
    PodcastDatabase,
    BookDatabase,
    PersistenceLayer,
)
from extractor.zhongdu import ZhongduExtractor
from extractor.douban import DoubanBookExtractor

log = logging.getLogger(__name__)


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        raise NotImplementedError(
            "Classes inherit Command must implement a execute method"
        )


class GetSourceIDCommand(Command):
    def __init__(self, source_database: SourceDatabase):
        self.source_database = source_database
        log.info("Create a GetSourceIDCommand object.")

    def _query_by_title(self, data):
        log.info(f"Query source database for: {data}")

        title = data["title"]
        filter = {"filter": {"property": "Title", "rich_text": {"equals": title}}}
        pages = self.source_database.query_pages(filter)

        page = None
        if len(pages) > 0:
            page = pages[0]
            log.info("Find page in source database.")
        else:
            log.info("Cannot find source.")

        return page

    def _create_page(self, data):
        page = self.source_database.create_page(data)
        return page

    def execute(self, data):
        log.info(f"Execute GetSourceID Command for: {data}")

        page = self._query_by_title(data)
        if page is None:
            page = self._create_page(data)
        log.info(f"Get source id: {page['id']}")

        return page["id"]


class GetPersonIDCommand(Command):
    def __init__(self, person_database: PersonDatabase):
        self.person_database = person_database
        log.info("Create a GetPersonIDCommand object.")

    def _query_by_name(self, data):
        log.info(f"Query person database for: {data}")

        name = data["name"]
        filter = {"filter": {"property": "Name", "rich_text": {"equals": name}}}
        pages = self.person_database.query_pages(filter)

        page = None
        if len(pages) > 0:
            page = pages[0]
            log.info("Find page in person database.")
        else:
            log.info("Cannot find person.")

        return page

    def _create_page(self, data):
        page = self.person_database.create_page(data)
        return page

    def execute(self, data):
        log.info(f"Execute GetPersonID Command for: {data}")

        page = self._query_by_name(data)
        if page is None:
            page = self._create_page(data)
        log.info(f"Get person id: {page['id']}")

        return page["id"]


class GetPeopleIDListCommand(Command):
    def __init__(self, get_person_id_command: GetPersonIDCommand):
        self.get_person_id_command = get_person_id_command
        log.info("Create a GetPeopleIDListCommand object.")

    def execute(self, author_list):
        log.info(f"Get author id list for: {author_list}")
        author_id_list = [
            self.get_person_id_command.execute(author) for author in author_list
        ]
        log.info(f"Get author id list: {author_id_list}")

        return author_id_list


class CreateSourceCommand(Command):
    def __init__(
        self,
        get_source_id_command: GetSourceIDCommand,
        get_person_id_command: GetPersonIDCommand,
        database: PersistenceLayer,
    ):
        self.get_source_id_command = get_source_id_command
        self.get_people_id_list_command = GetPeopleIDListCommand(get_person_id_command)
        self.database = database
        log.info("Create a CreateSourceCommand object.")

    def _query_by_title(self, title):
        log.info(
            f"Query {self.database.__class__.__name__} database for: title={title}"
        )

        filter = {"filter": {"property": "Title", "rich_text": {"equals": title}}}
        pages = self.database.query_pages(filter)

        page = None
        if len(pages) > 0:
            page = pages[0]
            log.info(f"Find source.")
        else:
            log.info("Source didn't exist.")

        return page

    # TODO: Separate parse data
    def execute(self, data):
        log.info("Execute CreateSource command.")

        source_id = self.get_source_id_command.execute(data)
        author_id_list = self.get_people_id_list_command.execute(data["author"])
        # TODO: Refactor
        if data.get("translator"):
            translator_id_list = self.get_people_id_list_command.execute(
                data["translator"]
            )
            data["translator"] = translator_id_list
        data["source_id"] = source_id
        data["author"] = author_id_list

        page = self._query_by_title(data["title"])
        if page is None:
            page = self.database.create_page(data)
        log.info(f"{self.database.__class__.__name__} page created.")

        return page


class AddByURLCommand(Command):
    def __init__(self, source_database, person_database, podcast_database):
        self.source_database = source_database
        self.person_database = person_database
        self.podcast_database = podcast_database
        log.info("Create a AddByURLCommand object.")

    def _get_extractors(self):
        extractors = [
            ZhongduExtractor(),
        ]
        log.info(f"Get extractors: {extractors}")
        return extractors

    def _get_create_commands(self):
        get_source_id_command = GetSourceIDCommand(self.source_database)
        get_person_id_command = GetPersonIDCommand(self.person_database)
        create_commands = {
            "Podcast": CreateSourceCommand(
                get_source_id_command, get_person_id_command, self.podcast_database
            )
        }
        log.info(f"Get create_commands: {create_commands}")

        return create_commands

    def execute(self, url):
        log.info(f"Execute AddByURL command.")

        extractors = self._get_extractors()
        create_commands = self._get_create_commands()

        page = None

        # Find a extractor that match the url
        for extractor in extractors:
            if extractor.match(url):
                data = extractor.extract(url)
                create_command = create_commands.get(data["type"])
                page = create_command.execute(data)
                break

        if page is None:
            log.info(f"Cannot find a extractor {url}.")

        return page


class AddByISBNCommand(Command):
    def __init__(self, source_database, person_database, book_database):
        self.source_database = source_database
        self.person_database = person_database
        self.database = book_database
        log.info("Create a AddByISBNCommand object.")

    def _get_extractors(self):
        extractors = [
            DoubanBookExtractor(),
        ]
        log.info(f"Get extractors: {extractors}")
        return extractors

    def _get_create_commands(self):
        get_source_id_command = GetSourceIDCommand(self.source_database)
        get_person_id_command = GetPersonIDCommand(self.person_database)
        create_commands = {
            "Book": CreateSourceCommand(
                get_source_id_command, get_person_id_command, self.database
            )
        }
        log.info(f"Get create_commands: {create_commands}")

        return create_commands

    def execute(self, isbn):
        log.info(f"Execute AddByISBN command.")

        extractors = self._get_extractors()
        create_commands = self._get_create_commands()

        page = None

        # Find a extractor that match the url
        for extractor in extractors:
            if extractor.match(isbn):
                data = extractor.extract(isbn)
                if data is None:
                    continue
                create_command = create_commands.get(data["type"])
                page = create_command.execute(data)
                break

        if page is None:
            log.info(f"Cannot find a extractor {isbn}.")

        return page
