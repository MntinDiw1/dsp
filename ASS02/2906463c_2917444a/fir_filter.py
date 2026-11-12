# task 3a + 4a - FIRfilter class functions
import numpy as np


class FIRfilter:
    def __init__(self, _coefficients):
        """
        Parameters:
        _coefficients: array
            The M filter coefficients calculated in Task 2.
        """
        self.coefficients = np.array(_coefficients, dtype=float) # load coefficients into object
        self.ntaps = len(self.coefficients) # get buffer array length

        self.buffer = np.zeros(self.ntaps, dtype=float) # generate buffer array

        self.offset = 0 # ring buffer index where the next sample is written

    def dofilter(self, v):
        """
        Parameters:
        v: float
            The incoming input sample x[n].

        Returns:
        float
            The filtered output sample y[n].
        """
        self.buffer[self.offset] = v # load current sample into buffer 

        k = self.offset + 1
        # output = sum[0:M-1](h(m) \dot x(n-m))
        output = (
            np.dot(self.coefficients[:k], self.buffer[self.offset::-1])  # fwd sum
            + np.dot(self.coefficients[k:], self.buffer[:self.offset:-1]) # backward sum
        ) # dot product multiply coefficients with samples in object

        # iterate offset position, reset to zero
        if self.offset == self.ntaps - 1:
            self.offset = 0
        else:
            self.offset += 1


        return float(output)

    def doFilterAdaptive(self, signal, noise, learningRate):
        """
        Parameters:
        signal: float
            Current contaminated ECG sample d[n].
        noise: float
            Current reference noise sample x[n] (e.g. sin(2*pi*50/fs * n)).
        learningRate: float
            LMS step size (mu) controlling how fast the weights adapt.

        Returns:
        float
            The cleaned ECG sample e[n] = d[n] - y[n].
        """
        read_idx = self.offset # store current write index before dofilter increments offset

        y = self.dofilter(noise) # filter reference noise x[n] to estimate interference y[n]

        e = signal - y # subtract estimated noise from signal to get error / clean ECG e[n]

        k = read_idx + 1
        step = learningRate * e # calculate LMS weight update factor (mu * e[n])
        # w_m[n+1] = w_m[n] + mu * e[n] * x[n-m]
        self.coefficients[:k] += step * self.buffer[read_idx::-1] # fwd tap weight update
        self.coefficients[k:] += step * self.buffer[:read_idx:-1] # backward tap weight update

        return float(e)