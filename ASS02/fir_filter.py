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

        output = 0.0
        read_idx = self.offset

        for k in range(self.ntaps):
            output += self.coefficients[k] * self.buffer[read_idx]
            
            read_idx -= 1
            if read_idx < 0:
                read_idx = self.ntaps - 1

        self.offset += 1
        if self.offset >= self.ntaps:
            self.offset = 0

        return float(output)


# TEST -REMOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOVE-
if __name__ == "__main__":
    test_coeffs = [0.5, -0.2, 0.1] # random
    firtest = FIRfilter(test_coeffs) # create object

    impulse = [1.0, 0.0, 0.0, 0.0] # unit impulse input 
    # for loop used here, fast enough for 250hz real time but can improve if wanted (also its a test :)
    outputs = [firtest.dofilter(sample) for sample in impulse] # filter operation

    print("Expected impulse response:", [0.5, -0.2, 0.1, 0.0])
    print("Actual filter outputs:    ", outputs)