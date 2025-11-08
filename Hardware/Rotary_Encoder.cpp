#include "Rotary_Encoder.h"
#include <string.h>


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



int turn(){
  int t =0;
currCLK = digitalRead(CLK);

  if(currCLK != lastCLK){//if it moved (turned)
    if(currCLK==HIGH){//only operates on the rising edge

      if(digitalRead(DT) != currCLK){
        delay(100);
        t=1;
        
      }
      else{
        delay(100);
        t=-1;
      }

    }

  }
  lastCLK = currCLK;
  return t;
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

