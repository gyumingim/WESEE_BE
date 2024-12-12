from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas.ocr_schema import OCRRequest
from services.ocr_service import OCRService
from services.braille_service import BrailleService
from utils.image_utils import save_image_from_base64
from config import IMG_PATH

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ocr_service = OCRService()
braille_service = BrailleService()

@app.post("/ocr")
def api_ocr(request: OCRRequest):
    save_image_from_base64(request.image, IMG_PATH)
    result = ocr_service.extract_text(IMG_PATH)
    dot_letters = braille_service.letter_to_braille(result)
    return {"dot_letters": dot_letters}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)