import numpy as np


class FIRfilter:
    def __init__(self, _coefficients):
        """
        Parameters:
        fir_coefficients: array
            The M filter coefficients calculated in Task 2.
        """
        self.coefficients = np.array(_coefficients, dtype=float)
        self.ntaps = len(self.coefficients)

        self.buffer = np.zeros(self.ntaps, dtype=float)

        self.offset = 0

    def dofilter(self, v):
        """
        Parameters:
        v: float
            The incoming input sample x[n].

        Returns:
        float
            The filtered output sample y[n].
        """
        self.buffer[self.offset] = v

        k = self.offset + 1
        output = (
            np.dot(self.coefficients[:k], self.buffer[self.offset::-1])
            + np.dot(self.coefficients[k:], self.buffer[:self.offset:-1])
        )

        self.offset += 1
        if self.offset >= self.ntaps:
            self.offset = 0

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
        read_idx = self.offset

        y = self.dofilter(noise)

        e = signal - y

        k = read_idx + 1
        step = learningRate * e
        self.coefficients[:k] += step * self.buffer[read_idx::-1]
        self.coefficients[k:] += step * self.buffer[:read_idx:-1]

        return float(e)