#5 - simulating real time heartbeat detection using fir_filter

import numpy as np
import matplotlib.pyplot as plt

from fir_design import fir_design
from fir_filter import FIRfilter
from support_funcs import import_ecg_data


# Load and format ECG data
t, ecg, sample_rate = import_ecg_data("saad_ecg_2.tsv")  # ECG to analyse
t_template, template_ecg, template_sample_rate = import_ecg_data("will_c_ecg2.tsv")  # other lab partner's ECG


#Apply filter from Task 3
h = fir_design(sample_rate, [[0,0.5], [45, 125]]) #these values were already set previously, seems wasteful to call them again.

#Extract PQRST from TEMPLATE - AI, UNDERSTAND THIS SQUILLIAM
fir = FIRfilter(h)
template_clean = np.zeros(len(template_ecg))
for i in range(len(template_ecg)):
        template_clean[i] = fir.dofilter(template_ecg[i])


