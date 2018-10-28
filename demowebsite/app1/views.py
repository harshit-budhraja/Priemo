from django.shortcuts import render
from django.http import HttpResponse
from .models import Message

# Create your views here.
def index(request):
    return HttpResponse("<h1>This is the app1</h1>")


def message(request):
    messages = Message.objects.all()
    text = '..........'
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

    db = firebase.database()

    u = db.child("users").get()

    userData = []
    if u.each() is not None:
        for users in u.each():
            # print(users.key(), users.val())
            userData.append([users.key(), users.val()])
    def getKey(item):
        return item[1]

    userData = sorted(userData, key = getKey, reverse=True)
    print(userData)
    return render(request, 'app1/index.html', {'userData': userData, 'text': text})


def index2(request):
    #!/usr/bin/env python3
    # Requires PyAudio and PySpeech.
    text = '..........'
    import speech_recognition as sr
    import requests
    
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        # audio = r.listen(source)
        audio = r.record(source, duration=10)
        #write audio to a WAV file
        with open("microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())
    
    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = r.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    url = "http://localhost:5000/prioritise/Harshit"
    headers = {"enctype": "multipart/form-data"}
    with open("microphone-results.wav", "rb") as fobj:
        r = requests.post(url, headers = headers, files={'audio', fobj})

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

    db = firebase.database()

    u = db.child("users").get()

    userData = []
    if u.each() is not None:
        for users in u.each():
            userData.append([users.key(), users.val()])

    def getKey(item):
        return item[1]

    userData = sorted(userData, key = getKey, reverse=True)
    print(userData)
    return render(request, 'app1/index.html', {'userData': userData, 'text': text})
