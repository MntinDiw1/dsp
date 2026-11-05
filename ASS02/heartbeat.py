#5 - simulating real time heartbeat detection using fir_filter

import numpy as np
import matplotlib.pyplot as plt

from fir_design import fir_design, mathced_filter
from fir_filter import FIRfilter


#Load and format ECG data - CAN THIS BE STREAMLINED / CALLED FROM TASK 1?
ECG_COLUMN = 8
ECG_FILE = "saad_ecg_2.tsv" #ECG to analyse

TEMPLATE_ECG_FILE = "will_c_ecg2" #other lab partner's ECG #which of my ECG files to use?

def load_ecg(file):
        data = np.loadtxt(file)
        t = data[:, 0]
        return data[:, ECG_COLUMN], 1/(t[1] - t[0])

ecg, sample_rate = load_ecg(ECG_FILE)
template_ecg, template_sample_rate = load_ecg(TEMPLATE_ECG_FILE)


#Apply filter from Task 3
h = fir_design(sample_rate, [[0,0.5], [45, 125]]) #these values were already set previously, seems wasteful to call them again.

#Extract PQRST from TEMPLATE - AI, UNDERSTAND THIS SQUILLIAM
fir = FIRfilter(h)
template_clean = np.zeroes(len(template_ecg))
for i in range (len(template)):
        template_clean[i] = fir.dofilter(template_ecg[i])

