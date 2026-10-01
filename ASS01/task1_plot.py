import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft


#Recommended: 48kHz | Signed 24-bit PCM | Mono (imperative)

#Load audio files
sample_rate_1cm, audio_1cm = wavfile.read("wav/1cm.wav")
sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")

def plot_audio(sample_rate, audio):

    #time (linear/normalised)
    n = len(audio)
    time = np.linspace(0, n/sample_rate, num=n) #array of times

    a_norm = audio / np.max(np.abs(audio)) #normalise to +-1

    #frequency (logarithmic)
    audio_fft = fft(audio)
    frequency = #blingblongblang bing bing hello!


    plt.subplot(2, 2, 1)
    plt.title("time domain)")
    plt.plot(time, a_norm)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude")

    plt.subplot(2, 2, 2)
    plt.title("frequency domain)")
    plt.plot (frequency, audio_fft)
    plt.xlabel("frequency (Hz)")
    plt.ylabel("amplitude")

return #??    


plot_audio(sample_rate_1cm, audio_1cm)
plot_audio(sample_rate_5cm, audio_5cm)