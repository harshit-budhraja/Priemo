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

# To save a base64 encoded string as a WAV
def saveWAV(encoded_string):
	CURR_PATH = subprocess.check_output("pwd", shell=True).strip().decode('ascii') + "/"
	NOW = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	FILENAME = "audio-" + NOW + ".wav"
	FILEPATH = CURR_PATH + "temp/"
	try:
		outfile = open(FILEPATH + FILENAME, 'wb')
		outfile.write(codecs.decode(encoded_string, 'base64'))
		return (FILEPATH + FILENAME)
	except:
		return ""


# To convert the speech (from audio signals) to text using Google's Engine
def speechToText(filepath):
	r = sr.Recognizer()
	infile = open(filepath, "r")
	with sr.AudioFile(infile) as source:
		audio = r.record(source)
		infile.close()
		try:
			return r.recognize_google(audio)
		except sr.UnknownValueError:
			print("[ERROR] Google Speech Recognition could not understand the input audio.")
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
	except:
		return ""

