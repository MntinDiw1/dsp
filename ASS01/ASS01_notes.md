# ASS01 Notes

## Recording

- **Voice:** Will
- **Sentence:** 'Saad and Will are electrowizards'
- **Sampling rate:** 48kHz
- **Encoding:** 24bits
- **Channels:** Mono

---

## Questions

*Remove or add answer once closed.*


## TDL

- [ ] Optimise code by avoiding repeated/wasteful logic!!!!
- [ ] INTERPOLATE THE EQUALISER
- [ ] compute X = fft(audio) ONCE in run_tasks.py and pass X into both functions. (tradeoffs?)
- [ ] send enhanced wav files to dedicated audio folder?
- [ ] annotate frequency plot (task 1) with analysis for report
- [ ] LINUX COMPATIBLE SUBMISSION
- [ ] Collect evidence of iteration for task 3 (with plots/param values)
- [ ] Clean up comments once report is written
- [ ] Delete any test functions (what to do with gain curve plot ??)
- 

---

## Notes for report

**AI use:** Claude, Opus 5.5, Anthropic

- Debugging faulty code syntax and logic, and suggesting methods of increasing code efficiency
- Using dBFS scale for freq. domain magnitude
- Suggested optimised pipeline for task 2.
- Checking task 1 readings against my analysis for report (verification)
- Explained the exciter and how non-linearity creates harmonics.
- Fixed gain curve increasing at both ends of spectrum
- Plotting overlay of both enhanced audio recordingds
- Plotting Harmonics for task 3

- remember to cd into ASS01

### Task 1

#### General approach

- `linspace` used to mark the point at which the audio was sampled.
- Normalised by dividing the audio 2**31 full scale.
- Defined x-axis for frequency-domain plot with `sample_rate / n` (n = number of samples), spanning DC to the Nyquist frequency of `sample_rate / 2`. Only the positive half is plotted as the spectrum is mirrored.

#### Report deliverables

- **iii.** **Visually identify vowel fundamental frequencies and mark these on a frequency spectrum:**
In both recordings, the vowel energy appears as a series of peaks starting at 95-110Hz (the fundamental). Peaks above the fundamental fall roughly at 100Hz increments between eachother. This spacing is expected for a harmonic series of an adult male speaking (include evidence). The slight variation between takes is due to minor changes in pitch between takes.

- **iv.** **Mark the consonant frequency ranges on a frequency spectrum.**
Above ~2kHz the harmonic series fades, and a broad hump appears with a peak around 4-8kHz. This appears to be consonant energy and appears as noise. It extends to further frequencies in the 5cm recording because the quieter distant recording loses its consonant energy to the noise floor sooner.

- **v.** **Mark the noise frequency ranges on a frequency spectrum.**
Above 16kHz both spectra flatten to about -150dB. Since this level doesnt change with distance, it doesn't come from the voice an it can thus be concluded that it is electronic noise.

---

### Task 2

#### General approach

- dB to linear amplitude = 10^(dB/20)
- Normalised according to full scale (24bits in 32bit int, left shifted by 8 bits (31bit division since its half the range)). - '#a_norm = audio / np.max(np.abs(audio))  # normalise to +-1' was incorrect
- np.real discards the imaginary axis (ADD TO REPORT !)
- Ran identity tests to check input matches output when no other changes are applied (clean pipeline)
- Ringing (Gibbs phenomenon): interpolation required
- export int32 type instead of float32 (why?)
- Cannot avoid reverb at 1m and thus there will always be an audible difference


### Report Deliverables

#### Justification of decisions for enhancer:

- Pop filter for 5cm, Low-cut for 1m

#### 5cm:

- Volume increase of __dB (WHY?)
- Low cut
- Bass boost of __dB between __Hz and __Hz (small because bass is already clear)
- __dB of Brightness added between __Hz and __Hz
- Noise reduction of __dB (why??)
- Pop filter @__Hz (below the fundamental)
Pop was identified to sit at 1.28-1.3s and lasts around 50ms (measured in Ableton). Most of it sits below 150Hz, however it exists throughout the spectrum and thus cannot be completely isolated/removed, WE TRIED.

#### 1m:

- Volume increase of __dB (WHY?). 
- Bass boost of __dB between __Hz and __Hz (larger to compensate for distance cutting low end - DO FURTHER RESEARCH!)
- __dB of Brightness added between __Hz and __Hz
- Noise reduction of __dB (WHYYYY)
- Low-cut to remove ambient rumble
- Noise audible once vocal ends, due to volume increase creating low SNR (+21dB VOLUME MATCH LIFTS THE NOISE L=FLOOR)

MATCH BOTH VOLUMES!!!

q-factor choices: q=0.1 for broad bands,q = 0 for notch, q = 0.1+ for 180-240Hz band (not fully finalised yet)

Hard edges caused audible ringing (Gibbs phenomenon), which is why interpolation was required (specifics, Saad can cover).



---

### Task 3

An exciter built on the 5cm recording, developed iteratively: an initial deisng, an examination of the result, a change, and at least two annotated graphs showing why. THE PROCESS IS GRADED - KEEP A LOG.

Feeding a pure sine into tanh will squash the peaks when the drive is high enough. This creates a square shape, introducing extra sine waves at multiples of the fundamental (harmonics). Since tan is an odd function (symmetric about 0), top and bottom are squashed equally which produces only the odd harmonics.

tanh only starts distorting once the input reaches +-1.

Harmonics plotted to visualise changes

**Attempt 1**

- 3f = 6kHz -> f = 2kHz (5f = 10kHz (not too high))
- Bandpass filter (1750-2250) used instead of tunable Highpass filter (see guide), reduces mud.
- width: 500Hz (wider input = wider output -> MUD)
- isolated 5-7kHz (surrounding 6kHz as baseline)
- drive: starting value = 10
- mix: 0.5

RESULT: robotic/high-frequency metallic sound (why do we think?)
tanh works as only odd harmonics visible (6 kHz (3rd), 10 kHz (5th), 14 kHz (7th))

**Attempt 2**

bring down the mix so the harmonics are quieter. increase the size of the sidechain band so increase that its not just a single tone.
might need to increase q value of bandpass to avoid Gibbs phenomenon.

For now, changes:
Drive: 3 (feed less into tanh to lower distortion)
Mix:0.1 (harmonics quieter)

Result: Green added harmonic peaks around -90dB at 6kHz. I hear clear boost in harmonics in desired region, k's and clicky sounds are more present. However I want this effect to cover a wider range of frequencies.

**Attempt 3**

Wanted to widen the range at which the harmonics were present, so I pushed the sidechain band up, and opened up the region where the harmonics would be present (4k-12kHz). This caused a lot of ringing, more so than attempt 1. (see function call for parameter values).

**Attempt 4**

To create a more subtle change, i started the keep band later (5.5kHz - keeps 3rd harmonic), and stop at 12kHz. Moving mix down to 0.15 would keep the output peak around the same level as the dry signal and thus not be overly harsh. 

**Attempt 5+**
Drive was increased iteratively from here up to drive=6. At this point I could hear the harmonics more clearly, however, it created a 'lisp' effect wherethe consonants were too prominent. This was fixed by reducing drive back down to 4, making the 'keep window" smaller (up to 10kHz), and playing with mix until a balance is struck.

The mix was increased and decreased until a 'sweetspot'  was found at mix=0.25. The k's and s's are more pronounced and the voice seems 'closer'. however it still sounds relatively the same.

