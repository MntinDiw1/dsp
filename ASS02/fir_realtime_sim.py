# 3b - Simulating realtime FIR filtering importing fir_design and fir_filter.

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data, vector_plot_export

# --- 1. Load ECG Data ---
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")
n = len(ecg)

# --- 2. Design FIR Filter (Task 2) ---
baseline_wander = [0, 0.5]  # Remove DC and low-frequency baseline drift
mains_hum = [45, 125]       # Remove 50 Hz mains hum and high-frequency noise up to Nyquist (fs/2)

h = fir_design(sample_rate, [baseline_wander, mains_hum])

# --- 3. Realtime Sample-by-Sample FIR Filtering (Task 3) ---
fir = FIRfilter(h)
ecg_filtered = np.zeros(n)

for i in range(n):
    ecg_filtered[i] = fir.dofilter(ecg[i])

# --- 4. Essential Plots: Filtered ECG (Time Domain, Zoomed Heartbeat, Frequency Spectrum) ---
freqs = np.arange(n // 2) * sample_rate / n
filt_fft = (1 / n) * np.abs(fft(ecg_filtered))

plt.figure(figsize=(12, 8))
plt.suptitle("Realtime FIR Filtered ECG")

# Full time domain
plt.subplot(3, 1, 1)
plt.title("Time Domain: Filtered ECG")
plt.plot(t, ecg_filtered)
plt.xlim(0, n / sample_rate)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")

# Zoomed single heartbeat (PQRST check)
plt.subplot(3, 1, 2)
plt.title("Zoomed Single Heartbeat (PQRST Complex)")
plt.plot(t, ecg_filtered)
plt.xlim(5.5, 6.7)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")

# Linear frequency spectrum
plt.subplot(3, 1, 3)
plt.title("Frequency Spectrum: Filtered ECG")
plt.plot(freqs, filt_fft[:n // 2])
plt.xlim(0, sample_rate / 2)
plt.ylim(0, 3e-5)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V)")

plt.tight_layout()
vector_plot_export("t3_filtered") # DO NOT SUBMIT WITHOUT COMMENTING OUT EXPORT CODE!!


# ==============================================================================
# --- NON-ESSENTIAL / EXTRA ANALYSIS PLOTS (Comment out or remove before submit)
# ==============================================================================

# Extra Plot 1: Task 2 FIR Filter Impulse & Frequency Response
M = len(h)
freqs_h = np.arange(M // 2 + 1) * sample_rate / M
H_mag = np.abs(fft(h))[:M // 2 + 1]

plt.figure(figsize=(12, 6))
plt.suptitle(f"FIR Filter Design (M = {M} taps, fs = {sample_rate:.0f} Hz)")

plt.subplot(2, 1, 1)
plt.title("Impulse Response h[n] (Shifted & Hamming Windowed)")
plt.plot(np.arange(M), h)
plt.xlim(0, M - 1)
plt.xlabel("Tap Index (n)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.title("Frequency Response |H(f)|")
plt.plot(freqs_h, H_mag)
plt.axvspan(0, 0.5, color="red", alpha=0.2, label="DC / Baseline Stopband (0-0.5 Hz)")
plt.axvspan(45, 125, color="orange", alpha=0.2, label="Mains / HF Stopband (45-125 Hz)")
plt.xlim(0, sample_rate / 2)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
vector_plot_export("t2_coeffs")

# Extra Plot 2: Initial Filter Transient & Delay-Aligned Unfiltered vs Filtered Comparison
group_delay = (M // 2) / sample_rate
transient_duration = M / sample_rate
beat_start, beat_end = 5.2, 6.8
in_window = (t >= beat_start) & (t <= beat_end)
ecg_zero_mean = ecg - np.mean(ecg[in_window])

plt.figure(figsize=(12, 8))
plt.suptitle("Realtime FIR Filter: Initial Transient and Two-Heartbeat Comparison")

plt.subplot(2, 1, 1)
plt.title(f"Initial Filter Transient (Buffer Fill = {transient_duration:.1f} s, Group Delay = {group_delay:.1f} s)")
plt.plot(t, ecg, alpha=0.5, label="Unfiltered ECG")
plt.plot(t, ecg_filtered, label="Filtered ECG")
plt.axvline(group_delay, color="red", linestyle="--", alpha=0.7, label=f"Group Delay ({group_delay:.1f} s)")
plt.axvline(transient_duration, color="green", linestyle=":", alpha=0.8, label=f"Transient Settled ({transient_duration:.1f} s)")
plt.xlim(0, 6.0)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.title("Two Heartbeat Periods: Unfiltered vs Filtered ECG")
plt.plot(t, ecg_zero_mean, alpha=0.5, label="Unfiltered ECG (DC mean subtracted)")
plt.plot(t, ecg_filtered, alpha=0.6, linestyle="--", label="Filtered ECG (with 2.0 s filter delay)")
plt.plot(t - group_delay, ecg_filtered, color="tab:orange", label="Filtered ECG (delay-aligned)")
plt.xlim(beat_start, beat_end)
plt.ylim(-1.2e-4, 2.0e-4)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
vector_plot_export("t3_transient_and_beats")

plt.show()
