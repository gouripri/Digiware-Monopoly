#ifndef NRF_H
#define NRF_H
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Arduino.h>



void nrf_setup_reciever();
void nrf_setup_transmitter();
void send();


#endif