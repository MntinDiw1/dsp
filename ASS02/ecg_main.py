import os
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # run from any folder; paths are relative to this file

ECG_COLUMN = 8  # ADC channel 2

def load_ecg(filename):
    data = np.loadtxt(os.path.join("ECG_DATA", filename))
    t = data[:, 0]                       # column 0: time in seconds
    return t, data[:, ECG_COLUMN]

t, ecg = load_ecg("will_c_ecg1.tsv")
fs = 1 / (t[1] - t[0])                   # 250 Hz, taken from the file rather than hard-coded