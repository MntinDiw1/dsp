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