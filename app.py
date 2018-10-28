from flask import Flask, redirect, jsonify, request, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
import utils
import brain

app = Flask(__name__)
CORS(app)

@app.route('/prioritise', methods=['POST'])
def webhook():
	if request.method == "POST":
		file = request.files['audio']
		print(file)
		fname = utils.getFileName()
		file.save(secure_filename(fname))
		tempaudio = utils.moveToTemp(fname)
		if tempaudio != "":
			brain.getEmotionFromVoice(tempaudio)
	return jsonify({"response": "true"})

if __name__ == '__main__':
	app.run()