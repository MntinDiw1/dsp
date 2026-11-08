from pathlib import Path
import time  # REMOVE FOR SUBMISSION
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR if (SCRIPT_DIR / "ecg1.tsv").exists() else SCRIPT_DIR.parent


def import_ecg_data(filename):
    """
    Parameters:
    filename: str or Path
        The name of the file containing the ECG data.

    Returns:
    tuple[np.ndarray, np.ndarray, float]
        (t, ecg, sample_rate) - time vector (s), ECG signal (V), and sampling rate (Hz).
    """
    ECG_COLUMN = 8  # ADC channel 2
    data = np.loadtxt(BASE_DIR / filename)
    t = data[:, 0]
    ecg = data[:, ECG_COLUMN]
    sample_rate = 1 / (t[1] - t[0])  # fs = 250 Hz

    return t, ecg, sample_rate


def vector_plot_export(savename):
    """
    Exports the current matplotlib figure as vector graphics (.svg and .pdf) to Report/figs/.

    Parameters:
    savename: str or Path
        Output file name (without extension).
    """
    figs_dir = BASE_DIR / "Report" / "figs"
    figs_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(savename).stem
    plt.savefig(figs_dir / f"{stem}.svg", format="svg", bbox_inches="tight")
    plt.savefig(figs_dir / f"{stem}.pdf", format="pdf", bbox_inches="tight")


# ==============================================================================
# ------ TASK 1: TIME AND FREQUENCY DOMAIN ECG ANALYSIS ------
# ==============================================================================
'''
Plot the ECG in the time- and frequency domain (linear axis) and identify 
the ECG and the noise in the spectrum. There is certainly baseline 
wander and 50Hz interference but there might be other interferences. 
Decide which frequency components need to be removed. Identify these 
frequencies representing noise using your judgement and knowledge 
about harmonics
'''


def plot_ecg(name, sample_rate, ecg, beat_start, beat_end):
    n = len(ecg)
    time_axis = np.arange(n) / sample_rate  # array of times

    # Frequency domain (linear)
    ecg_fft = (1 / n) * fft(ecg)
    mag_fft = np.abs(ecg_fft)
    freqs = np.arange(n // 2) * sample_rate / n  # frequency bins up to sample_rate/2

    plt.figure(figsize=(12, 8))
    plt.suptitle(f"ECG Analysis: {name}")

    # whole recording
    plt.subplot(2, 1, 1)
    plt.title("Time domain")
    plt.plot(time_axis, ecg)
    plt.xlim(0, n / sample_rate)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")

    # zoomed in
    plt.subplot(2, 1, 2)
    plt.title("Zoomed: Two Peaks")
    plt.plot(time_axis, ecg)
    plt.xlim(beat_start, beat_end)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")

    plt.tight_layout()  # stop axes overlapping
    vector_plot_export("t1_time")  # DO NOT SUBMIT WITHOUT COMMENTING OUT EXPORT CODE!!

    # --- figure 2: frequency domain ---
    plt.figure(figsize=(12, 8))
    plt.suptitle(f"ECG spectrum: {name}")

    plt.subplot(2, 1, 1)
    plt.title("Full spectrum")
    plt.plot(freqs[0:], mag_fft[0:n // 2])
    plt.xlim(0, sample_rate / 2)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (V)")

    # zoomed in spectrum
    plt.subplot(2, 1, 2)
    plt.title("Zoomed-in Spectrum")
    plt.plot(freqs[0:], mag_fft[0:n // 2])
    plt.xlim(0, sample_rate / 2)
    plt.ylim(0, 3e-5)  # reveals the small peaks (TUNE IT)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (V)")

    plt.tight_layout()  # stop axes overlapping
    vector_plot_export("t1_freq")  # DO NOT SUBMIT WITHOUT COMMENTING OUT EXPORT CODE!!


# Import primary ECG data & plot Task 1
t, ecg, sample_rate = import_ecg_data("ecg1.tsv")
n = len(ecg)
plot_ecg("Saad 2", sample_rate, ecg, 5.5, 6.7)  # pick a window containing a single beat


# ==============================================================================
# ------ TASK 2: FIR FILTER COEFFICIENT DESIGN ------
# ==============================================================================
def fir_design(sample_rate, ranges):
    ranges = np.array(ranges)
    min_width = np.min(ranges[:, 1] - ranges[:, 0])

    bin_size = min_width / 2
    M = int(sample_rate / bin_size)  # number of coefficients (explain!)

    M += M % 2  # ensure M is even

    '''
    The number of coefficients, M, is calculated based on the minimum width of the frequency range arguments.
    The minimum width is divided by 2 so that each range always has at least 2 bins to operate on.
    The number of coefficients is then calculated by dividing the sample rate by the bin size.
    M is made even so that the impulse response can be split into two equal halves when it is shifted.
    '''

    # Using folded axis to create a symmetric frequency response
    f = np.arange(M) * sample_rate / M  # freq. of each bin
    f = np.minimum(f, sample_rate - f)  # fold: bin M-k gets the same freq. as bin k
    H = np.ones(M)  # initialise frequencies to 1 (pass band)

    # define low and high
    for low, high in ranges:
        H[(f >= low) & (f <= high)] = 0  # remove bins in range (set to 0)

    # IFFT - produces the impulse response, keeping only the real part (H is mirrored, so complex cancels)
    h = np.real(ifft(H))

    # Swap the two halves (see 6.7.6 or Bernd's notes)
    h_shift = np.zeros(M)
    h_shift[0:M // 2] = h[M // 2:M]
    h_shift[M // 2:M] = h[0:M // 2]

    h_windowed = h_shift * np.hamming(M)

    '''
    Edge cases (DC and Nyquist) are covered by the folded axis (bin 0 and bin 125 [fs/2])
    '''
    return h_windowed


# Design FIR filter for Task 2 & subsequent tasks
baseline_wander = [0, 0.5]  # Remove DC and low-frequency baseline drift
mains_hum = [45, 125]       # Remove 50 Hz mains hum and high-frequency noise up to Nyquist (fs/2)

h = fir_design(sample_rate, [baseline_wander, mains_hum])
M = len(h)

# Plot Task 2 FIR Filter Impulse & Frequency Response
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
vector_plot_export("t2_coeffs")  # DO NOT SUBMIT WITHOUT COMMENTING OUT EXPORT CODE!!


# ==============================================================================
# ------ TASK 3: REALTIME FIR FILTER CLASS & SIMULATION ------
# ==============================================================================
'''
Create a Python FIR filter class which implements an FIR filter which has 
a method of the form value dofilter(self,value) where both the value 
argument and return value are scalars and not vectors (!) so that it can 
be used in a realtime system. The constructor of the class takes the 
coefficients as its input:
    class FIRfilter:
        def __init__(self,_coefficients):
            # your code here
        def dofilter(self,v):
            # your code here
        return result
Filter your ECG with the above FIR filter class using the coefficients from Task 2.
'''


class FIRfilter:
    def __init__(self, _coefficients):
        """
        Parameters:
        fir_coefficients: array
            The M filter coefficients calculated in Task 2.
        """
        self.coefficients = np.array(_coefficients, dtype=float)  # load coefficients into object
        self.ntaps = len(self.coefficients)  # get buffer array length

        self.buffer = np.zeros(self.ntaps, dtype=float)  # generate buffer array

        self.offset = 0  # set offset to zero

    def dofilter(self, v):
        """
        Parameters:
        v: float
            The incoming input sample x[n].

        Returns:
        float
            The filtered output sample y[n].
        """
        self.buffer[self.offset] = v  # load current sample into buffer

        k = self.offset + 1
        # output = sum[0:M-1](h(m) \dot x(n-m))
        output = (
            np.dot(self.coefficients[:k], self.buffer[self.offset::-1])  # fwd sum
            + np.dot(self.coefficients[k:], self.buffer[:self.offset:-1])  # backward sum
        )  # dot product multiply coefficients with samples in object

        # iterate offset position, reset to zero
        if self.offset == self.ntaps - 1:
            self.offset = 0
        else:
            self.offset += 1

        return float(output)

    def doFilterAdaptive(self, signal, noise, learningRate):
        """
        Parameters:
        signal: float
            Current contaminated ECG sample d[n].
        noise: float
            Current reference noise sample x[n] (e.g. sin(2*pi*50/fs * n)).
        learningRate: float
            LMS step size (mu) controlling how fast the weights adapt.

        Returns:
        float
            The cleaned ECG sample e[n] = d[n] - y[n].
        """
        read_idx = self.offset  # store current write index before dofilter increments offset

        y = self.dofilter(noise)  # filter reference noise x[n] to estimate interference y[n]

        e = signal - y  # subtract estimated noise from signal to get error / clean ECG e[n]

        k = read_idx + 1
        step = learningRate * e  # calculate LMS weight update factor (mu * e[n])
        # w_m[n+1] = w_m[n] + mu * e[n] * x[n-m]
        self.coefficients[:k] += step * self.buffer[read_idx::-1]  # fwd tap weight update
        self.coefficients[k:] += step * self.buffer[:read_idx:-1]  # backward tap weight update

        return float(e)


# --- Realtime Sample-by-Sample FIR Filtering (Task 3) ---
fir = FIRfilter(h)
ecg_filtered = np.zeros(n)
fir_latency_us = np.zeros(n)  # REMOVE FOR SUBMISSION

for i in range(n):
    t_start = time.perf_counter()  # REMOVE FOR SUBMISSION
    ecg_filtered[i] = fir.dofilter(ecg[i])
    fir_latency_us[i] = (time.perf_counter() - t_start) * 1e6  # REMOVE FOR SUBMISSION

# --- Essential Plots: Filtered ECG (Time Domain, Zoomed Heartbeat, Frequency Spectrum) ---
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
vector_plot_export("t3_filtered")  # DO NOT SUBMIT WITHOUT COMMENTING OUT EXPORT CODE!!

# Extra Plot: Initial Filter Transient & Delay-Aligned Unfiltered vs Filtered Comparison
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


# ==============================================================================
# ------ TASK 4: REALTIME ADAPTIVE LMS FILTERING ------
# ==============================================================================
# Adaptive LMS Filter Setup (combined DC + 50 Hz reference)
M_lms = 10
mu_lms = 0.01  # justify learning rate
f_noise = 50.0
lms = FIRfilter(np.zeros(M_lms))

# Realtime Adaptive Filtering
ecg_lms = np.zeros(n)
lms_latency_us = np.zeros(n)  # REMOVE FOR SUBMISSION

for i in range(n):
    t_start = time.perf_counter()  # REMOVE FOR SUBMISSION

    # Remove DC / baseline wander (1) & 50 Hz powerline interference (sine)
    noise_ref = 1 + np.sin(2 * np.pi * f_noise * i / sample_rate)
    ecg_lms[i] = lms.doFilterAdaptive(ecg[i], noise_ref, mu_lms)

    lms_latency_us[i] = (time.perf_counter() - t_start) * 1e6  # REMOVE FOR SUBMISSION

# Plotting (Raw ECG vs Adaptive LMS Filtered ECG)
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

# Extra Plot 1: Three-way signal comparison (Raw vs Adaptive LMS vs Fixed FIR)
plt.figure(figsize=(12, 8))  # REMOVE FOR SUBMISSION
plt.suptitle(f"Task 4 Comparison: Raw ECG vs Adaptive LMS ($M$ = {M_lms}, $\\mu$ = {mu_lms}) vs Task 3 Fixed FIR")  # REMOVE FOR SUBMISSION

plt.subplot(3, 1, 1)  # REMOVE FOR SUBMISSION
plt.title("Time Domain: Raw ECG vs Adaptive LMS vs Fixed FIR")  # REMOVE FOR SUBMISSION
plt.plot(t, ecg, alpha=0.4, label="Raw ECG")  # REMOVE FOR SUBMISSION
plt.plot(t, ecg_lms, label="Adaptive LMS")  # REMOVE FOR SUBMISSION
plt.plot(t, ecg_filtered, alpha=0.8, linestyle="--", label="Task 3 Fixed FIR")  # REMOVE FOR SUBMISSION
plt.xlim(0, n / sample_rate)  # REMOVE FOR SUBMISSION
plt.xlabel("Time (s)")  # REMOVE FOR SUBMISSION
plt.ylabel("Amplitude (V)")  # REMOVE FOR SUBMISSION
plt.legend(loc="upper right")  # REMOVE FOR SUBMISSION
plt.grid(True)  # REMOVE FOR SUBMISSION

plt.subplot(3, 1, 2)  # REMOVE FOR SUBMISSION
plt.title("Zoomed Single Heartbeat (PQRST Complex): Raw vs Adaptive LMS vs Fixed FIR")  # REMOVE FOR SUBMISSION
plt.plot(t, ecg - np.mean(ecg[in_beat]), alpha=0.4, label="Raw ECG (DC mean subtracted)")  # REMOVE FOR SUBMISSION
plt.plot(t, ecg_lms, label="Adaptive LMS")  # REMOVE FOR SUBMISSION
plt.plot(t - group_delay, ecg_filtered, linestyle="--", label=f"Task 3 Fixed FIR (delay-aligned by {group_delay:.1f} s)")  # REMOVE FOR SUBMISSION
plt.xlim(beat_start, beat_end)  # REMOVE FOR SUBMISSION
plt.ylim(-0.5e-3, 1.5e-3)  # REMOVE FOR SUBMISSION
plt.xlabel("Time (s)")  # REMOVE FOR SUBMISSION
plt.ylabel("Amplitude (V)")  # REMOVE FOR SUBMISSION
plt.legend(loc="upper right")  # REMOVE FOR SUBMISSION
plt.grid(True)  # REMOVE FOR SUBMISSION

plt.subplot(3, 1, 3)  # REMOVE FOR SUBMISSION
plt.title("Frequency Spectrum Comparison: Raw vs Adaptive LMS vs Fixed FIR")  # REMOVE FOR SUBMISSION
plt.plot(freqs[1:], raw_fft[1:n // 2], alpha=0.4, label="Raw Spectrum")  # REMOVE FOR SUBMISSION
plt.plot(freqs[1:], lms_fft[1:n // 2], label="Adaptive LMS")  # REMOVE FOR SUBMISSION
plt.plot(freqs[1:], filt_fft[1:n // 2], linestyle="--", label="Task 3 Fixed FIR")  # REMOVE FOR SUBMISSION
plt.xlim(0, sample_rate / 2)  # REMOVE FOR SUBMISSION
plt.ylim(0, 3e-5)  # REMOVE FOR SUBMISSION
plt.xlabel("Frequency (Hz)")  # REMOVE FOR SUBMISSION
plt.ylabel("Magnitude (V)")  # REMOVE FOR SUBMISSION
plt.legend(loc="upper right")  # REMOVE FOR SUBMISSION
plt.grid(True)  # REMOVE FOR SUBMISSION

plt.tight_layout()  # REMOVE FOR SUBMISSION
vector_plot_export("t4_compare")  # REMOVE FOR SUBMISSION

# Extra Plot 2: Execution Time & Per-Sample Latency Comparison (Adaptive LMS vs Fixed FIR)
lms_total_ms = np.sum(lms_latency_us) / 1e3  # REMOVE FOR SUBMISSION
fir_total_ms = np.sum(fir_latency_us) / 1e3  # REMOVE FOR SUBMISSION
lms_mean_us = np.mean(lms_latency_us)  # REMOVE FOR SUBMISSION
fir_mean_us = np.mean(fir_latency_us)  # REMOVE FOR SUBMISSION
lms_median_us = np.median(lms_latency_us)  # REMOVE FOR SUBMISSION
fir_median_us = np.median(fir_latency_us)  # REMOVE FOR SUBMISSION

print(f"Adaptive LMS ({M_lms} taps)     -> Total: {lms_total_ms:.2f} ms | Mean: {lms_mean_us:.2f} us/sample | Median: {lms_median_us:.2f} us/sample")  # REMOVE FOR SUBMISSION
print(f"Fixed FIR ({M} taps) -> Total: {fir_total_ms:.2f} ms | Mean: {fir_mean_us:.2f} us/sample | Median: {fir_median_us:.2f} us/sample")  # REMOVE FOR SUBMISSION

plt.figure(figsize=(12, 7))  # REMOVE FOR SUBMISSION
plt.suptitle("Computational Latency Comparison: Adaptive LMS vs Fixed FIR")  # REMOVE FOR SUBMISSION

# Per-sample latency across the recording
plt.subplot(2, 1, 1)  # REMOVE FOR SUBMISSION
plt.title("Per-Sample Processing Latency Over Time")  # REMOVE FOR SUBMISSION
plt.plot(t, lms_latency_us, alpha=0.7, label=f"Adaptive LMS ({M_lms} taps, mean = {lms_mean_us:.2f} $\\mu$s)")  # REMOVE FOR SUBMISSION
plt.plot(t, fir_latency_us, alpha=0.7, label=f"Fixed FIR ({M} taps, mean = {fir_mean_us:.2f} $\\mu$s)")  # REMOVE FOR SUBMISSION
plt.xlim(0, n / sample_rate)  # REMOVE FOR SUBMISSION
plt.ylim(0, max(np.percentile(lms_latency_us, 99), np.percentile(fir_latency_us, 99)) * 1.5)  # REMOVE FOR SUBMISSION
plt.xlabel("Time (s)")  # REMOVE FOR SUBMISSION
plt.ylabel("Latency ($\\mu$s / sample)")  # REMOVE FOR SUBMISSION
plt.legend(loc="upper right")  # REMOVE FOR SUBMISSION
plt.grid(True)  # REMOVE FOR SUBMISSION

# Bar chart comparing mean per-sample latency and total execution time
plt.subplot(2, 1, 2)  # REMOVE FOR SUBMISSION
plt.title(f"Mean Per-Sample Latency & Total Runtime ({n} samples)")  # REMOVE FOR SUBMISSION
methods = [f"Adaptive LMS\n({M_lms} taps, 0 s group delay)", f"Task 3 Fixed FIR\n({M} taps, {group_delay:.1f} s group delay)"]  # REMOVE FOR SUBMISSION
means = [lms_mean_us, fir_mean_us]  # REMOVE FOR SUBMISSION
bars = plt.bar(methods, means, width=0.4, color=["tab:blue", "tab:orange"])  # REMOVE FOR SUBMISSION
plt.ylabel("Mean Latency ($\\mu$s / sample)")  # REMOVE FOR SUBMISSION
plt.grid(axis="y")  # REMOVE FOR SUBMISSION

for bar, total_ms in zip(bars, [lms_total_ms, fir_total_ms]):  # REMOVE FOR SUBMISSION
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, f"{bar.get_height():.2f} $\\mu$s/sample\n(Total: {total_ms:.1f} ms)", ha="center", va="center", color="white", fontweight="bold")  # REMOVE FOR SUBMISSION

plt.tight_layout()  # REMOVE FOR SUBMISSION
vector_plot_export("t4_latency")  # REMOVE FOR SUBMISSION


# ==============================================================================
# ------ TASK 5: REALTIME HEARTBEAT DETECTION USING MATCHED FIR FILTER ------
# ==============================================================================
# Load partner's ECG data for template extraction
t_template, template_ecg, template_sample_rate = import_ecg_data("ecg2.tsv")

# Extract PQRST from partner's template ECG using Task 2 FIR filter coefficients
template_fir = FIRfilter(h)
template_clean = np.zeros(len(template_ecg))
for i in range(len(template_ecg)):
    template_clean[i] = template_fir.dofilter(template_ecg[i])

# Cut around the R peak (include QRS). An earlier sample would be affected by cleaning filter transient
R = 2576
template = template_clean[R - 12:R + 13]  # 25 samples
matched_fir = FIRfilter(np.flip(template))  # reverse coefficients in time
ecg_fir = FIRfilter(h)  # fresh cleaning filter for ECG

# Realtime sample-by-sample heartbeat detection loop
matched_fir_out = np.zeros(n)

THRESHOLD = 1.5e-11  # from matched filter plot
TRANSIENTS = len(template) + len(h)  # buffer fill time (cleaning + matched filter) = 1025 samples
MIN = 30
MAX = 200
LAST_BEAT = None  # index of previous beat
HEART_RATE = []
BEAT_TIMES = []

for i in range(n):
    matched_fir_out[i] = matched_fir.dofilter(ecg_fir.dofilter(ecg[i])) ** 2  # square to make positive (bigger values (peaks) become much bigger)
    if i <= TRANSIENTS:
        continue
    if matched_fir_out[i] > THRESHOLD and matched_fir_out[i - 1] <= THRESHOLD:
        peak = i
        if LAST_BEAT is not None:
            # Ensure heartrate is within reasonable range (30-200 bpm)
            momentary_rate = 60 * sample_rate / (peak - LAST_BEAT)  # bpm
            in_range = MIN < momentary_rate < MAX  # Heuristic 1

            prev_rate = HEART_RATE[-1] if HEART_RATE else momentary_rate  # prevent IndexError
            consistency = 0.75 * prev_rate < momentary_rate < 1.25 * prev_rate  # Heuristic 2
            if in_range and consistency:
                HEART_RATE.append(momentary_rate)
                BEAT_TIMES.append(peak / sample_rate)
        LAST_BEAT = peak

print(f"Heart rates calculated: {len(HEART_RATE)}, mean heart rate: {np.mean(HEART_RATE):.1f} bpm")

# --- TASK 5 ANALYSIS PLOTS ---

# Plot filtered template ECG against sample number to locate R peak (REMOVE)
plt.figure(figsize=(10, 4))
plt.title("Filtered Partner ECG (Template Source)")
plt.plot(template_clean)
plt.xlim(2500, 2800)
plt.xlabel("Sample")
plt.ylabel("Amplitude (V)")
plt.tight_layout()

# Plot template to check QRS range is covered
plt.figure(figsize=(8, 4))
plt.title("Extracted QRS Template (25 Samples)")
plt.plot(template)
plt.xlabel("Sample")
plt.ylabel("Amplitude (V)")
plt.tight_layout()

# Plot matched filter output
plt.figure(figsize=(12, 4))
plt.title("Squared Matched Filter Output")
plt.plot(matched_fir_out)
plt.xlabel("Sample")
plt.ylabel("Amplitude ($V^2$)")
plt.xlim(1000, n)
plt.ylim(0, 0.5e-10)
plt.tight_layout()

plt.show()
