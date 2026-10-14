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
sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")
audio_5cm = audio_5cm / (2**31)  # NORMALISE (32bits to store 24bit audio, bitwise shift?)

sample_rate_1m, audio_1m = wavfile.read("wav/1m.wav")
audio_1m = audio_1m / (2**31)


# ------ TASK 1 ------

# Plot audio files
plot_audio("5cm", sample_rate_5cm, audio_5cm)
plot_audio("1m", sample_rate_1m, audio_1m)

# ------ TASK 2 ------

# --- ENHANCER TEST ---
#does input match output with no changes applied ?
test_5cm = np.ones(len(audio_5cm)) #untouched gain arrays
test_1m = np.ones(len(audio_1m))
print("Identity test 5cm:", np.allclose(enhancer(audio_5cm, test_5cm), audio_5cm))
print("Identity test 1m:", np.allclose(enhancer(audio_1m, test_1m), audio_1m))
# --- END OF TEST ---

#array of n ones (floits). Each value is a multiplier for the corresponding bin
gain_array_5cm = np.ones(len(audio_5cm))
gain_array_1m = np.ones(len(audio_1m))

#PUT IN ANOTHER FUNCTION: build gain -> enhance -> save -> plot

#start by boosting 6kHz - BERND
#Increase global audio (match both distances and compare to reference)

# --- 5cm ---
#gain curve - gain_ctrl(Low freq, High freq, Gain change, ..., ...)
gain_ctrl(0, sample_rate_5cm //2 - 1, 20, sample_rate_5cm, gain_array_5cm) #VOLUME: doesn't multiply the Nyquist bin twice (?)
gain_ctrl(100, 250, 3, sample_rate_5cm, gain_array_5cm) #BASS BOOST
gain_ctrl(5000, 7000, 4, sample_rate_5cm, gain_array_5cm) #BRIGHTNESS
gain_ctrl(14000, sample_rate_5cm //2 - 1, -60, sample_rate_5cm, gain_array_5cm) #NOISE REMOVAL
gain_ctrl(0, 90, -30, sample_rate_5cm, gain_array_5cm) #POP FILTER
#REMOVE THE POP BY CUTTING LOWS FOR A FEW MILLISECONDS???

#apply gain + save
enhanced_5cm = enhancer(audio_5cm, gain_array_5cm)
wavfile.write("enhanced_5cm.wav", sample_rate_5cm, enhanced_5cm.astype(np.float32))

# --- 1m ---
#gain curve
gain_ctrl(0, sample_rate_1m//2 - 1, 38, sample_rate_1m, gain_array_1m) #VOLUME
gain_ctrl(100, 300, 6, sample_rate_1m, gain_array_1m)  #BASS BOOST
gain_ctrl(5000, 7000, 6, sample_rate_1m, gain_array_1m) #BRIGHTNESS
gain_ctrl(12000, sample_rate_1m//2 - 1, -60, sample_rate_1m, gain_array_1m) #NOISE REMOVAL
gain_ctrl(0, 60, -20, sample_rate_1m, gain_array_1m) #LOW-CUT (for room rumble)

#apply gain + save
enhanced_1m = enhancer(audio_1m, gain_array_1m)
wavfile.write("enhanced_1m.wav", sample_rate_1m, enhanced_1m.astype(np.float32))


# ------ TASK 3 ------




# Show audio plots
plt.show()