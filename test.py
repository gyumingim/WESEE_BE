from paddleocr import PaddleOCR
import gtts
import playsound as ps
import re
ocr = PaddleOCR(lang="korean")
 
IMG_PATH = "korImage.jpg"
MP3_PATH = "voiceKo.mp3"
result = ocr.ocr(IMG_PATH, cls=True)
 

answer = ""
for r in result[0]:
        answer += r[1][0] + " "

tts = gtts.gTTS(text=answer, lang="ko")
tts.save(MP3_PATH)
ps.playsound(MP3_PATH)

print(answer)