import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from task2_enhance import gain_ctrl, enhancer

    #Dry path

    #Exciter sidechain (HPF: 800-6kHz)

    # Big bottom sidechain (LPF: 50-190Hz)

    #Plot spectrum zoomed between 2-12kHz before and after each change (report: annotated graphs)

#Band selection (used for both the sidechain and the harmonic selection)
def band_pass(audio, sample_rate, lo, hi):
    gain_array = np.ones(len(audio))
    gain_ctrl(0, lo, -np.inf, sample_rate, gain_array) #low cut (0-lo)
    gain_ctrl(hi, sample_rate//2 -1, -np.inf, sample_rate, gain_array) #high cut (hi+)
    return enhancer(audio, gain_array)

def exciter(audio, sample_rate, in_lo, in_hi, keep_lo, keep_hi, drive, mix):
    #isolate the band
    sidechain_exciter = band_pass(audio, sample_rate, in_lo, in_hi)
    sidechain_exciter = sidechain_exciter / np.max(np.abs(sidechain_exciter)) #peak of 1, so drive is always effective

    #introduce non-linearity
    nonlin = np.tanh(drive * sidechain_exciter)

    #isolate the band around 6kHZ (5-7kHz? [TUNE]) - this rejetcs 5th harmonics since they lie outside the region
    target_band = band_pass(nonlin, sample_rate, keep_lo, keep_hi)

    #MIXER
    harmonics = mix * target_band
    return audio + harmonics, nonlin, harmonics #output, all harmonics from tanh, harmonics actually added

#Plot the harmonics on their own (for report)
def plot_harmonics(audio, nonlin, harmonics, sample_rate):
    n = len(audio)
    freqs = (np.arange(n // 2) * sample_rate / n)  # frequency bins for plotting

    plt.figure(figsize=(10, 5))
    plt.title("Exciter harmonics")
    for label, x in (("dry voice", audio), ("tanh output (all harmonics)", nonlin), ("added harmonics", harmonics)):
        mag_fft = 20 * np.log10(np.abs((1/n) * fft(x)[:n // 2]) + 1e-12)  # +1e-12 avoids log(0)
        plt.plot(freqs, mag_fft, alpha=0.6, label=label)
    plt.xscale("log")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("magnitude (dB)")
    plt.ylim(bottom=-180)
    plt.legend()
    plt.tight_layout()

#Plot the spectrum zoomed to 2-12kHz before and after the exciter (for report)
def plot_exciter_spectrum(audio, harmonics, sample_rate, in_lo, in_hi, keep_lo, keep_hi):
    n = len(audio)
    freqs = (np.arange(n // 2) * sample_rate / n)  # frequency bins for plotting
    zoom = (freqs >= 2000) & (freqs <= 12000)

    plt.figure(figsize=(12, 5))
    plt.title("Exciter spectrum (2kHz to 12kHz)")
    for label, x, style in (("before (dry)", audio, "g-"), ("added harmonics only", harmonics, "b--")):
        mag_fft = 20 * np.log10(np.abs((1/n) * fft(x)[:n // 2]) + 1e-12)  # +1e-12 avoids log(0)
        plt.plot(freqs[zoom], mag_fft[zoom], style, label=label)
    plt.xscale("log")
    plt.xticks([2000, 3000, 4000, 6000, 8000, 12000], ["2k", "3k", "4k", "6k", "8k", "12k"])
    plt.xlim(2000, 12000)
    plt.ylim(bottom=-150)
    plt.xlabel("frequency (Hz)")
    plt.ylabel("magnitude (dB)")

    y_bottom, y_top = plt.ylim()
    pad = 0.02 * (y_top - y_bottom)  # small gap from the edge

    # Annotate Sidechain
    plt.axvspan(in_lo, in_hi, color="orange", alpha=0.25)
    plt.text(np.sqrt(in_lo * in_hi), y_top - pad, f"sidechain\n{in_lo/1000:g}-{in_hi/1000:g} kHz", color="orange", horizontalalignment='center', verticalalignment='top')

    # Annotate Harmonics kept
    plt.axvspan(keep_lo, keep_hi, color="blue", alpha=0.25)
    plt.text(np.sqrt(keep_lo * keep_hi), y_top - pad, f"harmonics kept\n{keep_lo/1000:g}-{keep_hi/1000:g} kHz", color="blue", horizontalalignment='center', verticalalignment='top')

    plt.legend(loc="lower left")
    plt.tight_layout()

#ALSO PLOT COMPARISONS OF DIFFERENT DRIVE LEVELS
#TUNE THE SYSTEM AND RECORD IT TO SHOWCASE ITERATIVE DEVELOPMENT (REPORT)
