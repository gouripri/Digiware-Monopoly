#include "Rotary_Encoder.h"
#include <string.h>


int currCLK;
int lastCLK;
unsigned long lastButtonPress = 0;

void RotaryEncoder_setup(){
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP);


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
  currCLK = digitalRead(CLK);
  bool c = false;
 lastCLK = currCLK;

  if(digitalRead(SW)==LOW){
    //Serial.println("Clicked");
    delay(300); //so it doesn't register multiple clicks if you accidently hold the button down
    //Note: this unit is in milliseconds
    c = true;
  }
  return c;
}
