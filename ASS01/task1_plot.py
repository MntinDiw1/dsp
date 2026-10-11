import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# ---- TASK1: AUDIO PLOTTING & ANALYSIS ----
# a) plot audio in time domain 
# b) plot audio in frequency domain
# c) (Not Main Code) Visually identify vowel fundamental frequencies and mark these on a frequency spectrum.
# d) (Not Main Code) Mark the consonant frequency ranges on a frequency spectrum.
# e) (Not Main Code) Mark the noise frequency ranges on a frequency spectrum.


# Function to plot audio data in time and frequency domain
class task1:
    @staticmethod # this decorator allows the method to be called without creating an instance of the class
    def plot_audio_output_FFT(name, sample_rate, audio):
        plt.figure(figsize=(12, 5))

        # --- TIME (linear/normalised) ---
        n = len(audio)
        time = np.linspace(0, n / sample_rate, num=n)  # array of times

        #a_norm = audio / np.max(np.abs(audio))  # normalise to +-1

        # --- FREQUENCY (logarithmic) ---
        audio_fft = (1/n) * fft(audio)

        # decibels relative to full scale (dBFS) - the loudest level possible in a digital system.
        complex_mag_fft = 20 * np.log10(audio_fft)
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

        # full FFT sepctrum output to mark-up and apply transforms in task 2:
        fft_output = {freqs[i]: complex_mag_fft[i] for i in range(len(freqs))}  # dictionary of frequency bins and their corresponding magnitudes

        return fft_output  # for task 1, may change later
