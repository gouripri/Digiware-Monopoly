#include "nrf.h"
#include <RF24.h>
#include <Arduino.h>
#include <string.h>

RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00002"; // must match hub RX address
const char* ROLL = "ROLL";

// Initialize once
void nrf_setup_reciever(){
    radio.begin();
    radio.openReadingPipe(0, address);
    radio.startListening();
}

void nrf_setup_transmitter(){
    // Use same radio, just prepare TX
    radio.openWritingPipe(address); // send to hub
    radio.stopListening();
}

// Switch to TX/RX without calling begin()
void nrf_set_tx() { radio.stopListening(); }
void nrf_set_rx() { radio.startListening(); }

void send(const char* text) {
    Serial.println("SENT!");
    radio.write(text, strlen(text) + 1);
    delay(100);
}

bool recieve_and_go() {
    const char* GO_CO = "go";
    if (radio.available()) {
        char text[32] = "";
        radio.read(&text, sizeof(text));
        Serial.println(text);
        return isCommand(text, GO_CO);
    }
    return false;
}

bool isCommand(const char* input, const char* command) {
    int command_len = strlen(command);
    if (strlen(input) < command_len) return false;
    return (strncmp(input, command, command_len) == 0);
}

String recieve_landing() {
    if (radio.available()) {
        char text[32] = "";
        radio.read(&text, sizeof(text));
        if (strcmp(text, "go") != 0 && strcmp(text, "ROLL") != 0) {
            Serial.println("gottem");
            return String(text);
        }
    }
    return "none";
}
