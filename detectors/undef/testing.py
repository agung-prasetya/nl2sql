import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from detector import *
from evaluator import *

filepath_dataset = str(Path(__file__).parent / 'dataset' / 'dataset.xlsx')
folderpath_database = str(Path(__file__).parent / 'dataset')
detector = UndefDetector()
evaluator=SingleLabelEvaluator(filepath_dataset=filepath_dataset,folderpath_database=folderpath_database, detector=detector)
evaluator.evaluate()