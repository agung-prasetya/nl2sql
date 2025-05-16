import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from detector import *
from evaluator import *

detector = QtyDetector()
detector.detect('tampilkan data produk sebanyak lima puluh dua dan tampilkan keseratus dua puluh lima beserta data kelima untuk nama pemasok')