#include <Firmata.h>

const unsigned int MIN_SAMPLING_INTERVAL = 1; // 1 ms = 1000 Hz max
unsigned long samplingIntervalUs = 19000UL;   // Default interval (us)
unsigned long previousMicros = 0;
uint16_t analogInputsToReport = 0;            // Bitmask of enabled analog pins

void reportAnalogCallback(byte analogPin, int value) {
  if (analogPin < TOTAL_ANALOG_PINS) {
    if (value == 0) {
      analogInputsToReport &= ~(1U << analogPin);
    } else {
      analogInputsToReport |= (1U << analogPin);
    }
  }
}

void sysexCallback(byte command, byte argc, byte *argv) {
  if (command == SAMPLING_INTERVAL && argc > 1) {
    unsigned int interval = argv[0] + (argv[1] << 7);
    if (interval < MIN_SAMPLING_INTERVAL) {
      interval = MIN_SAMPLING_INTERVAL;
    }
    samplingIntervalUs = (unsigned long)interval * 1000UL;
    previousMicros = micros();
  }
}

void systemResetCallback() {
  analogInputsToReport = 0;
  samplingIntervalUs = 19000UL;
  previousMicros = micros();
}

void setup() {
  // Nano Every (ATmega4809): INTERNAL2V5 = 2.5 V internal reference (2x resolution
  // vs VDD; matches a 1.25 V DC midpoint). Keep VREF = 2.5 in record.py.
  analogReference(INTERNAL1V5);
  analogRead(A0); // discard first conversion after switching reference
  Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION,
                             FIRMATA_FIRMWARE_MINOR_VERSION);
  Firmata.attach(REPORT_ANALOG, reportAnalogCallback);
  Firmata.attach(START_SYSEX, sysexCallback);
  Firmata.attach(SYSTEM_RESET, systemResetCallback);
  Firmata.begin(115200);
  previousMicros = micros();
}

void loop() {
  while (Firmata.available()) {
    Firmata.processInput();
  }

  unsigned long currentMicros = micros();
  if (currentMicros - previousMicros >= samplingIntervalUs) {
    previousMicros += samplingIntervalUs;
    if (currentMicros - previousMicros >= samplingIntervalUs) {
      previousMicros = currentMicros; // resync if fallen behind
    }
    for (byte pin = 0; pin < TOTAL_ANALOG_PINS; pin++) {
      if (analogInputsToReport & (1U << pin)) {
        Firmata.sendAnalog(pin, analogRead(pin));
      }
    }
  }
}