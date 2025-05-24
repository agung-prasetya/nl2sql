from detectors import *
from evaluator import *
from flask import Flask, request, jsonify
import tempfile
import os
from flask_cors import CORS
from pathlib import Path


app = Flask(__name__)
CORS(app)

@app.route('/sorting/detect', methods=['POST'])
def predict_sorting():
    kalimat = request.form.get('kalimat')
    file = request.files.get('file')

    if not kalimat or not file:
        return jsonify({'error': 'Missing "kalimat" or "file database json" in request'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        detector = SortingDetector()
        detected_label = detector.detect(kalimat=kalimat,filepath_database_json=tmp_path)
    finally:
        os.remove(tmp_path)

    return jsonify({
        'kalimat': kalimat,
        'detected_label': detected_label
    })

@app.route('/sorting/evaluate', methods=['POST'])
def evaluate():
    filepath_dataset = str(Path(__file__).parent / "detectors/sorting/dataset/dataset.xlsx")
    folderpath_database = str(Path(__file__).parent / "detectors/sorting/dataset/")
    evaluator = SingleLabelEvaluator(filepath_dataset=filepath_dataset, folderpath_database=folderpath_database, detector=SortingDetector())
    
    hasil = evaluator.evaluate()
    metrics_dict = hasil['metrics'].to_dict(orient='index')

    total_data = len(evaluator.dataframe)
    jumlah_benar_total = round(hasil['accuracy'] * total_data)
    jumlah_salah_total = total_data - jumlah_benar_total

    y_true = evaluator.dataframe['label']
    y_pred = []

    for id, row in evaluator.dataframe.iterrows():
        kalimat = row['kalimat']
        filepath_database_json = str(Path(folderpath_database) / row['database'])
        predicted_label = evaluator.detector.detect(kalimat=kalimat, filepath_database_json=filepath_database_json)
        y_pred.append(predicted_label)

    df_pred = pd.DataFrame({'actual': y_true, 'predicted': y_pred})
    labels = sorted(df_pred['actual'].unique().tolist() + df_pred['predicted'].unique().tolist())

    # Tambahkan jumlah benar, salah, dan jumlah prediksi ke tiap label
    for label in metrics_dict:
        jumlah_benar = ((df_pred['actual'] == label) & (df_pred['predicted'] == label)).sum()
        jumlah_salah = ((df_pred['actual'] == label) & (df_pred['predicted'] != label)).sum()
        predicted_as_label = (df_pred['predicted'] == label).sum()

        metrics_dict[label]['jumlah_benar'] = int(jumlah_benar)
        metrics_dict[label]['jumlah_salah'] = int(jumlah_salah)

        # Tambahkan kolom: berapa kali masing-masing label diprediksi sebagai label ini
        for target_label in labels:
            pred_count = ((df_pred['actual'] == label) & (df_pred['predicted'] == target_label)).sum()
            metrics_dict[label][f'pred_as_{target_label.lower()}'] = int(pred_count)

    return jsonify({
        'accuracy': hasil['accuracy'],
        'benar': jumlah_benar_total,
        'salah': jumlah_salah_total,
        'metrics': metrics_dict
    })

    
if __name__ == '__main__':
    app.run(debug=True)