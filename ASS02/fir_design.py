#Task 2
import numpy as np
from scipy.fft import ifft

#Describe the function
def fir_design(sample_rate, ranges):

    ranges = np.array(ranges)
    min_width = np.min(ranges[:, 1] - ranges[:, 0])

    bin_size = min_width / 2
    M = int(sample_rate / bin_size) #number of coefficients (explain!)

    M += M%2 # ensure M is even

    '''
    The number of coefficients, M, is calculated based on the minimum width of the frequency range arguments.
    The minimum width is divided by 2 so that each range alway has at least 2 bins to operate on.
    The number of coefficients is then calculated by dividing the sample rate by the bin size.
    M is made even so that the impulse response can be split into two equal halves when it is shifted.
    '''

    #Using folded axis to create a symmetric frequency response
    f = np.arange(M) * sample_rate / M #freq. of eahc bin
    f = np.minimum(f, sample_rate - f) #fold: bin M-k gets the same freq. as bin k
    H = np.ones(M) #initialise frequencies to 1 (pass band)
    
    #define low and high
    for low, high in ranges:
        H[(f >= low) & (f <= high)] = 0 #remove bins in range (set to 0)

    # IFFT - produces the impulse response, keeping only the real part (H is mirrored, so complex cancels)
    h = np.real(ifft(H))

    # Swap the two halves (see 6.7.6 or Bernd's notes)
    h_shift = np.zeros(M)
    h_shift[0:M//2] = h[M//2:M]
    h_shift[M//2:M] = h[0:M//2]

    h_windowed = h_shift * np.hamming(M) #can this be used?

    '''
    Edge cases (DC and Nyquist) and covered by the folded axis (bin 0 and bin 125 [fs/2])
    '''
    return h_windowed


###REMOVE THIS POOPY
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from scipy.fft import fft
    from support_funcs import import_ecg_data, vector_plot_export

    _, _, sample_rate = import_ecg_data("ecg1.tsv")
    baseline_wander = [0, 0.5]
    mains_hum = [45, 125]

    h = fir_design(sample_rate, [baseline_wander, mains_hum])
    M = len(h)

    freqs_h = np.arange(M // 2 + 1) * sample_rate / M
    H_mag = np.abs(fft(h))[:M // 2 + 1]

    plt.figure(figsize=(12, 6))
    plt.suptitle(f"FIR Filter Design (M = {M} taps, fs = {sample_rate:.0f} Hz)")

    plt.subplot(2, 1, 1)
    plt.title("Impulse Response h[n] (Shifted & Hamming Windowed)")
    plt.plot(np.arange(M), h)
    plt.xlim(0, M - 1)
    plt.xlabel("Tap Index (n)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.title("Frequency Response |H(f)|")
    plt.plot(freqs_h, H_mag)
    plt.axvspan(0, 0.5, color="red", alpha=0.2, label="DC / Baseline Stopband (0-0.5 Hz)")
    plt.axvspan(45, 125, color="orange", alpha=0.2, label="Mains / HF Stopband (45-125 Hz)")
    plt.xlim(0, sample_rate / 2)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain")
    plt.legend(loc="upper right")
    plt.grid(True)

    plt.tight_layout()
    vector_plot_export("t2_coeffs")
    plt.show()