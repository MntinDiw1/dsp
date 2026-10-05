# ASS01 Notes

## Recording

### Attempt 1

- **Voice:** Will
- **Sentence:** 'Fractal Metasurface Absorbers with Octave-Spanning Bandwidth' (rerecord with good mic)
- **Sampling rate:** 96 kHz
- **Encoding:** Signed 24-bit PCM
- **Channels:** Mono

### Attempt 2

- **Voice:** Gabe
- **Sentence:**
- **Sampling rate:**
- **Encoding:**
- **Channels:** Mono

---

## Questions

*Remove or add answer once closed.*

1. Can we use built-in functions from libraries (e.g. `np.fft`)?
2. How to identify consonants/vowels as per the assignment doc?
3. Are our plots accurate/expected?
4. Normalise both axes?
5. How to fix arbitrary reference for dB scale (currently reaches 250 dB)?
6. Can audio files be loaded more efficiently?
7. Why does VS Code change code formatting when Ctrl+S is pressed?

## TDL

- [ ] dBFS y-axis scaling for freq. domain
- [ ] Look into audio enhancement for task 2

---

## Notes for report

**AI use:** Claude Code, Sonnet 5.5, Anthropic

- Debugging faulty code syntax and logic, and suggesting methods of increasing code efficiency
- Using dBFS scale for freq. domain magnitude

### Task 1

#### General approach

- `linspace` used to mark the point at which the audio was sampled.
- Normalised by dividing the audio by its maximum absolute value.
- Defined x-axis for frequency-domain plot with `sample_rate / n` (n = number of samples), spanning DC to the Nyquist frequency of `sample_rate / 2`. Only the positive half is plotted as the spectrum is mirrored.

#### Report deliverables

- **iii.** 'Identify fundamental frequencies, explain':
- **iv.**
- **v.**
