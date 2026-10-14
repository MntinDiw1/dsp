import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
# IFNDEF type statements not required in python, it wont try to import a file twice.

# Assignmnet files
#CAN ALSO IMPORT THE WHOLE FILE
from task1_plot import plot_audio
from task2_enhance import gain_ctrl, enhancer

# --- Recommended: 48kHz | Signed 24-bit PCM | Mono (imperative) ---

# Load audio files and normalise (32 bit int)
sample_rate_1m, audio_1m = wavfile.read("wav/1m.wav")
audio_1m = audio_1m / (2**31)

sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")
audio_5cm = audio_5cm / (2**31)  # NORMALISE (32bits to store 24bit audio, bitwise shift?)


# --- TASK 1 ---

# Plot audio files
plot_audio("1m", sample_rate_1m, audio_1m)
plot_audio("5cm", sample_rate_5cm, audio_5cm)



# --- TASK 2 ---
#COLLAPSE GAIN ARRAYS INTO 'EQ' LISTS (VOID FOR LOOPS!!!)

#make ones array the length of audio
#array of n ones (floits). Each value is a multiplier for the corresponding bin
gain_array_5cm = np.ones(len(audio_5cm))
gain_array_1m = np.ones(len(audio_1m))
# ^where to put this (embded into a function?)


# --- ENHANCER TEST ---
#does input match output with no changes applied ?
gain_ctrl(20, 20000, 0, sample_rate_5cm, gain_array_5cm) #unnecessary but useful for test isolation
gain_ctrl(20, 20000, 0, sample_rate_1m, gain_array_1m )

test_5cm = np.ones(len(audio_5cm))   # fresh, untouched gain arrays
test_1m = np.ones(len(audio_1m))

print("Identity test 5cm:", np.allclose(enhancer(audio_5cm, test_5cm), audio_5cm))
print("Identity test 1m:", np.allclose(enhancer(audio_1m, test_1m), audio_1m))
# --- END OF TEST ---


'''start by boosting 6kHz - BERND'''
'''FIND OPTIMAL EQ SETTING (USING ABLETON) AND JUSTIFY FOR REPORT'''
'''Increase global audio (match both distances and compare to reference)'''
# 5cm
#BASS BOOST
gain_ctrl(60, 240, 12, sample_rate_5cm, gain_array_5cm) #TUNE
#BRIGHTNESS
gain_ctrl(1000, 4000, 6, sample_rate_5cm, gain_array_5cm) #TUNE

# 1m
#BASS BOOST
gain_ctrl(60, 240, 12, sample_rate_1m, gain_array_1m) #TUNE
#BRIGHTNESS
gain_ctrl(1000, 4000, 6, sample_rate_1m, gain_array_1m) #TUNE

##PLOT (envelope or delta - see what was removed) TO CHECK


# Show audio plots
plt.show()