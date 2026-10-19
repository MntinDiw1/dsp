import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

from task2_enhance import gain_ctrl, enhancer


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

    #isolate the band around 6kHZ - this rejetcs 5th harmonics since they lie outside the region
    target_band = band_pass(nonlin, sample_rate, keep_lo, keep_hi)

    #MIXER
    harmonics = mix * target_band

    return audio + harmonics, nonlin, harmonics #output, all harmonics from tanh, harmonics actually added

#Plot the harmonics on their own (for report)
def plot_harmonics(audio, nonlin, harmonics, sample_rate, in_lo, in_hi, keep_lo, keep_hi, name):
    
    n = len(audio)
    freqs = np.arange(n // 2) * sample_rate / n  # frequency bins for plotting

    plt.figure(figsize=(10, 5))
    plt.title("Exciter harmonics: " + name)

    for label, x in (("dry voice", audio),
                     ("tanh output (all harmonics)", nonlin),
                     ("added harmonics", harmonics)):
        mag = np.abs(fft(x)[:n // 2]) / n
        mag_db = 20 * np.log10(mag + 1e-12)  # +1e-12 avoids log(0)
        plt.plot(freqs[1:], mag_db[1:], alpha=0.6, label=label)  # skip DC for log axis

    plt.xscale("log")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.xlim(20, sample_rate / 2)
    plt.ylim(bottom=-180)

    # Get axis limits after plotting so annotations sit near the top
    y_bottom, y_top = plt.ylim()
    pad = 0.03 * (y_top - y_bottom)
    x_mid = lambda lo, hi: np.sqrt(lo * hi)  # geometric mean = centre on log axis

    # Annotate sidechain band
    plt.axvspan(in_lo, in_hi, color="blue", alpha=0.25)
    plt.text(x_mid(in_lo, in_hi), y_top - pad,
             f"sidechain\n{in_lo/1000:g}-{in_hi/1000:g} kHz",
             color="blue", ha="center", va="top")

    # Annotate harmonics kept
    plt.axvspan(keep_lo, keep_hi, color="green", alpha=0.25)
    plt.text(x_mid(keep_lo, keep_hi), y_top - pad,
             f"harmonics kept\n{keep_lo/1000:g}-{keep_hi/1000:g} kHz",
             color="green", ha="center", va="top")

    plt.legend(loc="lower left")
    plt.tight_layout()