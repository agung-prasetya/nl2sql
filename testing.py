from evaluators import *
from detectors import *

detector = ColumnDetector()
evaluator = MultilabelEvaluator(path_file_dataset='evaluators/dataset_column.xlsx', detector=detector)
evaluator.evaluate(path_folder_database='../databases/column_detector/')