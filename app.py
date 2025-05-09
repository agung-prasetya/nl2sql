from flask import Flask, request, jsonify
from detectors import DDLDetector
from evaluators.evaluator import Evaluator
import tempfile
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/ddl/predict', methods=['POST'])
def predict_ddl():
    detector = DDLDetector()
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

@app.route('/ddl/evaluate', methods=['POST'])
def evaluate():
    file_xlsx = request.files.get('file')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        file_xlsx.save(tmp.name)
        tmp_path = tmp.name
    
    try:
        detector = DDLDetector()
        evaluator = Evaluator(path_file_dataset=tmp_path, detector=detector)
        hasil = evaluator.evaluate()

        return jsonify(hasil)
    finally:
        os.remove(tmp_path)

    

if __name__ == '__main__':
    app.run(debug=True)
