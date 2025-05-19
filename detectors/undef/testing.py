import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from detector import *
from evaluator import *

detector = UndefDetector()
filepath_database = str(Path(__file__).parent/'dataset/inventori_2.json')
detector.detect('Singkirkan tabel sementara itu.',filepath_database_json=filepath_database)