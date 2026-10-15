#Experimental playground to be implemented with run_tasks.py once working. For now this should be self-contained.

import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

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
    return audio + (mix * target_band)

#Import audio and normalise
sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")
audio_5cm = audio_5cm / (2**31)

# --- ATTEMPT1: f = 2kHz (3F = 6kHz). WIDTH = 500Hz
output = exciter(audio_5cm, sample_rate_5cm, 1750, 2250, 5000, 7000, drive=1, mix=0.25) #TUNE
#Results:

# --- ATTEMPT2:



#Figure out where the sidechain peaks so that the input reaches near +-1 (generalise the system so drive is always effective)
#PLOT BEFORE AND AFTER EXCITER FOR REPORT
#ALSO PLOT COMPARISONS OF DIFFERENT DRIVE LEVELS
#TUNE THE SYSTEM AND RECORD IT TO SHOWCASE ITERATIVE DEVELOPMENT (REPORT)
