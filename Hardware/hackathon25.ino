#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

#define width 128
#define height 32
#define addr 0x3c

#include "Rotary_Encoder.h"
#include "UI.h"

//for this to make sense, view the timing diagram here: https://howtomechatronics.com/tutorials/arduino/rotary-encoder-works-use-arduino/






void setup() {


  //display setup
  UI_setup();

  RotaryEncoder_setup();



}

void loop() {

}




