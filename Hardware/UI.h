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

void UI_setup();
void updateScreen(String text);
void Start_setup();
void Pturn_setup();
void Wait_setup();
void Final_Setup();

#endif
