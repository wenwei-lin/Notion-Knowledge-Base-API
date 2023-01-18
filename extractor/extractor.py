from abc import ABC, abstractmethod
import re
import requests

class Extractor(ABC):
    @abstractmethod
    def match(self, url) -> bool:
        raise NotImplementedError("Classes inherit Extractor should implement a match method.")
    
    def extract(self, url) -> dict:
        raise NotImplementedError("Classes inherit Extractor should implement a extract method.")

class ZhongduExtractor(Extractor):
    def match(self, url):
        pattern = re.compile(r'ny.zdline.cn/mobile/audioText')
        return bool(pattern.search(url))
    
    def _get_artId(self, url):
        pattern = re.compile(r'artId=(\d+)')
        artId = pattern.findall(url)[0]
        return artId
    
    def _get_meta_info(self, artId):
        endpoint = f'http://ny.zdline.cn/h5/article/newDetailToH5.do?ticket=null&artId={artId}&code='
        meta_info = requests.get(endpoint).json()
        return meta_info
    
    def _get_author_list(self, meta_info):
        raw_authors = meta_info['model']['aboutAuthors']
        authors = []

        for raw_author in raw_authors:
            author = {
                "name": raw_author['name'],
                "icon_url": raw_author['pic'],
                "description": raw_author['desc'] 
            }
            authors.append(author)
        
        return authors
    
    def _get_published(self, meta_info):
        published = meta_info['model']['dayStr']
        if len(published) <= 5:
            published = "2023-" + published
        return published
    
    def _get_duration(self, meta_info):
        audio_time = meta_info['model']['audioInfo'][0]['audioTime']
        audio_time = audio_time.split(':')[0]
        return int(audio_time)
    
    def _extract_from_meta_info(self, meta_info):
        data = {
            "title": meta_info['model']['title'],
            "description": meta_info['model']['daodu'],
            "icon_url": meta_info['model']['openPic'],
            "cover": meta_info['model']['openPic'],
            "author": self._get_author_list(meta_info),
            "published": self._get_published(meta_info),
            "duration": self._get_duration(meta_info),
            "type": "Podcast",
            "language": "Chinese",
            "series": meta_info['model']['zhuanlan']['name']
        }
        return data

    def extract(self, url) -> dict:
        artId = self._get_artId(url)
        meta_info = self._get_meta_info(artId)
        data = self._extract_from_meta_info(meta_info)
        return data
