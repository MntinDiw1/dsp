import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# Function to plot audio data in time and frequency domain
def plot_audio(name, sample_rate, audio):
    plt.figure(figsize=(12, 5))

    # Time domain  
    n = len(audio)
    time = np.linspace(0, n / sample_rate, num=n)  # array of times

    # Frequency domain
    audio_fft = (1/n) * fft(audio)

    # decibels relative to full scale (dBFS) - the loudest level possible in a digital system.
    mag_fft = 20 * np.log10(np.abs(audio_fft))
    freqs = (np.arange(n // 2) * sample_rate / n)  # frequency bins for plotting (//2 returns integer not float)

    print(f"File: {name}, Sample Rate: {sample_rate}")

    # time domain plot
    plt.suptitle(f"Audio Analysis: {name}")
    plt.subplot(1, 2, 1)
    plt.title("time domain")
    plt.plot(time, audio)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude")

    # frequency domain plot  
    plt.subplot(1, 2, 2)
    plt.title("frequency domain")
    plt.plot(freqs, mag_fft[: n // 2])
    plt.xlabel("frequency (Hz)")
    plt.xscale("log")  # make logarithmic scale like standard EQ's/visualisers
    plt.ylabel("magnitude (dB)")

    plt.tight_layout()  # stop axes overlapping

    return None
