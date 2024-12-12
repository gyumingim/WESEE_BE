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
import hbcvt

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

def decimal_to_braille_binary(dot_letters):
    braille_binaries = []
    
    for decimal_dot in dot_letters:
        # 십진수를 6자리 2진수로 변환
        binary_dot = format(decimal_dot, '06b')
        
        # 문자열 2진수를 정수 리스트로 변환
        binary_list = [int(bit) for bit in binary_dot]
        
        braille_binaries.append(binary_list[:6])
    
    return braille_binaries

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
@app.post("/ocr")
def api_ocr(request: OCRRequest):
    save_image_to_base64(request.image)
    result = ocr_base64()

    # play_TTS(result)

    dot_letters = []
    for letter in hbcvt.h2b.text(result):
        for consonant in letter[1]:
            dot_letter = 0
            ord_value = 64
            print("------원본점자-----")
            print(consonant[1][0])
            for dot in consonant[1][0]:
                dot_letter += int(dot) * ord_value
                ord_value /= 2
            dot_letters.append(int(dot_letter))
    print("------10진수 점자-----")
    print(dot_letters)
    converted_braille = decimal_to_braille_binary(dot_letters)
    print("------복호화 점자-----")
    print(converted_braille)

    return {"result": result}




# 시작 코드
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)