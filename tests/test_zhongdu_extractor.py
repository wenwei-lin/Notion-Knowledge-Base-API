from extractor.zhongdu import ZhongduExtractor
import logging

class TestZhongduExtractor:
    def setup_method(self, test_method):
        self.extractor = ZhongduExtractor()
    
    def test_extract(self):
        data = self.extractor.extract("http://ny.zdline.cn/mobile/audioText?artId=158504&sm=app")

        data = self.extractor.extract("http://ny.zdline.cn/mobile/audioText?artId=173481&sm=app")

        data = self.extractor.extract("http://ny.zdline.cn/mobile/audioText/?artId=184270&sm=app")

