import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
# IFNDEF type statements not required in python, it wont try to import a file twice.

# Assignmnet files
#CAN ALSO IMPORT THE WHOLE FILE
from task1_plot import plot_audio
from task2_enhance import gain_ctrl, enhancer, plot_gain_array

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

#start by boosting 6kHz - BERND
#Increase global audio (match both distances and compare to reference)

# --- 5cm ---
#gain curve - gain_ctrl(Low freq, High freq, Gain change, ..., ...)
#gain_ctrl(0, sample_rate_5cm //2 - 1, 12, sample_rate_5cm, gain_array_5cm) #VOLUME: doesn't multiply the Nyquist bin twice (?)
gain_ctrl(0, 60, -12, sample_rate_5cm, gain_array_5cm, 100) #LOW CUT: Remove rumble and some POP energy
gain_ctrl(95, 400, 3.5, sample_rate_5cm, gain_array_5cm, 100) #BASS BOOST: The first couple harmonics for depth
gain_ctrl(3000, 10000, 6, sample_rate_5cm, gain_array_5cm, 100) #BRIGHTNESS: The noisy consonant region + extra for clarity
gain_ctrl(12200, sample_rate_5cm //2 - 1, -12, sample_rate_5cm, gain_array_5cm, 100) #HIGH CUT: Remove any hiss

#apply gain + save
plot_gain_array(gain_array_5cm,sample_rate_5cm,"5cm")
enhanced_5cm = enhancer(audio_5cm, gain_array_5cm)
wavfile.write("enhanced_5cm.wav", sample_rate_5cm, ((2**31-1)*enhanced_5cm).astype(np.int32))

# --- 1m ---
#gain curve
gain_ctrl(0, sample_rate_1m//2 - 1, 21, sample_rate_1m, gain_array_1m) #VOLUME: Match to  5cm recording (matching peaks)
gain_ctrl(0, 85, -12, sample_rate_1m, gain_array_1m) #LOW CUT: trim room rumble (less 'boxy')
gain_ctrl(105, 300, 5.5, sample_rate_1m, gain_array_1m)  #BASS BOOST: fundamental higher @1m + restoring depth 
#gain_ctrl(300, 700, -0.5, sample_rate_1m, gain_array_1m) #MIDS: Making the sample less 'muddy'
gain_ctrl(2800, 10000, 6, sample_rate_1m, gain_array_1m) #BRIGHTNESS
gain_ctrl(13000, sample_rate_1m//2 - 1, -12, sample_rate_1m, gain_array_1m) #HIGH CUT consonants end lower
#gain_ctrl(0, sample_rate_1m//2 - 1, 38, sample_rate_1m, gain_array_1m) #VOLUME
gain_ctrl(100, 300, 6, sample_rate_1m, gain_array_1m, 10)  #BASS BOOST
gain_ctrl(5000, 7000, 6, sample_rate_1m, gain_array_1m, 20) #BRIGHTNESS
gain_ctrl(16000, sample_rate_1m//2 - 1, -60, sample_rate_1m, gain_array_1m, 30) #NOISE REMOVAL
gain_ctrl(0, 60, -20, sample_rate_1m, gain_array_1m, 50) #LOW-CUT (for room rumble)

#apply gain + save
plot_gain_array(gain_array_1m,sample_rate_1m,"1m")
enhanced_1m = enhancer(audio_1m, gain_array_1m)
wavfile.write("enhanced_1m.wav", sample_rate_1m, ((2**31-1)*enhanced_1m).astype(np.int32)) #int32 scaled up (mention in report)

#PLOT GAIN CURVE - I want to see the volume

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





# Show audio plots
plt.show()