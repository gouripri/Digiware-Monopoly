#include "nrf.h"
#include "UI.h"

const char *go = "go";
int check = 0;

// Property name storage (received from Python via Serial)
char propertyName[32] = "GO";  // Default property name
bool propertyNameUpdated = false;

// Periodic "go" signal timing
unsigned long lastGoSignalTime = 0;
const unsigned long GO_SIGNAL_INTERVAL = 10;  // 10 milliseconds
bool sendToPlayer1 = true;  // Alternate between players
bool waitingForRoll = false;  // Track if we're waiting for a roll

void setup() {
  Serial.begin(9600);
  // Wait for Serial connection to be established
  while (!Serial) {
    ; // Wait for serial port to connect
  }
  
  // put your setup code here, to run once:
  nrf_setup_transmitter1();
  nrf_setup_reciever();
  
  // Initialize OLED display
  UI_setup();
  
  // Send initial ready message to Python
  Serial.println("Arduino Ready");
  
  // Send initial "go" signal immediately
  nrf_setup_transmitter1();
  send(go);
  Serial.println("Initial go signal sent to Player 1");
  lastGoSignalTime = millis();  // Initialize timer
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
      
      // Display property name on OLED screen
      updateScreen(propName);
      
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
  
  // Send periodic "go" signal every 10ms (only when not waiting for roll)
  if (!waitingForRoll) {
    unsigned long currentTime = millis();
    if (currentTime - lastGoSignalTime >= GO_SIGNAL_INTERVAL) {
      if (sendToPlayer1) {
        nrf_setup_transmitter1();
        send(go);
      } else {
        nrf_setup_transmitter2();
        send(go);
      }
      sendToPlayer1 = !sendToPlayer1;  // Alternate between players
      lastGoSignalTime = currentTime;
    }
  }

  // PLAYER 1 TURN
  waitingForRoll = true;
  nrf_setup_transmitter1();
  send(go);
  lastGoSignalTime = millis();  // Reset timer
  
  while(!recieve_roll()){
    // While waiting for roll, send "go" every 10ms and check for property updates
    unsigned long currentTime = millis();
    if (currentTime - lastGoSignalTime >= GO_SIGNAL_INTERVAL) {
      nrf_setup_transmitter1();
      send(go);
      lastGoSignalTime = currentTime;
    }
    readPropertyFromSerial();
    delay(1);
  }
  
  waitingForRoll = false;
  
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
  waitingForRoll = true;
  nrf_setup_transmitter2();
  send(go);
  lastGoSignalTime = millis();  // Reset timer
  
  while(!recieve_roll()){
    // While waiting for roll, send "go" every 10ms and check for property updates
    unsigned long currentTime = millis();
    if (currentTime - lastGoSignalTime >= GO_SIGNAL_INTERVAL) {
      nrf_setup_transmitter2();
      send(go);
      lastGoSignalTime = currentTime;
    }
    readPropertyFromSerial();
    delay(1);
  }
  
  waitingForRoll = false;
  
  delay(300);
  Serial.println("P2,Roll");  // Send roll event to Python
  delay(300);
  
  check++;
}