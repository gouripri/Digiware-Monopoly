#include "nrf.h"


const char *go = "go";
int check =0;


char* propertyName = "tophat";


void setup() {
 Serial.begin(9600);
 // put your setup code here, to run once:
 nrf_setup_transmitter1();
 nrf_setup_reciever();


}


void loop() {
 // put your main code here, to run repeatedly




// PLAYER 1 TURN
 nrf_setup_transmitter1();
 send(go);
 while(!recieve_roll()){
   delay (1);
 }
 delay(300);
 Serial.println("P1,Roll");                   //KEEP THOIS
 delay(300);




delay(5000);
send(propertyName);
 Serial.print("Sent property: ");
 Serial.println(propertyName);
 delay(500);




//PLAYER 2 TURN
 nrf_setup_transmitter2();
 send(go);
 while(!recieve_roll()){
   delay(1);
 }
 check ++;








}



