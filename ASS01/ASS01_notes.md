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
- **Sampling rate:** 48kHz
- **Encoding:** 24bits
- **Channels:** Mono

---

## Questions

*Remove or add answer once closed.*


## TDL

- [ ] Implement global x_axis_Hz function for all tasks (use FOLD DOWN (DFT stuff))
- [ ] Optimise code by avoiding repeated/wasteful logic!!!!
- [ ] implement 1/n to FFT - calculate average

## FIXING SAADS CODE:

- REMOVE ALL UNNECESSARY BULLSHIT... Goal is simply and readable code.
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
- **v.** The region that probably just contains noise is (the frequencies outside 20Hz-20kHz and frequencies that cannot be reached by male human voice (RESEARCH))

---

### Task 2

#### General approach

- dB to linear amplitude = 10^(dB/20)
- Normalised according to full scale (24bits in 32bit{float?} (31bit division since its half the range)). - '#a_norm = audio / np.max(np.abs(audio))  # normalise to +-1' was incorrect

