import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from detector import *
from evaluator import *

detector = QtyDetector()
detector.detect('tampilkan total penjualan diatas Rp50.000.000,00 beserta nama pembelinya')
