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

# --- Recommended: 48kHz | Signed 24-bit PCM | Mono (imperative) ---

# Load audio files
"""sample_rate_1m, audio_1m = wavfile.read("wav/1m.wav")"""
"""audio_1m = audio_1m / (2**23)"""

sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")
audio_5cm = audio_5cm / (2**31)  # NORMALISE (32bits to store 24bit audio, bitwise shift?)

# Load audio files
"""plot_audio("1m", sample_rate_1m, audio_1m)"""
plot_audio("5cm", sample_rate_5cm, audio_5cm)  # how to plot both sets of data in seperate windows?


# ---- TASK2: AUDIO ENHANCER ----
#a) make voice sound clearer + more 'interesting' as heard on radio shows
#b) remove noise
#c) explain what kind of noise needs to be removed and which frequency range it has.
#d) explain how you would like to improve the speech by looking into the loss of base freqs. with distance, and pop sounds when mic is close.

#input should be MONO, FLOAT, and NORMALISED.

def enhancer(sample_rate, audio):

    #FILTER PARAMETERS
    LOW_CUT = 20  #Hz
    HIGH_CUT = 20000  #Hz
    #BASS BOOST PARAMETERS
    BB_dB = 12 #dB
    BB_LOW, BB_HI = 60, 240 #Hz
    #BRIGHTNESS PARAMETERS    
    Brt_dB = 6
    Brt_LOW, Brt_HI  = 1000, 4000 #Hz

    # --- FFT ---
    audio_fft = fft(audio)

    # --- GAIN CONTROL (dB) ---
    n = len(audio) #full spectrum
    gain = np.ones(n) #array of n ones (floits). Each value is a multiplier for the corresponding bin

    #LOW CUT
    #There are as many bins per Hz as time (s)
    #(n / F_s) = length of recording (s)
    LC_bin = (LOW_CUT * n) // sample_rate #Hz->bin 
    
    #HIGH CUT
    HC_bin = (HIGH_CUT * n) // sample_rate #Hz->bin

    #BASS BOOST
    BB_GAIN = 10 ** (BB_dB / 20)  # convert dB to linear gain

    BB_LO_bin = (BB_LOW * n) // sample_rate    # Hz -> bin number, same as your LC_bin
    BB_HI_bin = (BB_HI * n) // sample_rate
    gain[BB_LO_bin:BB_HI_bin] *= BB_GAIN #x = x * y #MUST APPLY TO MIRROR (SEE BERND ADVICE)
    #BRIGHTNESS?

    #NOISE REMOVAL

    # AXIS
    # IFFT
    # SCALE

    enhanced_audio = #SCIPY OR NUMPY??

    return enhanced_audio







plt.show()
