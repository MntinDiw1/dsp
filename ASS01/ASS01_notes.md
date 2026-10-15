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

- Should all tasks be independant from eachother?
- compute FFT once or multiple times?
- Task 1 audio analysis: (fundamentals or DIFFERENT vowels?)
- how to remove POP?
- is it okay that we call the function for each specific band?
- what format/size to export for task2
- create function for the enhancer loop.
- TASK 3 Feedback


## TDL

- [ ] Optimise code by avoiding repeated/wasteful logic!!!!
- [ ] INTERPOLATE THE EQUALISER
- [ ] compute X = fft(audio) ONCE in run_tasks.py and pass X into both functions. (tradeoffs?)
- [ ] send enhanced wav files to dedicated audio folder?
- [ ] annotate frequency plot (task 1) with analysis for report
- [ ] LINUX COMPATIBLE SUBMISSION
- [ ] Collect evidence of iteration for task 3 (with plots/param values)

---

## Notes for report

**AI use:** Claude, Opus 5.5, Anthropic

- Debugging faulty code syntax and logic, and suggesting methods of increasing code efficiency
- Using dBFS scale for freq. domain magnitude
- Suggested optimised pipeline for task 2.
- Checking task 1 readings against my analysis for report (verification)
- Explained the exciter and how non-linearity creates harmonics.
- Suggestions for fixing hiss in task 2

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

### Report Deliverables

#### Justification of decisions for enhancer:

- Pop filter for 5cm, Low-cut for 1m

#### 5cm:

- Volume increase of __dB (WHY?)
- Bass boost of __dB between __Hz and __Hz (small because bass is already clear)
- __dB of Brightness added between __Hz and __Hz
- Noise reduction of __dB (why??)
- Pop filter @__Hz (below the fundamental)
Pop was identified to sit at 1.28-1.3s and lasts around 50ms (measured in Ableton). Most of it sits below 150Hz, however it exists throughout the spectrum and thus cannot be completely isolated/removed. (LOOK INTO WHY POP OCCURS)

#### 1m:

- Volume increase of __dB (WHY?). 
Note: increasing 1m distance volume will increase noise floor alongside ti which isnt ideal
- Bass boost of __dB between __Hz and __Hz (larger to compensate for distance cutting low end - DO FURTHER RESEARCH!)
- __dB of Brightness added between __Hz and __Hz
- Noise reduction of __dB (WHYYYY)
- Low-cut to remove ambient rumble

---

### Task 3

An exciter built on the 5cm recording, developed iteratively: an initial deisng, an examination of the result, a change, and at least two annotated graphs showing why. THE PROCESS IS GRADED - KEEP A LOG.

Feeding a pure sine into tanh will squash the peaks when the drive is high enough. This creates a square shape, introducing extra sine waves at multiples of the fundamental (harmonics). Since tan is an odd function (symmetric about 0), top and bottom are squashed equally which produces only the odd harmonics.

tanh only starts distorting once the input reaches +-1.

**Attempt 1**

- 3f = 6kHz -> f = 2kHz (5f = 10kHz (not too high))
- Bandpass filter used instead of tunable Highpass filter (see guide), reduces mud.
- width: 500Hz (wider input = wider output -> MUD)
- drive: starting value = (how to set it so that it doesnt depend on how loud the recording is?).
- mix: 

**Attempt 2**