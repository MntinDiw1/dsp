import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft


# Function to plot audio data in time and frequency domain
def plot_audio(name, sample_rate, audio):
    plt.figure(figsize=(12, 5))

    # time (linear/normalised)
    n = len(audio)
    time = np.linspace(0, n / sample_rate, num=n)  # array of times

    a_norm = audio / np.max(np.abs(audio))  # normalise to +-1

    # frequency (logarithmic)
    audio_fft = fft(audio)
    a_fft = 20 * np.log10(
        np.abs(audio_fft)
    )  # magnitude of complex value in dB (20*log10(|x|))
    freqs = (
        np.arange(n // 2) * sample_rate / n
    )  # frequency bins for plotting (//2 returns integer not float)

    print(f"File: {name}, Sample Rate: {sample_rate}")

    plt.suptitle(f"Audio Analysis: {name}")
    plt.subplot(1, 2, 1)
    plt.title("time domain")
    plt.plot(time, a_norm)
    plt.xlabel("time (s)")
    plt.ylabel("amplitude")

    plt.subplot(1, 2, 2)
    plt.title("frequency domain")
    plt.plot(freqs, a_fft[: n // 2])
    plt.xlabel("frequency (Hz)")
    plt.xscale("log")  # make logarithmic scale like standard EQ's/visualisers???
    plt.ylabel("magnitude (dB)")
    plt.xlim(20, 20000)  # TOGGLE DEPENDING ON ANALYSIS

    plt.tight_layout()  # stop axes overlapping

    return None  # for task 1, may change later


"""Recommended: 48kHz | Signed 24-bit PCM | Mono (imperative)"""

# Load audio files
# sample_rate_1m, audio_1m = wavfile.read("wav/1m.wav")
sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")

# Load audio files
# plot_audio("1m", sample_rate_1m, audio_1m)
plot_audio(
    "5cm", sample_rate_5cm, audio_5cm
)  # how to plot both sets of data in seperate windows?

plt.show()
