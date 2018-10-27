from flask import Flask, redirect, jsonify, request, render_template
from flask_cors import CORS
import json
import utils

app = Flask(__name__)
CORS(app)

@app.route('/prioritise', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	wav_output = utils.saveWAV(req['encoded'])
	if wav_output != "":
		text_output = utils.speechToText(wav_output)
		if text_output != "":
			utils.saveText(text_output)
		return jsonify({"response": "true"})

if __name__ == '__main__':
	app.run()