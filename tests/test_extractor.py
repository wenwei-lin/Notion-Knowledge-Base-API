import unittest
from extractor.zhongdu import ZhongduExtractor

class ZhongduExtractorTester(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = ZhongduExtractor()
    
    def testExtract(self):
        data = self.extractor.extract("http://ny.zdline.cn/mobile/audioText?artId=158504&sm=app")
        print(data)
        data = self.extractor.extract("http://ny.zdline.cn/mobile/audioText?artId=173481&sm=app")
        print(data)
        data = self.extractor.extract("http://ny.zdline.cn/mobile/audioText/?artId=184270&sm=app")
        print(data)

if __name__ == "__main__":
    unittest.main()