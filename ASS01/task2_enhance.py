import numpy as np
import matplotlib.pyplot as plt #plot the envelope/EQ visualisation?
from scipy.io import wavfile
from scipy.fft import fft, ifft

# ---- TASK2: AUDIO ENHANCER ----
#a) make voice sound clearer + more 'interesting' as heard on radio shows
#b) remove noise
#c) explain what kind of noise needs to be removed and which frequency range it has.
#d) explain how you would like to improve the speech by looking into the loss of base freqs. with distance, and pop sounds when mic is close.


#input audio should be MONO, FLOAT, and NORMALISED.

# --- GAIN CONTROL (dB) ---
#function that describes gain adjustments to specific frequency ranges.
def gain_ctrl(low, high, amp_dB, sample_rate, gain_array):

    n = len(gain_array) #full spectrum

    LO_bin = (low * n) // sample_rate #Hz->bin
    HI_bin = (high * n) // sample_rate #Hz->bin

    dB__2_lin = 10 ** (amp_dB / 20)  # convert dB to linear gain

    gain_array[LO_bin:HI_bin + 1] *= dB__2_lin #x = x * y
    gain_array[n - HI_bin:n - LO_bin + 1] *= dB__2_lin #mirror

    return None

# --- ENHANCER --- 
#takes gain array and applies it to audio
def enhancer(audio, gain_array):

    #FFT the full signal (all (n) bins)
    audio_fft = fft(audio)

    #multiple the bins by gain_array
    audio_enhanced = audio_fft * gain_array

    #IDEA: loop over bands (low,high,dB tuples) and call the band function or each (DONT DO RN)

    #IFFT gives back all (n) samples, then keep the real part
    audio_ifft = ifft(audio_enhanced) #is this wrong? half the spectrum? (RE vs IM)
    audio_ifft_real = np.real(audio_ifft) #extract the real part (IM part should be ~0 since gain array is mirrored), removing noise from mirror.

    return audio_ifft_real
