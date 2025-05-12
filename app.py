from flask import Flask, request, jsonify
from detectors import *
from evaluators import *
import tempfile
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def detect(detector):
    kalimat = request.form.get('kalimat')
    file = request.files.get('file')

    if not kalimat or not file:
        return jsonify({'error': 'Missing "kalimat" or file in request'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        predicted_label = detector.detect(kalimat=kalimat, file_database_json=tmp_path)
    finally:
        os.remove(tmp_path)

    return jsonify({
        'kalimat': kalimat,
        'predicted_label': predicted_label
    })

@app.route('/column/predict', methods=['POST'])
def predict_column():
    detector = ColumnDetector()
    return detect(detector=detector)

@app.route('/column/evaluate', methods=['POST'])
def evaluate_predictor():
    detector = ColumnDetector()

    file = request.files.get('file')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        evaluator = MultilabelEvaluator(path_file_dataset=tmp_path, detector=detector)
        result = evaluator.evaluate('../databases/column_detector/')
    finally:
        os.remove(tmp_path)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
