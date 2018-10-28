# Import for codecs encoding-decoding (base64)
import codecs
# Import for handling json
import json
# Import from speech to text engine
import speech_recognition as sr
# Import for getting system datetime
import datetime
# Import for subprocesses to communicate with the terminal
import subprocess
# Import OS module for system functions
import os
# For calling UNIX Shell utilities
import shutil

CURR_PATH = subprocess.check_output("pwd", shell=True).strip().decode('ascii') + "/"
FILEPATH = CURR_PATH + "temp/"
if not os.path.exists(FILEPATH):
	os.system("mkdir " + FILEPATH)

# Pass the audio data to an encoding function.
def encode_audio(audio):
	audio_content = audio.read()
	return base64.b64encode(audio_content)

# Pass the encoded text data to a decoding function
def decode_audio(encoded_text):
	return base64.b64decode(encoded_text)

# Get a unique file name for audio saving
def getFileName():
	NOW = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	FILENAME = "audio-" + NOW + ".wav"
	return (FILENAME)

def moveToTemp(file):
	CURR_PATH = subprocess.check_output("pwd", shell=True).strip().decode('ascii') + "/"
	FILEPATH = CURR_PATH + "temp/"
	shutil.move(CURR_PATH + "/" + file, FILEPATH + file)
	return (FILEPATH + file)


# To convert the speech (from audio signals) to text using Google's Engine
def speechToText(filepath):
	r = sr.Recognizer()
	infile = open(filepath, "r")
	with sr.AudioFile(infile) as source:
		audio = r.record(source)
		infile.close()
		try:
			return r.recognize_google(audio)
		except sr.UnknownValueError as e:
			print("[ERROR] Google Speech Recognition could not understand the input audio; {0}".format(e))
			return ""
		except sr.RequestError as e:
			print("[ERROR] Could not request results from Google Speech Recognition service; {0}".format(e))
			return ""


# To save the text to the temps/ directory
def saveText(text):
	CURR_PATH = subprocess.check_output("pwd", shell=True).strip().decode('ascii') + "/"
	NOW = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	FILENAME = "text-" + NOW + ".txt"
	FILEPATH = CURR_PATH + "temp/"
	try:
		outfile = open(FILEPATH + FILENAME, 'w')
		outfile.write(text)
		outfile.close()
		return (FILEPATH + FILENAME)
	except Exception as e:
		print(e)
		return ""

