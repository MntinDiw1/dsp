#3b - simulating RT FIR filtering importing fir_design and fir_filter.

import numpy as np

from fir_design import fir_design
import FIRfilter #why wont this work?

#Declare frequency ranges to remove [MOVE TO FIR_REALTIME_SIM???]
baseline_wander = [0, 0.5]
mains_hum = [45, 125] #explain why 125Hz is upper band


FIRfilter.Firfilter(fir_design) #?