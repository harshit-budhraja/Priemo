import codecs
import json

def saveAsWAV(encoded_string):
	try:
		outfile = open('test.wav', 'wb')
		outfile.write(codecs.decode(encoded_string, 'base64'))
		outfile.close()
		return True
	except:
		return False

