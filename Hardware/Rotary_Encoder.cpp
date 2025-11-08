#include "Rotary_Encoder.h"
#include <string.h>

int option = 0;
int currCLK;
int lastCLK;
unsigned long lastButtonPress = 0;

void RotaryEncoder_setup(){
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP);

  Serial.begin(9600); //starts the serial mointor, the input is the speed of communication
  lastCLK = digitalRead(CLK); 

}






bool click(){
  int btnState = digitalRead(SW);
  bool clicked = false;
  
  if (btnState == LOW ) {
    if(millis() - lastButtonPress > 50){
      clicked = true;
    }
		lastButtonPress = millis();
	}
return clicked;
}

int scroll(){
	// Read the current state of CLK
	currCLK = digitalRead(CLK);

	if (currCLK != lastCLK  && currCLK == 1){

		if (digitalRead(DT) != currCLK) {
      if (option != 3){
			  option ++;			
      }
		} 
    else {
      if (option != 0){
			  option --;
//			  currentDir ="CW";
      }
		}
    delay(10);
  }
  lastCLK = currCLK;

  //added this cuz its being weird
  if (option < 0){
    option =0;
  }
  if (option > 3){
    option =3;
  }


  return option;
}

