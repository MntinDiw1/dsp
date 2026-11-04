import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from ecg_plot import plot_ecg #to class or not to class, that is the question




# --- TASK 1 PLOTS ---
plot_ecg("Saad 2", sample_rate, ecg, 5.5, 6.5) # pick a window containing a single beat
plt.show()