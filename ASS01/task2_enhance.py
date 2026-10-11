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
        fft_freqs = np.real(fft_data[:, 0])
        
        transform_freqs = transform_matrix[:, 0]
        transform_gains = transform_matrix[:, 1]
        
        # Interpolate the gains to match the FFT frequency bins.
        # Frequencies outside the transform range will use the nearest end-point gain.
        interpolated_gains = np.interp(fft_freqs, transform_freqs, transform_gains)
        
        # Create output array of the exact same shape and type
        transformed_fft_data = np.zeros_like(fft_data, dtype=complex)
        
        # Copy the original frequencies over safely
        transformed_fft_data[:, 0] = fft_data[:, 0]
        
        # Apply the interpolated gains to the magnitudes via element-wise multiplication
        transformed_fft_data[:, 1] = fft_data[:, 1] + interpolated_gains
        
        return transformed_fft_data
    
    @staticmethod
    def inverse_FFT(fft_data, sample_rate, save_filename):
        '''
        Performs an inverse FFT using standard ifft and saves the resulting time-domain audio to a WAV file.
        '''
        # Extract the halved spectrum (positive frequencies including DC at index 0)
        half_spectrum = fft_data[:, 1]

        # Reconstruct negative frequencies: 
        # Take the complex conjugate of the bins (excluding the DC bin at index 0) and reverse the order
        negative_freqs = np.conj(half_spectrum[1:][::-1])
        
        # Concatenate the positive and negative frequencies to restore the original size
        full_spectrum = np.concatenate((half_spectrum, negative_freqs))
        
        # Undo the 20 * log10
        linear_spectrum = 10 ** (full_spectrum / 20)
        
        # 2. Reverse the manual (1/n) scaling
        n = len(linear_spectrum)
        linear_spectrum = linear_spectrum * n

        # Perform the inverse FFT on the restored linear spectrum
        time_domain_audio = np.real(ifft(linear_spectrum))
        
        # Normalize to [-1.0, 1.0] to prevent clipping when saving as float32
        max_amplitude = np.max(np.abs(time_domain_audio))
        if max_amplitude > 0:
            time_domain_audio = time_domain_audio / max_amplitude
        
        # Write to file
        wavfile.write(save_filename, sample_rate, time_domain_audio.astype(np.float32))

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
    