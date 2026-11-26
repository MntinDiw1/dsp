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
VREF = 5 # ADC reference (V): default AREF on the Uno = its 5 V supply
PLOT_N = 2 * SAMPLE_RATE # 2s sampling window

# name the recording test1, test2, ...h
n = 1
while (BASE_DIR / "data" / f"test{n}.tsv").exists():
    n += 1
name = f"test{n}"


#KEY LOGGER
samples = [] # raw ADC values
keys = [] # [sample index, key] per key press
def key_press(press):
    key = "space" if press.key == " " else press.key # prevents error in the .tsv columns
    keys.append([len(samples), key]) # latest sample index [WTCH FOR DELAY FROM PROCESSING]

# disable matplotlib keyboard shortcuts
for k in plt.rcParams:
    if k.startswith("keymap."):
        plt.rcParams[k] = []

PORT = Arduino.AUTODETECT
board = Arduino(PORT)
board.analog[0].register_callback(samples.append) # callback: store each sample
board.samplingOn(1000 // SAMPLE_RATE) # sampling interval in ms
board.analog[0].enable_reporting()
start = time.perf_counter()
plt.figure()
plt.title("Type here, close the window to stop")
plt.gcf().canvas.mpl_connect("key_press_event", key_press)

line, = plt.plot(np.zeros(PLOT_N))
plt.ylim(0, VREF) # full ADC range, so clipping is visible
plt.ylabel("Voltage (V)")

def update(frame):
    if len(samples) >= PLOT_N:
        line.set_ydata(np.array(samples[-PLOT_N:]) * VREF)

ani = animation.FuncAnimation(plt.gcf(), update, interval=50, cache_frame_data=False) # redraw at ~20 Hz (matplotlib's limit here), outside the callback
plt.show() # blocks until the window is closed

elapsed = time.perf_counter() - start
board.exit() # also stops sampling and closes the serial port

(BASE_DIR / "data").mkdir(exist_ok=True)
# header: key list at the top of the file (np.loadtxt skips these # lines), samples below
key_list = "\n".join(f"{i}\t{i / SAMPLE_RATE:.3f}\t{key}" for i, key in keys)
header = f"fs = {SAMPLE_RATE} Hz, samples: A0 as fraction of AREF\nkeys: sample index, time (s), key\n{key_list}"
np.savetxt(BASE_DIR / "data" / f"{name}.tsv", samples, fmt="%.4f", header=header)
print(f"Saved {name}: {len(samples)} samples and {len(keys)} key presses, measured sampling rate: {len(samples) / elapsed:.0f} Hz")
