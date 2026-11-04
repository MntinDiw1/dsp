#3b - simulating RT FIR filtering importing fir_design and fir_filter.

import numpy as np

from fir_design import fir_design
from fir_filter import FIRfilter #why wont this work?

#Declare frequency ranges to remove
baseline_wander = [0, 0.5] #Remove baseline wander
mains_hum = [45, 125] #Remove 50Hz mains hum #explain why 125Hz is upper band


FIRfilter.Firfilter(fir_design(sample_rate, [baseline_wander, mains_hum]))