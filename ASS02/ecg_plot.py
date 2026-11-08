'''
Plot the ECG in the time- and frequency domain (linear axis) and identify 
the ECG and the noise in the spectrum. There is certainly baseline 
wander and 50Hz interference but there might be other interferences. 
Decide which frequency components need to be removed. Identify these 
frequencies representing noise using your judgement and knowledge 
about harmonics
'''

import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt

from support_funcs import import_ecg_data, vector_plot_export

# ------ TASK 1 PLOTS ------ 
# Function to plot ECG signal in the time and frequency domain
def plot_ecg(name, sample_rate, ecg, beat_start, beat_end):
    n = len(ecg)
    time = np.arange(n) / sample_rate # array of times

    # Frequency domain (linear)
    ecg_fft = (1 / n) * fft(ecg)
    mag_fft = np.abs(ecg_fft)
    freqs = np.arange(n // 2) * sample_rate / n # frequency bins up to sample_rate/2

    plt.figure(figsize=(12, 8))
    plt.suptitle(f"ECG Analysis: {name}")

    # whole recording
    plt.subplot(2, 1, 1)
    plt.title("Time domain")
    plt.plot(time, ecg)
    plt.xlim(0, n / sample_rate)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")

    # zoomed in
    plt.subplot(2, 1, 2)
    plt.title("Zoomed: Two Peaks")
    plt.plot(time, ecg)
    plt.xlim(beat_start, beat_end)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")

    plt.tight_layout() # stop axes overlapping
    vector_plot_export("t1_time") # DO NOT SUBMIT WITHOUT COMMENTING OUT EXPORT CODE!!

    # --- figure 2: frequency domain ---
    plt.figure(figsize=(12, 8))
    plt.suptitle(f"ECG spectrum: {name}")

    plt.subplot(2, 1, 1)
    plt.title("Full spectrum")
    plt.plot(freqs[0:], mag_fft[0:n // 2])
    plt.xlim(0, sample_rate / 2)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (V)")

    # zoomed in spectrum
    plt.subplot(2, 1, 2)
    plt.title("Zoomed-in Spectrum")
    plt.plot(freqs[0:], mag_fft[0:n // 2])
    plt.xlim(0, sample_rate / 2)
    plt.ylim(0, 3e-5) # reveals the small peaks (TUNE IT)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (V)")

    plt.tight_layout() # stop axes overlapping
    vector_plot_export("t1_freq") # DO NOT SUBMIT WITHOUT COMMENTING OUT EXPORT CODE!!

# import ECG Data & plot
t, ecg, sample_rate = import_ecg_data("ecg1.tsv")
plot_ecg("Saad 2", sample_rate, ecg, 5.5, 6.7) # pick a window containing a single beat
plt.show()

#TODO: fix plot text, title, legend etc.