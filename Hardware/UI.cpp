

#include "UI.h"
Adafruit_SSD1306 display(width, height);

void UI_setup(){
  display.begin(SSD1306_SWITCHCAPVCC, addr);
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);

  display.println("DigiWare");

  display.println("Monopoly");

  display.display();
  delay(200);


}


void updateScreen(String text){
  display.clearDisplay();

  display.setCursor(0, 0);
  display.println(text);

  display.display();


}
