# Sensor & Component Technical Mini-Doc

This reference guide details the 19 sensors and actuators from your inventory list. Several items in the list were identified using UK/European distributor stock codes (**The Pi Hut**, **Farnell / Element14**, and **RS Components**) or PCB silkscreen batch markings; these have been cross-referenced and decoded to their exact manufacturer part numbers below.

---

## 1. Load Cell (Generic)
* **Component Type:** Strain Gauge Force Transducer (Wheatstone Bridge) typically paired with an **HX711** 24-bit ADC breakout board.
* **What It Measures:**
  * **Force & Weight (Mass):** Measures mechanical deformation (strain) under tension or compression and converts it into a differential millivolt signal proportional to applied weight.
  * **Bending / Torque / Mechanical Load:** Detects structural stress, load distribution, or physical pressure applied to a mounting point.
* **Datasheet & Technical Links:**
  * [SparkFun Generic Straight Bar Load Cell Datasheet (TAL220)](https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/TAL220M4M5Update.pdf)
  * [Avia Semiconductor HX711 24-Bit Load Cell ADC Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf)

---

## 2. Temp Sensor - 102835 (`DS18B20` Waterproof Probe)
* **Decoded Part Info:** **The Pi Hut SKU `102835`** — Waterproof DS18B20-Compatible 1-Wire Digital Temperature Sensor ($1\text{ m}$ cable).
* **What It Measures:**
  * **Ambient, Liquid, or Soil Temperature:** Measures temperature from $-55\,^\circ\text{C}$ to $+125\,^\circ\text{C}$ with $\pm 0.5\,^\circ\text{C}$ accuracy (between $-10\,^\circ\text{C}$ and $+85\,^\circ\text{C}$).
  * **Multi-Point Thermal Gradients:** Because each sensor has a unique 64-bit serial code on a 1-Wire digital bus, multiple probes can share a single microcontroller pin to measure temperature across different zones simultaneously.
* **Datasheet & Technical Links:**
  * [Analog Devices / Maxim Integrated DS18B20 Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf)
  * [The Pi Hut Product Page (SKU 102835)](https://thepihut.com/products/waterproof-ds18b20-digital-temperature-sensor-extras)

---

## 3. Ultrasonic - 100284 (`HC-SR04`)
* **Decoded Part Info:** **The Pi Hut SKU `100284`** — HC-SR04 Ultrasonic Distance Range Sensor.
* **What It Measures:**
  * **Non-Contact Distance / Range:** Measures distance to solid or liquid surfaces between $2\text{ cm}$ and $400\text{ cm}$ using $40\text{ kHz}$ acoustic sonar pulses within a $15^\circ\text{–}30^\circ$ cone.
  * **Acoustic Time-of-Flight ($\Delta t$):** Outputs a high-level pulse whose duration equals the round-trip travel time of the ultrasonic wave ($d = \frac{v_{\text{sound}} \cdot \Delta t}{2}$).
  * **Liquid Level & Obstacle Presence:** Used in tanks for fluid depth measurement or on mobile robotics for collision detection.
* **Datasheet & Technical Links:**
  * [SparkFun HC-SR04 Ultrasonic Sensor Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
  * [The Pi Hut Product Page (SKU 100284)](https://thepihut.com/products/ultrasonic-distance-sensor-hcsr04)

---

## 4. IR Receiver - 225-1442 (`Vishay TSSP4P38`)
* **Decoded Part Info:** **Farnell Order Code `2251442` (`225-1442`)** — Vishay `TSSP4P38` $38\text{ kHz}$ Infrared Mid-Range Proximity & Light Barrier Receiver ($940\text{ nm}$ peak sensitivity).
* **What It Measures:**
  * **Reflective Proximity Distance (up to $2\text{ m}$):** Unlike standard fixed-gain TV remote receivers, the `TSSP4P38` outputs a pulse width proportional to the *amount of $38\text{ kHz}$ modulated IR light reflected* off a target object.
  * **Light Barrier / Beam Break Detection (up to $45\text{ m}$):** Detects when an object interrupts a modulated IR beam across a doorway, conveyor, or perimeter.
  * **Target Reflectivity:** Estimates relative surface reflectance at $940\text{ nm}$ when distance is fixed.
* **Datasheet & Technical Links:**
  * [Vishay TSSP4P38 Official Datasheet](https://www.vishay.com/docs/82474/tssp4p38.pdf)
  * [Farnell UK Listing (2251442)](https://uk.farnell.com/vishay/tssp4p38/ir-receiver-45m-0-12mw-m2-side/dp/2251442)

---

## 5. Temp Sensor - V182 (`LM35D` Module / Automotive EGT Probe)
* **Decoded Part Info:** Commonly matches the **`V182` PCB silkscreen revision code** found on 3-pin **`LM35D` Analog Temperature Sensor Breakout Modules** ($4\text{ V}\text{–}30\text{ V}$). *(Note: In automotive contexts, `V182` also designates an NTC/PTC Exhaust Gas Temperature probe).*
* **What It Measures:**
  * **Centigrade Temperature (Linear Analog Voltage):** The `LM35D` measures $0\,^\circ\text{C}$ to $100\,^\circ\text{C}$ (or $-55\,^\circ\text{C}$ to $+150\,^\circ\text{C}$ on full `LM35` variants) with a linear scale factor of $+10\text{ mV}/^\circ\text{C}$.
  * **Surface or Air Thermal Changes:** Directly read via any microcontroller Analog-to-Digital Converter (ADC) pin without needing cold-junction compensation.
* **Datasheet & Technical Links:**
  * [Texas Instruments LM35 / LM35D Precision Centigrade Sensor Datasheet](https://www.ti.com/lit/ds/symlink/lm35.pdf)

---

## 6. Current Sensor - W4345A (`VAC L2050-W434` / Hall-Effect Current Sensor)
* **Decoded Part Info:** Matches the **Vacuumschmelze (VAC) `T60004-L2050-W434`** ($54\text{ A}$ Closed-Loop Compensation Current Sensor) or a board batch silkscreen (`W4345A`) on an **Allegro `ACS712`** Hall-effect current sensor module.
* **What It Measures:**
  * **AC and DC Electrical Current ($I$):** Measures bidirectional current (up to $\pm 50\text{ A}$ / $54\text{ A}$ for the VAC sensor, or $\pm 5\text{ A}$, $\pm 20\text{ A}$, $\pm 30\text{ A}$ for the `ACS712`) with galvanic isolation between the high-current conductor and low-voltage logic.
  * **Current Ripple, Inrush & Fault Currents:** Tracks real-time current waveforms, motor stall currents, or short-circuit spikes via an analog voltage output proportional to magnetic flux in the core.
* **Datasheet & Technical Links:**
  * [VAC T60404 / L2050 Closed-Loop Current Sensor Datasheet](https://datasheet4u.com/datasheets/VAC/T60404-N4646-X664/1148230)
  * [Allegro ACS712 Hall-Effect Linear Current Sensor Datasheet](https://www.alldatasheet.com/datasheet-pdf/pdf/168326/ALLEGRO/ACS712.html)

---

## 7. ToF Distance - VL53L4CD
* **Component Type:** STMicroelectronics `VL53L4CD` Time-of-Flight (ToF) High-Accuracy Proximity & Ranging Sensor ($\text{I}^2\text{C}$ interface, $940\text{ nm}$ Class 1 VCSEL laser).
* **What It Measures:**
  * **High-Precision Short-to-Mid Range Distance:** Measures absolute distance from **$1\text{ mm}$ up to $1300\text{ mm}$ ($1.3\text{ m}$)** independent of target color, surface finish, or reflectivity.
  * **Ultra-Close Proximity ($< 10\text{ mm}$):** Specifically optimized for very short distances down to $1\text{ mm}$ with minimal linearity error.
  * **Ambient IR Photon Rate & Return Signal Rate:** Reports signal strength (kcps) and ambient infrared noise levels to evaluate measurement confidence.
* **Datasheet & Technical Links:**
  * [STMicroelectronics VL53L4CD Official Datasheet](https://www.st.com/resource/en/datasheet/vl53l4cd.pdf)

---

## 8. Line Track - TCRT5000 (Breakout Board)
* **Component Type:** Vishay `TCRT5000` Reflective Optical Sensor ($950\text{ nm}$ IR LED emitter + phototransistor) on a breakout module (often includes an `LM393` comparator for digital thresholding).
* **What It Measures:**
  * **Surface Reflectivity / Contrast (Line Tracking):** Distinguishes between high-reflectivity surfaces (white paper/floor) and low-reflectivity surfaces (black electrical tape) at short range ($0.2\text{ mm}$ to $15\text{ mm}$, optimal at $2.5\text{ mm}$).
  * **Short-Range Object Presence:** Detects objects passing directly in front of the sensor via analog reflection intensity or a triggered digital HIGH/LOW threshold.
  * **Shaft Rotation / Encoder Ticks:** Counts RPM when aimed at a rotating disc with alternating black and white segments.
* **Datasheet & Technical Links:**
  * [Vishay TCRT5000 Reflective Optical Sensor Datasheet](https://www.vishay.com/docs/83760/tcrt5000.pdf)

---

## 9. Adafruit TMP117 QT
* **Component Type:** Texas Instruments `TMP117` High-Accuracy Digital Temperature Sensor on an Adafruit STEMMA QT / Qwiic $\text{I}^2\text{C}$ Breakout Board (Adafruit Product ID `4821`).
* **What It Measures:**
  * **NIST-Traceable Precision Temperature:** Measures from $-55\,^\circ\text{C}$ to $+150\,^\circ\text{C}$ with a 16-bit resolution of **$0.0078125\,^\circ\text{C}$** and an accuracy of **$\pm 0.1\,^\circ\text{C}$** (from $-20\,^\circ\text{C}$ to $+50\,^\circ\text{C}$), meeting ASTM E1112 and ISO 80601 medical thermometer standards.
  * **Programmable Thermal Alert Thresholds:** Tracks high/low temperature limits and triggers hardware alert interrupts (Therm mode or Alert mode).
* **Datasheet & Technical Links:**
  * [Texas Instruments TMP117 Official Datasheet](https://www.ti.com/lit/gpn/TMP117)
  * [Adafruit TMP117 Breakout Guide & Documentation PDF](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-tmp117-high-accuracy-i2c-temperature-monitor.pdf)

---

## 10. ToF Distance - VL53L1X
* **Component Type:** STMicroelectronics `VL53L1X` Long-Distance Time-of-Flight Laser-Ranging Sensor ($\text{I}^2\text{C}$ interface, $940\text{ nm}$ VCSEL).
* **What It Measures:**
  * **Long-Range Absolute Distance:** Measures distance from **$40\text{ mm}$ up to $4000\text{ mm}$ ($4\text{ m}$)** at up to $50\text{ Hz}$ ranging frequency, independent of target reflectance.
  * **Programmable Region of Interest (ROI):** Uses a $16 \times 16$ SPAD (Single Photon Avalanche Diode) receiving array that allows software reduction of the field of view (FoV) from $27^\circ$ down to $15^\circ$ or basic multi-zone directional gesture/entry detection.
* **Datasheet & Technical Links:**
  * [STMicroelectronics VL53L1X Official Datasheet](https://www.st.com/resource/en/datasheet/vl53l1x.pdf)

---

## 11. 184-5122 (`Seeed Studio 316040001` Mini Vibration Motor)
* **Decoded Part Info:** **RS Components Stock No. `184-5122`** — Seeed Studio `316040001` ($1020$ Coin/Pancake Mini Vibration DC Motor, $3\text{ V DC}$, $10000\text{ RPM}$).
* **What It Measures / Does:**
  * **Note — Actuator (Output Device):** This item is primarily an **eccentric rotating mass (ERM) haptic actuator** rather than a sensor; when powered at $2.5\text{ V}\text{–}3.8\text{ V}$, it generates physical vibration ($10000\text{ RPM}$) for haptic feedback and silent alerts.
  * **Back-EMF Vibration Pick-up (Passive Mode):** If mechanically shaken while unpowered, a permanent-magnet DC vibration motor generates a small back-EMF voltage across its leads, though dedicated accelerometers (`ADXL335`) are far better suited for measuring vibration.
* **Datasheet & Technical Links:**
  * [RS Components Product Page (184-5122)](https://uk.rs-online.com/web/p/power-motor-robotics-development-tools/1845122)
  * [Seeed Studio 316040001 Product & 1020 Motor Datasheet Page](https://www.seeedstudio.com/Mini-vibration-motor-2-0mm-p-2300.html)

---

## 12. Prox PSA240/30 (`Comus / Assemtech PSA240/30`)
* **Decoded Part Info:** **Comus / Assemtech `PSA240/30`** (Farnell `607-186`) — Rectangular Flange-Mount Magnetic Reed Proximity Switch (SPST-NO, $240\text{ V AC}$, $10\text{ VA}$).
* **What It Measures:**
  * **Magnetic Proximity / Door & Window Interlock State:** Detects the presence of a permanent magnet (such as mating magnet `PSM`) within an **$8\text{ mm}$ sensing gap**, closing a dry reed switch contact.
  * **End-of-Travel Position & Cycle Counting:** Senses when a moving carriage, safety guard, lid, or float reaches a home or limit position.
* **Datasheet & Technical Links:**
  * [Comus International PSA240/30 Official Product & Datasheet Page](https://www.digikey.co.uk/en/products/detail/comus-international/PSA-240-30-BLUE/11562460)
  * [Farnell UK Listing & Technical Datasheet (607186)](https://uk.farnell.com/comus-assemtech/psa240-30/sensor-reed-400vac-8mm/dp/607186)

---

## 13. Dust K16-07 (`Sharp GP2Y1010AU0F` Optical Dust Sensor)
* **Decoded Part Info:** `K16-07` is a lot/date stamp commonly printed on the metallic shield of the **Sharp `GP2Y1010AU0F`** Compact Optical Dust Sensor module.
* **What It Measures:**
  * **Airborne Particulate Matter (PM) & Dust Density:** Measures the concentration of fine suspended dust and smoke particles (up to $0.5\text{ mg/m}^3$, sensitivity $0.5\text{ V per } 0.1\text{ mg/m}^3$) by detecting infrared light ($940\text{ nm}$) scattered by particles passing through its central air hole.
  * **Smoke vs. House Dust Differentiation:** By analyzing the pulse height and fluctuation pattern of the analog voltage output, it helps distinguish cigarette/combustion smoke from larger airborne dust particles.
* **Datasheet & Technical Links:**
  * [Sharp GP2Y1010AU0F Optical Dust Sensor Datasheet](https://www.mouser.com/datasheet/2/365/gp2y1010au_e-183866.pdf)

---

## 14. Pressure - Sensirion 1230319 (`Sensirion SDP816-500Pa`)
* **Decoded Part Info:** **Sensirion `SDP816-500Pa`** (`#1230319`) — CMOSens® Differential Pressure Sensor with Analog Output and Dual Tube Ports.
* **What It Measures:**
  * **Differential Gas Pressure ($\Delta P$):** Measures the pressure difference between two ports from **$-500\text{ Pa}$ to $+500\text{ Pa}$** ($\pm 2\text{ inH}_2\text{O}$) for air and non-aggressive gases with zero offset drift and $0.1\text{ Pa}$ zero-point accuracy.
  * **Volumetric & Mass Airflow Rate:** When connected across a Pitot tube, Venturi, or orifice plate, the differential pressure reading directly measures gas flow velocity and mass flow (configurable for linear or square-root output transfer functions).
  * **Filter Clogging / Pressure Drop:** Monitors the pressure drop across HVAC, cleanroom, or medical ventilator filters.
* **Datasheet & Technical Links:**
  * [Sensirion SDP8xx Analog Series (SDP816-500Pa) Official Datasheet](https://sensirion.com/media/documents/68DF0025/6667FEEF/DP_DS_SDP8xx_analog.pdf)
  * [Sensirion SDP816-500Pa Catalog Page](https://sensirion.com/products/catalog/SDP816-500Pa)

---

## 15. Hall Effect A1302 179 1388 (`Allegro A1302KUA-T`)
* **Decoded Part Info:** **Farnell Order Code `1791388` (`179-1388`)** — Allegro MicroSystems `A1302KUA-T` Continuous-Time Ratiometric Linear Hall-Effect Sensor (3-pin SIP package).
* **What It Measures:**
  * **Magnetic Flux Density ($B$) & Polarity:** Outputs an analog voltage directly proportional to the perpendicular magnetic field strength (sensitivity of **$1.3\text{ mV/Gauss}$**). Quiescent output sits at $0.5 \times V_{\text{CC}}$; a South pole increases the voltage toward $V_{\text{CC}}$, while a North pole decreases it toward $0\text{ V}$.
  * **Non-Contact Linear/Rotary Position:** Tracks the continuous position or angle of a moving permanent magnet.
  * **Current Sensing (with external core):** When placed in the air gap of a ferrite toroid, measures current flowing through a wire passing through the core.
* **Datasheet & Technical Links:**
  * [Allegro MicroSystems A1301 / A1302 Official Datasheet](https://media.digikey.com/pdf/Data%20Sheets/Allegro%20PDFs/A1301,02.pdf)
  * [Farnell UK Listing (1791388)](https://uk.farnell.com/allegro-microsystems/a1302kua-t/sensor-hall-effect-linear-3sip/dp/1791388)

---

## 16. INA260 Power Sensor
* **Component Type:** Texas Instruments `INA260` Precision Digital Current, Voltage, and Power Monitor with Integrated $2\text{ m}\Omega$ Shunt Resistor ($\text{I}^2\text{C}$ interface, commonly on an Adafruit breakout board).
* **What It Measures:**
  * **High-Side or Low-Side DC Current ($I$):** Measures continuous bidirectional current up to **$\pm 15\text{ A}$** with $1.25\text{ mA}$ resolution (16-bit ADC).
  * **Bus Voltage ($V$):** Measures power supply / load bus voltages up to **$36\text{ V}$** with $1.25\text{ mV}$ resolution.
  * **Electrical Power ($P$):** An internal hardware multiplier automatically calculates real-time power consumption in Watts ($P = I \times V$) with $10\text{ mW}$ resolution.
  * **Energy Accumulation ($\text{Wh}$ / $\text{mAh}$):** When sampled over time by a microcontroller, measures battery state-of-charge and total energy consumed.
* **Datasheet & Technical Links:**
  * [Texas Instruments INA260 Official Datasheet](https://www.ti.com/lit/gpn/ina260)
  * [Adafruit INA260 Breakout Guide & Documentation PDF](https://cdn-learn.adafruit.com/downloads/pdf/adafruit-ina260-current-voltage-power-sensor-breakout.pdf)

---

## 17. Microphone (Generic)
* **Component Type:** Electret Condenser Microphone (ECM) capsule typically mounted on a preamplifier breakout board (e.g., `MAX4466` for analog audio waveforms) or a comparator board (e.g., `LM393` / `KY-037` for sound threshold detection).
* **What It Measures:**
  * **Acoustic Sound Pressure Waves (Audio Waveform):** Converts air pressure fluctuations ($20\text{ Hz}\text{–}20\text{ kHz}$) into an AC analog voltage signal for audio recording, FFT frequency spectrum analysis, or pitch detection.
  * **Sound Volume / Relative Decibel Level (SPL):** Measures peak-to-peak amplitude (loudness) of ambient noise.
  * **Acoustic Impulses / Threshold Events:** Detects sudden transients like claps, knocks, glass breakage, or machinery anomalies.
* **Datasheet & Technical Links:**
  * [Analog Devices MAX4466 Microphone Preamplifier Datasheet](https://cdn-shop.adafruit.com/datasheets/MAX4465-MAX4469.pdf)
  * [CUI Devices Generic Electret Condenser Microphone Capsule Datasheet (CMA-4544PF-W)](https://www.cuidevices.com/product/resource/cma-4544pf-w.pdf)

---

## 18. Micro Tilt 1573413 (`Comus / Assemtech Micro Tilt Switch`)
* **Decoded Part Info:** Distributor catalog code `1573413` (`157-3413`) — Micro-Miniature Non-Mercury Ball Tilt Switch (such as the **Comus / Assemtech `CW1300-1`** or **`MS1` / `TM1000Q`** hermetically sealed micro-tilt series).
* **What It Measures:**
  * **Binary Tilt / Angular Orientation Threshold:** Acts as a passive mechanical switch that opens or closes an electrical circuit when tilted past a specific threshold angle (typically $15^\circ$ to $45^\circ$ from horizontal).
  * **Tip-Over & Tamper Detection:** Senses if equipment, portable heaters, or packages have been tipped over or inverted.
  * **Motion / Shake Wake-Up:** Triggers a ultra-low-power hardware interrupt when a device is picked up or jostled (consumes zero standby power when open).
* **Datasheet & Technical Links:**
  * [Comus / Assemtech CW1300 Series Micro Tilt Switch Datasheet](https://www.farnell.com/datasheets/1825428.pdf)

---

## 19. Accelerometer ADXL335
* **Component Type:** Analog Devices `ADXL335` 3-Axis MEMS Analog Accelerometer ($\pm 3\,g$ full-scale range, $X_{\text{OUT}}$, $Y_{\text{OUT}}$, $Z_{\text{OUT}}$ analog voltage outputs).
* **What It Measures:**
  * **Static Acceleration (Gravity / 3D Tilt & Inclination Angle):** Measures the $1\,g$ vector of Earth's gravity across $X, Y, Z$ axes, allowing calculation of exact pitch and roll angles ($\theta = \arctan\left(\frac{A_x}{\sqrt{A_y^2 + A_z^2}}\right)$).
  * **Dynamic Acceleration:** Measures linear acceleration, deceleration, shock, and impact forces up to **$\pm 3\,g$** (sensitivity $\approx 300\text{ mV}/g$ at $3\text{ V}$ supply).
  * **Vibration & Seismic Motion:** Measures mechanical vibration frequencies from $0.5\text{ Hz}$ up to $1600\text{ Hz}$ ($X, Y$ axes) and $550\text{ Hz}$ ($Z$ axis).
* **Datasheet & Technical Links:**
  * [Analog Devices ADXL335 Official Product & Datasheet Page](https://www.analog.com/en/products/adxl335.html)
  * [SparkFun / Analog Devices ADXL335 PDF Datasheet](https://www.sparkfun.com/datasheets/Components/SMD/adxl335.pdf)

---

## Quick Comparison Matrix

| Listed Item | Decoded Model / Part | Output Interface | Primary Measurement |
| :--- | :--- | :--- | :--- |
| **Load Cell Generic** | Strain Gauge + `HX711` | Differential Analog / 2-Wire Serial | Weight, Force, Mechanical Strain |
| **Temp sensor - 102835** | `DS18B20` (Pi Hut `102835`) | Digital (1-Wire) | Temperature ($-55\,^\circ\text{C}$ to $+125\,^\circ\text{C}$) |
| **Ultrasonic - 100284** | `HC-SR04` (Pi Hut `100284`) | Digital Pulse Width (Trig/Echo) | Ultrasonic Distance ($2\text{ cm}\text{–}400\text{ cm}$) |
| **IR reciver - 225-1442** | Vishay `TSSP4P38` (Farnell `2251442`) | Digital Pulse Width ($38\text{ kHz}$ IR) | IR Reflective Proximity ($2\text{ m}$) & Beam Break ($45\text{ m}$) |
| **Temp Sensor - V182** | `LM35D` Module (`V182` PCB) | Analog Voltage ($10\text{ mV}/^\circ\text{C}$) | Temperature ($0\,^\circ\text{C}$ to $100\,^\circ\text{C}$) |
| **current sensor - W4345A** | VAC `L2050-W434` / `ACS712` | Analog Voltage | Isolated AC/DC Electrical Current |
| **ToF distance - VL53L4CD** | ST `VL53L4CD` | Digital ($\text{I}^2\text{C}$) | High-Precision Laser Distance ($1\text{ mm}\text{–}1.3\text{ m}$) |
| **Line track - TCRT5000** | Vishay `TCRT5000` Breakout | Analog & Digital (Comparator) | Surface Reflectivity / Contrast ($0.2\text{ mm}\text{–}15\text{ mm}$) |
| **Adafruit TMP117 QT** | TI `TMP117` (Adafruit `4821`) | Digital ($\text{I}^2\text{C}$) | High-Accuracy Temperature ($\pm 0.1\,^\circ\text{C}$) |
| **ToF distance - VL53L1X** | ST `VL53L1X` | Digital ($\text{I}^2\text{C}$) | Long-Range Laser Distance ($40\text{ mm}\text{–}4\text{ m}$) |
| **184-5122** | Seeed `316040001` (RS `184-5122`) | $3\text{ V DC}$ Power Input | *Actuator:* Haptic Vibration ($10000\text{ RPM}$) |
| **Prox PSA240/30** | Comus `PSA240/30` | Dry Contact (Reed Switch) | Magnetic Proximity ($8\text{ mm}$ gap) |
| **Dust K16-07** | Sharp `GP2Y1010AU0F` | Analog Voltage (Pulsed LED) | Airborne Dust & Smoke Particle Density |
| **Pressure - Sensiron 1230319**| Sensirion `SDP816-500Pa` | Analog Voltage | Differential Gas Pressure ($\pm 500\text{ Pa}$) & Airflow |
| **Hall effect A1302 179 1388**| Allegro `A1302KUA-T` (Farnell `1791388`)| Ratiometric Analog Voltage | Magnetic Flux Density ($1.3\text{ mV/G}$) & Polarity |
| **INa260 Power sensor** | TI `INA260` | Digital ($\text{I}^2\text{C}$) | DC Current ($\pm 15\text{ A}$), Voltage ($36\text{ V}$), Power ($W$) |
| **Microphon Generic** | Electret Capsule + `MAX4466`/`LM393` | Analog Audio / Digital Threshold | Sound Pressure Level, Audio Frequency, Claps |
| **micro tilt 1573413** | Comus `CW1300` / `MS1` Micro Tilt | Dry Contact (Mechanical Switch) | Tilt Angle Threshold & Shake Detection |
| **Accellerometer ADXL335** | Analog Devices `ADXL335` | 3-Channel Analog ($X, Y, Z$) | 3-Axis Acceleration ($\pm 3\,g$), Tilt Angle, Vibration |