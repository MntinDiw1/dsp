import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

# Function to plot audio data in time and frequency domain
def plot_audio(name, sample_rate, audio, vowels_Start, vowels_end, consonants_start, consonant_end, noise_start, noise_end=0):
    plt.figure(figsize=(12, 5))

    # Time domain  
    n = len(audio)
    time = np.linspace(0, n / sample_rate, num=n)  # array of times

    # Frequency domain
    audio_fft = (1/n) * fft(audio)

    # decibels relative to full scale (dBFS) - the loudest level possible in a digital system.
    mag_fft = 20 * np.log10(np.abs(audio_fft) + 1e-10) # Added small offset to avoid log10(0)
    freqs = (np.arange(n // 2) * sample_rate / n)  # frequency bins for plotting

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
    plt.show()

    # vowel/consonant/noise id
    
    # Calculate harmonics
    harmonic1_start = vowels_Start * 2
    harmonic1_end = vowels_end * 2
    harmonic2_start = vowels_Start * 3
    harmonic2_end = vowels_end * 3
    harmonic3_start = vowels_Start * 4
    harmonic3_end = vowels_end * 4
    
    # If noise_end wasn't provided, default it to the Nyquist frequency
    if noise_end == 0:
        noise_end = sample_rate / 2

    # Plot setup
    plt.figure(figsize=(12, 5))
    plt.suptitle(f"Annotated frequency domain: {name}")
    plt.plot(freqs, mag_fft[: n // 2])
    plt.xlabel("frequency (Hz)")
    plt.xscale("log")
    plt.ylabel("magnitude (dB)")

    # Get y-limits after plotting so labels sit at the very bottom/top
    y_bottom, y_top = plt.ylim()
    pad = 0.02 * (y_top - y_bottom)  # small gap from the edge

    # Annotate Vowels
    plt.axvspan(vowels_Start, vowels_end, color="red", alpha=0.25)
    plt.text(np.sqrt(vowels_Start * vowels_end), y_bottom + pad, "Vowels", color="red", rotation=90, horizontalalignment='center', verticalalignment='bottom')

    # Annotate Harmonics
    plt.text(np.sqrt(harmonic1_start * harmonic1_end), y_bottom + pad, "Harmonics 1, 2, 3", color="orange", rotation=90, horizontalalignment='center', verticalalignment='bottom')

    plt.axvspan(harmonic1_start, harmonic1_end, color="orange", alpha=0.25)

    plt.axvspan(harmonic2_start, harmonic2_end, color="orange", alpha=0.25)

    plt.axvspan(harmonic3_start, harmonic3_end, color="orange", alpha=0.25)

    # Annotate Consonants
    plt.axvspan(consonants_start, consonant_end, color="blue", alpha=0.25)
    plt.text(np.sqrt(consonants_start * consonant_end), y_bottom + pad, "Consonants", color="blue", rotation=90, horizontalalignment='center', verticalalignment='bottom')

    # Annotate Noise (top of the graph)
    plt.axvspan(noise_start, noise_end, color="gray", alpha=0.25)
    plt.text(np.sqrt(noise_start * noise_end), y_top - pad, "Noise", color="gray", rotation=90, horizontalalignment='center', verticalalignment='top')
    
    plt.tight_layout()
    plt.show()

    return None