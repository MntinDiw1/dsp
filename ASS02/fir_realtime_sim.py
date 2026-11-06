# 3b & 4 - Simulating RT FIR and Adaptive LMS filtering importing fir_design and fir_filter.

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data, vector_plot_export

# --- 1. Load ECG Data ---
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")
n = len(ecg)

# --- 2. Design Fixed FIR Filter (Task 2 / Task 3) ---
# Frequency ranges to remove:
# - baseline_wander [0, 0.5] Hz: removes DC offset and slow respiration/movement drift.
# - mains_hum [45, 125] Hz: removes 50 Hz powerline interference and high-frequency noise
#   up to the Nyquist frequency (fs / 2 = 125 Hz), which is the maximum representable frequency.
baseline_wander = [0, 0.5]
mains_hum = [45, 125]

# fir_design calculates M = fs / (min_width / 2) = 250 / 0.25 = 1000 taps (0.25 Hz bin width),
# sets stopband bins to 0 on a folded symmetric frequency axis, takes the real IFFT,
# shifts the impulse response to be causal (centred at M/2), and applies a Hamming window.
h = fir_design(sample_rate, [baseline_wander, mains_hum])
M = len(h)

# --- 3. Set Up Adaptive LMS Filter (Task 4) ---
# Pre-remove DC / baseline wander (0 - 0.5 Hz) so the 50 Hz LMS canceller operates on a zero-mean ECG.
h_hp = fir_design(sample_rate, [baseline_wander])
hp_filter = FIRfilter(h_hp)

M_lms = 10               # Number of adaptive filter taps (1 period of 50 Hz at 250 Hz is 5 samples)
learning_rate = 0.01     # LMS step size (mu)
f_noise = 50.0           # 50 Hz mains interference reference frequency
lms_filter = FIRfilter(np.zeros(M_lms))

# --- 4. Real-Time Sample-by-Sample Filtering (Simple FIR & Adaptive LMS) ---
fir = FIRfilter(h)
ecg_filtered = np.zeros(n)
ecg_hp = np.zeros(n)
ecg_lms = np.zeros(n)

for i in range(n):
    # Simple fixed FIR filter (Task 3)
    ecg_filtered[i] = fir.dofilter(ecg[i])

    # Adaptive LMS filter (Task 4): high-pass filter first, then cancel 50 Hz interference
    ecg_hp[i] = hp_filter.dofilter(ecg[i])
    noise_ref = np.sin(2 * np.pi * f_noise * i / sample_rate)
    ecg_lms[i] = lms_filter.doFilterAdaptive(ecg_hp[i], noise_ref, learning_rate)

# --- 5. Plot Initial Transient & Two Heartbeat Periods (Task 3 Simple FIR vs Unfiltered) ---
group_delay = (M // 2) / sample_rate      # Linear-phase group delay: (M / 2) / fs = 2.0 s
transient_duration = M / sample_rate      # Full buffer fill time: M / fs = 4.0 s

plt.figure(figsize=(12, 8))
plt.suptitle("Real-Time FIR Filter: Initial Transient and Two-Heartbeat Comparison")

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

beat_start, beat_end = 5.2, 6.8  # ~1.6 s window covering two heartbeat periods (~1.5 Hz heart rate)
in_window = (t >= beat_start) & (t <= beat_end)
ecg_zero_mean = ecg - np.mean(ecg[in_window])

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

# --- 6. Plot Raw vs Filtered ECG (Time & Frequency Domain Overview) ---
freqs_ecg = np.arange(n // 2) * sample_rate / n
raw_fft = (1 / n) * np.abs(fft(ecg))
filt_fft = (1 / n) * np.abs(fft(ecg_filtered))
hp_fft = (1 / n) * np.abs(fft(ecg_hp))
lms_fft = (1 / n) * np.abs(fft(ecg_lms))

plt.figure(figsize=(12, 8))
plt.suptitle("Real-Time FIR Filtering of ECG Signal")

plt.subplot(3, 1, 1)
plt.title("Time Domain: Raw vs Filtered ECG")
plt.plot(t, ecg, alpha=0.5, label="Raw ECG")
plt.plot(t, ecg_filtered, label="Filtered ECG")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.subplot(3, 1, 2)
plt.title("Zoomed Single Heartbeat (PQRST Complex)")
plt.plot(t, ecg_filtered, color="tab:orange")
plt.xlim(5.5, 6.7)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.grid(True)

plt.subplot(3, 1, 3)
plt.title("Frequency Spectrum: Raw vs Filtered")
plt.plot(freqs_ecg[1:], raw_fft[1:n // 2], alpha=0.5, label="Raw Spectrum")
plt.plot(freqs_ecg[1:], filt_fft[1:n // 2], label="Filtered Spectrum")
plt.xlim(0, sample_rate / 2)
plt.ylim(0, 3e-5)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
vector_plot_export("t3_filtered")

# --- 7. Plot & Compare Adaptive LMS vs Task 3 Fixed FIR ---
plt.figure(figsize=(12, 8))
plt.suptitle(f"Task 4: Adaptive LMS Filter (M = {M_lms}, $\\mu$ = {learning_rate}) vs Task 3 Fixed FIR Filter")

plt.subplot(3, 1, 1)
plt.title("Time Domain: Baseline-Corrected ECG vs LMS Filtered vs Fixed FIR")
plt.plot(t, ecg_hp, alpha=0.4, label="HP Only (0-0.5 Hz removed)")
plt.plot(t, ecg_lms, label="Adaptive LMS (50 Hz cancelled)")
plt.plot(t, ecg_filtered, alpha=0.7, linestyle="--", label="Task 3 Fixed FIR")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.subplot(3, 1, 2)
plt.title("Two Heartbeat Periods: Adaptive LMS vs Fixed FIR")
plt.plot(t, ecg_hp, alpha=0.35, label="HP Only (with 50 Hz hum)")
plt.plot(t, ecg_lms, label="Adaptive LMS")
plt.plot(t, ecg_filtered, linestyle="--", label="Task 3 Fixed FIR")
plt.xlim(beat_start, beat_end)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.subplot(3, 1, 3)
plt.title("Frequency Spectrum Comparison")
plt.plot(freqs_ecg[1:], hp_fft[1:n // 2], alpha=0.4, label="HP Only")
plt.plot(freqs_ecg[1:], lms_fft[1:n // 2], label="Adaptive LMS")
plt.plot(freqs_ecg[1:], filt_fft[1:n // 2], linestyle="--", label="Task 3 Fixed FIR")
plt.xlim(0, sample_rate / 2)
plt.ylim(0, 3e-5)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V)")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
vector_plot_export("t4_compare")

plt.show()

