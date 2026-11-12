# Task 3b - Simulating realtime FIR filtering importing fir_design and fir_filter.

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data

# FIR Filter params from Task 2 (also used by heartbeat.py)
BASELINE_WANDER = [0, 0.5]  # Remove DC and low-frequency baseline drift
MAINS_AND_HF_HUM = [45, 125]  # Remove 50 Hz mains hum and high-frequency noise up to Nyquist (fs/2)

def run_fir_filter(ecg, sample_rate):
    # generate list of tap coeffs
    h = fir_design(sample_rate, [BASELINE_WANDER, MAINS_AND_HF_HUM])

    # create object and generate output list
    fir = FIRfilter(h)
    ecg_filtered = []

    for sample in ecg:
        ecg_filtered.append(fir.dofilter(sample))

    # convert list into np to plot
    ecg_filtered = np.array(ecg_filtered)
    group_delay = (len(h) // 2) / sample_rate # linear-phase FIR delay: centre tap is at M/2 after the half swap
    print(f"FIR filter: M = {len(h)} taps, group delay = {group_delay:.3f} s")

    return ecg_filtered, group_delay


if __name__ == "__main__": # since its being imported we need to prevent plotting repeats
    # load ECG Data
    t, ecg, sample_rate = import_ecg_data("ecg1.tsv")

    ecg_filtered, group_delay = run_fir_filter(ecg, sample_rate)
    n = len(ecg_filtered)

    # generate plots
    # Filtered ECG (Time Domain, Zoomed Heartbeat, Frequency Spectrum) ---
    freqs = np.arange(n // 2) * sample_rate / n
    raw_fft = (1 / n) * np.abs(fft(ecg))
    filt_fft = (1 / n) * np.abs(fft(ecg_filtered))

    beat_start, beat_end = 5.5, 6.7
    in_beat = (t >= beat_start) & (t <= beat_end)

    plt.figure(figsize=(12, 8))
    plt.suptitle("Task 3: Realtime FIR Filtered ECG: ECG 1")

    # Full time domain
    plt.subplot(3, 1, 1)
    plt.title("Time Domain: Raw vs Filtered ECG")
    plt.plot(t, ecg, alpha=0.5, label="Unfiltered ECG")
    plt.plot(t, ecg_filtered, label="Filtered ECG")
    plt.xlim(0, n / sample_rate)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")
    plt.legend(loc="upper right")
    plt.grid()

    # Zoomed single heartbeat (PQRST check)
    plt.subplot(3, 1, 2)
    plt.title("Zoomed Heartbeat (PQRST Complex): Raw vs Filtered ECG")
    plt.plot(t, ecg - np.mean(ecg[in_beat]), alpha=0.5, label="Unfiltered ECG (DC mean subtracted)")
    plt.plot(t - group_delay, ecg_filtered, label=f"Filtered ECG (delay-aligned by {group_delay:.1f} s)")
    plt.xlim(beat_start, beat_end)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")
    plt.legend(loc="lower right")
    plt.grid()

    # Linear frequency spectrum
    plt.subplot(3, 1, 3)
    plt.title("Frequency Spectrum: Raw vs Filtered ECG")
    plt.plot(freqs, raw_fft[:n // 2], alpha=0.5, label="Unfiltered Spectrum")
    plt.plot(freqs, filt_fft[:n // 2], label="Filtered Spectrum")
    plt.xlim(0, sample_rate / 2)
    plt.ylim(0, 3e-5)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (V)")
    plt.legend(loc="upper right")
    plt.grid()

    plt.tight_layout()
    plt.show()