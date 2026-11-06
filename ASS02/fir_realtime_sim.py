# 3b - Simulating RT FIR filtering importing fir_design and fir_filter.

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data, vector_plot_export

# --- 1. Load ECG Data ---
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")

# --- 2. Design FIR Filter ---
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

# --- 3. Real-Time Sample-by-Sample Filtering ---
# Instantiate FIRfilter directly (FIRfilter is the class imported from fir_filter)
fir = FIRfilter(h)
ecg_filtered = np.zeros(len(ecg))

for i in range(len(ecg)):
    ecg_filtered[i] = fir.dofilter(ecg[i])

# --- 4. Plot FIR Filter Design (Impulse & Frequency Response) ---
freqs_h = np.arange(M // 2 + 1) * sample_rate / M
h_fft = np.abs(fft(h))
H_mag = h_fft[:M // 2 + 1]

plt.figure(figsize=(12, 6))
plt.suptitle(f"FIR Filter Design (M = {M} taps, fs = {sample_rate:.0f} Hz)")

plt.subplot(2, 1, 1)
plt.title("Impulse Response h[n] (Shifted & Hamming Windowed)")
plt.plot(np.arange(M), h)
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
plt.legend()
plt.grid(True)
plt.tight_layout()
vector_plot_export("t2_coeffs")

# --- 5. Plot Raw vs Filtered ECG (Time & Frequency Domain) ---
n = len(ecg)
freqs_ecg = np.arange(n // 2) * sample_rate / n
raw_fft = (1 / n) * np.abs(fft(ecg))
filt_fft = (1 / n) * np.abs(fft(ecg_filtered))

plt.figure(figsize=(12, 8))
plt.suptitle("Real-Time FIR Filtering of ECG Signal")

plt.subplot(3, 1, 1)
plt.title("Time Domain: Raw vs Filtered ECG")
plt.plot(t, ecg, alpha=0.5, label="Raw ECG")
plt.plot(t, ecg_filtered, label="Filtered ECG")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.title("Zoomed Single Heartbeat (PQRST Complex)")
plt.plot(t, ecg_filtered, color="tab:orange")
plt.xlim(5.5, 6.5)
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
plt.legend()
plt.grid(True)
plt.tight_layout()
vector_plot_export("t3_filtered")

plt.show()
