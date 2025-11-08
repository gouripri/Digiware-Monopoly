#include "nrf.h"
RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00001"; // address must match receiver



void nrf_setup_reciever(){
  radio.begin();
  
  //for reciever
  radio.openReadingPipe(0, address);
  radio.startListening(); // this one listens
}

void nrf_setup_transmitter(){
  radio.begin();
  
  // for transmitter
  radio.openWritingPipe(address);
  radio.stopListening(); // this one sends data


}


void send() {
  const char text[] = "Hello!";
  radio.write(&text, sizeof(text));
  delay(1000); // send every second

}