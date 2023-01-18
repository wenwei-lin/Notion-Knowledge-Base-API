from abc import ABC, abstractmethod
from persistence.database import SourceDatabase, PersonDatabase, PodcastDatabase


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        raise NotImplementedError(
            "Classes inherit Command must implement a execute method"
        )


class GetSourceIDCommand(Command):
    def __init__(self, source_database: SourceDatabase):
        self.source_database = source_database

    def _query_by_title(self, data):
        title = data["title"]
        filter = {"filter": {"property": "Title", "rich_text": {"equals": title}}}

        pages = self.source_database.query_pages(filter)
        if len(pages) > 0:
            return pages[0]
        else:
            return None

    def _create_page(self, data):
        page = self.source_database.create_page(data)
        return page

    def execute(self, data):
        page = self._query_by_title(data)
        if page is None:
            page = self._create_page(data)
        return page["id"]


class GetPersonIDCommand(Command):
    def __init__(self, person_database: PersonDatabase):
        self.person_database = person_database

    def _query_by_name(self, data):
        name = data["name"]
        filter = {"filter": {"property": "Name", "rich_text": {"equals": name}}}

        pages = self.person_database.query_pages(filter)
        if len(pages) > 0:
            return pages[0]
        else:
            return None

    def _create_page(self, data):
        page = self.person_database.create_page(data)
        return page

    def execute(self, data):
        page = self._query_by_name(data)
        if page is None:
            page = self._create_page(data)
        return page["id"]


class CreatePodcastCommand(Command):
    def __init__(
        self,
        get_source_id_command: GetSourceIDCommand,
        get_person_id_command: GetPersonIDCommand,
        podcast_database: PodcastDatabase,
    ):
        self.get_source_id_command = get_source_id_command
        self.get_person_id_command = get_person_id_command
        self.podcast_database = podcast_database

    def _get_author_id(self, author_list: list):
        return [self.get_person_id_command.execute(author) for author in author_list]

    def _get_source_id(self, data):
        return self.get_source_id_command.execute(data)

    def _query_podcast(self, title):
        filter = {"filter": {"property": "Title", "rich_text": {"equals": title}}}

        pages = self.podcast_database.query_pages(filter)
        if len(pages) > 0:
            return pages[0]
        else:
            return None

    def execute(self, data):
        source_id = self._get_source_id(data)
        author_id = self._get_author_id(data["author"])
        data["source_id"] = source_id
        data["author"] = author_id

        podcast = self._query_podcast(data["title"])
        if podcast is None:
            podcast = self.podcast_database.create_page(data)

        return podcast
