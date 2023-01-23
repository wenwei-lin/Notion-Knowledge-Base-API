from extractor.base import Extractor
import re
import requests
import logging

log = logging.getLogger(__name__)


class ZhongduExtractor(Extractor):
    def match(self, url):
        pattern = re.compile(r"ny.zdline.cn/mobile/audio")
        match_result = bool(pattern.search(url))

        if match_result:
            log.info(f"Zhongdu Extractor can process {url}.")
        else:
            log.info(f"Zhongdu Extractor cannot process {url}.")

        return match_result

    def _get_artId(self, url):
        pattern = re.compile(r"artId=(\d+)")
        artId = pattern.findall(url)[0]
        log.info(f"Get artId: {artId}")

        return artId

    def _get_meta_info(self, artId):
        endpoint = f"http://ny.zdline.cn/h5/article/newDetailToH5.do?ticket=null&artId={artId}&code="
        meta_info = requests.get(endpoint).json()
        log.info(f"Get meta info from: {endpoint}")

        return meta_info

    def _get_author_list(self, meta_info):
        raw_authors = meta_info["model"]["aboutAuthors"]
        authors = []

        for raw_author in raw_authors:
            author = {
                "name": raw_author["name"],
                "icon_url": raw_author["pic"],
                "description": raw_author["desc"],
            }
            authors.append(author)
        log.info(f"Get author list: {authors}")

        return authors

    def _get_published(self, meta_info):
        published = meta_info["model"]["dayStr"]
        log.info(f"Get dayStr from Zhongdu: {published}")

        if len(published) <= 5:
            published = "2023-" + published
        log.info(f"Get published date: {published}")

        return published

    def _get_duration(self, meta_info):
        audio_time = meta_info["model"]["audioInfo"][0]["audioTime"]
        audio_time = audio_time.split(":")[0]
        log.info(f"Get duration: {audio_time}")

        return int(audio_time)

    def _extract_from_meta_info(self, meta_info):
        data = {
            "title": meta_info["model"]["title"],
            "description": meta_info["model"]["daodu"],
            "icon_url": meta_info["model"]["openPic"],
            "cover_url": meta_info["model"]["openPic"],
            "author": self._get_author_list(meta_info),
            "published": self._get_published(meta_info),
            "duration": self._get_duration(meta_info),
            "type": "Podcast",
            "language": "Chinese",
            "series": meta_info["model"]["zhuanlan"]["name"],
        }
        log.info(f"Extract data from Zhongdu: {data}")

        return data

    def extract(self, url) -> dict:
        artId = self._get_artId(url)
        meta_info = self._get_meta_info(artId)
        data = self._extract_from_meta_info(meta_info)
        return data
