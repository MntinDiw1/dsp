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
- np.real discards the tiny imaginary part left by rounding errors (the gain array is mirrored, so the IFFT output is real in theory) (ADD TO REPORT !)
- Ran identity tests to check input matches output when no other changes are applied (clean pipeline)
- Ringing (Gibbs phenomenon): interpolation required
- export as int32: same 32-bit integer PCM container as the input (24-bit audio in 32-bit ints). Scaled back up by 2^31-1 so +-1.0 maps to full scale; outputs peak at 0.12 (5cm) and 0.15 (1m), so nothing clips.
- Cannot avoid reverb at 1m and thus there will always be an audible difference


### Report Deliverables

#### Justification of decisions for enhancer:

- Pop filter for 5cm, Low-cut for 1m
- Hard edges caused audible ringing (Gibbs phenomenon), which is why interpolation was required (specifics, Saad can cover). Final q-factor choices: q=0.1 for broad bands, q=0.25 for the 480-505Hz notch and the 2.2-2.8kHz cut, q=0.3 for the 1m low cut + bass boost (they meet at 85-95Hz and rang at ~95Hz with q=0.1). The 1m volume match stays at q=0 so it is flat across the whole spectrum.

#### 5cm:

- No volume change: 5cm is the reference level that the 1m recording is matched to.
- Low cut / pop filter of -16dB below 80Hz (below the ~96Hz fundamental). Removes rumble and some pop energy.
Pop was identified to sit at 1.28-1.3s and lasts around 50ms (measured in Ableton). Most of it sits below 150Hz, however it exists throughout the spectrum and thus cannot be completely isolated/removed, WE TRIED. Cutting up to 150Hz would also remove the fundamental, so the cut stops at 80Hz.
- Bass boost of +4dB between 95Hz and 400Hz: the fundamental and first few harmonics, for depth. Small because bass is already strong at 5cm (proximity effect, see 1m).
- +6dB of Brightness added between 3kHz and 10kHz: the consonant region from task 1 (hump peaking at 4-8kHz), for clarity.
- Noise reduction (high cut) of -12dB above 12.2kHz to remove hiss. Kept moderate because 5cm consonant energy extends higher than at 1m (task 1), so a deeper cut would dull it.

#### 1m:

- Volume increase of +21dB to match the 5cm recording: the measured RMS difference between the raw recordings is 21.0dB (peaks differ by 22.0dB). The inverse square law predicts 26dB (20log10(100cm/5cm)); the measured drop is smaller because room reflections add energy at 1m.
- Low cut of -12dB below 85Hz to remove ambient/room rumble (less 'boxy'). Net +9dB once the volume match is included.
- Bass boost of +6dB between 95Hz and 180Hz, around the ~104Hz fundamental of this take (slightly higher than 5cm's ~96Hz). Larger than 5cm because the 1m recording has no proximity effect: a directional mic boosts bass when the source is very close, so the 5cm take is bass-heavy and the 1m take sounds thin by comparison. (CHECK: mic is directional/cardioid)
- Notch of -12dB between 480Hz and 505Hz to remove a ~483Hz whine, clearly visible in the noise floor after the voice ends. Not mains hum: there is no 50Hz component and 483Hz is not a multiple of 50Hz.
- Cut of -4dB between 2.2kHz and 2.8kHz: the 1m recording has a ~6dB bump around 2.5kHz compared to 5cm (likely room reflections), so it is reduced to match.
- +7dB of Brightness added between 3kHz and 10kHz. The raw 1m recording is 3-5dB duller at 8-10kHz relative to its overall level (likely because the direct sound is weaker at 1m and the room's reflected sound carries less high-frequency energy), and its consonants are lost to the noise floor sooner (task 1).
- Noise reduction (high cut) of -30dB above 13kHz (net -9dB once the volume match is included). Consonants end lower at 1m, so above 13kHz there is only noise, which the +21dB volume match would otherwise lift.
- Noise audible once vocal ends, due to the volume increase creating low SNR (+21dB VOLUME MATCH LIFTS THE NOISE FLOOR). A fixed gain curve cannot separate noise from voice in the same frequency band.

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

