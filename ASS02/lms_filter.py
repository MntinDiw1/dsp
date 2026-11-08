# 4 - Simulating realtime adaptive LMS filtering importing fir_filter.

import time #REMOVE FOR SUBMISSION
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from fir_filter import FIRfilter
from support_funcs import import_ecg_data

# Load ECG Data 
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")
n = len(ecg)

# sequential Adaptive LMS Filter Setup
# DC & baseline wander LMS canceller (constant reference = 1.0)
M_dc = 1
mu_dc = 0.0125 # justify learning rate?
lms_dc = FIRfilter(np.zeros(M_dc))

# 50 Hz mains hum LMS canceller (50 Hz sine reference)
M_50 = 10
mu_50 = 0.01 # justify learnign rate 
f_noise = 50.0
lms_50 = FIRfilter(np.zeros(M_50))

# realtime adaptive Filtering ---
ecg_lms = np.zeros(n)
lms_latency_us = np.zeros(n) #REMOVE FOR SUBMISSION

for i in range(n):
    t_start = time.perf_counter() #REMOVE FOR SUBMISSION

    # remove DC offset and slow baseline wander
    ecg_no_dc = lms_dc.doFilterAdaptive(ecg[i], 1.0, mu_dc)

    # remove 50 Hz powerline interference
    noise_50 = np.sin(2 * np.pi * f_noise * i / sample_rate)
    ecg_lms[i] = lms_50.doFilterAdaptive(ecg_no_dc, noise_50, mu_50)

    lms_latency_us[i] = (time.perf_counter() - t_start) * 1e6 #REMOVE FOR SUBMISSION

# Plotting (Raw ECG vs Adaptive LMS Filtered ECG)
freqs = np.arange(n // 2) * sample_rate / n
raw_fft = (1 / n) * np.abs(fft(ecg))
lms_fft = (1 / n) * np.abs(fft(ecg_lms))

beat_start, beat_end = 5.5, 6.7
in_beat = (t >= beat_start) & (t <= beat_end)

plt.figure(figsize=(12, 8))
plt.suptitle("Realtime Adaptive LMS Filtering: Raw vs LMS Filtered ECG")

# Full time domain
plt.subplot(3, 1, 1)
plt.title("Time Domain: Raw vs Adaptive LMS")
plt.plot(t, ecg, alpha=0.5, label="Raw ECG")
plt.plot(t, ecg_lms, label="Adaptive LMS")
plt.xlim(0, n / sample_rate)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")

# Zoomed single heartbeat (raw zero-meaned over window so both sit on 0 V for comparison)
plt.subplot(3, 1, 2)
plt.title("Zoomed Single Heartbeat (PQRST Complex): Raw vs Adaptive LMS")
plt.plot(t, ecg - np.mean(ecg[in_beat]), alpha=0.5, label="Raw ECG (DC mean subtracted)")
plt.plot(t, ecg_lms, label="Adaptive LMS")
plt.xlim(beat_start, beat_end)
plt.ylim(-0.5e-3, 1.5e-3)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude (V)")
plt.legend(loc="upper right")

# Linear frequency spectrum
plt.subplot(3, 1, 3)
plt.title("Frequency Spectrum: Raw vs Adaptive LMS")
plt.plot(freqs[1:], raw_fft[1:n // 2], alpha=0.5, label="Raw Spectrum")
plt.plot(freqs[1:], lms_fft[1:n // 2], label="Adaptive LMS Spectrum")
plt.xlim(0, sample_rate / 2)
plt.ylim(0, 3e-5)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (V)")
plt.legend(loc="upper right")

plt.tight_layout()


# ==============================================================================
# --- NON-ESSENTIAL / EXTRA ANALYSIS PLOTS (Comment out or remove before submit)
# ==============================================================================

from fir_design import fir_design #REMOVE FOR SUBMISSION
from support_funcs import vector_plot_export #REMOVE FOR SUBMISSION

# Fixed FIR filter from Task 3 for three-way comparison (Raw vs LMS vs Fixed FIR)
baseline_wander = [0, 0.5] #REMOVE FOR SUBMISSION
mains_hum = [45, 125] #REMOVE FOR SUBMISSION
h_fixed = fir_design(sample_rate, [baseline_wander, mains_hum]) #REMOVE FOR SUBMISSION
fixed_fir = FIRfilter(h_fixed) #REMOVE FOR SUBMISSION

ecg_fixed = np.zeros(n) #REMOVE FOR SUBMISSION
fir_latency_us = np.zeros(n) #REMOVE FOR SUBMISSION
for i in range(n): #REMOVE FOR SUBMISSION
    t_start = time.perf_counter() #REMOVE FOR SUBMISSION
    ecg_fixed[i] = fixed_fir.dofilter(ecg[i]) #REMOVE FOR SUBMISSION
    fir_latency_us[i] = (time.perf_counter() - t_start) * 1e6 #REMOVE FOR SUBMISSION

fixed_fft = (1 / n) * np.abs(fft(ecg_fixed)) #REMOVE FOR SUBMISSION
group_delay = (len(h_fixed) // 2) / sample_rate #REMOVE FOR SUBMISSION

# Extra Plot 1: Three-way signal comparison (Raw vs Adaptive LMS vs Fixed FIR)
plt.figure(figsize=(12, 8)) #REMOVE FOR SUBMISSION
plt.suptitle(f"Task 4 Comparison: Raw ECG vs Adaptive LMS ($M_{{50}}$ = {M_50}, $\\mu_{{50}}$ = {mu_50}) vs Task 3 Fixed FIR") #REMOVE FOR SUBMISSION

plt.subplot(3, 1, 1) #REMOVE FOR SUBMISSION
plt.title("Time Domain: Raw ECG vs Adaptive LMS vs Fixed FIR") #REMOVE FOR SUBMISSION
plt.plot(t, ecg, alpha=0.4, label="Raw ECG") #REMOVE FOR SUBMISSION
plt.plot(t, ecg_lms, label="Adaptive LMS") #REMOVE FOR SUBMISSION
plt.plot(t, ecg_fixed, alpha=0.8, linestyle="--", label="Task 3 Fixed FIR") #REMOVE FOR SUBMISSION
plt.xlim(0, n / sample_rate) #REMOVE FOR SUBMISSION
plt.xlabel("Time (s)") #REMOVE FOR SUBMISSION
plt.ylabel("Amplitude (V)") #REMOVE FOR SUBMISSION
plt.legend(loc="upper right") #REMOVE FOR SUBMISSION
plt.grid(True) #REMOVE FOR SUBMISSION

plt.subplot(3, 1, 2) #REMOVE FOR SUBMISSION
plt.title("Zoomed Single Heartbeat (PQRST Complex): Raw vs Adaptive LMS vs Fixed FIR") #REMOVE FOR SUBMISSION
plt.plot(t, ecg - np.mean(ecg[in_beat]), alpha=0.4, label="Raw ECG (DC mean subtracted)") #REMOVE FOR SUBMISSION
plt.plot(t, ecg_lms, label="Adaptive LMS") #REMOVE FOR SUBMISSION
plt.plot(t - group_delay, ecg_fixed, linestyle="--", label=f"Task 3 Fixed FIR (delay-aligned by {group_delay:.1f} s)") #REMOVE FOR SUBMISSION
plt.xlim(beat_start, beat_end) #REMOVE FOR SUBMISSION
plt.ylim(-0.5e-3, 1.5e-3) #REMOVE FOR SUBMISSION
plt.xlabel("Time (s)") #REMOVE FOR SUBMISSION
plt.ylabel("Amplitude (V)") #REMOVE FOR SUBMISSION
plt.legend(loc="upper right") #REMOVE FOR SUBMISSION
plt.grid(True) #REMOVE FOR SUBMISSION

plt.subplot(3, 1, 3) #REMOVE FOR SUBMISSION
plt.title("Frequency Spectrum Comparison: Raw vs Adaptive LMS vs Fixed FIR") #REMOVE FOR SUBMISSION
plt.plot(freqs[1:], raw_fft[1:n // 2], alpha=0.4, label="Raw Spectrum") #REMOVE FOR SUBMISSION
plt.plot(freqs[1:], lms_fft[1:n // 2], label="Adaptive LMS") #REMOVE FOR SUBMISSION
plt.plot(freqs[1:], fixed_fft[1:n // 2], linestyle="--", label="Task 3 Fixed FIR") #REMOVE FOR SUBMISSION
plt.xlim(0, sample_rate / 2) #REMOVE FOR SUBMISSION
plt.ylim(0, 3e-5) #REMOVE FOR SUBMISSION
plt.xlabel("Frequency (Hz)") #REMOVE FOR SUBMISSION
plt.ylabel("Magnitude (V)") #REMOVE FOR SUBMISSION
plt.legend(loc="upper right") #REMOVE FOR SUBMISSION
plt.grid(True) #REMOVE FOR SUBMISSION

plt.tight_layout() #REMOVE FOR SUBMISSION
vector_plot_export("t4_compare") #REMOVE FOR SUBMISSION

# Extra Plot 2: Execution Time & Per-Sample Latency Comparison (Adaptive LMS vs Fixed FIR)
lms_total_ms = np.sum(lms_latency_us) / 1e3 #REMOVE FOR SUBMISSION
fir_total_ms = np.sum(fir_latency_us) / 1e3 #REMOVE FOR SUBMISSION
lms_mean_us = np.mean(lms_latency_us) #REMOVE FOR SUBMISSION
fir_mean_us = np.mean(fir_latency_us) #REMOVE FOR SUBMISSION
lms_median_us = np.median(lms_latency_us) #REMOVE FOR SUBMISSION
fir_median_us = np.median(fir_latency_us) #REMOVE FOR SUBMISSION

print(f"Adaptive LMS ({M_dc + M_50} taps total) -> Total: {lms_total_ms:.2f} ms | Mean: {lms_mean_us:.2f} us/sample | Median: {lms_median_us:.2f} us/sample") #REMOVE FOR SUBMISSION
print(f"Fixed FIR ({len(h_fixed)} taps)        -> Total: {fir_total_ms:.2f} ms | Mean: {fir_mean_us:.2f} us/sample | Median: {fir_median_us:.2f} us/sample") #REMOVE FOR SUBMISSION

plt.figure(figsize=(12, 7)) #REMOVE FOR SUBMISSION
plt.suptitle("Computational Latency Comparison: Adaptive LMS vs Fixed FIR") #REMOVE FOR SUBMISSION

# Per-sample latency across the recording
plt.subplot(2, 1, 1) #REMOVE FOR SUBMISSION
plt.title("Per-Sample Processing Latency Over Time") #REMOVE FOR SUBMISSION
plt.plot(t, lms_latency_us, alpha=0.7, label=f"Adaptive LMS ({M_dc + M_50} taps, mean = {lms_mean_us:.2f} $\\mu$s)") #REMOVE FOR SUBMISSION
plt.plot(t, fir_latency_us, alpha=0.7, label=f"Fixed FIR ({len(h_fixed)} taps, mean = {fir_mean_us:.2f} $\\mu$s)") #REMOVE FOR SUBMISSION
plt.xlim(0, n / sample_rate) #REMOVE FOR SUBMISSION
plt.ylim(0, max(np.percentile(lms_latency_us, 99), np.percentile(fir_latency_us, 99)) * 1.5) #REMOVE FOR SUBMISSION
plt.xlabel("Time (s)") #REMOVE FOR SUBMISSION
plt.ylabel("Latency ($\\mu$s / sample)") #REMOVE FOR SUBMISSION
plt.legend(loc="upper right") #REMOVE FOR SUBMISSION
plt.grid(True) #REMOVE FOR SUBMISSION

# Bar chart comparing mean per-sample latency and total execution time
plt.subplot(2, 1, 2) #REMOVE FOR SUBMISSION
plt.title(f"Mean Per-Sample Latency & Total Runtime ({n} samples)") #REMOVE FOR SUBMISSION
methods = [f"Adaptive LMS\n({M_dc + M_50} taps, 0 s group delay)", f"Task 3 Fixed FIR\n({len(h_fixed)} taps, {group_delay:.1f} s group delay)"] #REMOVE FOR SUBMISSION
means = [lms_mean_us, fir_mean_us] #REMOVE FOR SUBMISSION
bars = plt.bar(methods, means, width=0.4, color=["tab:blue", "tab:orange"]) #REMOVE FOR SUBMISSION
plt.ylabel("Mean Latency ($\\mu$s / sample)") #REMOVE FOR SUBMISSION
plt.grid(axis="y") #REMOVE FOR SUBMISSION

for bar, total_ms in zip(bars, [lms_total_ms, fir_total_ms]): #REMOVE FOR SUBMISSION
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, f"{bar.get_height():.2f} $\\mu$s/sample\n(Total: {total_ms:.1f} ms)", ha="center", va="center", color="white", fontweight="bold") #REMOVE FOR SUBMISSION

plt.tight_layout() #REMOVE FOR SUBMISSION
vector_plot_export("t4_latency") #REMOVE FOR SUBMISSION

plt.show()
