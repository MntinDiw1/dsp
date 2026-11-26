#records raw piezo data from A0 to data/testN.tsv (FOR TESTING & ANALYSIS ONLY)

'''
- matplotlib window receives the key presses.
- click on window, type, then close window to save
'''

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pyfirmata2 import Arduino
import time

BASE_DIR = Path(__file__).resolve().parent #data/ is always next to the script

SAMPLE_RATE = 1000 #Arduino maximum sampling rate (Hz)
BAUD_RATE = 115200 # must match Firmata.begin() in pizo_basic.ino
VREF = 1.5 # ADC reference (V): must match analogReference() in pizo_basic.ino (VDD=5.0, INTERNAL4V3=4.3, INTERNAL2V5=2.5, INTERNAL1V5=1.5)
DC_BIAS = 0.7 # expected hardware DC midpoint (V): ~0.71 V from 5 V -> 3 MOhm / 500 kOhm divider
PLOT_N = 2 * SAMPLE_RATE # 2s sampling window

# name the recording test1, test2, ...h
n = 1
while (BASE_DIR / "data" / f"test{n}.tsv").exists():
    n += 1
name = f"test{n}"


#KEY LOGGER
samples = [] # raw ADC values
keys = [] # [sample index, key] per key press
first_sample_t = None
last_sample_t = None

def on_sample(value):
    global first_sample_t, last_sample_t
    now = time.perf_counter()
    if first_sample_t is None:
        first_sample_t = now
    last_sample_t = now
    samples.append(value)

def key_press(press):
    key = "space" if press.key == " " else press.key # prevents error in the .tsv columns
    keys.append([len(samples), key]) # latest sample index [WTCH FOR DELAY FROM PROCESSING]

# disable matplotlib keyboard shortcuts
for k in plt.rcParams:
    if k.startswith("keymap."):
        plt.rcParams[k] = []

PORT = Arduino.AUTODETECT
board = Arduino(PORT, baudrate=BAUD_RATE)
board.analog[0].register_callback(on_sample) # callback: store each sample and track timestamps
board.samplingOn(1000 // SAMPLE_RATE) # sampling interval in ms
board.analog[0].enable_reporting()
plt.figure()
plt.title("Type here, close the window to stop")
plt.gcf().canvas.mpl_connect("key_press_event", key_press)

line, = plt.plot(np.full(PLOT_N, DC_BIAS))
plt.axhline(DC_BIAS, color="tab:green", linestyle="--", linewidth=0.8, alpha=0.7, label=f"Expected DC bias ({DC_BIAS:.2f} V)")
plt.ylim(0, VREF) # full ADC range (0 to 1.5 V), so clipping is visible
plt.ylabel("Voltage (V)")
plt.legend(loc="upper right", fontsize=8)

def update(frame):
    if len(samples) >= PLOT_N:
        line.set_ydata(np.array(samples[-PLOT_N:]) * VREF)

ani = animation.FuncAnimation(plt.gcf(), update, interval=50, cache_frame_data=False) # redraw at ~20 Hz (matplotlib's limit here), outside the callback
plt.show() # blocks until the window is closed

board.exit() # also stops sampling and closes the serial port

if len(samples) > 1 and first_sample_t is not None and last_sample_t > first_sample_t:
    measured_fs = (len(samples) - 1) / (last_sample_t - first_sample_t)
else:
    measured_fs = float(SAMPLE_RATE)

(BASE_DIR / "data").mkdir(exist_ok=True)
# header: key list at the top of the file (np.loadtxt skips these # lines), samples below
key_list = "\n".join(f"{i}\t{i / measured_fs:.3f}\t{key}" for i, key in keys)
header = f"fs = {measured_fs:.2f} Hz, VREF = {VREF} V, samples: A0 as fraction of AREF\nkeys: sample index, time (s), key\n{key_list}"
np.savetxt(BASE_DIR / "data" / f"{name}.tsv", samples, fmt="%.4f", header=header)
dc_v = float(np.mean(samples)) * VREF if samples else float("nan")
print(f"Saved {name}: {len(samples)} samples and {len(keys)} key presses, measured fs: {measured_fs:.2f} Hz, DC bias: {dc_v:.3f} V (VREF={VREF} V)")
