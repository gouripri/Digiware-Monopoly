


#include "Rotary_Encoder.h"
#include "UI.h"
#include "nrf.h"
//for this to make sense, view the timing diagram here: https://howtomechatronics.com/tutorials/arduino/rotary-encoder-works-use-arduino/



void setup() {


  //display setup
  UI_setup();

  RotaryEncoder_setup();

  nrf_setup_transmitter();
  //nrf_setup_reciever();

}

void loop() {

}




