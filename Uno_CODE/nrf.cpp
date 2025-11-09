#include "nrf.h"
RF24 radiot(9, 10);  // CE, CSN
RF24 radior(7, 8);   // CE, CSN




const byte address1[6] = "00002";  // address must match receiver
const byte address2[6] = "00001";
const char *roll = "ROLL";


void nrf_setup_reciever() {
 radior.begin();


 //for reciever
 radior.openReadingPipe(0, address2);
 radior.openReadingPipe(1, address1);
 radior.startListening();  // this one listens
}


void nrf_setup_transmitter1() {
 radiot.begin();


 // for transmitter
 radiot.openWritingPipe(address1);
 radiot.stopListening();  // this one sends data
}
void nrf_setup_transmitter2() {
 radiot.begin();


 // for transmitter
 radiot.openWritingPipe(address2);
 radiot.stopListening();  // this one sends data
}




void send(const char* text) {


 radiot.write(text, strlen(text) + 1);
 //Serial.println("sent");
 delay(100);  // send every second
}


bool recieve_roll() {


 if (radior.available()) {
   char text[32] = "";
   radior.read(&text, sizeof(text));
   if (isCommand(text, roll)){
     return true;
   }
 return false;
}
return false;
}




bool isCommand(const char* input, const char* command) {
 int command_len = strlen(command);
  // 1. Check if the input is long enough to contain the command
 if (strlen(input) < command_len) {
   return false;
 }
  // 2. Use strncmp to compare exactly the length of the command
 // It returns 0 if they match.
 return (strncmp(input, command, command_len) == 0);
}

