from gtts import gTTS
import playsound as ps

class TTSService:
    @staticmethod
    def play_tts(text, lang="ko", save_path="voiceKo.mp3"):
        tts = gTTS(text=text, lang=lang)
        tts.save(save_path)
        ps.playsound(save_path)