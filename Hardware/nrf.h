#ifndef NRF_H
#define NRF_H
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Arduino.h>
#include <string.h>







void nrf_setup_reciever();
void nrf_setup_transmitter();
void send(const char* command);
bool recieve_and_go();
bool isCommand(const char* input, const char* command);
String recieve_landing();



#endif
