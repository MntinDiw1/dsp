# Report figure export - NOT part of the submission.
#
# Runs the submitted scripts, takes the signals they compute and re-plots them in one
# consistent style, saving each figure as PDF and SVG in report/figs/.
# No filtering or detection logic lives here, so the figures cannot drift from the submitted code.
#
# Usage (from anywhere):  python reportCode.py

from pathlib import Path
import runpy
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")  # save to file only, no plot windows
import matplotlib.pyplot as plt
from scipy.fft import fft

REPORT_DIR = Path(__file__).resolve().parent
CODE_DIR = REPORT_DIR.parent  # folder holding the submitted scripts and ecg1.tsv / ecg2.tsv
FIGS_DIR = REPORT_DIR / "figs"
sys.path.insert(0, str(CODE_DIR))  # lets the submitted scripts import each other

# One style for every figure
RAW, FIR, LMS, MATCHED = "tab:blue", "tab:orange", "tab:green", "tab:purple"
ZOOM = (5.5, 6.7)  # s, the two-heartbeat window used by the submitted scripts
SPECTRUM_YMAX = 3e-5  # V, vertical zoom of the spectra used by the submitted scripts
plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 9, "legend.fontsize": 8,
    "lines.linewidth": 0.8, "axes.grid": True, "grid.alpha": 0.4,
    "axes.formatter.limits": (-3, 3), "axes.formatter.use_mathtext": True,
})


def run_script(name):
    """Runs a submitted script without showing its plots and returns its variables."""
    plt.show = lambda *args, **kwargs: None
    variables = runpy.run_path(str(CODE_DIR / name), run_name="__main__")
    plt.close("all")
    return variables


def spectrum(x):
    """Single-sided linear magnitude spectrum |FFT(x)|/N with its frequency axis k*fs/N."""
    n = len(x)
    return np.arange(n // 2) * fs / n, np.abs(fft(x))[:n // 2] / n


def panel(title, xlabel, ylabel, xlim=None, ylim=None, legend=None):
    """Titles and labels the current subplot."""
    plt.title(title, loc="left")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim:
        plt.xlim(*xlim)
    if ylim:
        plt.ylim(*ylim)
    if legend:
        plt.legend(loc=legend)


def zoom_ylim(time, *traces):
    """Fits the y-axis to what is visible inside the ZOOM window, leaving room on top for the legend."""
    visible = np.concatenate([x[(time >= ZOOM[0]) & (time <= ZOOM[1])] for x in traces])
    height = visible.max() - visible.min()
    plt.ylim(visible.min() - 0.15 * height, visible.max() + 0.45 * height)


def shade_stopbands():
    """Shades the two frequency ranges removed by the Task 2 FIR filter."""
    for low, high in stopbands:
        plt.axvspan(low, high, color="0.8", alpha=0.5, lw=0)
    plt.fill_between([], [], color="0.8", alpha=0.5, label="FIR stopbands")  # one legend entry for both


def save(name):
    plt.tight_layout()
    for extension in ("pdf", "svg"):
        plt.savefig(FIGS_DIR / f"{name}.{extension}")
    plt.close()
    print(f"saved figs/{name}.pdf and .svg")


# ---------- Run the submitted code ----------
task3 = run_script("fir_realtime_sim.py")
task4 = run_script("lms_filter.py")
task5 = run_script("heartbeat.py")

t, ecg, fs = task3["t"], task3["ecg"], task3["sample_rate"]
ecg_fir, group_delay = task3["ecg_filtered"], task3["group_delay"]
stopbands = [task3["BASELINE_WANDER"], task3["MAINS_AND_HF_HUM"]]
ecg_lms = task4["ecg_lms"]
h, template = task5["h"], task5["template"]
matched_out, threshold, transients = task5["matched_fir_out"], task5["THRESHOLD"], task5["TRANSIENTS"]
beat_idx, heart_rate, delay = task5["beat_idx"], task5["heart_rate"], task5["delay"]

M = len(h)
duration = len(ecg) / fs
ecg_centred = ecg - np.mean(ecg[(t >= ZOOM[0]) & (t <= ZOOM[1])])  # raw ECG moved onto 0 V for the zooms
freqs, raw_mag = spectrum(ecg)
_, fir_mag = spectrum(ecg_fir)
_, lms_mag = spectrum(ecg_lms)
FIGS_DIR.mkdir(exist_ok=True)


# ---------- Task 1: raw ECG in the time domain ----------
plt.figure(figsize=(7, 3.1))

plt.subplot(2, 1, 1)
plt.plot(t, ecg, color=RAW)
panel("(a) Raw ECG 1: full recording", "Time (s)", "Amplitude (V)", xlim=(0, duration))

plt.subplot(2, 1, 2)
plt.plot(t, ecg, color=RAW)
panel("(b) Raw ECG 1: two heartbeats", "Time (s)", "Amplitude (V)", xlim=ZOOM)
zoom_ylim(t, ecg)

save("t1_time")


# ---------- Task 1: raw ECG in the frequency domain (linear axes) ----------
plt.figure(figsize=(7, 6))

plt.subplot(3, 1, 1)
plt.plot(freqs, raw_mag, color=RAW)
plt.annotate("DC offset and\nbaseline wander", (0, raw_mag[0]), xytext=(8, 0.85 * raw_mag[0]),
             va="center", arrowprops={"arrowstyle": "->"})
peak_50 = np.argmax(raw_mag * (freqs > 45))
plt.annotate("50 Hz mains", (freqs[peak_50], raw_mag[peak_50]), xytext=(58, 0.4 * raw_mag[0]),
             va="center", arrowprops={"arrowstyle": "->"})
panel("(a) Spectrum of raw ECG 1: full scale", "Frequency (Hz)", "Magnitude (V)", xlim=(0, fs / 2))

plt.subplot(3, 1, 2)
plt.plot(freqs, raw_mag, color=RAW)
shade_stopbands()
panel("(b) Magnitude axis zoomed", "Frequency (Hz)", "Magnitude (V)",
      xlim=(0, fs / 2), ylim=(0, SPECTRUM_YMAX), legend="upper right")

plt.subplot(3, 1, 3)
plt.plot(freqs, raw_mag, color=RAW, marker=".", markersize=2)
shade_stopbands()
panel("(c) Magnitude and frequency axes zoomed: 0 to 10 Hz", "Frequency (Hz)", "Magnitude (V)",
      xlim=(0, 10), ylim=(0, 2 * SPECTRUM_YMAX), legend="upper right")

save("t1_freq")


# ---------- Task 2: FIR coefficients and their frequency response ----------
response_freqs = np.arange(16 * M) * fs / (16 * M)  # zero-padded FFT shows the response between the bins
response = np.abs(fft(h, 16 * M))

plt.figure(figsize=(7, 5))

plt.subplot(2, 2, 1)
plt.plot(h, color=FIR)
plt.axvline(M // 2, color="k", ls=":", label=f"centre tap M/2 = {M // 2}")
panel(f"(a) Coefficients h[n], M = {M}", "Tap index n", "Amplitude", xlim=(0, M - 1), legend="center right")

plt.subplot(2, 2, 2)
plt.plot(response_freqs, response, color=FIR)
shade_stopbands()
panel("(b) Frequency response |H(f)|", "Frequency (Hz)", "Gain", xlim=(0, fs / 2), legend="upper right")

for position, (title, xlim) in enumerate([("(c) Lower band edge", (0, 2)), ("(d) Upper band edge", (43, 47))], start=3):
    plt.subplot(2, 2, position)
    plt.plot(response_freqs, response, color=FIR)
    shade_stopbands()
    panel(title, "Frequency (Hz)", "Gain", xlim=xlim)

save("t2_coeffs")


# ---------- Task 3: realtime FIR filtering ----------
PQRST = {"P": 5.628, "Q": 5.752, "R": 5.784, "S": 5.808, "T": 5.992}  # s, read off the zoomed plot

plt.figure(figsize=(7, 6.4))

plt.subplot(3, 1, 1)
plt.plot(t, ecg, color=RAW, alpha=0.6, label="Raw ECG")
plt.plot(t, ecg_fir, color=FIR, label="FIR filtered ECG")
plt.axvspan(0, M / fs, color="0.8", alpha=0.5, lw=0, label=f"Buffer fill ({M} samples)")
panel("(a) Full recording", "Time (s)", "Amplitude (V)", xlim=(0, duration), legend="upper right")

plt.subplot(3, 1, 2)
plt.plot(t, ecg_centred, color=RAW, alpha=0.6, label="Raw ECG (mean removed)")
plt.plot(t - group_delay, ecg_fir, color=FIR, label=f"FIR filtered ECG (shifted back by {group_delay:.3f} s)")
for label, time in PQRST.items():
    below = label in "QS"
    plt.annotate(label, (time, np.interp(time, t - group_delay, ecg_fir)), xytext=(0, -6 if below else 6),
                 textcoords="offset points", ha="center", va="top" if below else "bottom", weight="bold",
                 bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5, "alpha": 0.8})
panel("(b) Two heartbeats", "Time (s)", "Amplitude (V)", xlim=ZOOM)
plt.legend(loc="upper right", ncol=2)
zoom_ylim(t, ecg_centred)

plt.subplot(3, 1, 3)
plt.plot(freqs, raw_mag, color=RAW, alpha=0.6, label="Raw ECG")
plt.plot(freqs, fir_mag, color=FIR, label="FIR filtered ECG")
shade_stopbands()
panel("(c) Spectrum, magnitude axis zoomed", "Frequency (Hz)", "Magnitude (V)",
      xlim=(0, fs / 2), ylim=(0, SPECTRUM_YMAX), legend="upper right")

save("t3_filtered")


# ---------- Task 4: adaptive LMS filter against the FIR filter ----------
plt.figure(figsize=(7, 8))

for position, (title, xlim) in enumerate([("(a) Full recording", (0, duration)), ("(b) Start-up: first 6 s", (0, 6))], start=1):
    plt.subplot(4, 1, position)
    plt.plot(t, ecg_fir, color=FIR, label="FIR filtered ECG")
    plt.plot(t, ecg_lms, color=LMS, alpha=0.8, label="LMS filtered ECG")
    panel(title, "Time (s)", "Amplitude (V)", xlim=xlim, legend="upper right")

plt.subplot(4, 1, 3)
plt.plot(t - group_delay, ecg_fir, color=FIR, label=f"FIR filtered ECG (shifted back by {group_delay:.3f} s)")
plt.plot(t, ecg_lms, color=LMS, alpha=0.8, label="LMS filtered ECG (no shift)")
panel("(c) Two heartbeats", "Time (s)", "Amplitude (V)", xlim=ZOOM)
plt.legend(loc="upper right", ncol=2)
zoom_ylim(t, ecg_lms)

plt.subplot(4, 1, 4)
plt.plot(freqs, fir_mag, color=FIR, label="FIR filtered ECG")
plt.plot(freqs, lms_mag, color=LMS, alpha=0.8, label="LMS filtered ECG")
panel("(d) Spectrum, magnitude axis zoomed", "Frequency (Hz)", "Magnitude (V)",
      xlim=(0, fs / 2), ylim=(0, SPECTRUM_YMAX), legend="upper right")

save("t4_compare")


# ---------- Task 5: matched filter detection ----------
template_ms = (np.arange(len(template)) - len(template) // 2) / fs * 1000  # time relative to the R peak
output_label = f"Time (s), output delayed by {delay:.2f} s"

plt.figure(figsize=(7, 6.4))

plt.subplot(3, 1, 1)
plt.plot(template_ms, template, color=FIR, marker=".")
panel(f"(a) QRS template from FIR filtered ECG 2 ({len(template)} samples)", "Time relative to R peak (ms)", "Amplitude (V)")

for position, (title, xlim, ymax) in enumerate([("(b) Squared matched filter output for ECG 1", (0, duration), 6.5e-11),
                                                ("(c) Two heartbeats", (ZOOM[0] + delay, ZOOM[1] + delay), 3e-11)], start=2):
    plt.subplot(3, 1, position)
    plt.plot(t, matched_out, color=MATCHED, label="Squared matched filter output")
    plt.axhline(threshold, color="tab:red", ls="--", label=f"Threshold ({threshold:.1e} V$^4$)")
    plt.plot(t[beat_idx], matched_out[beat_idx], "kx", markersize=4, label=f"Detected beats with a rate ({len(beat_idx)})")
    plt.axvspan(0, transients / fs, color="0.8", alpha=0.5, lw=0, label=f"Buffer fill, ignored ({transients} samples)")
    panel(title, output_label, "Amplitude (V$^4$)", xlim=xlim, ylim=(0, ymax))
plt.subplot(3, 1, 2)
plt.legend(loc="upper right", ncol=2)

save("t5_detection")


# ---------- Task 5: momentary heart rate ----------
plt.figure(figsize=(7, 2.6))
plt.plot(t[beat_idx] - delay, heart_rate, color=MATCHED, marker=".")
panel(f"Momentary heart rate of ECG 1 (mean {np.mean(heart_rate):.1f} bpm)", "Time (s)", "Heart rate (bpm)", xlim=(0, duration))

save("t5_heartrate")
