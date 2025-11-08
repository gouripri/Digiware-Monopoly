#ifndef OLED_H
#define OLED_H

#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>

#include <Arduino.h>

#define width 128
#define height 32
#define addr 0x3c

void UI_setup();
void updateScreen(String text);

#endif
