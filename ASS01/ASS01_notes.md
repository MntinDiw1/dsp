
## Recording

### Attempt 1

Voice: Will
Sentence: 'Fractal Metasurface Absorbers with Octave-Spanning' Bandwidth (rerecord with good mic)
Sampling Rate 96kHz
Encoding: Signed 24-bit PCM
Recorded in Mono
---

### ATTEMPT 2

Voice: Gabe
Sentence: 
Sampling Rate:
Encoding:
Recorded in Mono
---

## TDL

- Record 2x Audio Files (5cm & 1cm) with good microphone

1. i. Plot audio in the time domain (linear/normalised)
   ii. Plot audio in the frequency domain (logarithmic)

2.    

## Questions (remove or add answer once closed)

1. Can we use built-in functions from libraries (e.g. np.fft)?
2. How to identify consonants/vowels as per the assignment doc?
3. Are our plots accurate/expected?
4. Normalise both axis?
5. How to fix arbitrary reference for dB scale (currently says 250dB)
6. can audio files be loaded more efficiently?


## Notes for report

Note: AI was used in this assignment:
Claude Code, Sonnet 5.5, Anthropic -> debugging faulty code syntax AND logic + suggesting methods of increasing code efficiency.

**Task 1**
- linspace used to mark the point at which the audio was sampled.
- normalised by dividing the audio by its maximum absolute value.
- defined x-axis for frequency-domain plot with sample_rate / number of samples (n). spanning DC noise to Nyquist Frequency of sample_rate / 2 (thus only the +ve half is plotted as spectrum is mirrored)
- 