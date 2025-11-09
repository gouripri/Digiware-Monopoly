#ifndef ROTARY_H
#define ROTARY_H

#define CLK 2
#define DT 3
#define SW 4

#include <Arduino.h>


void RotaryEncoder_setup();
int turn();
bool click();

#endif
