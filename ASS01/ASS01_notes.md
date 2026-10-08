# ASS01 Notes

## Recording

### Attempt 1

- **Voice:** Will
- **Sentence:** 'Fractal Metasurface Absorbers with Octave-Spanning Bandwidth' (rerecord with good mic)
- **Sampling rate:** 96 kHz
- **Encoding:** Signed 24-bit PCM
- **Channels:** Mono

### Attempt 2

- **Voice:** Will
- **Sentence:** 'Saad and Will are electrowizards'
- **Sampling rate:**
- **Encoding:**
- **Channels:** 

---

## Questions

*Remove or add answer once closed.*

1. How to identify consonants/vowels as per the assignment doc? (internet/Bernd)
2. Are our plots accurate/expected? (Bernd)
3. Normalise both axes? (Bernd)
4. is dBFS scaling correct (Bernd)
5. Can audio files be loaded more efficiently?
6. Full-scale or Peak??
7. Am i normalising in the correct places (v important)?

## TDL

- [X] dBFS y-axis scaling for freq. domain
- [ ] Look into audio enhancement for task 2
- [ ] Implement global x_axis_Hz function for all tasks (use FOLD DOWN (DFT stuff))
- [ ] Optimise code by avoiding repeated logic!!!!

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
- dB to linear amplitude = 10^(dB/20)

#### Report deliverables

- **iii.** 'Identify fundamental frequencies, explain':
- **iv.**
- **v.** The region that probably just contains noise is (the frequencies outside 20Hz-20kHz and frequencies that cannot be reached by male human voice (RESEARCH))
