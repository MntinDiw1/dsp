# 4 - Simulating RT LMS filtering importing fir_filter

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data, vector_plot_export

# --- 1. Load ECG Data ---
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")
N = len(ecg)

# --- 2. Pre-remove DC / Baseline Wander (0 - 0.5 Hz High-Pass FIR) ---
# Removes DC offset and slow baseline drift so the 50 Hz LMS canceller operates on a zero-mean ECG.
h_hp = fir_design(sample_rate, [[0, 0.5]])
hp_filter = FIRfilter(h_hp)

# Fixed FIR filter from Task 3 (for comparison)
h_fixed = fir_design(sample_rate, [[0, 0.5], [45, 125]])
fixed_fir = FIRfilter(h_fixed)

# --- 3. Real-Time Sample-by-Sample LMS Filtering ---
M_lms = 10               # Number of adaptive filter taps (1 period of 50 Hz at 250 Hz is 5 samples)
learning_rate = 0.01     # LMS step size (mu)
f_noise = 50.0           # 50 Hz mains interference reference frequency

lms = FIRfilter(np.zeros(M_lms))

ecg_hp = np.zeros(N)
ecg_lms = np.zeros(N)
ecg_fixed = np.zeros(N)

for n in range(N):
    # Step 1: High-pass filter raw sample to remove DC / baseline wander
    ecg_hp[n] = hp_filter.dofilter(ecg[n])

    # Step 2: Generate scalar 50 Hz reference noise and run adaptive LMS step
    noise = np.sin(2 * np.pi * f_noise * n / sample_rate)
    ecg_lms[n] = lms.doFilterAdaptive(ecg_hp[n], noise, learning_rate)

    # Task 3 fixed FIR filter output for direct comparison
    ecg_fixed[n] = fixed_fir.dofilter(ecg[n])

# --- 4. Plot & Compare Adaptive LMS vs Task 3 Fixed FIR ---
freqs = np.arange(N // 2) * sample_rate / N
hp_fft = (1 / N) * np.abs(fft(ecg_hp))
lms_fft = (1 / N) * np.abs(fft(ecg_lms))
fixed_fft = (1 / N) * np.abs(fft(ecg_fixed))

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
plt.title("Zoomed Single Heartbeat (PQRST Complex Comparison)")
plt.plot(t, ecg_hp, alpha=0.35, label="HP Only (with 50 Hz hum)")
plt.plot(t, ecg_lms, label="Adaptive LMS")
plt.plot(t, ecg_fixed, linestyle="--", label="Task 3 Fixed FIR")
plt.xlim(5.5, 6.7)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.subplot(3, 1, 3)
plt.title("Frequency Spectrum Comparison")
plt.plot(freqs[1:], hp_fft[1:N // 2], alpha=0.4, label="HP Only")
plt.plot(freqs[1:], lms_fft[1:N // 2], label="Adaptive LMS")
plt.plot(freqs[1:], fixed_fft[1:N // 2], linestyle="--", label="Task 3 Fixed FIR")
plt.xlim(0, sample_rate / 2)
plt.ylim(0, 3e-5)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
vector_plot_export("t4_compare")

plt.show()


from support_funcs import import_ecg_data

# --- 1. Load ECG Data ---
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")
