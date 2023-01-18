import azure.functions as func
import logging
import os

from logic.commands import AddByURLCommand
from persistence.notion import NotionManager
from persistence.database import PersonDatabase, SourceDatabase, PodcastDatabase

app = func.FunctionApp()

def get_add_by_url_command():
    notion = NotionManager(os.getenv('NOTION_TOKEN'))
    person_database = PersonDatabase(notion, os.getenv("PERSON_DATABASE_ID"))
    source_database = SourceDatabase(notion, os.getenv("SOURCE_DATABASE_ID"))
    podcast_database = PodcastDatabase(notion, os.getenv("PODCAST_DATABASE_ID"))
    add_by_url_command = AddByURLCommand(source_database, person_database, podcast_database)

    return add_by_url_command

@app.function_name(name="AddByURL")
@app.route(route="add/source")
def add_source(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("AddSourceToNotion function processed a request.")

    add_by_url_command = get_add_by_url_command()
    url = req.params.get('url')
    if url:
        page = add_by_url_command.execute(url)

        if page:
            return func.HttpResponse(
                "Add successfully",
                status_code=200
            )
    
    return func.HttpResponse(
        "Error",
        status_code=400
    )




