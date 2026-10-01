import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


#Recommended 48kHz | 24-bit PCM 

sample_rate, audio_1cm = wavfile.read("1cm.wav")
sample_rate, audio_5cm = wavfile.read("5cm.wav")

time = np.arange

#plot
print(f"sample_rate: {sample_rate}")

plt.subplot(2, 1, 1)
plt.title("1cm")
plt.plot(time,audio_1cm)