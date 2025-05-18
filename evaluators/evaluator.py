import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from detectors.dml_detector import DMLDetector

class Evaluator:
    def __init__(self, dataframe, detector):
        self.dataframe = dataframe
        self.detector = detector

    def evaluate(self, path_folder_database):
        import time
        true = self.dataframe['label']
        predicted = []
        hasil = []

        waktu_pendek = []
        waktu_panjang = []

        for index, row in self.dataframe.iterrows():
            kalimat = row['kalimat']
            file_database_json = os.path.join(path_folder_database, row['database'])

            start_time = time.time()
            predicted_label = self.detector.detect(kalimat=kalimat, file_database_json=file_database_json)
            exec_time = round(time.time() - start_time, 4)

            predicted.append(predicted_label)
            hasil.append({
                'no': index + 1,
                'kalimat': kalimat,
                'fakta': row['label'],
                'output': predicted_label,
                'waktu_eksekusi': exec_time
            })

            if len(kalimat.split()) <= 10:
                waktu_pendek.append(exec_time)
            else:
                waktu_panjang.append(exec_time)

        labels = sorted(set(true) | set(predicted))
        confusion_matrix = pd.crosstab(true, predicted, rownames=['Actual'], colnames=['Predicted'], dropna=False)
        confusion_matrix = confusion_matrix.reindex(index=labels, columns=labels, fill_value=0)

        metrics = pd.DataFrame(index=labels, columns=['precision', 'recall', 'f1'], dtype=float)

        for label in labels:
            TP = confusion_matrix.at[label, label]
            FP = confusion_matrix[label].sum() - TP
            FN = confusion_matrix.loc[label].sum() - TP

            precision = TP/(TP+FP) if (TP + FP) > 0 else 0
            recall = TP/(TP + FN) if (TP + FN) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

            metrics.loc[label] = [round(precision * 100, 2), round(recall * 100, 2), round(f1 * 100, 2)]

        # metrics.loc['macro'] = [
        #     round(metrics['precision'].mean(), 2),
        #     round(metrics['recall'].mean(), 2),
        #     round(metrics['f1'].mean(), 2)
        # ]
        filtered = metrics.drop(index='NODML', errors='ignore')
        metrics.loc['macro'] = [
            round(filtered['precision'].mean(), 2),
            round(filtered['recall'].mean(), 2),
            round(filtered['f1'].mean(), 2)
        ]

        accuracy = round((true == predicted).mean() * 100, 2)

        statistik_waktu = {
            "rata_pendek": round(sum(waktu_pendek) / len(waktu_pendek), 4) if waktu_pendek else 0,
            "rata_panjang": round(sum(waktu_panjang) / len(waktu_panjang), 4) if waktu_panjang else 0,
            "jumlah_pendek": len(waktu_pendek),
            "jumlah_panjang": len(waktu_panjang)
        }

        return {
            "accuracy": accuracy,
            "metrics": metrics.to_dict(orient='index'),
            "hasil": hasil,
            "statistik": statistik_waktu
        }
        
# class Evaluator():
#     def __init__(self, path_file_dataset, detector):
#         self.dataframe = pd.read_excel(path_file_dataset, engine='openpyxl')
#         self.detector = detector

#     def evaluate(self, path_folder_database):
#         base_dir = os.path.dirname(os.path.abspath(__file__))
#         full_db_path = os.path.abspath(os.path.join(base_dir, path_folder_database))

#         true = self.dataframe['label']
#         predicted = []
#         for _, row in self.dataframe.iterrows():
#             kalimat = row['kalimat']
#             file_database_json = os.path.join(full_db_path, row['database'])
#             predicted_label = self.detector.detect(kalimat=kalimat, file_database_json=file_database_json)
#             predicted.append(predicted_label)

#         labels = sorted(set(true) | set(predicted))

#         confusion_matrix = pd.crosstab(true, predicted, rownames=['Actual'], colnames=['Predicted'], dropna=False)
#         confusion_matrix = confusion_matrix.reindex(index=labels, columns=labels, fill_value=0)

#         metrics = pd.DataFrame(index=labels, columns=['precision', 'recall', 'f1'], dtype=float)

#         for label in labels:
#             TP = confusion_matrix.at[label, label]
#             FP = confusion_matrix[label].sum() - TP
#             FN = confusion_matrix.loc[label].sum() - TP

#             precision = TP/(TP+FP) if (TP + FP) > 0 else 0
#             recall = TP/(TP + FN) if (TP + FN) > 0 else 0
#             f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

#             metrics.loc[label] = [precision, recall, f1]


#         filtered = metrics.drop(index='NODML', errors='ignore')
#         metrics.loc['macro'] = [
#             round(filtered['precision'].mean(), 2),
#             round(filtered['recall'].mean(), 2),
#             round(filtered['f1'].mean(), 2)
#         ]
#         # metrics.loc['macro'] = [
#         #     round(metrics['precision'].mean(), 2),
#         #     round(metrics['recall'].mean(), 2),
#         #     round(metrics['f1'].mean(), 2)
#         # ]
#         accuracy = (true == predicted).mean()

#         print(f'Accuracy: {accuracy:.2f}')
#         print(metrics)


# dml_detector = DMLDetector()
# evaluator = Evaluator(path_file_dataset='evaluators/dataset_dml.xlsx', detector=dml_detector)
# evaluator.evaluate(path_folder_database='../databases/dml_detector/')