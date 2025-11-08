#include "Rotary_Encoder.h"
#include "UI.h"
#include "nrf.h"
//for this to make sense, view the timing diagram here: https://howtomechatronics.com/tutorials/arduino/rotary-encoder-works-use-arduino/

int options = 0; 
int mode = START; 
bool change = false; 
void setup() {


  //display setup
  UI_setup();

  RotaryEncoder_setup();

  nrf_setup_transmitter();
  //nrf_setup_reciever();

}

void loop() {
int adder = scroll();
if (adder !=0 ){
  if ( (adder == -1 && options > 0) || (adder == 1 && mode == PTURN && options < 2) ||(adder == 1 && mode != PTURN && options < 1) ){
    change = true;
    options += adder;
  }

    if (change == true){

      if(mode == START) {
        if (options == 0){
          updateScreen("Properties");
        }
        if (options == 1){
          updateScreen("Balance");
        }

      }


      else if (mode == PTURN){
        if (options == 0){
          updateScreen ("Pro")
        }
        if (options == 1){}
        if (options == 2){}

      }
      else if(mode == WAIT){
        updateScreen("");

      }
      else if(mode == FINAL)
      if (options == 0){
        updateScreen("Buy");
      }
      if (options == 1){
        updateScreen("End Turn");
      }

    }
  }

   change = false;
}




