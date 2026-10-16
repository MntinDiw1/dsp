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
def gain_ctrl(low, high, amp_dB, sample_rate, gain_array, q=0):
    """
    q = 0    -> (near) brick-wall, ramps one FFT bin wide (default)
    q = 0.25 -> each edge ramps over 25% of the bandwidth
    q = 1    -> ramps meet in the middle: a triangle
    """
    n = len(gain_array)
    half = n // 2
    bin_hz = sample_rate / n
    freqs = np.arange(half + 1) * bin_hz

    q = np.clip(q, 0.0, 1.0)                  # >1 would make the ramps cross
    ramp_hz = max(q * (high - low), bin_hz)   # never narrower than one bin
    r = ramp_hz / 2

    # bands that start at DC or end at Nyquist: push that ramp outside the spectrum so the ends get the full gain
    if low <= 0:
        low = -ramp_hz
    if high >= sample_rate // 2 - 1:
        high = sample_rate / 2 + ramp_hz

    xp = [low - r, low + r, high - r, high + r]
    fp = [0.0,     amp_dB,  amp_dB,   0.0]
    profile_dB = np.interp(freqs, xp, fp, left=0.0, right=0.0)

    gain_array[:half + 1] *= 10.0 ** (profile_dB / 20.0)
    gain_array[half + 1:] = gain_array[1:n - half][::-1]   # mirror to the negative frequencies
    return gain_array

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
