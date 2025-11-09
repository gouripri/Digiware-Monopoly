# Arduino Setup Guide

This guide will help you upload and run the Arduino code for the Monopoly game.

## Hardware Requirements

### For Hub (Central Controller):
- **Arduino Uno** (or compatible)
- **2x NRF24L01 modules** (one for TX, one for RX)
- **USB cable** to connect to computer

### For Player Devices:
- **Arduino Uno** (or compatible) - one per player
- **1x NRF24L01 module** per device
- **OLED Display** (SSD1306, 128x32) - I2C
- **Rotary Encoder** with button
- **USB cable** per device

## Step 1: Install Arduino IDE

1. Download Arduino IDE from: https://www.arduino.cc/en/software
2. Install and open Arduino IDE

## Step 2: Install Required Libraries

Open Arduino IDE and install these libraries:

### Via Library Manager (Sketch → Include Library → Manage Libraries):

1. **RF24 by TMRh20**
   - Search for "RF24"
   - Install "RF24" by TMRh20

2. **Adafruit SSD1306** (for player devices only)
   - Search for "Adafruit SSD1306"
   - Install "Adafruit SSD1306" by Adafruit

3. **Adafruit GFX Library** (for player devices only)
   - Search for "Adafruit GFX"
   - Install "Adafruit GFX Library" by Adafruit

## Step 3: Upload Hub Code (Central Controller)

The hub connects to Python and manages player communication.

1. **Open the Hub Project**
   - In Arduino IDE: File → Open
   - Navigate to: `Uno_CODE/hub.ino`
   - Arduino IDE will automatically open all related files (`nrf.cpp`, `nrf.h`)

2. **Select Board and Port**
   - Tools → Board → **Arduino Uno** (or your board)
   - Tools → Port → Select your Arduino port
     - Mac: `/dev/tty.usbmodem...` or `/dev/tty.usbserial...`
     - Windows: `COM3`, `COM4`, etc.
     - Linux: `/dev/ttyUSB0` or `/dev/ttyACM0`

3. **Upload Code**
   - Click Upload button (→) or press `Ctrl+U` (Windows/Linux) / `Cmd+U` (Mac)
   - Wait for "Done uploading" message

4. **Verify Upload**
   - Open Serial Monitor: Tools → Serial Monitor
   - Set baud rate to **9600**
   - You should see: `Arduino Ready`

## Step 4: Upload Player Device Code

Each player needs their own Arduino device.

1. **Open the Player Device Project**
   - In Arduino IDE: File → Open
   - Navigate to: `Hardware/hackathon25.ino`
   - Arduino IDE will automatically open related files

2. **Configure Player Number** (Important!)
   - In `hackathon25.ino`, line 216, change:
     ```cpp
     updateScreen("Player 1");  // CHANGE THIS FOR EACH REMOTE
     ```
   - For Player 2 device, change to: `updateScreen("Player 2");`
   - For Player 3, etc.

3. **Select Board and Port**
   - Tools → Board → **Arduino Uno** (or your board)
   - Tools → Port → Select the Arduino port for THIS device
   - **Note**: Disconnect other Arduinos or use different ports

4. **Upload Code**
   - Click Upload button
   - Wait for "Done uploading"

5. **Repeat for Each Player**
   - Disconnect current device
   - Connect next player's Arduino
   - Change player number in code
   - Upload again

## Step 5: Hardware Connections

### Hub Arduino Connections:

**NRF24L01 Module 1 (Transmitter):**
- VCC → 3.3V
- GND → GND
- CE → Pin 9
- CSN → Pin 10
- SCK → Pin 13
- MOSI → Pin 11
- MISO → Pin 12

**NRF24L01 Module 2 (Receiver):**
- VCC → 3.3V
- GND → GND
- CE → Pin 7
- CSN → Pin 8
- SCK → Pin 13
- MOSI → Pin 11
- MISO → Pin 12

### Player Device Connections:

**NRF24L01 Module:**
- VCC → 3.3V
- GND → GND
- CE → Pin 9
- CSN → Pin 10
- SCK → Pin 13
- MOSI → Pin 11
- MISO → Pin 12

**OLED Display (SSD1306):**
- VCC → 5V (or 3.3V)
- GND → GND
- SDA → Pin A4 (SDA)
- SCL → Pin A5 (SCL)

**Rotary Encoder:**
- CLK → Pin 2
- DT → Pin 3
- SW (Button) → Pin 4
- VCC → 5V
- GND → GND

## Step 6: Run the Complete System

1. **Connect Hub Arduino** to computer via USB
2. **Power Player Devices** (via USB or external power)
3. **Run Python Game:**
   ```bash
   python main.py
   ```
   Or specify port manually:
   ```bash
   python main.py --port /dev/tty.usbmodem14101  # Mac/Linux
   python main.py --port COM3  # Windows
   ```

## Troubleshooting

### "Could not find Arduino port"
- Make sure Arduino is connected via USB
- Check Arduino IDE: Tools → Port (should show your Arduino)
- Try different USB cable
- On Mac: May need USB drivers

### "Compilation error: RF24.h: No such file or directory"
- Install RF24 library (see Step 2)
- Restart Arduino IDE after installing libraries

### "Compilation error: Adafruit_SSD1306.h: No such file or directory"
- Install Adafruit SSD1306 and GFX libraries (see Step 2)
- Only needed for player devices, not hub

### Serial Monitor shows nothing
- Check baud rate is set to 9600
- Make sure correct port is selected
- Try unplugging and replugging USB cable
- Close Serial Monitor before running Python (only one program can use Serial)

### NRF24L01 not working
- Check all connections (especially power: 3.3V, not 5V!)
- Verify CE and CSN pins match code
- Make sure addresses match between hub and players
- NRF modules need stable power - use capacitors if needed (10µF + 100nF)

### OLED not displaying
- Check I2C address (default is 0x3C)
- Verify SDA/SCL connections
- Some OLEDs need 5V, others 3.3V - check your module

## Testing Individual Components

### Test Hub Arduino:
1. Upload `hub.ino`
2. Open Serial Monitor (9600 baud)
3. Should see: `Arduino Ready`
4. Connect Python game to test communication

### Test Player Device:
1. Upload `hackathon25.ino`
2. OLED should show "Player X" on startup
3. Rotary encoder should navigate menus
4. Button should select options

## Next Steps

Once Arduino code is uploaded and working:
1. Run Python game: `python main.py`
2. Game will auto-detect Arduino or you can specify port
3. Players can interact via their devices
4. Hub manages communication between Python and players

For more details, see `SETUP_GUIDE.md`

