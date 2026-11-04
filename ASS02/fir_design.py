'''
Create a general purpose function which calculates the FIR coefficients
by providing the sampling rate and an array of frequency ranges which
need to be removed also taking care of edge cases such as DC removal.
The design function should use the IFFT to calculate the coefficients and
also calculates the number of coefficients. Explain your reasoning of how
the number of coefficients are calculated
'''

import numpy as np
from scipy.fftpack import ifft

from ecg_plot import sample_rate

#Remove baseline wander

#Remove 50Hz mains hum

#Test removing everything above 40Hz: would remove noise but could also remove some of the QRS complex

#Declare frequency ranges to remove
baseline_wander = [0, 0.5]
mains_hum = [45, 125] #why 125Hz specifically? - to remove harmonics?


def fir_coeff(sample_rate, ranges)