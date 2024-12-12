from paddleocr import PaddleOCR
from config import IMG_PATH

class OCRService:
    def __init__(self, lang="korean"):
        self.ocr = PaddleOCR(lang=lang)

    def extract_text(self, image_path):
        result = self.ocr.ocr(image_path, cls=False)
        return " ".join([r[1][0] for r in result[0]])