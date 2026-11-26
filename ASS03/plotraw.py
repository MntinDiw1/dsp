"""Visualise raw piezo recordings saved by record.py (time domain, zoomed keystrokes, FFT)."""

from pathlib import Path
import re
import sys
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_FILE = BASE_DIR / "data" / "test10.tsv"

# Positive-edge keystroke detector parameters
ADC_MAX_CODE = 1023.0           # 10-bit Arduino ADC full-scale code
NOISE_FLOOR_ADC_LEVELS = 3.0    # Minimum threshold floor (2-3 ADC levels)
PEAK_THRESH_FRAC = 0.85         # Raise threshold to this fraction of pulse peak to ignore ring-down
HOLD_MS = 50.0                  # Peak-capture / refractory hold window (ms)
DECAY_TAU_MS = 55.0             # Exponential decay time constant of dynamic threshold (ms)
MAX_PEAK_RATIO = 4.5            # Ignore pulses > MAX_PEAK_RATIO * reference peak (bump/outlier rejection)
REF_DECAY_S = 1.5               # Decay time constant of reference peak so an initial big peak doesn't stick
MATCH_EARLY_MS = 120.0          # Piezo edge may precede logged matplotlib key event by up to this (ms)
MATCH_LATE_MS = 60.0            # Piezo edge may follow logged matplotlib key event by up to this (ms)


def load_recording(path: Path):
    """Parse header metadata, key presses, and raw ADC samples from a testN.tsv file."""
    fs = 1000.0
    vref = 2.5
    keys = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("#"):
                break
            text = line.lstrip("#").strip()

            fs_match = re.search(r"fs\s*=\s*([0-9.]+)\s*Hz", text)
            if fs_match:
                fs = float(fs_match.group(1))
            vref_match = re.search(r"VREF\s*=\s*([0-9.]+)\s*V", text)
            if vref_match:
                vref = float(vref_match.group(1))

            parts = text.split("\t")
            if len(parts) == 3 and parts[0].isdigit():
                keys.append((int(parts[0]), float(parts[1]), parts[2]))

    samples = np.loadtxt(path, dtype=float)
    return fs, vref, keys, samples


def clean_glitches(samples: np.ndarray):
    """Replace out-of-range Firmata serial glitch samples (<0 or >1) via linear interpolation."""
    bad = (samples < 0.0) | (samples > 1.0)
    cleaned = samples.copy()
    bad_idx = np.flatnonzero(bad)
    if bad_idx.size > 0:
        good_idx = np.flatnonzero(~bad)
        cleaned[bad_idx] = np.interp(bad_idx, good_idx, samples[good_idx])
    return cleaned, bad_idx


def detect_positive_edges(
    ac_mv: np.ndarray,
    fs: float,
    vref: float,
    floor_adc_levels: float = NOISE_FLOOR_ADC_LEVELS,
    peak_thresh_frac: float = PEAK_THRESH_FRAC,
    hold_ms: float = HOLD_MS,
    decay_tau_ms: float = DECAY_TAU_MS,
    max_peak_ratio: float = MAX_PEAK_RATIO,
    ref_decay_s: float = REF_DECAY_S,
):
    """Detect positive edges with a decaying dynamic threshold and oversized-peak rejection.

    - Threshold never drops below `floor_adc_levels` ADC steps (2-3 LSB noise floor).
    - After a positive-edge crossing, threshold rises with the pulse peak during `hold_ms`
      to suppress smaller ring-down oscillations, then decays exponentially (`decay_tau_ms`)
      back toward the noise floor so subsequent keystrokes are not skipped after a big peak.
    - Peaks much larger than the decaying reference peak (`> max_peak_ratio * ref_peak`)
      are ignored as outliers/bumps, with the threshold capped so following keys aren't missed.
    """
    lsb_mv = (vref / ADC_MAX_CODE) * 1e3
    noise_floor_mv = floor_adc_levels * lsb_mv
    decay_alpha = float(np.exp(-1.0 / max(decay_tau_ms * 1e-3 * fs, 1.0)))
    ref_decay_alpha = float(np.exp(-1.0 / max(ref_decay_s * fs, 1.0)))
    hold_n = max(1, int(round(hold_ms * 1e-3 * fs)))
    ref_floor_mv = 2.0 * noise_floor_mv

    n = len(ac_mv)
    thresh_trace = np.empty(n, dtype=float)
    thresh = noise_floor_mv
    ref_peak = None

    detected = []  # (edge_idx, peak_idx, peak_mv)
    ignored = []   # (edge_idx, peak_idx, peak_mv)

    in_pulse = False
    pulse_start = 0
    pulse_peak_idx = 0
    pulse_peak_mv = 0.0
    hold_left = 0

    for i in range(n):
        x = float(ac_mv[i])
        prev = float(ac_mv[i - 1]) if i > 0 else 0.0

        if not in_pulse:
            # Decay dynamic threshold exponentially toward noise floor (never below it)
            thresh = max(noise_floor_mv, noise_floor_mv + (thresh - noise_floor_mv) * decay_alpha)
        if ref_peak is not None:
            ref_peak = max(ref_floor_mv, ref_floor_mv + (ref_peak - ref_floor_mv) * ref_decay_alpha)

        if in_pulse:
            if x > pulse_peak_mv:
                pulse_peak_mv = x
                pulse_peak_idx = i
            thresh = max(thresh, noise_floor_mv, peak_thresh_frac * pulse_peak_mv)
            hold_left -= 1
            if hold_left <= 0:
                in_pulse = False
                if ref_peak is not None and pulse_peak_mv > max_peak_ratio * ref_peak:
                    ignored.append((pulse_start, pulse_peak_idx, pulse_peak_mv))
                    # Cap post-outlier threshold so normal keystrokes right after aren't skipped
                    thresh = min(thresh, max(noise_floor_mv, peak_thresh_frac * ref_peak * 1.5))
                else:
                    detected.append((pulse_start, pulse_peak_idx, pulse_peak_mv))
                    ref_peak = pulse_peak_mv if ref_peak is None else 0.5 * ref_peak + 0.5 * pulse_peak_mv
        else:
            if prev < thresh <= x:
                in_pulse = True
                pulse_start = i
                pulse_peak_idx = i
                pulse_peak_mv = x
                hold_left = hold_n
                thresh = max(thresh, noise_floor_mv, peak_thresh_frac * x)

        thresh_trace[i] = thresh

    # Finalize a pulse still open at end-of-recording
    if in_pulse:
        if ref_peak is not None and pulse_peak_mv > max_peak_ratio * ref_peak:
            ignored.append((pulse_start, pulse_peak_idx, pulse_peak_mv))
        else:
            detected.append((pulse_start, pulse_peak_idx, pulse_peak_mv))

    return detected, ignored, thresh_trace, noise_floor_mv


def compare_keystrokes(keys, detected, fs: float):
    """Match sensed positive-edge keystrokes against known logged key presses."""
    used_edges = set()
    matched_pairs = []  # (key_idx, edge_idx, dt_ms)

    for k_idx, _kt, _key in keys:
        best_j = None
        best_score = float("inf")
        best_dt_ms = 0.0
        for j, (edge_idx, _peak_idx, _peak_mv) in enumerate(detected):
            if j in used_edges:
                continue
            dt_ms = (edge_idx - k_idx) / fs * 1e3
            # Piezo vibration typically leads the GUI key event by ~20-40 ms
            if -MATCH_EARLY_MS <= dt_ms <= MATCH_LATE_MS:
                score = abs(dt_ms + 25.0)
                if score < best_score:
                    best_score = score
                    best_j = j
                    best_dt_ms = dt_ms
        if best_j is not None:
            used_edges.add(best_j)
            matched_pairs.append((k_idx, detected[best_j][0], best_dt_ms))

    tp = len(matched_pairs)
    fp = len(detected) - tp
    fn = len(keys) - tp
    precision = tp / len(detected) if detected else 0.0
    recall = tp / len(keys) if keys else 0.0
    f1 = (2.0 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "known": len(keys),
        "sensed": len(detected),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "matched_pairs": matched_pairs,
    }


def main():
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FILE
    fs, vref, keys, raw = load_recording(data_path)
    samples, glitch_idx = clean_glitches(raw)

    t = np.arange(len(samples)) / fs
    volts = samples * vref
    dc_mean = float(np.mean(volts))
    ac_mv = (volts - dc_mean) * 1e3  # AC component in mV

    # Dynamic positive-edge keystroke detection & comparison against logged keys
    detected, ignored, thresh_mv, noise_floor_mv = detect_positive_edges(ac_mv, fs, vref)
    stats = compare_keystrokes(keys, detected, fs)
    det_idx = np.array([e[0] for e in detected], dtype=int)
    ign_idx = np.array([e[0] for e in ignored], dtype=int)

    # Summary stats
    print(f"File: {data_path.name}")
    print(f"Samples: {len(samples)} ({t[-1]:.2f} s at fs = {fs:.2f} Hz, VREF = {vref:.2f} V)")
    print(f"DC bias: {dc_mean:.4f} V ({np.mean(samples):.4f} of AREF)")
    print(f"Range:   {volts.min():.4f} V to {volts.max():.4f} V (peak-to-peak: {(volts.max() - volts.min()) * 1e3:.1f} mV)")
    print(f"Noise floor ({NOISE_FLOOR_ADC_LEVELS:.1f} ADC levels): {noise_floor_mv:.2f} mV")
    print(f"Keystrokes — Known: {stats['known']} | Sensed: {stats['sensed']} (diff: {stats['sensed'] - stats['known']:+d}) | Ignored big peaks: {len(ignored)}")
    if stats["known"] > 0:
        print(
            f"Comparison — Matched (TP): {stats['tp']} | Extra (FP): {stats['fp']} | Missed (FN): {stats['fn']} "
            f"| Precision: {stats['precision']:.1%} | Recall: {stats['recall']:.1%} | F1: {stats['f1']:.1%}"
        )
        if len(keys) >= 2:
            active_min = (keys[-1][0] - keys[0][0]) / fs / 60.0
            if active_min > 0:
                known_wpm = (stats["known"] / 5.0) / active_min
                sensed_in_span = sum(1 for e in detected if keys[0][0] - int(0.15 * fs) <= e[0] <= keys[-1][0] + int(0.15 * fs))
                sensed_wpm = (sensed_in_span / 5.0) / active_min
                print(f"Typing rate (active span {active_min * 60:.1f} s) — Known: {known_wpm:.1f} WPM | Sensed: {sensed_wpm:.1f} WPM")
    if glitch_idx.size > 0:
        print(f"Glitches interpolated ({glitch_idx.size}): indices {glitch_idx.tolist()}, raw values {raw[glitch_idx].tolist()}")

    fig, axes = plt.subplots(3, 1, figsize=(13, 9), constrained_layout=True)
    fig.suptitle(
        f"{data_path.name}  |  fs = {fs:.2f} Hz, VREF = {vref:.2f} V, DC = {dc_mean:.3f} V  |  "
        f"Keys Known: {stats['known']}, Sensed: {stats['sensed']} (TP: {stats['tp']}, Ignored: {len(ignored)})",
        fontsize=11,
    )

    # 1. Full time-domain waveform (V) with key-press markers
    ax1 = axes[0]
    ax1.plot(t, volts, linewidth=0.7, label="A0 voltage")
    ax1.axhline(dc_mean, color="tab:green", linestyle="--", linewidth=0.9, alpha=0.8, label=f"DC mean ({dc_mean:.3f} V)")
    for idx, kt, key in keys:
        if key == "space":
            color, alpha = "tab:orange", 0.5
        elif key in ("enter", "backspace"):
            color, alpha = "tab:red", 0.35
        else:
            color, alpha = "0.5", 0.25
        ax1.axvline(kt, color=color, linewidth=0.7, alpha=alpha)
    if det_idx.size > 0:
        ax1.plot(t[det_idx], volts[det_idx], "^", color="tab:green", markersize=4, alpha=0.75, label=f"Sensed edges ({len(det_idx)})")
    if ign_idx.size > 0:
        ax1.plot(t[ign_idx], volts[ign_idx], "x", color="tab:red", markersize=5, alpha=0.85, label=f"Ignored big peaks ({len(ign_idx)})")
    ax1.set_title("Full Recording (lines = known keys; green ^ = sensed edges; red x = ignored oversized peaks)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Voltage (V)")
    ax1.set_xlim(0, t[-1])
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper right", fontsize=8)

    # 2. Zoomed AC view (mV) around the first typing segment with dynamic threshold & detected edges
    ax2 = axes[1]
    if keys:
        t_start = max(0.0, keys[0][1] - 0.5)
        t_end = min(t[-1], t_start + 5.0)
    else:
        t_start, t_end = 0.0, min(t[-1], 5.0)
    mask = (t >= t_start) & (t <= t_end)
    ax2.plot(t[mask], ac_mv[mask], linewidth=0.8, label="AC signal")
    ax2.plot(t[mask], thresh_mv[mask], color="tab:purple", linewidth=1.0, alpha=0.9, label="Dynamic threshold")
    ax2.axhline(noise_floor_mv, color="tab:purple", linestyle=":", linewidth=0.8, alpha=0.7, label=f"Floor ({NOISE_FLOOR_ADC_LEVELS:.1f} LSB = {noise_floor_mv:.1f} mV)")
    ax2.axhline(0.0, color="0.4", linestyle="--", linewidth=0.7)

    vis_det = det_idx[(t[det_idx] >= t_start) & (t[det_idx] <= t_end)] if det_idx.size > 0 else np.array([], dtype=int)
    vis_ign = ign_idx[(t[ign_idx] >= t_start) & (t[ign_idx] <= t_end)] if ign_idx.size > 0 else np.array([], dtype=int)
    if vis_det.size > 0:
        ax2.plot(t[vis_det], ac_mv[vis_det], "^", color="tab:green", markersize=6, zorder=4, label=f"Positive edges ({vis_det.size} in view)")
    if vis_ign.size > 0:
        ax2.plot(t[vis_ign], ac_mv[vis_ign], "x", color="tab:red", markersize=7, zorder=4, label=f"Ignored peaks ({vis_ign.size} in view)")

    y_top = float(np.max(ac_mv[mask])) if np.any(mask) else 10.0
    y_bot = float(np.min(ac_mv[mask])) if np.any(mask) else -10.0
    pad = max((y_top - y_bot) * 0.2, 5.0)
    ax2.set_ylim(y_bot - pad * 0.4, y_top + pad)

    visible_keys = [(idx, kt, k) for idx, kt, k in keys if t_start <= kt <= t_end]
    for i, (idx, kt, key) in enumerate(visible_keys):
        color = "tab:orange" if key == "space" else ("tab:red" if key in ("enter", "backspace") else "tab:blue")
        ax2.axvline(kt, color=color, linestyle=":", linewidth=0.9, alpha=0.7)
        label = "SPC" if key == "space" else ("BS" if key == "backspace" else ("ENT" if key == "enter" else key))
        y_text = y_top + pad * (0.25 if i % 2 == 0 else 0.65)
        ax2.text(kt, y_text, label, fontsize=8, ha="center", va="bottom", color=color)

    ax2.set_title(f"Zoomed AC Signal ({t_start:.1f} s – {t_end:.1f} s, DC removed, dynamic positive-edge detector)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("AC Signal (mV)")
    ax2.set_xlim(t_start, t_end)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right", fontsize=8)

    # 3. Single-sided FFT magnitude spectrum (DC removed, Hann windowed)
    ax3 = axes[2]
    n = len(ac_mv)
    window = np.hanning(n)
    ac_v = volts - dc_mean
    fft_mag = np.abs(np.fft.rfft(ac_v * window)) / (np.sum(window) / 2.0)
    freqs = np.fft.rfftfreq(n, d=1.0 / fs)
    fft_db = 20.0 * np.log10(np.maximum(fft_mag, 1e-12))

    ax3.plot(freqs, fft_db, linewidth=0.8)
    ax3.axvline(50.0, color="tab:red", linestyle="--", linewidth=0.9, alpha=0.7, label="50 Hz mains")
    ax3.set_title("Magnitude Spectrum (DC removed, Hann window)")
    ax3.set_xlabel("Frequency (Hz)")
    ax3.set_ylabel("Magnitude (dB re 1 V)")
    ax3.set_xlim(0, fs / 2.0)
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc="upper right", fontsize=8)

    plt.show()


if __name__ == "__main__":
    main()
