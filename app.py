from flask import Flask, redirect, jsonify, request, render_template
from flask_cors import CORS
import json
import utils

app = Flask(__name__)
CORS(app)

@app.route('/prioritise', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	utils.saveAsWAV(req['encoded'])
	return jsonify({"response": "true"})

if __name__ == '__main__':
	app.run()