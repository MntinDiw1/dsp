'''
Create a general purpose function which calculates the FIR coefficients
by providing the sampling rate and an array of frequency ranges which
need to be removed also taking care of edge cases such as DC removal.
The design function should use the IFFT to calculate the coefficients and
also calculates the number of coefficients. Explain your reasoning of how
the number of coefficients are calculated
'''