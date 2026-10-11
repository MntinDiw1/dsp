import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft

# ---- TASK2: AUDIO ENHANCER ----
#a) make voice sound clearer + more 'interesting' as heard on radio shows
#b) remove noise
#c) explain what kind of noise needs to be removed and which frequency range it has.
#d) explain how you would like to improve the speech by looking into the loss of base freqs. with distance, and pop sounds when mic is close.

#input should be MONO, FLOAT, and NORMALISED.

def enhancer(sample_rate, audio):

    #FILTER PARAMETERS
    LOW_CUT = 20  #Hz
    HIGH_CUT = 20000  #Hz
    #BASS BOOST PARAMETERS
    BB_dB = 12 #dB
    BB_LOW, BB_HI = 60, 240 #Hz
    #BRIGHTNESS PARAMETERS    
    Brt_dB = 6
    Brt_LOW, Brt_HI  = 1000, 4000 #Hz

    # --- FFT ---
    audio_fft = fft(audio)

    # --- GAIN CONTROL (dB) ---
    n = len(audio) #full spectrum
    gain = np.ones(n) #array of n ones (floits). Each value is a multiplier for the corresponding bin

    #LOW CUT
    #There are as many bins per Hz as time (s)
    #(n / F_s) = length of recording (s)
    LC_bin = (LOW_CUT * n) // sample_rate #Hz->bin 
    
    #HIGH CUT
    HC_bin = (HIGH_CUT * n) // sample_rate #Hz->bin

    #BASS BOOST
    BB_GAIN = 10 ** (BB_dB / 20)  # convert dB to linear gain

    BB_LO_bin = (BB_LOW * n) // sample_rate    # Hz -> bin number, same as your LC_bin
    BB_HI_bin = (BB_HI * n) // sample_rate
    gain[BB_LO_bin:BB_HI_bin] *= BB_GAIN #x = x * y #MUST APPLY TO MIRROR (SEE BERND ADVICE)
    #BRIGHTNESS?

    #NOISE REMOVAL

    # AXIS
    # IFFT
    # SCALE

    #enhanced_audio = #SCIPY OR NUMPY??

    return enhanced_audio