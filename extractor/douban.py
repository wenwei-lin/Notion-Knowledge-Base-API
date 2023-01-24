from bs4 import BeautifulSoup
import requests
import json
import re
import logging
from datetime import datetime

from extractor.base import Extractor

log = logging.getLogger(__name__)


class DoubanBookExtractor(Extractor):
    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.7 (KHTML, like Gecko) Chrome/20.0.1099.0 Safari/536.7 QQBrowser/6.14.15493.201"
        }

        log.info("Create a DoubanBookExtractor object.")

    def match(self, isbn: str) -> bool:
        isbn = isbn.replace("-", "")
        pattern = re.compile(f"^[0-9]*$")

        match_result = bool(pattern.search(isbn))

        if match_result:
            log.info(f"DoubanBook Extractor can process {isbn}.")
        else:
            log.info(f"DoubanBook Extractor cannot process {isbn}.")

        return match_result

    def _get_douban_url(self, isbn):
        endpoint = f"https://book.douban.com/isbn/{isbn}/"
        response = requests.get(endpoint, headers=self.headers)
        douban_url = response.url

        if douban_url == endpoint:
            log.info(f"Cannot find forwarding url for {isbn}")
            douban_url = None
        else:
            log.info(f"Get Douban url for book(isbn={isbn}): {douban_url}")

        return douban_url

    def _load_page(self, url):
        html_doc = requests.get(url, headers=self.headers).text
        self.soup = BeautifulSoup(html_doc, "lxml")

        schema_tag = self.soup.find("script", type="application/ld+json")
        self.schema = json.loads(schema_tag.string)

        log.info(f"Extract schema object of {url}: {self.schema}")

    def _get_title(self):
        title = self.schema["name"].strip()
        log.info(f"Get title: {title}")

        return title

    def _get_author(self):
        author_list = []
        for author in self.schema["author"]:
            author_name = re.sub(r"\[.*\]", "", author["name"]).strip()
            if author_name.find("·") != -1:
                names = author_name.split("·")
                names = [name.strip() for name in names]
                author_name = " · ".join(names)
            author_list.append({"name": author_name, "icon_emoji": "🧑\u200d🏫"})

        log.info(f"Get author: {author_list}")
        return author_list

    def _get_cover(self):
        cover = self.soup.find("meta", property="og:image")["content"]
        log.info(f"Get cover: {cover}")

        return cover

    def _get_publisher(self):
        publisher = None
        publisher_tag = self.soup.find("span", string="出版社:")
        if publisher_tag:
            publisher = str(publisher_tag.next_sibling.next_sibling.string)
        log.info(f"Get publisher: {publisher}")

        return publisher

    def _get_original_title(self):
        original_title = None
        original_title_tag = self.soup.find("span", string="原作名:")
        if original_title_tag:
            original_title = str(original_title_tag.next_sibling).strip()
        log.info(f"Get original title: {original_title}")

        return original_title

    def _get_translator(self):
        translator_list = None
        translator_tag = self.soup.find("span", string=" 译者")
        if translator_tag:
            translator_tag = translator_tag.find_next_siblings("a")
            translator_list = [
                {"name": str(translator.string), "icon_emoji": "🧑\u200d🏫"}
                for translator in translator_tag
            ]
        log.info(f"Get translator: {translator_list}")

        return translator_list

    def _get_published(self):
        published = None
        published_tag = self.soup.find("span", string="出版年:")
        if published_tag:
            raw_date = str(published_tag.next_sibling).split("-")
            year = int(raw_date[0])
            month = int(raw_date[1])
            day = int(raw_date[2]) if len(raw_date) > 2 else 1
            published_date = datetime(year, month, day)
            published = datetime.strftime(published_date, "%Y-%m-%d")
        log.info(f"Get published: {published}")

        return published

    def _get_pages(self):
        pages = None
        pages_tag = self.soup.find("span", string="页数:")
        if pages_tag:
            pages = int(pages_tag.next_sibling.string)
        log.info(f"Get pages: {pages}")

        return pages

    def _get_douban_ranking(self):
        douban_ranking = None
        douban_ranking_tag = self.soup.find("strong", property="v:average")
        if douban_ranking_tag:
            douban_ranking = float(douban_ranking_tag.string)
        log.info(f"Get douban ranking: {douban_ranking}")
        return douban_ranking

    def _get_description(self):
        description = None
        intro_tag_list = self.soup.findAll("div", class_="intro")
        if len(intro_tag_list) > 0:
            if intro_tag_list[0].find("a"):
                intro_tag = intro_tag_list[1]
            else:
                intro_tag = intro_tag_list[0]

            log.info(f"Description tag is: {intro_tag}")
            description = ""
            for paragraph in intro_tag.children:
                if paragraph.string:
                    description = description + paragraph.string
                    description = description + "\n"
            description.strip()
        log.info(f"Get description: {description}")
        return description

    def extract(self, isbn) -> dict:
        douban_url = self._get_douban_url(isbn)
        data = None
        if douban_url:
            self._load_page(douban_url)
            data = {
                "title": self._get_title(),
                "description": self._get_description(),
                "author": self._get_author(),
                "cover_url": self._get_cover(),
                "icon_url": self._get_cover(),
                "publisher": self._get_publisher(),
                "original_title": self._get_original_title(),
                "translator": self._get_translator(),
                "published": self._get_published(),
                "pages": self._get_pages(),
                "douban_ranking": self._get_douban_ranking(),
                "douban_url": douban_url,
                "isbn": isbn,
                "type": "Book",
            }
            log.info(f"Extract data from {douban_url}:\n{json.dumps(data, indent=4)}")
        return data
