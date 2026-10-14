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
low_cut = gain_ctrl(0, 1750, -np.inf, sample_rate_5cm, gain_array_5cm)
high_cut = gain_ctrl(2250, sample_rate_5cm//2 -1, sample_rate_5cm, gain_array_5cm)

sidechain_exciter = enhancer(audio_5cm, gain_array_5cm)

#introduce non-linearity
nonlin = np




#TO DO: REMOVE THE POP!!