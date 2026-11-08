#5 - simulating real time heartbeat detection using fir_filter

import numpy as np
import matplotlib.pyplot as plt

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data, vector_plot_export

#FUNCTIONISE MORE THINGS IN THIS ASSIGNMENT????

#INCLUDE CLEARERR STAGES SEPERATED BY COMMENTS

# Load and format ECG data
t, ecg, sample_rate = import_ecg_data("ecg1.tsv")  # ECG to analyse
t_template, template_ecg, template_sample_rate = import_ecg_data("ecg2.tsv")  # other lab partner's ECG


#Apply filter from Task 3
h = fir_design(sample_rate, [[0,0.5], [45, 125]]) #these values were already set previously, seems wasteful to call them again.

#Extract PQRST from TEMPLATE
template_fir = FIRfilter(h)
template_clean = np.zeros(len(template_ecg))
for i in range(len(template_ecg)):
        template_clean[i] = template_fir.dofilter(template_ecg[i])


#Cut around the R peak (include QRS). An earlier sample would be affected by cleaning filter transient
R = 2576
template = template_clean[R-12:R+13] #25 sampples
matched_fir = FIRfilter(np.flip(template)) #reverse coefficients in time
ecg_fir = FIRfilter(h) #fresh cleaning filter for ECG

#real time loop (rename this)
matched_fir_out = np.zeros(len(ecg))

THRESHOLD = 1.5e-11 #from matched filter plot
TRANSIENTS = len(template) + len(h) #buffer fill time (cleaning + matched filter) = 1025 samples
MIN = 30
MAX = 200
LAST_BEAT = None #index of previous beat
HEART_RATE = []
BEAT_TIMES = []

for i in range(len(ecg)):
    matched_fir_out[i] = matched_fir.dofilter(ecg_fir.dofilter(ecg[i])) ** 2 #square to make positive (bigger values (peaks) become much bigger))
    if i <= TRANSIENTS:
        continue
    if matched_fir_out[i] > THRESHOLD and matched_fir_out[i-1] <= THRESHOLD:
        peak = i
        if LAST_BEAT != None:
            #Ensure heartrate is within reasonable range (30-200 bpm)
            momentary_rate = 60* sample_rate / (peak - LAST_BEAT) #bpm
            in_range =  MIN < momentary_rate < MAX #Heuristic 1

            prev_rate = HEART_RATE[-1] if HEART_RATE else momentary_rate #prevent IndexError
            consistency = 0.75*prev_rate < momentary_rate < 1.25*prev_rate #Heuristic 2
            if in_range and consistency:
                HEART_RATE.append(momentary_rate)
                BEAT_TIMES.append(peak / sample_rate)
        LAST_BEAT = peak     

print(f"Heart rates calculated: {len(HEART_RATE)}, mean heart rate: {np.mean(HEART_RATE):.1f} bpm")


# --- PLOTS ---
delay = (len(h) // 2 + len(template) // 2) / sample_rate # approx. delay added by cleaning + matched filter
beat_idx = np.round(np.array(BEAT_TIMES) * sample_rate).astype(int)
template_ms = (np.arange(len(template)) - len(template) // 2) / sample_rate * 1000 # time relative to R peak

plt.figure(figsize=(12, 8))
plt.suptitle("Matched Filter R-Peak Detection")

# Template (matched filter coefficients before time reversal)
plt.subplot(2, 1, 1)
plt.title(f"QRS Template from ECG 2 ({len(template)} samples)")
plt.plot(template_ms, template, marker=".")
plt.xlabel("Time relative to R peak (ms)")
plt.ylabel("Amplitude (V)")
plt.grid(True)

# Squared matched filter output with threshold and detected beats
plt.subplot(2, 1, 2)
plt.title("Squared Matched Filter Output: ECG 1")
plt.plot(t, matched_fir_out, label="Squared matched filter output")
plt.axhline(THRESHOLD, color="red", linestyle="--", label=f"Threshold ({THRESHOLD:.1e})")
plt.plot(t[beat_idx], matched_fir_out[beat_idx], "x", color="black", label=f"Detected beats ({len(beat_idx)})")
plt.axvspan(0, TRANSIENTS / sample_rate, color="grey", alpha=0.2, label="Buffer fill (ignored)")
plt.xlim(0, len(ecg) / sample_rate)
plt.ylim(0, 0.5e-10)
plt.xlabel(f"Time (s), output delayed by {delay:.2f} s")
plt.ylabel("Amplitude (V$^4$)")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
vector_plot_export("t5_detection")

# Momentary heart rate after heuristics
plt.figure(figsize=(12, 5))
plt.title("Momentary Heart Rate: ECG 1")
plt.plot(BEAT_TIMES, HEART_RATE, marker="o", label="Momentary heart rate")
plt.axhline(np.mean(HEART_RATE), color="red", linestyle="--", label=f"Mean ({np.mean(HEART_RATE):.1f} bpm)")
plt.xlim(0, len(ecg) / sample_rate)
plt.xlabel(f"Time (s), output delayed by {delay:.2f} s")
plt.ylabel("Heart rate (bpm)")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
vector_plot_export("t5_heartrate")

plt.show()


