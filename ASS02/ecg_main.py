import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft


# --- IMPORT ECG DATA ---
ECG_COLUMN = 8  # ADC channel 2 (counting from 0)

data = np.loadtxt("ECG_DATA/saad_ecg_1.tsv")   # cd into ASS02
t = data[:, 0] # column 0: time (s)
ecg = data[:, ECG_COLUMN]
sample_rate = 1 / (t[1] - t[0]) # sample_rate = 250 Hz

# --- TASK 1 PLOTS --- 

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
    plt.subplot(3, 1, 1)
    plt.title("time domain")
    plt.plot(time, ecg)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude (V)")

    # one heartbeat (PQRST)
    plt.subplot(3, 1, 2)
    plt.title("one heartbeat")
    plt.plot(time, ecg)
    plt.xlim(beat_start, beat_end)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude (V)")

    # frequency domain
    plt.subplot(3, 1, 3)
    plt.title("frequency domain")
    plt.plot(freqs[1:], mag_fft[1:n // 2]) # skip bin 0 [WHY???]
    plt.xlabel("frequency (Hz)")
    plt.ylabel("magnitude (V)")
    plt.ylim(0, 0.00001) #TOGGLE: make small peaks more visible

    plt.tight_layout() # stop axes overlapping


plot_ecg("Saad 1", sample_rate, ecg, 5.5, 6.5) # pick a window containing a single beat
plt.show()