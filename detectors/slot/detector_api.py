from detectors import *
from evaluator import *
from flask import Flask, request, jsonify
import tempfile
import os
from flask_cors import CORS
from pathlib import Path


app = Flask(__name__)
CORS(app)

@app.route('/slot/detect', methods=['POST'])
def predict_slot():
    pass

@app.route('/slot/evaluate', methods=['POST'])
def evaluate():
    pass

    

if __name__ == '__main__':
    app.run(debug=True)