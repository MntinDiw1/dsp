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
#function that applied gain adjustments to specific frequency ranges.

#TDL: 
# where is gain_array coming from?
#nest within larger Task 2 function (rember to create 2 arrays for each audio file)
def enhancer(low, high, amp_dB, sample_rate, gain_array):

    n = len(gain_array) #full spectrum

    LO_bin = (low * n) // sample_rate #Hz->bin
    HI_bin = (high * n) // sample_rate #Hz->bin

    dB__2_lin = 10 ** (amp_dB / 20)  # convert dB to linear gain

    gain_array[LO_bin:HI_bin + 1] *= dB__2_lin #x = x * y
    gain_array[n - HI_bin:n - LO_bin + 1] *= dB__2_lin #mirror


    return None
