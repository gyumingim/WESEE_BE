from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware 
from paddleocr import PaddleOCR 
import base64
from pydantic import BaseModel
from PIL import Image
import io
import base64
import gtts
import playsound as ps

# 인스턴스 설정
app = FastAPI()
ocr = PaddleOCR(lang="korean")

# 상수 지정
MP3_PATH = "voiceKo.mp3"
IMG_PATH = 'temp_image.png'

# ORM 선언
class OCRRequest(BaseModel):
    image: str

# 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# base64를 이미지로 decode해서 png로 저장
def save_image_to_base64(base64_image):
    image_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_bytes))
    image.save(IMG_PATH)

# png 안 글자 OCR을 통해 글자 인식
def ocr_base64():
    result = ocr.ocr(IMG_PATH, cls=False)
    answer = ""
    for r in result[0]:
        answer += r[1][0] + " "
    return answer

# 인식된 글자 TTS 출력
def play_TTS(result):
    tts = gtts.gTTS(text=result, lang="ko")
    tts.save(MP3_PATH)
    ps.playsound(MP3_PATH)

# base64 문자열 입력받고
# 결과로 OCR 인식 글자 return
@app.post("/api/ocr")
def api_ocr(request: OCRRequest):
    save_image_to_base64(request.image)
    result = ocr_base64()

    play_TTS(result)

    return {"result": result}




# 시작 코드
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)