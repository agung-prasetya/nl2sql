import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from detector import *
from evaluator import *
<<<<<<< HEAD
=======

filepath_dataset = str(Path(__file__).parent / 'dataset' / 'dataset.xlsx')
folderpath_database = str(Path(__file__).parent / 'dataset')
detector = UndefDetector()
evaluator=SingleLabelEvaluator(filepath_dataset=filepath_dataset,folderpath_database=folderpath_database, detector=detector)
evaluator.evaluate()
>>>>>>> 227bbeae17282e11182d16fcbd9b7ea00e8bae29
