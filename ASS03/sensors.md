# Analog Sensor Technical Mini-Doc

This reference guide details the **9 analog-output sensors** filtered from your original inventory list. Purely digital sensors ($\text{I}^2\text{C}$, 1-Wire, pulse-width), mechanical switches (reed/tilt), and actuators have been removed.

---

## 1. Load Cell (Generic)
* **Component Type:** Strain Gauge Force Transducer (Wheatstone Bridge). *(Note: Outputs a raw differential analog millivolt signal directly from the bridge, though often paired with an **HX711** 24-bit ADC breakout board for microcontroller reading).*
* **What It Measures:**
  * **Force & Weight (Mass):** Measures mechanical deformation (strain) under tension or compression and converts it into a differential millivolt signal proportional to applied weight.
  * **Bending / Torque / Mechanical Load:** Detects structural stress, load distribution, or physical pressure applied to a mounting point.
* **Datasheet & Technical Links:**
  * [SparkFun Generic Straight Bar Load Cell Datasheet (TAL220)](https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/TAL220M4M5Update.pdf)
  * [Avia Semiconductor HX711 24-Bit Load Cell ADC Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf)

---

## 2. Temp Sensor - V182 (`LM35D` Module / Automotive EGT Probe)
* **Decoded Part Info:** Commonly matches the **`V182` PCB silkscreen revision code** found on 3-pin **`LM35D` Analog Temperature Sensor Breakout Modules** ($4\text{ V}\text{–}30\text{ V}$). *(Note: In automotive contexts, `V182` also designates an NTC/PTC Exhaust Gas Temperature probe, which is also an analog resistive sensor).*
* **What It Measures:**
  * **Centigrade Temperature (Linear Analog Voltage):** The `LM35D` measures $0\,^\circ\text{C}$ to $100\,^\circ\text{C}$ (or $-55\,^\circ\text{C}$ to $+150\,^\circ\text{C}$ on full `LM35` variants) with a linear scale factor of $+10\text{ mV}/^\circ\text{C}$.
  * **Surface or Air Thermal Changes:** Directly read via any microcontroller Analog-to-Digital Converter (ADC) pin without needing cold-junction compensation.
* **Datasheet & Technical Links:**
  * [Texas Instruments LM35 / LM35D Precision Centigrade Sensor Datasheet](https://www.ti.com/lit/ds/symlink/lm35.pdf)

---

## 3. Current Sensor - W4345A (`VAC L2050-W434` / Hall-Effect Current Sensor)
* **Decoded Part Info:** Matches the **Vacuumschmelze (VAC) `T60004-L2050-W434`** ($54\text{ A}$ Closed-Loop Compensation Current Sensor) or a board batch silkscreen (`W4345A`) on an **Allegro `ACS712`** Hall-effect current sensor module.
* **What It Measures:**
  * **AC and DC Electrical Current ($I$):** Measures bidirectional current (up to $\pm 50\text{ A}$ / $54\text{ A}$ for the VAC sensor, or $\pm 5\text{ A}$, $\pm 20\text{ A}$, $\pm 30\text{ A}$ for the `ACS712`) with galvanic isolation between the high-current conductor and low-voltage logic.
  * **Current Ripple, Inrush & Fault Currents:** Tracks real-time current waveforms, motor stall currents, or short-circuit spikes via an analog voltage output proportional to magnetic flux in the core.
* **Datasheet & Technical Links:**
  * [VAC T60404 / L2050 Closed-Loop Current Sensor Datasheet](https://datasheet4u.com/datasheets/VAC/T60404-N4646-X664/1148230)
  * [Allegro ACS712 Hall-Effect Linear Current Sensor Datasheet](https://www.alldatasheet.com/datasheet-pdf/pdf/168326/ALLEGRO/ACS712.html)

---

## 4. Line Track - TCRT5000 (Breakout Board)
* **Component Type:** Vishay `TCRT5000` Reflective Optical Sensor ($950\text{ nm}$ IR LED emitter + phototransistor) on a breakout module (provides both raw analog output `A0` from the phototransistor and an `LM393` comparator digital threshold output `D0`).
* **What It Measures:**
  * **Surface Reflectivity / Contrast (Line Tracking):** Distinguishes between high-reflectivity surfaces (white paper/floor) and low-reflectivity surfaces (black electrical tape) at short range ($0.2\text{ mm}$ to $15\text{ mm}$, optimal at $2.5\text{ mm}$).
  * **Short-Range Object Presence & Distance Curve:** Detects objects passing directly in front of the sensor via continuous analog reflection intensity.
  * **Shaft Rotation / Encoder Ticks:** Counts RPM when aimed at a rotating disc with alternating black and white segments.
* **Datasheet & Technical Links:**
  * [Vishay TCRT5000 Reflective Optical Sensor Datasheet](https://www.vishay.com/docs/83760/tcrt5000.pdf)

---

## 5. Dust K16-07 (`Sharp GP2Y1010AU0F` Optical Dust Sensor)
* **Decoded Part Info:** `K16-07` is a lot/date stamp commonly printed on the metallic shield of the **Sharp `GP2Y1010AU0F`** Compact Optical Dust Sensor module.
* **What It Measures:**
  * **Airborne Particulate Matter (PM) & Dust Density:** Measures the concentration of fine suspended dust and smoke particles (up to $0.5\text{ mg/m}^3$, sensitivity $0.5\text{ V per } 0.1\text{ mg/m}^3$) by detecting infrared light ($940\text{ nm}$) scattered by particles passing through its central air hole.
  * **Smoke vs. House Dust Differentiation:** By analyzing the pulse height and fluctuation pattern of the analog voltage output, it helps distinguish cigarette/combustion smoke from larger airborne dust particles.
* **Datasheet & Technical Links:**
  * [Sharp GP2Y1010AU0F Optical Dust Sensor Datasheet](https://www.mouser.com/datasheet/2/365/gp2y1010au_e-183866.pdf)

---

## 6. Pressure - Sensirion 1230319 (`Sensirion SDP816-500Pa`)
* **Decoded Part Info:** **Sensirion `SDP816-500Pa`** (`#1230319`) — CMOSens® Differential Pressure Sensor with Ratiometric Analog Voltage Output and Dual Tube Ports.
* **What It Measures:**
  * **Differential Gas Pressure ($\Delta P$):** Measures the pressure difference between two ports from **$-500\text{ Pa}$ to $+500\text{ Pa}$** ($\pm 2\text{ inH}_2\text{O}$) for air and non-aggressive gases with zero offset drift and $0.1\text{ Pa}$ zero-point accuracy.
  * **Volumetric & Mass Airflow Rate:** When connected across a Pitot tube, Venturi, or orifice plate, the differential pressure reading directly measures gas flow velocity and mass flow (configurable for linear or square-root analog output transfer functions).
  * **Filter Clogging / Pressure Drop:** Monitors the pressure drop across HVAC, cleanroom, or medical ventilator filters.
* **Datasheet & Technical Links:**
  * [Sensirion SDP8xx Analog Series (SDP816-500Pa) Official Datasheet](https://sensirion.com/media/documents/68DF0025/6667FEEF/DP_DS_SDP8xx_analog.pdf)
  * [Sensirion SDP816-500Pa Catalog Page](https://sensirion.com/products/catalog/SDP816-500Pa)

---

## 7. Hall Effect A1302 179 1388 (`Allegro A1302KUA-T`)
* **Decoded Part Info:** **Farnell Order Code `1791388` (`179-1388`)** — Allegro MicroSystems `A1302KUA-T` Continuous-Time Ratiometric Linear Hall-Effect Sensor (3-pin SIP package).
* **What It Measures:**
  * **Magnetic Flux Density ($B$) & Polarity:** Outputs an analog voltage directly proportional to the perpendicular magnetic field strength (sensitivity of **$1.3\text{ mV/Gauss}$**). Quiescent output sits at $0.5 \times V_{\text{CC}}$; a South pole increases the voltage toward $V_{\text{CC}}$, while a North pole decreases it toward $0\text{ V}$.
  * **Non-Contact Linear/Rotary Position:** Tracks the continuous position or angle of a moving permanent magnet.
  * **Current Sensing (with external core):** When placed in the air gap of a ferrite toroid, measures current flowing through a wire passing through the core.
* **Datasheet & Technical Links:**
  * [Allegro MicroSystems A1301 / A1302 Official Datasheet](https://media.digikey.com/pdf/Data%20Sheets/Allegro%20PDFs/A1301,02.pdf)
  * [Farnell UK Listing (1791388)](https://uk.farnell.com/allegro-microsystems/a1302kua-t/sensor-hall-effect-linear-3sip/dp/1791388)

---

## 8. Microphone (Generic)
* **Component Type:** Electret Condenser Microphone (ECM) capsule typically mounted on a preamplifier breakout board (e.g., `MAX4466` for analog audio waveforms) or a comparator board (e.g., `LM393` / `KY-037` which provides both raw analog output `A0` and digital threshold `D0`).
* **What It Measures:**
  * **Acoustic Sound Pressure Waves (Audio Waveform):** Converts air pressure fluctuations ($20\text{ Hz}\text{–}20\text{ kHz}$) into an AC analog voltage signal for audio recording, FFT frequency spectrum analysis, or pitch detection.
  * **Sound Volume / Relative Decibel Level (SPL):** Measures peak-to-peak amplitude (loudness) of ambient noise.
  * **Acoustic Impulses / Threshold Events:** Detects sudden transients like claps, knocks, glass breakage, or machinery anomalies.
* **Datasheet & Technical Links:**
  * [Analog Devices MAX4466 Microphone Preamplifier Datasheet](https://cdn-shop.adafruit.com/datasheets/MAX4465-MAX4469.pdf)
  * [CUI Devices Generic Electret Condenser Microphone Capsule Datasheet (CMA-4544PF-W)](https://www.cuidevices.com/product/resource/cma-4544pf-w.pdf)

---

## 9. Accelerometer ADXL335
* **Component Type:** Analog Devices `ADXL335` 3-Axis MEMS Analog Accelerometer ($\pm 3\,g$ full-scale range, $X_{\text{OUT}}$, $Y_{\text{OUT}}$, $Z_{\text{OUT}}$ analog voltage outputs).
* **What It Measures:**
  * **Static Acceleration (Gravity / 3D Tilt & Inclination Angle):** Measures the $1\,g$ vector of Earth's gravity across $X, Y, Z$ axes, allowing calculation of exact pitch and roll angles ($\theta = \arctan\left(\frac{A_x}{\sqrt{A_y^2 + A_z^2}}\right)$).
  * **Dynamic Acceleration:** Measures linear acceleration, deceleration, shock, and impact forces up to **$\pm 3\,g$** (sensitivity $\approx 300\text{ mV}/g$ at $3\text{ V}$ supply).
  * **Vibration & Seismic Motion:** Measures mechanical vibration frequencies from $0.5\text{ Hz}$ up to $1600\text{ Hz}$ ($X, Y$ axes) and $550\text{ Hz}$ ($Z$ axis).
* **Datasheet & Technical Links:**
  * [Analog Devices ADXL335 Official Product & Datasheet Page](https://www.analog.com/en/products/adxl335.html)
  * [SparkFun / Analog Devices ADXL335 PDF Datasheet](https://www.sparkfun.com/datasheets/Components/SMD/adxl335.pdf)

---

## Quick Comparison Matrix (Analog Sensors Only)

| Listed Item | Decoded Model / Part | Analog Output Interface | Primary Measurement |
| :--- | :--- | :--- | :--- |
| **Load Cell Generic** | Strain Gauge Bridge | Differential Analog ($\text{mV/V}$) | Weight, Force, Mechanical Strain |
| **Temp Sensor - V182** | `LM35D` Module (`V182` PCB) | Linear Analog Voltage ($10\text{ mV}/^\circ\text{C}$) | Temperature ($0\,^\circ\text{C}$ to $100\,^\circ\text{C}$) |
| **current sensor - W4345A** | VAC `L2050-W434` / `ACS712` | Analog Voltage / Current | Isolated AC/DC Electrical Current |
| **Line track - TCRT5000** | Vishay `TCRT5000` Breakout | Analog Voltage (`A0`) + Digital (`D0`) | Surface Reflectivity / Contrast ($0.2\text{ mm}\text{–}15\text{ mm}$) |
| **Dust K16-07** | Sharp `GP2Y1010AU0F` | Analog Voltage ($0.5\text{ V} / 0.1\text{ mg/m}^3$) | Airborne Dust & Smoke Particle Density |
| **Pressure - Sensiron 1230319**| Sensirion `SDP816-500Pa` | Ratiometric Analog Voltage | Differential Gas Pressure ($\pm 500\text{ Pa}$) & Airflow |
| **Hall effect A1302 179 1388**| Allegro `A1302KUA-T` (Farnell `1791388`)| Ratiometric Analog Voltage ($1.3\text{ mV/G}$) | Magnetic Flux Density & Polarity |
| **Microphon Generic** | Electret Capsule + `MAX4466`/`LM393` | Analog Audio Waveform (`A0`) | Sound Pressure Level, Audio Frequency, Claps |
| **Accellerometer ADXL335** | Analog Devices `ADXL335` | 3-Channel Analog ($X_{\text{OUT}}, Y_{\text{OUT}}, Z_{\text{OUT}}$) | 3-Axis Acceleration ($\pm 3\,g$), Tilt Angle, Vibration |