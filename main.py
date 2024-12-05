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

# FastAPI 인스턴스 생성
app = FastAPI()
ocr = PaddleOCR(lang="korean")
MP3_PATH = "voiceKo.mp3"

class OCRRequest(BaseModel):
    image: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

def decode_base64_image(base64_image, output_file="decoded_image.jpg"):
    image_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_bytes))
    
    image.save('temp_image.png')
 
    img_path = "temp_image.png"
    result = ocr.ocr(img_path, cls=False)
    answer = ""
    for r in result[0]:
        answer += r[1][0] + " "
    return answer


# 기본 라우트 설정
@app.post("/api/ocr")
def api_ocr(request: OCRRequest):
    # Base64 이미지 디코딩
    result = decode_base64_image(request.image)

    # OCR 결과 처리
    # answer = ""
    # cnt = 0
    # while True:
    #     try:
    #         answer += result['words'][cnt]['text'] + " "
    #         cnt += 1
    #     except IndexError:
    #         break

    tts = gtts.gTTS(text=result, lang="ko")
    tts.save(MP3_PATH)
    ps.playsound(MP3_PATH)

    return {"result": result}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)