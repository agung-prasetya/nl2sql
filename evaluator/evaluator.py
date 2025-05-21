from pathlib import Path
from sklearn.metrics import (
    accuracy_score, f1_score, hamming_loss,
    precision_score, recall_score, jaccard_score
)
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
from detectors import *

class SingleLabelEvaluator():
    def __init__(self, filepath_dataset, folderpath_database, detector):
        self.dataframe = pd.read_excel(filepath_dataset, engine='openpyxl')
        self.dataframe.sort_values('database')
        self.folderpath_database = folderpath_database
        self.detector = detector

    def evaluate(self):        
        
        y_true = self.dataframe['label']
        y_predicted = []
        
        for id, row in self.dataframe.iterrows():
            kalimat = row['kalimat']
            
            filepath_database_json = str(Path(self.folderpath_database)/row['database'])
            predicted_label = self.detector.detect(kalimat=kalimat, filepath_database_json=filepath_database_json)
            
            y_predicted.append(predicted_label)
            print(f"{id};{row['label']};{predicted_label};{kalimat}")

        labels = sorted(set(y_true) | set(y_predicted))

        confusion_matrix = pd.crosstab(y_true, y_predicted, rownames=['Actual'], colnames=['Predicted'], dropna=False)
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

        accuracy = (y_true == y_predicted).mean()

        print(f'Accuracy: {accuracy:.2f}')
        print(metrics)

        return {'accuracy':accuracy, 'metrics':metrics}


class MultiLabelEvaluator():
    def __init__(self, filepath_dataset, folderpath_database, detector):
        self.dataframe = pd.read_excel(filepath_dataset, engine='openpyxl')
        self.dataframe.sort_values('database')
        self.folderpath_database = folderpath_database
        self.detector = detector

    def evaluate(self):
        y_true = []
        y_predicted = []
        for id, row in self.dataframe.iterrows():
            kalimat = row['kalimat']

            filepath_database_json = str(Path(self.folderpath_database)/row['database'])
            predicted_label = self.detector.detect(kalimat=kalimat, filepath_database_json=filepath_database_json)
            
            y_predicted.append(predicted_label)

            labels = [label.strip() for label in row['label'].strip().split(',')]
            y_true.append(labels)
            
            print(f"{labels==predicted_label};{id};{labels};{predicted_label};{kalimat}")

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
            'hamming':hamming
        }