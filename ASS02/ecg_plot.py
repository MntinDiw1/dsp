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
    plt.title("time domain")
    plt.plot(time, ecg)
    plt.xlim(0, n / sample_rate)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude (V)")

    # one heartbeat (PQRST)
    plt.subplot(2, 1, 2)
    plt.title("one heartbeat")
    plt.plot(time, ecg)
    plt.xlim(beat_start, beat_end)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude (V)")

    plt.tight_layout() # stop axes overlapping
    vector_plot_export("t1_time")

    # --- figure 2: frequency domain ---
    plt.figure(figsize=(12, 8))
    plt.suptitle(f"ECG spectrum: {name}")

    plt.subplot(2, 1, 1)
    plt.title("full spectrum")
    plt.plot(freqs[0:], mag_fft[0:n // 2])
    plt.xlim(0, sample_rate / 2)
    plt.xlabel("frequency (Hz)")
    plt.ylabel("magnitude (V)")

    # zoomed in spectrum
    plt.subplot(2, 1, 2)
    plt.title("zoomed-in spectrum")
    plt.plot(freqs[0:], mag_fft[0:n // 2])
    plt.xlim(0, sample_rate / 2)
    plt.ylim(0, 3e-5) # reveals the small peaks (TUNE IT)
    plt.xlabel("frequency (Hz)")
    plt.ylabel("magnitude (V)")

    plt.tight_layout() # stop axes overlapping
    vector_plot_export("t1_freq")

# --- IMPORT ECG DATA ---
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")
plot_ecg("Saad 2", sample_rate, ecg, 5.5, 6.7) # pick a window containing a single beat
plt.show()

#TODO: fix plot text, title, legend etc.