import matplotlib.pyplot as plt
from scipy.io import wavfile

# Assignmnet Files
from task1_plot import plot_audio
from task2_enhance import enhancer



# --- Recommended: 48kHz | Signed 24-bit PCM | Mono (imperative) ---

# Load audio files
sample_rate_1m, audio_1m = wavfile.read("wav/1m.wav")
audio_1m = audio_1m / (2**23)

sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")
audio_5cm = audio_5cm / (2**31)  # NORMALISE (32bits to store 24bit audio, bitwise shift?)

# Plot audio files
plot_audio("1m", sample_rate_1m, audio_1m)
plot_audio("5cm", sample_rate_5cm, audio_5cm)  # how to plot both sets of data in seperate windows?

# Show audio plots
plt.show()