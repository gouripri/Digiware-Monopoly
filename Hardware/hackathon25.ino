#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

#define width 128
#define height 32
#define addr 0x3c

#include "Rotary_Encoder.h"


//for this to make sense, view the timing diagram here: https://howtomechatronics.com/tutorials/arduino/rotary-encoder-works-use-arduino/


Adafruit_SSD1306 display(width, height);



void setup() {


  //display setup
  display.begin(SSD1306_SWITCHCAPVCC, addr);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);

  display.println("DigiWare");

  display.println("Monopoly");

  display.display();
  delay(200);

  RotaryEncoder_setup();



}

void loop() {
  int t = turn();
  if(t ==1){
    Serial.println("Clockwise ");
    delay(500);
  }
  if (t == -1){
    Serial.println("CounterClockwise");
    delay(500);
  }
  t=0;
}


void updateScreen(String text){
  display.clearDisplay();

  display.setCursor(0, 0);
  display.println(text);

  display.display();


}

