
#include <Arduino.h>
#define MARK_EXCESS_MICROS    20 // recommended for the cheap VS1838 modules
#define INFO // To see valuable informations from universal decoder for pulse width or pulse distance protocols

#include <IRremote.hpp>


#define IR_RECEIVE_PIN 2

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(3, OUTPUT);
    digitalWrite(3, HIGH);
    Serial.begin(115200);   // Status message will be sent to PC at 9600 baud
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); // Start the receiver, enable feedback LED, take LED feedback pin from the internal boards definition

    //Serial.print(F("Ready to receive IR signals of protocols: "));
    //printActiveIRProtocols(&Serial);
    //Serial.print(F("at pin "));
    //Serial.println(IR_RECEIVE_PIN);
}

//+=============================================================================
// The repeating section of the code
//
void loop() {
    if (IrReceiver.decode()) { // Grab an IR code
        // Check if the buffer overflowed
        if (IrReceiver.decodedIRData.flags & IRDATA_FLAGS_WAS_OVERFLOW) {
            Serial.println(F("Overflow detected"));
        } else {
            if (IrReceiver.decodedIRData.protocol == RC5 && IrReceiver.decodedIRData.address == 0x19) {
                if (IrReceiver.decodedIRData.command == 0xF || IrReceiver.decodedIRData.command == 0xE) {
                    Serial.println("power");
                    digitalWrite(4, HIGH);
                    delay(10);
                    digitalWrite(4, LOW);
                    delay(1000);
                }
            }
            else if (IrReceiver.decodedIRData.protocol == RC5 && IrReceiver.decodedIRData.address == 0x10) {
                if (IrReceiver.decodedIRData.command == 0x10) {
                    Serial.println("volume: up");
                } else if (IrReceiver.decodedIRData.command == 0x11) {
                    Serial.println("volume: down");
                }
            }
            else {
                IrReceiver.printIRResultShort(&Serial);
            }
        }
        IrReceiver.resume(); // Prepare for the next value
    }
}
