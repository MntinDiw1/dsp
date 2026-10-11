import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
# IFNDEF type statements not required in python, it wont try to import a file twice.


# Assignmnet files
from task1_plot import task1
from task2_enhance import task2


# --- Recommended: 48kHz | Signed 24-bit PCM | Mono (imperative) ---

# Load audio files
sample_rate_1m, audio_1m = wavfile.read("wav/1m.wav")
audio_1m = audio_1m / (2**23)

sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")
audio_5cm = audio_5cm / (2**31)  # NORMALISE (32bits to store 24bit audio, bitwise shift?)

# Plot audio files
fft1m = task1().plot_audio_output_FFT("1m", sample_rate_1m, audio_1m)
fft5cm = task1().plot_audio_output_FFT("5cm", sample_rate_5cm, audio_5cm)

# Show audio plots
plt.show()

# DIAGNOSTIC ONLY!! REMOVE FOR FINAL SUBMISSION
# Save csv files of FFT outputs
#np.savetxt("fft_output_1m.csv", np.array(list(fft1m.items())), delimiter=",", header="Frequency (Hz), Magnitude (dB)", comments="")
#np.savetxt("fft_output_5cm.csv", np.array(list(fft5cm.items())), delimiter=",", header="Frequency (Hz), Magnitude (dB)", comments="")


# Task 2: Audio Enhancement:
enhancement_Matrix = np.array([[100, 2], 
                               [500, 1.5], 
                               [1000, 1], 
                               [2000, 0.8], 
                               [4000, 0.5], 
                               [8000, 0.3], 
                               [16000, 0.2]])

# Apply enhancement transform to both audio files
enhanced_fft_1m = task2().apply_transform(np.array(list(fft1m.items())), enhancement_Matrix)
enhanced_fft_5cm = task2().apply_transform(np.array(list(fft5cm.items())), enhancement_Matrix)

# DIAGNOSTIC ONLY!! REMOVE FOR FINAL SUBMISSION
# Save csv files of FFT outputs
#np.savetxt("enhanced_fft_output_1m.csv", enhanced_fft_1m, delimiter=",", header="Frequency (Hz), Magnitude (dB)", comments="")
#np.savetxt("enhanced_fft_output_5cm.csv", enhanced_fft_5cm, delimiter=",", header="Frequency (Hz), Magnitude (dB)", comments="")

#generate enhanced audio files (broken)
task2().inverse_FFT(enhanced_fft_1m, sample_rate_1m, "enhanced_1m.wav")
task2().inverse_FFT(enhanced_fft_5cm, sample_rate_5cm, "enhanced_5cm.wav")