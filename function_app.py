import azure.functions as func
import logging
import os

from logic.commands import AddByURLCommand, AddByISBNCommand
from notion.notion import NotionManager
from notion.database import (
    PersonDatabase,
    SourceDatabase,
    PodcastDatabase,
    BookDatabase,
)

log = logging.getLogger(__name__)
app = func.FunctionApp()

notion = NotionManager(os.getenv("NOTION_TOKEN"))
person_database = PersonDatabase(notion, os.getenv("PERSON_DATABASE_ID"))
source_database = SourceDatabase(notion, os.getenv("SOURCE_DATABASE_ID"))
podcast_database = PodcastDatabase(notion, os.getenv("PODCAST_DATABASE_ID"))
book_database = BookDatabase(notion, os.getenv("BOOK_DATABASE_ID"))


def get_add_by_url_command():
    add_by_url_command = AddByURLCommand(
        source_database, person_database, podcast_database
    )
    return add_by_url_command


def get_add_by_isbn_command():
    add_by_isbn_command = AddByISBNCommand(
        source_database, person_database, book_database
    )
    return add_by_isbn_command


def get_parameter(req: func.HttpRequest, name):
    value = req.params.get(name)
    if not value:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            value = req_body.get(name)
    log.info(f"Get parameter from request: {name}={value}")

    return value


@app.function_name(name="AddByURL")
@app.route(route="addURL", auth_level=func.AuthLevel.ANONYMOUS)
def add_source(req: func.HttpRequest) -> func.HttpResponse:
    log.info("AddByURL function processed a request.")

    add_by_url_command = get_add_by_url_command()
    url = get_parameter(req, "url")

    response = func.HttpResponse(
        "Cannot find parameter 'url' in request body.", status_code=400
    )

    if url:
        page = add_by_url_command.execute(url)
        if page:
            response = func.HttpResponse("Source Added", status_code=200)
        else:
            response = func.HttpResponse("Cannot find a extractor processing this url.", status_code=400)

    return response


@app.function_name(name="AddByISBN")
@app.route(route="addBook", auth_level=func.AuthLevel.ANONYMOUS)
def add_source(req: func.HttpRequest) -> func.HttpResponse:
    log.info("AddByISBN function processed a request.")

    add_by_isbn_command = get_add_by_isbn_command()
    url = get_parameter(req, "isbn")

    response = func.HttpResponse(
        "Cannot find parameter 'isbn' in request body.", status_code=400
    )

    if url:
        page = add_by_isbn_command.execute(url)
        if page:
            response = func.HttpResponse("Book Added", status_code=200)
        else:
            response = func.HttpResponse("Cannot find a extractor processing this isbn.", status_code=400)

    return response
