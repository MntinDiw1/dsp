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

        for k in range(self.ntaps):
            self.coefficients[k] += learningRate * e * self.buffer[read_idx]
            
            read_idx -= 1
            if read_idx < 0:
                read_idx = self.ntaps - 1

        return float(e)


# TEST -REMOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOVE-
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from scipy.fft import ifft

    # --- Test 1: Unit Impulse Sanity Check ---
    test_coeffs = [0.5, -0.2, 0.1] # random
    firtest = FIRfilter(test_coeffs) # create object

    impulse = [1.0, 0.0, 0.0, 0.0] # unit impulse input 
    # for loop used here, fast enough for 250hz real time but can improve if wanted (also its a test :)
    outputs = [firtest.dofilter(sample) for sample in impulse] # filter operation

    print("Expected impulse response:", [0.5, -0.2, 0.1, 0.0])
    print("Actual filter outputs:    ", outputs)

    # 100% AI Generated code, no human input.
    # --- Test 2: Realistic Test Filter on saad_ecg_1.tsv (Before vs After Overlay) ---
    data = np.loadtxt("ECG_DATA/saad_ecg_1.tsv")
    t = data[:, 0]
    ecg_raw = data[:, 8]  # column 8 = ADC channel 2
    fs = 250.0

    # Quick 500-tap IFFT test filter:
    # 1) Highpass only (removes DC/wander 0-1 Hz, keeps 50 Hz so LMS can cancel it)
    M = 500
    f_resp_hp = np.ones(M)
    k_hp = int(round(1.0 / fs * M))
    f_resp_hp[0 : k_hp + 1] = 0
    f_resp_hp[M - k_hp : M] = 0

    h_hp = np.real(ifft(f_resp_hp))
    h_hp_shift = np.zeros(M)
    h_hp_shift[0 : M // 2] = h_hp[M // 2 : M]
    h_hp_shift[M // 2 : M] = h_hp[0 : M // 2]
    hp_coeffs = h_hp_shift * np.hamming(M)
    hp_coeffs -= np.mean(hp_coeffs)

    # 2) Full Highpass + 50 Hz Bandstop (for Task 3 FIR filter)
    f_resp_full = f_resp_hp.copy()
    k1, k2 = int(round(48.0 / fs * M)), int(round(52.0 / fs * M))
    f_resp_full[k1 : k2 + 1] = 0
    f_resp_full[M - k2 : M - k1 + 1] = 0

    h_full = np.real(ifft(f_resp_full))
    h_full_shift = np.zeros(M)
    h_full_shift[0 : M // 2] = h_full[M // 2 : M]
    h_full_shift[M // 2 : M] = h_full[0 : M // 2]
    prac_coeffs = h_full_shift * np.hamming(M)
    prac_coeffs -= np.mean(prac_coeffs)  # ensure strict 0 DC gain after windowing

    # --- Run Task 3 (Fixed Bandstop FIR) and Task 4 (Adaptive LMS) sample-by-sample ---
    print("Filtering saad_ecg_1.tsv with Fixed FIR (Task 3) & Adaptive LMS (Task 4)...")
    ecg_fir = FIRfilter(prac_coeffs)

    # For Task 4: Highpass removes DC drift first, then LMS cancels 50 Hz using a 50 Hz sine reference
    hp_fir = FIRfilter(hp_coeffs)
    M_lms = 50
    learning_rate = 0.002
    lms_fir = FIRfilter(np.zeros(M_lms))  # LMS weights start at 0!

    ecg_filtered = np.zeros(len(ecg_raw))
    ecg_dc_removed = np.zeros(len(ecg_raw))
    ecg_lms = np.zeros(len(ecg_raw))

    for i, v in enumerate(ecg_raw):
        # Task 3: Fixed FIR (DC + 50Hz bandstop)
        ecg_filtered[i] = ecg_fir.dofilter(v)

        # Task 4: DC removal followed by Adaptive LMS with 50 Hz reference
        dc_clean = hp_fir.dofilter(v)
        ecg_dc_removed[i] = dc_clean
        noise_ref = np.sin(2.0 * np.pi * 50.0 / fs * i)
        ecg_lms[i] = lms_fir.doFilterAdaptive(dc_clean, noise_ref, learning_rate)

    # Group delay = (M/2)/fs = 1.0s; buffer fill = M/fs = 2.0s
    delay = (M / 2) / fs
    fill_idx = M  # index where buffer is completely filled (t = 2.0s)

    plt.figure(figsize=(12, 9))
    plt.suptitle("Task 3 (Fixed FIR) vs Task 4 (Adaptive LMS) on Saad ECG 1")

    # 1. Full Recording Overlay (after initial buffer fill)
    plt.subplot(2, 1, 1)
    plt.title("Full Recording (After 2s Highpass Buffer Fill)")
    plt.plot(t[fill_idx:] - delay, ecg_dc_removed[fill_idx:], label="Before 50Hz Removal (DC removed only)", alpha=0.45)
    plt.plot(t[fill_idx:] - delay, ecg_filtered[fill_idx:], label="Task 3: Fixed Bandstop FIR", color="tab:orange", linewidth=1.2)
    plt.plot(t[fill_idx:] - delay, ecg_lms[fill_idx:], label="Task 4: Adaptive LMS Filter", color="tab:green", linestyle="--", linewidth=1.2)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")
    plt.legend(loc="upper right")

    # 2. Single Heartbeat Overlay (5.5s - 6.5s)
    plt.subplot(2, 1, 2)
    plt.title("One Heartbeat (5.5s - 6.5s): Noisy vs Fixed FIR vs Adaptive LMS")
    plt.plot(t - delay, ecg_dc_removed, label="Before 50Hz Removal (with 50Hz hum)", alpha=0.55)
    plt.plot(t - delay, ecg_filtered, label="Task 3: Fixed Bandstop FIR", color="tab:orange", linewidth=2.0)
    plt.plot(t - delay, ecg_lms, label="Task 4: Adaptive LMS Filter", color="tab:green", linestyle="--", linewidth=1.8)
    plt.xlim(5.5, 6.5)
    plt.ylim(-0.0006, 0.0020)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (V)")
    plt.legend(loc="upper right")

    plt.tight_layout()
    plt.show()
