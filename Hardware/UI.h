#ifndef OLED_H
#define OLED_H

#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

#include <Arduino.h>

#define width 128
#define height 32
#define addr 0x3c



const int START =0;
const int PTURN = 1;
const int WAIT = 2; 
const int FINAL = 3;
const int INSIDE_OPT = 1;
const int OUTSIDE_OPT = 0; 
const int AFTER_ROLL = 2; 

void UI_setup();
void updateScreen(String text);


#endif
