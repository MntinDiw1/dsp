#Experimental playground to be implemented with run_tasks.py once working. For now this should be self-contained.

import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

from task2_enhance import gain_ctrl, enhancer

    #Dry path

    #Exciter sidechain (HPF: 800-6kHz)

    # Big bottom sidechain (LPF: 50-190Hz)

    #Plot spectrum zoomed between 2-12kHz before and after each change (report: annotated graphs)



#Import audio and normalise
sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")
audio_5cm = audio_5cm / (2**31)

#Band selection

#ATTEMPT1: f = 2kHz (3F = 6kHz). WIDTH = 500Hz
gain_array_5cm = np.ones(len(audio_5cm))
#isolate the band
gain_ctrl(0, 1750, -np.inf, sample_rate_5cm, gain_array_5cm) #low cut (0-1750Hz)
gain_ctrl(2250, sample_rate_5cm//2 -1, -np.inf, sample_rate_5cm, gain_array_5cm) #high cut (2250Hz+)

sidechain_exciter = enhancer(audio_5cm, gain_array_5cm)

#introduce non-linearity
drive = 1
nonlin = np.tanh(drive * sidechain_exciter)

#isolate the band around 6kHZ (5-7kHz? [TUNE]) - this rejetcs 5th harmonics since they lie outside the region
#second gain array that keeps 6kHz region
gain_array_5cm_6kHz = np.ones(len(audio_5cm))
gain_ctrl(0, 5000, -np.inf, sample_rate_5cm, gain_array_5cm_6kHz) # low band (0-5kHz)
gain_ctrl(7000, sample_rate_5cm//2 -1, -np.inf, sample_rate_5cm, gain_array_5cm_6kHz) # high band (7kHz+)

target_band = enhancer(nonlin, gain_array_5cm_6kHz)

#TUNABLE HIGHPASS FILTER

#MIXER
mix_ratio = 0.25 #TUNE
output = audio_5cm + (mix_ratio * target_band)

#TO DO: REMOVE THE POP!!