#include <Firmata.h>

const unsigned int MIN_SAMPLING_INTERVAL = 1; // 1 ms = 1000 Hz max
unsigned int samplingInterval = 19;           // Default interval (ms)
unsigned long previousMillis = 0;
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
    samplingInterval = (interval < MIN_SAMPLING_INTERVAL)
                           ? MIN_SAMPLING_INTERVAL
                           : interval;
  }
}

void systemResetCallback() {
  analogInputsToReport = 0;
  samplingInterval = 19;
}

void setup() {
  Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION,
                             FIRMATA_FIRMWARE_MINOR_VERSION);
  Firmata.attach(REPORT_ANALOG, reportAnalogCallback);
  Firmata.attach(START_SYSEX, sysexCallback);
  Firmata.attach(SYSTEM_RESET, systemResetCallback);
  Firmata.begin(57600);
}

void loop() {
  while (Firmata.available()) {
    Firmata.processInput();
  }

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= samplingInterval) {
    previousMillis = currentMillis;
    for (byte pin = 0; pin < TOTAL_ANALOG_PINS; pin++) {
      if (analogInputsToReport & (1U << pin)) {
        Firmata.sendAnalog(pin, analogRead(pin));
      }
    }
  }
}