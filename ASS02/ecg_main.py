import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from ecg_plot import plot_ecg #to class or not to class, that is the question

# --- IMPORT ECG DATA ---
ECG_COLUMN = 8  # ADC channel 2 (counting from 0)

data = np.loadtxt("ECG_DATA/saad_ecg_1.tsv")   # cd into ASS02
t = data[:, 0] # column 0: time (s)
ecg = data[:, ECG_COLUMN]
sample_rate = 1 / (t[1] - t[0]) # sample_rate = 250 Hz


# --- TASK 1 PLOTS ---
plot_ecg("Saad 1", sample_rate, ecg, 5.5, 6.5) # pick a window containing a single beat
plt.show()