#5 - simulating real time heartbeat detection using fir_filter

import numpy as np
import matplotlib.pyplot as plt

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data

#FUNCTIONISE MORE THINGS IN THIS ASSIGNMENT????

#INCLUDE CLEARERR STAGES SEPERATED BY COMMENTS

# Load and format ECG data
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")  # ECG to analyse
t_template, template_ecg, template_sample_rate = import_ecg_data("will_c_ecg2.tsv")  # other lab partner's ECG


#Apply filter from Task 3
h = fir_design(sample_rate, [[0,0.5], [45, 125]]) #these values were already set previously, seems wasteful to call them again.

#Extract PQRST from TEMPLATE - AI, UNDERSTAND THIS SQUILLIAM
template_fir = FIRfilter(h)
template_clean = np.zeros(len(template_ecg))
for i in range(len(template_ecg)):
        template_clean[i] = template_fir.dofilter(template_ecg[i])


#Cut around the R peak (include QRS). An earlier sample would be affected by cleaning filter transient
R = 2576
template = template_clean[R-12:R+13]
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
        momentary_rate = (60* sample_rate / peak - LAST_BEAT)
        in_range =  MIN < momentary_rate < MAX
        hysteresis = abs(momentary_rate - HEART_RATE[-1]) < 0.25 * HEART_RATE[-1] #is that the right thing to call it?



print("", len*(heart_rates), np.mean(heart_rates))


# --- ANALYSIS PLOTS ---

#Plot filtered template ecg against sample_number to locate R peak (REMOVE)
plt.plot(template_clean)
plt.xlim(2500, 2800)
plt.xlabel("sample")
plt.show()

#Plot template to check QRS range is covered
plt.plot(template)
plt.xlabel("sample")
plt.ylabel("amplitude")
plt.show()
#plot matched_filter
plt.plot(matched_fir_out)
plt.xlabel("sample")
plt.ylabel("amplitude")
plt.xlim(1000, len(ecg))
plt.ylim(0, 0.5e-10)
plt.show()



