import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from detector import *
from evaluator import *

detector = QtyDetector()
detector.detect('pertama 156.0001 3,89823888 Rp5.000.000,00')