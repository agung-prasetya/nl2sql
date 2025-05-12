from sklearn.metrics import (
    accuracy_score, f1_score, hamming_loss,
    precision_score, recall_score, jaccard_score
)
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
import os
from detectors import ColumnDetector

class MultilabelEvaluator():
    def __init__(self, path_file_dataset, detector):
        self.dataframe = pd.read_excel(path_file_dataset, engine='openpyxl')
        self.detector = detector
    
    def evaluate(self, path_folder_database):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_db_path = os.path.abspath(os.path.join(base_dir, path_folder_database))

        y_true = []
        y_predicted = []
        for _, row in self.dataframe.iterrows():
            kalimat = row['kalimat']
            file_database_json = os.path.join(full_db_path, row['database'])
            
            labels = [label.strip() for label in row['label'].strip().split(',')]
            
            y_true.append(labels)

            predicted_label = self.detector.detect(kalimat=kalimat, file_database_json=file_database_json)

            y_predicted.append(predicted_label)

        binarizer = MultiLabelBinarizer()
        y_true_binerized = binarizer.fit_transform(y_true)
        y_predicted_binerized = binarizer.transform(y_predicted)

        exact_match_ratio = accuracy_score(y_true_binerized, y_predicted_binerized)
        precision_micro = precision_score(y_true_binerized, y_predicted_binerized, average='micro')
        recall_micro = recall_score(y_true_binerized, y_predicted_binerized, average='micro')
        f1_micro = f1_score(y_true_binerized, y_predicted_binerized, average='micro')

        precision_macro = precision_score(y_true_binerized, y_predicted_binerized, average='macro')
        recall_macro = recall_score(y_true_binerized, y_predicted_binerized, average='macro')
        f1_macro = f1_score(y_true_binerized, y_predicted_binerized, average='macro')

        hamming = hamming_loss(y_true_binerized, y_predicted_binerized)

        jaccard = jaccard_score(y_true_binerized, y_predicted_binerized, average='samples')

        # Print results
        print(f"Exact Match Ratio: {exact_match_ratio:.2f}")
        print(f"Micro Precision: {precision_micro:.2f}, Recall: {recall_micro:.2f}, F1: {f1_micro:.2f}")
        print(f"Macro Precision: {precision_macro:.2f}, Recall: {recall_macro:.2f}, F1: {f1_macro:.2f}")
        print(f"Hamming Loss: {hamming:.2f}")
        print(f"Jaccard Similarity: {jaccard:.2f}")

        return {
            'exact_match_ratio':exact_match_ratio,
            'micro':{
                'precision':precision_micro,
                'recall':recall_micro,
                'f1':f1_micro
            },
            'macro':{
                'precision':precision_macro,
                'recall':recall_macro,
                'f1':f1_macro
            },
            'hamming':hamming,
            'jaccard':jaccard
        }