# Quick Start Guide - Running with Arduino

## Step 1: Install Arduino Libraries

1. **Open Arduino IDE**
   - Download from https://www.arduino.cc/en/software if you don't have it

2. **Install Required Libraries:**
   - Go to: **Sketch → Include Library → Manage Libraries**
   - Search and install:
     - **"RF24" by TMRh20** (for NRF24L01 radio)
     - **"Adafruit SSD1306"** (for OLED display)
     - **"Adafruit GFX Library"** (required by SSD1306)

## Step 2: Upload Arduino Code

1. **Open the Arduino sketch:**
   - File → Open → Navigate to `Uno_CODE/hub.ino`

2. **Select Board and Port:**
   - Tools → Board → **Arduino Uno**
   - Tools → Port → Select your Arduino port
     - On Mac, it's usually `/dev/tty.usbmodem...` or `/dev/tty.usbserial...`
     - You can see available ports by running: `ls /dev/tty.* | grep -E "(usb|serial|modem)"`

3. **Upload:**
   - Click the Upload button (→) or press `Cmd+U` (Mac) / `Ctrl+U` (Windows/Linux)
   - Wait for "Done uploading"

4. **Verify:**
   - Open Serial Monitor: Tools → Serial Monitor
   - Set baud rate to **9600**
   - You should see: `Arduino Ready`

## Step 3: Run Python Game

1. **Navigate to project directory:**
   ```bash
   cd /Users/gouripriya/munch/Digiware-Monopoly
   ```

2. **Install Python dependencies (if not already done):**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python3 main.py
   ```

   The game will automatically detect and connect to your Arduino!

## Troubleshooting

### "Failed to connect to Arduino"
- Make sure Arduino code is uploaded successfully
- Check Serial Monitor shows "Arduino Ready"
- Close Serial Monitor in Arduino IDE (only one program can use Serial at a time)
- Try unplugging and replugging USB cable

### "Board not found" or upload fails
- Check USB cable connection
- Try a different USB port
- Make sure correct port is selected in Tools → Port
- On Mac: Install CH340/CH341 drivers if using clone boards

### Library not found
- Make sure you installed all three libraries:
  - RF24 by TMRh20
  - Adafruit SSD1306
  - Adafruit GFX Library
- Restart Arduino IDE after installing libraries

### Test Mode (Without Arduino)
If you want to test without Arduino:
- Edit `src/graphics/game_window.py` line 40
- Change `test_mode=False` to `test_mode=True`
- Run: `python3 main.py`
- Use SPACE key to roll dice

