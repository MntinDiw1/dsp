import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
# IFNDEF type statements not required in python, it wont try to import a file twice.

# Assignmnet files
from task1_plot import plot_audio
from task2_enhance import gain_ctrl, enhancer, plot_gain_array
from task3_exciter import exciter, plot_harmonics

# --- Recommended: 48kHz | Signed 24-bit PCM | Mono (imperative) ---

# Load audio files and normalise (32 bit int)
sample_rate_5cm, audio_5cm = wavfile.read("wav/5cm.wav")
audio_5cm = audio_5cm / (2**31)  # NORMALISE (32bits to store 24bit audio, bitwise shift?)

sample_rate_1m, audio_1m = wavfile.read("wav/1m.wav")
audio_1m = audio_1m / (2**31)


# ------ TASK 1 ------

# Plot audio files
#plot_audio("5cm", sample_rate_5cm, audio_5cm)
#plot_audio("1m", sample_rate_1m, audio_1m)

# ------ TASK 2 ------

##TRIMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# --- ENHANCER TEST ---
#does input match output with no changes applied ?
test_5cm = np.ones(len(audio_5cm)) #untouched gain arrays
test_1m = np.ones(len(audio_1m))
print("Identity test 5cm:", np.allclose(enhancer(audio_5cm, test_5cm), audio_5cm))
print("Identity test 1m:", np.allclose(enhancer(audio_1m, test_1m), audio_1m))
# --- END OF TEST ---

# --- VOLUME MATCH ---

#array of n ones (floits). Each value is a multiplier for the corresponding bin
gain_array_5cm = np.ones(len(audio_5cm))
gain_array_1m = np.ones(len(audio_1m))

#PUT IN ANOTHER FUNCTION: build gain -> enhance -> save -> plot

# --- 5cm ---
#gain curve - gain_ctrl(Low freq, High freq, Gain change, ..., ..., q=0)
gain_ctrl(0, 80, -16, sample_rate_5cm, gain_array_5cm, q=0.1) #LOW CUT: Remove rumble and some POP energy
gain_ctrl(95, 400, 4, sample_rate_5cm, gain_array_5cm, q=0.1) #BASS BOOST: The first couple harmonics for depth
gain_ctrl(3000, 10000, 6, sample_rate_5cm, gain_array_5cm, q=0.1) #BRIGHTNESS: The noisy consonant region + extra for clarity
gain_ctrl(12200, sample_rate_5cm //2 - 1, -12, sample_rate_5cm, gain_array_5cm, q=0.1) #HIGH CUT: Remove any hiss

#apply gain + save
plot_gain_array(gain_array_5cm,sample_rate_5cm,"5cm")
enhanced_5cm = enhancer(audio_5cm, gain_array_5cm)
wavfile.write("enhanced_5cm.wav", sample_rate_5cm, ((2**31-1)*enhanced_5cm).astype(np.int32))

# --- 1m ---
#gain curve
gain_ctrl(0, sample_rate_1m//2 - 1, 21, sample_rate_1m, gain_array_1m) #VOLUME: Match to  5cm recording (matching peaks)
gain_ctrl(0, 85, -12, sample_rate_1m, gain_array_1m, q=0.3) #LOW CUT: trim room rumble (less 'boxy')
gain_ctrl(95, 180, 6, sample_rate_1m, gain_array_1m, q=0.3)  #BASS BOOST: fundamental higher @1m + restoring depth to voice 
gain_ctrl(480, 505, -12, sample_rate_1m, gain_array_1m, q=0.25)  #Reduce the 500Hz spike/whine (10th harmonic of MAINS HUM??)
gain_ctrl(2200, 2800, -4, sample_rate_1m, gain_array_1m, q=0.25)  #ROOM RESONANCE: 1m bump ~2.5kHz vs 5cm
gain_ctrl(3000, 10000, 7, sample_rate_1m, gain_array_1m, q=0.1) #BRIGHTNESS
gain_ctrl(13000, sample_rate_1m//2 - 1, -30, sample_rate_1m, gain_array_1m, q=0.1) #HIGH CUT consonants end lower

#apply gain + save
plot_gain_array(gain_array_1m,sample_rate_1m,"1m")
enhanced_1m = enhancer(audio_1m, gain_array_1m)
wavfile.write("enhanced_1m.wav", sample_rate_1m, ((2**31-1)*enhanced_1m).astype(np.int32)) #int32 scaled up (mention in report)

##TRIMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# --- AUDIO OVERLAY ---
def plot_overlay(signals):
    # signals: list of (label, sample_rate, audio)
    plt.figure(figsize=(8, 5))

    for label, fs, audio in signals:
        n = len(audio)
        mag_fft = 20 * np.log10(np.abs((1/n) * np.fft.fft(audio)) + 1e-12)  # +1e-12 avoids log(0)
        freqs = np.arange(n // 2) * fs / n

        plt.plot(freqs, mag_fft[: n // 2], alpha=0.6, label=label)

    plt.title("Enhanced audio: 5cm vs 1m (frequency domain)")
    plt.xlabel("frequency (Hz)")
    plt.xscale("log")
    plt.ylabel("magnitude (dB)")
    plt.legend()

    plt.tight_layout()

plot_overlay([("5cm", sample_rate_5cm, enhanced_5cm),
              ("1m", sample_rate_1m, enhanced_1m)])
# --- END OF OVERLAY ---

# ------ TASK 3 ------

#Run on RAW and ENHANCED audio       

#exciter(.., .., in_low, in_high, keep_lo, keep_hi, drive, mix)

# --- ATTEMPT1: f = 2kHz (3F = 6kHz). WIDTH = 500Hz
#apply exciter + save
exciter_5cm, nonlin_5cm, harmonics_5cm = exciter(audio_5cm, sample_rate_5cm, 1750, 2250, 5000, 7000, drive=10, mix=0.5)
plot_harmonics(audio_5cm, nonlin_5cm, harmonics_5cm, sample_rate_5cm)
wavfile.write("exciter_5cm.wav", sample_rate_5cm, ((2**31-1)*exciter_5cm).astype(np.int32))
#Results:

# --- ATTEMPT2:


# Show audio plots
plt.show()