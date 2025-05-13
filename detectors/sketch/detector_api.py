from detectors import *
from evaluator import *
from flask import Flask, request, jsonify
import tempfile
import os
from flask_cors import CORS
from pathlib import Path


app = Flask(__name__)
CORS(app)

@app.route('/sketch/detect', methods=['POST'])
def predict_sketch():
    pass

@app.route('/sketch/evaluate', methods=['POST'])
def evaluate():
    pass

    

if __name__ == '__main__':
    app.run(debug=True)