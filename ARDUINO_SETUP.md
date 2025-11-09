# Arduino Setup Guide

## Quick Start Steps

### 1. Install Arduino IDE
- Download from: https://www.arduino.cc/en/software
- Install and open Arduino IDE

### 2. Install Required Library
The code uses the **RF24** library for NRF24L01 communication:

1. In Arduino IDE, go to: **Sketch → Include Library → Manage Libraries**
2. Search for: `RF24`
3. Install: **"RF24" by TMRh20** (version 1.4.5 or newer)

### 3. Hardware Connections
Connect NRF24L01 modules to Arduino Uno:

**For Transmitter (radiot):**
- CE → Pin 9
- CSN → Pin 10
- MOSI → Pin 11
- MISO → Pin 12
- SCK → Pin 13
- VCC → 3.3V (NOT 5V!)
- GND → GND

**For Receiver (radior):**
- CE → Pin 7
- CSN → Pin 8
- MOSI → Pin 11 (shared)
- MISO → Pin 12 (shared)
- SCK → Pin 13 (shared)
- VCC → 3.3V (NOT 5V!)
- GND → GND

⚠️ **Important:** NRF24L01 modules require 3.3V power. Using 5V will damage them!

### 4. Upload Code to Arduino

1. **Connect Arduino Uno** to your computer via USB cable

2. **Open the sketch:**
   - File → Open → Navigate to `Uno_CODE/hub.ino`

3. **Select Board:**
   - Tools → Board → **Arduino Uno**

4. **Select Port:**
   - Tools → Port → Select your Arduino port
   - **Mac:** Usually `/dev/tty.usbmodem...` or `/dev/tty.usbserial...`
   - **Windows:** Usually `COM3`, `COM4`, etc.
   - **Linux:** Usually `/dev/ttyUSB0` or `/dev/ttyACM0`

5. **Upload:**
   - Click the Upload button (→) or press `Ctrl+U` (Windows/Linux) / `Cmd+U` (Mac)
   - Wait for "Done uploading" message

### 5. Verify Upload

1. **Open Serial Monitor:**
   - Tools → Serial Monitor
   - Set baud rate to **9600** (bottom right)

2. **Check for message:**
   - You should see: `Arduino Ready`
   - If you see this, the code is running correctly!

### 6. Run Python Game

Once Arduino is ready, run the Python game:

```bash
cd /Users/gouripriya/coco/Digiware-Monopoly
python main.py
```

The Python script will automatically connect to the Arduino via Serial.

## Troubleshooting

### "Board not found" or upload fails
- Check USB cable connection
- Try a different USB port
- Make sure correct port is selected in Tools → Port
- On Mac: Install CH340/CH341 drivers if using clone boards

### Serial Monitor shows nothing
- Check baud rate is set to 9600
- Press reset button on Arduino
- Close Serial Monitor before running Python (only one program can use Serial)

### Library not found
- Make sure you installed "RF24" by TMRh20
- Try: Sketch → Include Library → Manage Libraries → Search "RF24"
- Restart Arduino IDE after installing

### NRF24L01 not working
- Verify 3.3V power (NOT 5V!)
- Check all connections
- Ensure proper SPI connections (MOSI, MISO, SCK)
- Try adding a 10µF capacitor between VCC and GND on NRF module

## Testing Without Hardware

If you want to test the Python game without Arduino:
- Edit `src/graphics/game_window.py`
- Change `test_mode=False` to `test_mode=True`
- Run: `python main.py`
- Use SPACE key to roll dice

