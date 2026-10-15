import numpy as np
import matplotlib.pyplot as plt #plot the envelope/EQ visualisation?
from scipy.fft import fft, ifft

# ---- TASK2: AUDIO ENHANCER ----
#a) make voice sound clearer + more 'interesting' as heard on radio shows
#b) remove noise
#c) explain what kind of noise needs to be removed and which frequency range it has.
#d) explain how you would like to improve the speech by looking into the loss of base freqs. with distance, and pop sounds when mic is close.


#input audio should be MONO, FLOAT, and NORMALISED.

# --- GAIN CONTROL (dB) ---
#function that describes gain adjustments to specific frequency ranges.
def gain_ctrl(low, high, amp_dB, sample_rate, gain_array, q_factor=0):  # q_factor = ramp width in bins (0 = hard edges)
    n = len(gain_array)

    LO_bin = (low * n) // sample_rate    # Hz -> bin
    HI_bin = (high * n) // sample_rate

    lin = 10 ** (amp_dB / 20)            # dB -> linear

    # distance of every bin from DC (so bin k and bin n-k get the same gain)
    k = np.arange(n)
    folded = np.minimum(k, n - k)

    # trapezoid: 1 -> lin over q_factor bins, flat, then lin -> 1
    # (np.interp holds the end values, so anything outside is 1,
    #  and a ramp that would start below bin 0 is simply cut off)
    trap = np.interp(folded,
                     [LO_bin - q_factor, LO_bin, HI_bin, HI_bin + q_factor],
                     [1.0,               lin,    lin,    1.0])

    gain_array *= trap
    return None

def plot_gain_array(gain_array, sample_rate, name):
    n = len(gain_array)
    freqs = (np.arange(n // 2) * sample_rate / n)  # frequency bins for plotting

    plt.figure(figsize=(10, 5))
    plt.title("Gain Control Curve " + name)
    plt.plot(freqs, 20 * np.log10(np.abs(gain_array[:n // 2])), color='green')
    plt.xscale("log")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain (dB)")
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()  # plt.show() is called once at the end of run_tasks.py

    return None

# --- ENHANCER --- 
#takes gain array and applies it to audio
def enhancer(audio, gain_array):

    #FFT the full signal (all (n) bins)
    audio_fft = fft(audio)

    #multiply the bins by gain_array
    audio_enhanced = audio_fft * gain_array

    #IFFT gives back all (n) samples, then keep the real part
    audio_ifft = ifft(audio_enhanced)
    audio_ifft_real = np.real(audio_ifft) #extract the real part (IM part should be ~0 since gain array is mirrored)

    return audio_ifft_real
