import azure.functions as func
import logging
import os

from logic.commands import AddByURLCommand
from persistence.notion import NotionManager
from persistence.database import PersonDatabase, SourceDatabase, PodcastDatabase

log = logging.getLogger(__name__)
app = func.FunctionApp()


def get_add_by_url_command():
    notion = NotionManager(os.getenv("NOTION_TOKEN"))
    person_database = PersonDatabase(notion, os.getenv("PERSON_DATABASE_ID"))
    source_database = SourceDatabase(notion, os.getenv("SOURCE_DATABASE_ID"))
    podcast_database = PodcastDatabase(notion, os.getenv("PODCAST_DATABASE_ID"))
    add_by_url_command = AddByURLCommand(
        source_database, person_database, podcast_database
    )

    return add_by_url_command


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

    return response
