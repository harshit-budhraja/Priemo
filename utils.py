# Import for handling json
import json
# Import for getting system datetime
import datetime
# Import for subprocesses to communicate with the terminal
import subprocess
# Import OS module for system functions
import os
# For calling UNIX Shell utilities
import shutil
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from os.path import join, dirname

CURR_PATH = subprocess.check_output("pwd", shell=True).strip().decode('ascii') + "/"
FILEPATH = CURR_PATH + "temp/"
if not os.path.exists(FILEPATH):
	os.system("mkdir " + FILEPATH)
service = SpeechToTextV1(
    username='17e91a4d-b13b-4860-933e-434d92cf8cce',
    password='4crAinRbKs5y',
    url='https://stream.watsonplatform.net/speech-to-text/api'
)

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
	with open(join(dirname(__file__), filepath),'rb') as audio_file:
		res = json.dumps(
		    service.recognize(
		        audio=audio_file,
		        content_type='audio/wav',
		        timestamps=False,
		        word_confidence=False).get_result(),
		    indent=1)

		d = json.loads(res)
		output = ""
		#print(len(d["results"]))
		for i in range(0, len(d["results"])):
		    output += d["results"][i]["alternatives"][0]["transcript"]
		return output


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

