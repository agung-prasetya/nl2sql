from flask import Flask, request, jsonify, send_from_directory
from detectors import DMLDetector
import tempfile
import os
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/test-kalimat")
def test_kalimat():
    return send_from_directory("frontend", "test-kalimat.html")

@app.route("/test-dataset")
def test_dataset():
    return send_from_directory("frontend", "test-dataset.html")

@app.route('/dml/predict', methods=['POST'])
def predict():
    kalimat = request.form.get('kalimat')
    file = request.files.get('file')

    if not kalimat or not file:
        return jsonify({'error': 'Missing "kalimat" or file in request'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        detector = DMLDetector()
        predicted_label = detector.detect(kalimat=kalimat, file_database_json=tmp_path)
    finally:
        os.remove(tmp_path)

    return jsonify({
        'kalimat': kalimat,
        'predicted_label': predicted_label
    })
    
@app.route('/uji', methods=['POST'])
def uji_dataset():
    import tempfile
    from evaluators.evaluator import Evaluator
    from detectors.dml_detector import DMLDetector
    csv_file = request.files.get('csv_file')
    json_files = request.files.getlist('json_file')

    if not csv_file or not json_files:
        return jsonify({"error": "CSV dan JSON harus diunggah"}), 400

    # Simpan semua JSON file ke folder sementara
    temp_json_dir = tempfile.mkdtemp()
    for file in json_files:
        path = os.path.join(temp_json_dir, file.filename)
        file.save(path)

    # Baca CSV menjadi dataframe
    df = pd.read_csv(csv_file)

    # Detektor & Evaluator
    detector = DMLDetector()
    evaluator = Evaluator(dataframe=df, detector=detector)
    result = evaluator.evaluate(temp_json_dir)

    # Ambil nilai macro average dari metrics
    metrics = result["metrics"]
    macro = metrics.get("macro", {"precision": 0, "recall": 0, "f1": 0})

    return jsonify({
        "akurasi": f"{result['accuracy']}%",
        "presisi": f"{macro['precision']}%",
        "recall": f"{macro['recall']}%",
        "f1_score": f"{macro['f1']}%",
        "hasil": result["hasil"],
        "statistik": result["statistik"]
    })

if __name__ == '__main__':
    app.run(debug=True)
