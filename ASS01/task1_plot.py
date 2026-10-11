import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft

# ---- TASK1: AUDIO PLOTTING & ANALYSIS ----


# Function to map frequency bins to their value in Hz (k = bin) - TO USE ACROSS TASKS!!!
#implement fold down?

#def x_axis_Hz(k, sample_rate, n):
#    k = np.arange(n)
#    return k * sample_rate / n 


# Function to plot audio data in time and frequency domain
def plot_audio(name, sample_rate, audio):
    plt.figure(figsize=(12, 5))

    # --- TIME (linear/normalised) ---
    n = len(audio)
    time = np.linspace(0, n / sample_rate, num=n)  # array of times

    #a_norm = audio / np.max(np.abs(audio))  # normalise to +-1

    # --- FREQUENCY (logarithmic) ---
    audio_fft = (1/n) * fft(audio)

    # decibels relative to full scale (dBFS) - the loudest level possible in a digital system.

    mag_fft = 20 * np.log10(np.abs(audio_fft))
    freqs = (np.arange(n // 2) * sample_rate / n)  # frequency bins for plotting (//2 returns integer not float)

    print(f"File: {name}, Sample Rate: {sample_rate}")

    plt.suptitle(f"Audio Analysis: {name}")
    plt.subplot(1, 2, 1)
    plt.title("time domain")
    plt.plot(time, audio)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude")

    plt.subplot(1, 2, 2)
    plt.title("frequency domain")
    plt.plot(freqs, mag_fft[: n // 2])
    plt.xlabel("frequency (Hz)")
    plt.xscale("log")  # make logarithmic scale like standard EQ's/visualisers
    plt.ylabel("magnitude (dB)")
    # plt.xlim(20, 20000)  # TOGGLE DEPENDING ON ANALYSIS

    plt.tight_layout()  # stop axes overlapping

    return None  # for task 1, may change later