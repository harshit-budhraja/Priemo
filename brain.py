from detect_emotion_from_voice.detect_from_speech import voice2emo
import subprocess
import utils
import json
import pyrebase

config = {
"apiKey": "AIzaSyARiwrSJ0kfZmfhaENfPOBwrVNvU-oYUnU",
"authDomain": "voice-dca81.firebaseapp.com",
"databaseURL": "https://voice-dca81.firebaseio.com",
"projectId": "voice-dca81",
"storageBucket": "voice-dca81.appspot.com",
"messagingSenderId": "50025772710"
}
firebase = pyrebase.initialize_app(config)

# Communicate with the Tone Analyser CNN Model
def getEmotionFromVoice(wav_path):
	jsonOutput_voice = voice2emo(wav_path)
	return jsonOutput_voice

# Communicate with the Text Analyser Model
def getEmotionFromText(text):
	CURR_PATH = subprocess.check_output("pwd", shell=True).strip().decode('ascii') + "/"
	l = utils.saveText(text)
	jsonOutput_text = subprocess.check_output("python " + CURR_PATH + "detect_emotion_from_text/sentiment_analysis.py " + l, shell=True).strip().decode('ascii')
	return jsonOutput_text


def getPriorityScore(vj, tj, name):
    points = 0
    voiceJSON = json.loads(vj)
    textJSON = json.loads(tj)

    if voiceJSON["emotion"] == "anger":
        points += 5
    elif voiceJSON["emotion"] == "fearful":
        points += 4
    elif voiceJSON["emotion"] == "sad":
        points += 3
    elif voiceJSON["emotion"] == "calm":
        points += 2
    elif voiceJSON["emotion"] == "happy":
        points += 1

    positiveEmotions = ["calm", "happy"]
    negativeEmotions = ["anger", "fearful", "sad"]

    if voiceJSON["emotion"] in positiveEmotions:
        points += textJSON["delightful"]
        points += textJSON["loving"]
    elif voiceJSON["emotion"] in negativeEmotions:
        points += textJSON["fearful"]
        points += textJSON["angry"]
        points += textJSON["sad"]

    db = firebase.database()
    db.child("users").child(name).set(points)

    