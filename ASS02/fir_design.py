'''
Create a general purpose function which calculates the FIR coefficients
by providing the sampling rate and an array of frequency ranges which
need to be removed also taking care of edge cases such as DC removal.
The design function should use the IFFT to calculate the coefficients and
also calculates the number of coefficients. Explain your reasoning of how
the number of coefficients are calculated
'''

import numpy as np
from scipy import fft, ifft

#Remove baseline wander
#Remove 50Hz mains hum

#Describe the function
def fir_design(sample_rate, ranges):

    #convert each range to bins with the formula (k = f × M / fs) 

    min_width_v1 = min([r[1] - r[0] for r in ranges]) #can for loop be used?
    #alternative:
    ranges = np.array(ranges)
    min_width_v2 = np.min(ranges[:, 1] - ranges[:, 0])

    bin_size = min_width_v1 / 2
    M = int(sample_rate / bin_size) #number of coefficients (explain!)
    #why does M have to be even?
    M += M%2 #ensure M is even (modulo operator is the remainder after division) 

    '''
    The number of coefficients, M, is calculated based on the minimum width of the frequency range arguments.
    The minimum width is divided by 2 so that each range alway has at least 2 bins to operate on.
    The number of coefficients is then calculated by dividing the sample rate by the bin size.
    M is made even so that the filter always has a symmetric impulse response (required for linear phase filters)
    '''

    # Build the frequency response of the filter (M long array with a value for each bin)

    #define low and high
    for r in ranges:
        low = r[0]
        high = r[1]
    #Using folded axis to create a symmetric frequency response
    f = np.arange(M) * sample_rate / M #freq. of eahc bin
    f = np.minimum(f, sample_rate - f) #fold: bin M-k gets the same freq. as bin k

    H[(f >= low) & (f <= high)] = 0 #remove bins in range (set to 0) - SHOULD I DO THE INVERSE OF THIS? (set to 1 outside range)

    return beepbeep.itis.I.the.computer.