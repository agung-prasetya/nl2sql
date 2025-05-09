import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
# from detectors.dml_detector import DMLDetector
# from detectors.ddl_detector import DDLDetector
from detectors.sorting_detector import SortingDetector

class Evaluator():
    def __init__(self, path_file_dataset, detector):
        self.dataframe = pd.read_excel(path_file_dataset, engine='openpyxl')
        self.detector = detector

    def evaluate(self, path_folder_database):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_db_path = os.path.abspath(os.path.join(base_dir, path_folder_database))

        true = self.dataframe['label']
        predicted = []
        for _, row in self.dataframe.iterrows():
            kalimat = row['kalimat']
            file_database_json = os.path.join(full_db_path, row['database'])
            predicted_label = self.detector.detect(kalimat=kalimat, file_database_json=file_database_json)
            predicted.append(predicted_label)

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

            metrics.loc[label] = [precision, recall, f1]

        accuracy = (true == predicted).mean()

        print(f'Accuracy: {accuracy:.2f}')
        print(metrics)


detector = SortingDetector()

evaluator = Evaluator(path_file_dataset='evaluators/dataset_sorting.xlsx', detector=detector)
evaluator.evaluate(path_folder_database='../databases/sorting_detector/')