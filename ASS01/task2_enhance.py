from email.mime import audio

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft

# ---- TASK2: AUDIO ENHANCER ----
#a) make voice sound clearer + more 'interesting' as heard on radio shows
#b) remove noise
#c) explain what kind of noise needs to be removed and which frequency range it has.
#d) explain how you would like to improve the speech by looking into the loss of base freqs. with distance, and pop sounds when mic is close.


class task2:
    #input audio should be MONO, FLOAT, and NORMALISED.

    @staticmethod
    def apply_transform(fft_data, transform_matrix):
        '''
        Applies a frequency-domain transformation to the FFT data.
        Interpolates the transform matrix gains to match the exact frequency bins of the FFT data.
        '''        
        # Extract frequencies. np.interp requires 1D arrays of real numbers
        fft_freqs = np.real(fft_data[:, 0]) #REMOVE???????
        
        transform_freqs = np.real(transform_matrix[:, 0])
        transform_gains = transform_matrix[:, 1]
        
        # Interpolate the gains to match the FFT frequency bins.
        # Frequencies outside the transform range will use the nearest end-point gain.
        interpolated_gains = np.interp(fft_freqs, transform_freqs, transform_gains)
        
        # Create output array of the exact same shape and type
        transformed_fft_data = np.zeros_like(fft_data, dtype=complex)
        
        # Copy the original frequencies over safely
        transformed_fft_data[:, 0] = fft_data[:, 0]
        
        # Apply the interpolated gains to the magnitudes via element-wise multiplication
        transformed_fft_data[:, 1] = fft_data[:, 1] * interpolated_gains
        
        return transformed_fft_data
    
    @staticmethod
    def inverse_FFT(fft_data, sample_rate, save_filename):
        '''
        Performs an inverse FFT using standard ifft by manually rebuilding 
        the conjugate-symmetric negative frequencies.
        '''
        positive_spectrum = np.real(fft_data[:, 1])
        n_half = len(positive_spectrum)
        
        # Calculate the full time-domain length.
        n_full = 2 * (n_half - 1)
        
        # Initialize the full complex spectrum array
        full_spectrum = np.zeros(n_full, dtype=complex)
        
        # Place the DC bin, positive frequencies, and Nyquist bin
        full_spectrum[:n_half] = positive_spectrum
        
        # Reconstruct the negative frequencies.
        full_spectrum[n_half:] = np.conj(positive_spectrum[1:-1][::-1])
        
        # Perform the standard inverse FFT
        time_domain_audio = ifft(full_spectrum)
        
        # Extract the real part (imaginary part will be effectively zero due to perfect symmetry)
        time_domain_real = np.real(time_domain_audio)
        
        # Normalize to [-1.0, 1.0] to prevent clipping when saving as float32
        max_amplitude = np.max(np.abs(time_domain_real))
        if max_amplitude > 0:
            time_domain_real = time_domain_real / max_amplitude
            
        # Write to file
        wavfile.write(save_filename, sample_rate, time_domain_real.astype(np.float32))

        return None


    # --- GAIN CONTROL (dB) ---
    #function that applied gain adjustments to specific frequency ranges.

    #TDL: 
    # where is gain_array coming from?
    #nest within larger Task 2 function (rember to create 2 arrays for each audio file)
    def gain_ctrl(low, high, amp_dB, sample_rate, gain_array):

        n = len(gain_array) #full spectrum

        LO_bin = (low * n) // sample_rate #Hz->bin
        HI_bin = (high * n) // sample_rate #Hz->bin

        dB__2_lin = 10 ** (amp_dB / 20)  # convert dB to linear gain

        gain_array[LO_bin:HI_bin+1] *= dB__2_lin #x = x * y #MUST APPLY TO MIRROR (SEE BERND ADVICE)
        gain_array[n-HI_bin:n-LO_bin+1] *= dB__2_lin #mirror


        return None

    #audio enhancement
    #array of n ones (floits). Each value is a multiplier for the corresponding bin
    gain_array_5cm = np.ones(len(audio_5cm))
    gain_array_1m = np.ones(len(audio_1m))
  # ^where to put this (embded into a function?)

    #NOISE REMOVAL
    # AXIS
    # SCALE

    # 5cm
    #BASS BOOST
    gain_ctrl(60, 240, 12, sample_rate_5cm, gain_array_5cm) #TUNE
    #BRIGHTNESS
    gain_ctrl(1000, 4000, 6, sample_rate_5cm, gain_array_5cm) #TUNE

    # 1m
    #BASS BOOST
    gain_ctrl(60, 240, 12, sample_rate_1m, gain_array_1m) #TUNE
    #BRIGHTNESS
    gain_ctrl(1000, 4000, 6, sample_rate_1m, gain_array_1m) #TUNE

    ##PLOT TO CHECK