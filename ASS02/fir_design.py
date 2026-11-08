#Task 2
import numpy as np
from scipy.fft import ifft

#This function determines the FIR coefficients for freq. ranges specified in the function arguments (2D array: [low, high]) and a given sample rate.
def fir_design(sample_rate, ranges):

    ranges = np.array(ranges)
    min_width = np.min(ranges[:, 1] - ranges[:, 0])

    bin_size = min_width / 2
    M = int(sample_rate / bin_size) #half the narrowest stopband, so every stopband covers at least 2 bins

    M += M%2 # ensure M is even

    #Using folded axis to create a symmetric frequency response
    f = np.arange(M) * sample_rate / M #freq. of each bin
    f = np.minimum(f, sample_rate - f) #fold: bin M-k gets the same freq. as bin k
    H = np.ones(M) #initialise frequencies to 1 (pass band)
    
    #define low and high, setting the bins within this band to 0.
    for low, high in ranges:
        H[(f >= low) & (f <= high)] = 0 #remove bins in range (set to 0)

    # IFFT - produces the impulse response, keeping only the real part (H is mirrored, so complex cancels)
    h = np.real(ifft(H))

    # Swap the two halves: centres the impulse response at M/2
    h_shift = np.zeros(M)
    h_shift[0:M//2] = h[M//2:M]
    h_shift[M//2:M] = h[0:M//2]

    h_windowed = h_shift * np.hamming(M) #apply hamming window to reduce Gibbs ripple from truncation

    #Edge cases (DC and Nyquist) are covered by the folded axis (bin 0 and bin M/2 [fs/2])
    
    return h_windowed
