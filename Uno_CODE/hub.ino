#include "nrf.h"

const char *go = "go";
int check = 0;

// Property name storage (received from Python via Serial)
char propertyName[32] = "GO";  // Default property name
bool propertyNameUpdated = false;

void setup() {
  Serial.begin(9600);
  // Wait for Serial connection to be established
  while (!Serial) {
    ; // Wait for serial port to connect
  }
  
  // put your setup code here, to run once:
  nrf_setup_transmitter1();
  nrf_setup_reciever();
  
  // Send initial ready message to Python
  Serial.println("Arduino Ready");
}

// Function to read messages from Serial (from Python)
void readPropertyFromSerial() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();
    
    // Check if message is in format "Property: <name>"
    if (message.startsWith("Property: ")) {
      String propName = message.substring(10);  // Extract property name after "Property: "
      propName.trim();
      
      // Copy to propertyName buffer (max 31 chars + null terminator)
      propName.toCharArray(propertyName, sizeof(propertyName));
      propertyNameUpdated = true;
      
      // Echo back to Serial for confirmation
      Serial.print("Received property: ");
      Serial.println(propertyName);
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly
  
  // Always check for property updates from Python
  readPropertyFromSerial();

  // PLAYER 1 TURN
  nrf_setup_transmitter1();
  send(go);
  
  while(!recieve_roll()){
    // While waiting for roll, also check for property updates
    readPropertyFromSerial();
    delay (1);
  }
  
  delay(300);
  Serial.println("P1,Roll");  // Send roll event to Python
  delay(300);

  // Send property name via NRF to player device (if updated)
  if (propertyNameUpdated) {
    send(propertyName);
    Serial.print("Sent property via NRF: ");
    Serial.println(propertyName);
    propertyNameUpdated = false;  // Reset flag
    delay(500);
  }

  // PLAYER 2 TURN
  nrf_setup_transmitter2();
  send(go);
  
  while(!recieve_roll()){
    // While waiting for roll, also check for property updates
    readPropertyFromSerial();
    delay(1);
  }
  
  delay(300);
  Serial.println("P2,Roll");  // Send roll event to Python
  delay(300);
  
  check++;
}
