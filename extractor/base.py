from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def match(self, url) -> bool:
        raise NotImplementedError("Classes inherit Extractor should implement a match method.")
    
    @abstractmethod
    def extract(self, url) -> dict:
        raise NotImplementedError("Classes inherit Extractor should implement a extract method.")