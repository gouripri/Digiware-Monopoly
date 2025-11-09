#ifndef NRF_H
#define NRF_H
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Arduino.h>
#include <string.h>










void nrf_setup_reciever();
void nrf_setup_transmitter1();
void nrf_setup_transmitter2();
void send(const char* command);
bool recieve_roll();
bool isCommand(const char* input, const char* command);
void send_property(const char* property);


#endif

