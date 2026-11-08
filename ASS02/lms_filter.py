# Task 4b - Simulating realtime adaptive LMS filtering importing fir_filter.

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from fir_filter import FIRfilter
from fir_realtime_sim import run_fir_filter
from support_funcs import import_ecg_data

# Load ECG Data
t, ecg, sample_rate = import_ecg_data("ecg1.tsv")

# Run Task 3 FIR filter for comparison
ecg_fir, group_delay = run_fir_filter(ecg, sample_rate)

# Adaptive LMS Filter Setup: two cancellers in series

# DC / baseline wander canceller (constant reference = 1.0)
M_DC = 1 # number of taps
mu_dc = 0.0125 # learning rate
lms_dc = FIRfilter(np.zeros(M_DC)) # generate buffer array

# 50 Hz mains canceller (50 Hz sine reference)
M_lms = 10 # number of taps
mu_lms = 0.01 # learnign rate
f_noise = 50.0 # ref signal frequency
lms = FIRfilter(np.zeros(M_lms)) # generate buffer aray

# Realtime Adaptive Filtering
ecg_lms = [] # results list

for i, sample in enumerate(ecg):

    # remove DC / baseline wander
    ecg_no_dc = lms_dc.doFilterAdaptive(sample, 1.0, mu_dc)
    # remove 50 Hz powerline interference
    noise_50 = np.sin(2 * np.pi * f_noise * i / sample_rate)
    ecg_lms.append(lms.doFilterAdaptive(ecg_no_dc, noise_50, mu_lms))

ecg_lms = np.array(ecg_lms) # convert to np array to plot
n = len(ecg_lms)

# Plotting (FIR Filtered ECG vs Adaptive LMS Filtered ECG)
freqs = np.arange(n // 2) * sample_rate / n
fir_fft = (1 / n) * np.abs(fft(ecg_fir))
lms_fft = (1 / n) * np.abs(fft(ecg_lms))

beat_start, beat_end = 5.5, 6.7

plt.figure(figsize=(12, 8))
plt.suptitle("Task 4: Realtime Adaptive LMS vs FIR Filtered ECG: ECG 1")

# Full time domain
plt.subplot(3, 1, 1)
plt.title("Time Domain: FIR vs Adaptive LMS Filtered ECG")
plt.plot(t, ecg_fir, alpha=0.7, label="FIR Filtered ECG")
plt.plot(t, ecg_lms, alpha=0.8, label="Adaptive LMS Filtered ECG")
plt.xlim(0, n / sample_rate)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid()

# Zoomed single heartbeat (PQRST check)
plt.subplot(3, 1, 2)
plt.title("Zoomed Heartbeat (PQRST Complex): FIR vs Adaptive LMS Filtered ECG")
plt.plot(t - group_delay, ecg_fir, alpha=0.8, label=f"FIR Filtered ECG (delay-aligned by {group_delay:.1f} s)")
plt.plot(t, ecg_lms, alpha=0.8, label="Adaptive LMS Filtered ECG")
plt.xlim(beat_start, beat_end)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="lower right")
plt.grid()

# Linear frequency spectrum
plt.subplot(3, 1, 3)
plt.title("Frequency Spectrum: FIR vs Adaptive LMS Filtered ECG")
plt.plot(freqs, fir_fft[:n // 2], alpha=0.7, label="FIR Spectrum")
plt.plot(freqs, lms_fft[:n // 2], alpha=0.8, label="Adaptive LMS Spectrum")
plt.xlim(0, sample_rate / 2)
plt.ylim(0, 3e-5)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V)")
plt.legend(loc="upper right")
plt.grid()

plt.tight_layout()
plt.show()