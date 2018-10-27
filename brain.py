from detect_emotion_from_voice.detect_from_speech import voice2emo

# Communicate with the Tone Analyser CNN Model
def getEmotionFromVoice(wav_path):
	print(voice2emo(wav_path))

"""
# Communicate with the Text Analyser Model
def getEmotionFromText(text_path):
	return text2emo(text_path)
"""