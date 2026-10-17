import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.io import wavfile

def plot_audio_with_highlights(file_path, highlight_freqs=None):
    """
    Reads a WAV file and plots its time domain and frequency domain.
    
    Parameters:
    - file_path: path to the .wav file
    - highlight_freqs: dictionary of {frequency_in_Hz: "Label String"}
    """
    # Load audio data
    sample_rate, audio = wavfile.read(file_path)
    name = file_path.split('/')[-1]

    # Handle stereo by isolating the left channel
    if len(audio.shape) > 1:
        audio = audio[:, 0]
        
    # Prevent log10(0) warnings by adding a tiny epsilon
    audio = audio + 1e-10

    plt.figure(figsize=(14, 5))

    # --- TIME DOMAIN ---
    n = len(audio)
    time = np.linspace(0, n / sample_rate, num=n) 

    plt.suptitle(f"Audio Analysis: {name}", fontsize=14)
    
    plt.subplot(1, 2, 1)
    plt.title("Time Domain")
    plt.plot(time, audio, color='cornflowerblue')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # --- FREQUENCY DOMAIN ---
    audio_fft = (1/n) * fft(audio)
    
    # decibels relative to full scale (dBFS)
    mag_fft = 20 * np.log10(np.abs(audio_fft))
    freqs = (np.arange(n // 2) * sample_rate / n) 

    plt.subplot(1, 2, 2)
    plt.title("Frequency Domain")
    plt.plot(freqs, mag_fft[: n // 2], color='darkslategray')
    plt.xlabel("Frequency (Hz)")
    plt.xscale("log") 
    plt.ylabel("Magnitude (dB)")

    # --- HIGHLIGHT FREQUENCIES ---
    if highlight_freqs:
        # Generate distinct colors for each highlighted frequency
        colors = plt.cm.get_cmap('Set1', len(highlight_freqs))
        
        for i, (freq, label) in enumerate(highlight_freqs.items()):
            # Plot vertical lines on the frequency spectrum
            plt.axvline(x=freq, color=colors(i), linestyle='--', linewidth=2, 
                        label=f'{label} ({freq} Hz)')
            
            # Add text label slightly above the bottom of the graph
            plt.text(freq * 1.1, plt.ylim()[0] + 10, label, color=colors(i), 
                     rotation=90, verticalalignment='bottom')

        plt.legend(loc="upper right")

    plt.tight_layout() 
    plt.show()

if __name__ == "__main__":
    # Define frequencies to highlight based on your tasks
    frequencies_to_mark = {
        90: "Low frequency noise",
        100: "Vowel Fundamental 1",
        200: "Vowel 1 Harmonic",
        300: "Vowel Fundamental 2",
        400: "Vowel 1 Harmonic",
        500: "Vowel 2 Harmonic",
        #3500: "Consonant Range",
        10000: "High frequency noise"
    }
    
plot_audio_with_highlights("../wav/5cm.wav", highlight_freqs=frequencies_to_mark)