# 4 - Simulating realtime adaptive LMS filtering importing fir_design and fir_filter.

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data, vector_plot_export

# --- 1. Load ECG Data ---
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")
n = len(ecg)

# --- 2. Filter Setup (Task 4 Adaptive LMS & Task 3 Fixed FIR for Comparison) ---
baseline_wander = [0, 0.5]
mains_hum = [45, 125]

# High-pass FIR filter to remove DC and baseline drift before 50 Hz LMS cancellation
h_hp = fir_design(sample_rate, [baseline_wander])
hp_filter = FIRfilter(h_hp)

# Fixed FIR filter from Task 3 for comparison
h_fixed = fir_design(sample_rate, [baseline_wander, mains_hum])
fixed_fir = FIRfilter(h_fixed)

# Adaptive LMS filter parameters
M_lms = 10               # Number of adaptive taps (1 period of 50 Hz at 250 Hz is 5 samples)
learning_rate = 0.01     # LMS step size (mu)
f_noise = 50.0           # 50 Hz mains interference reference frequency
lms_filter = FIRfilter(np.zeros(M_lms))

# --- 3. Realtime Sample-by-Sample Filtering ---
ecg_hp = np.zeros(n)
ecg_lms = np.zeros(n)
ecg_fixed = np.zeros(n)

for i in range(n):
    ecg_hp[i] = hp_filter.dofilter(ecg[i])
    noise_ref = np.sin(2 * np.pi * f_noise * i / sample_rate)
    ecg_lms[i] = lms_filter.doFilterAdaptive(ecg_hp[i], noise_ref, learning_rate)
    ecg_fixed[i] = fixed_fir.dofilter(ecg[i])

# --- 4. Essential Plots: Adaptive LMS vs Fixed FIR (Time, Zoomed Heartbeat, Spectrum) ---
freqs = np.arange(n // 2) * sample_rate / n
lms_fft = (1 / n) * np.abs(fft(ecg_lms))
fixed_fft = (1 / n) * np.abs(fft(ecg_fixed))

plt.figure(figsize=(12, 8))
plt.suptitle("Adaptive LMS Filter vs Fixed FIR Filter")

# Full time domain
plt.subplot(3, 1, 1)
plt.title("Time Domain: Adaptive LMS vs Fixed FIR")
plt.plot(t, ecg_lms, label="Adaptive LMS")
plt.plot(t, ecg_fixed, linestyle="--", label="Fixed FIR")
plt.xlim(0, n / sample_rate)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")

# Zoomed single heartbeat (PQRST comparison)
plt.subplot(3, 1, 2)
plt.title("Zoomed Single Heartbeat (PQRST Complex)")
plt.plot(t, ecg_lms, label="Adaptive LMS")
plt.plot(t, ecg_fixed, linestyle="--", label="Fixed FIR")
plt.xlim(5.5, 6.7)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")

# Linear frequency spectrum
plt.subplot(3, 1, 3)
plt.title("Frequency Spectrum: Adaptive LMS vs Fixed FIR")
plt.plot(freqs, lms_fft[:n // 2], label="Adaptive LMS")
plt.plot(freqs, fixed_fft[:n // 2], linestyle="--", label="Fixed FIR")
plt.xlim(0, sample_rate / 2)
plt.ylim(0, 3e-5)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V)")
plt.legend(loc="upper right")

plt.tight_layout()


# ==============================================================================
# --- NON-ESSENTIAL / EXTRA ANALYSIS PLOTS (Comment out or remove before submit)
# ==============================================================================

# Extra Plot 1: Full Report Comparison Including HP-Only Intermediate Signal
hp_fft = (1 / n) * np.abs(fft(ecg_hp))
beat_start, beat_end = 5.2, 6.8

plt.figure(figsize=(12, 8))
plt.suptitle(f"Task 4: Adaptive LMS Filter (M = {M_lms}, $\\mu$ = {learning_rate}) vs Task 3 Fixed FIR Filter")

plt.subplot(3, 1, 1)
plt.title("Time Domain: Baseline-Corrected ECG vs LMS Filtered vs Fixed FIR")
plt.plot(t, ecg_hp, alpha=0.4, label="HP Only (0-0.5 Hz removed)")
plt.plot(t, ecg_lms, label="Adaptive LMS (50 Hz cancelled)")
plt.plot(t, ecg_fixed, alpha=0.7, linestyle="--", label="Task 3 Fixed FIR")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.subplot(3, 1, 2)
plt.title("Two Heartbeat Periods: Adaptive LMS vs Fixed FIR")
plt.plot(t, ecg_hp, alpha=0.35, label="HP Only (with 50 Hz hum)")
plt.plot(t, ecg_lms, label="Adaptive LMS")
plt.plot(t, ecg_fixed, linestyle="--", label="Task 3 Fixed FIR")
plt.xlim(beat_start, beat_end)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.subplot(3, 1, 3)
plt.title("Frequency Spectrum Comparison")
plt.plot(freqs[1:], hp_fft[1:n // 2], alpha=0.4, label="HP Only")
plt.plot(freqs[1:], lms_fft[1:n // 2], label="Adaptive LMS")
plt.plot(freqs[1:], fixed_fft[1:n // 2], linestyle="--", label="Task 3 Fixed FIR")
plt.xlim(0, sample_rate / 2)
plt.ylim(0, 3e-5)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
vector_plot_export("t4_compare") # DO NOT SUBMIT WITHOUT COMMENTING OUT EXPORT CODE!!

plt.show()
