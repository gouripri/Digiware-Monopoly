# Setup and Run Guide

## Prerequisites

### Hardware Required:
- Arduino Uno (with USB cable)
- NRF24L01 radio modules (for wireless communication with player devices)
- Player devices with NRF24L01 modules (if using multi-player mode)

### Software Required:
- Arduino IDE (for uploading code to Arduino)
- Python 3.7+ 
- pip (Python package manager)

## Step 1: Upload Arduino Code

1. **Open Arduino IDE**
   - Install Arduino IDE from https://www.arduino.cc/en/software

2. **Install Required Libraries**
   - Open Arduino IDE → Sketch → Include Library → Manage Libraries
   - Search and install:
     - `RF24` by TMRh20 (for NRF24L01 communication)
     - `nRF24L01` (if needed)

3. **Upload Code to Arduino**
   - Connect Arduino Uno to your computer via USB
   - Open `Uno_CODE/hub.ino` in Arduino IDE
   - Select the correct board: Tools → Board → Arduino Uno
   - Select the correct port: Tools → Port → (your Arduino port, e.g., `/dev/tty.usbmodem...` on Mac, `COM3` on Windows)
   - Click Upload button (or press Ctrl+U / Cmd+U)
   - Wait for "Done uploading" message

4. **Verify Upload**
   - Open Serial Monitor: Tools → Serial Monitor
   - Set baud rate to 9600
   - You should see "Arduino Ready" message

## Step 2: Set Up Python Environment

1. **Navigate to Project Directory**
   ```bash
   cd /Users/gouripriya/chocolate/Digiware-Monopoly
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs:
   - `pygame` (for game graphics)
   - `pyserial` (for Arduino communication)

## Step 3: Run the Game

### Option A: Auto-Detect Arduino Port (Recommended)
```bash
python main.py
```

The game will automatically try to find and connect to your Arduino.

### Option B: Specify Arduino Port Manually

If auto-detection doesn't work, you can specify the port:

**On Mac/Linux:**
```bash
python main.py --port /dev/tty.usbmodem14101
```

**On Windows:**
```bash
python main.py --port COM3
```

To find your port:
- **Mac/Linux**: Run `ls /dev/tty.*` and look for `usbmodem` or `usbserial`
- **Windows**: Check Device Manager → Ports (COM & LPT)
- **Arduino IDE**: Tools → Port shows available ports

### Option C: Test Mode (Without Arduino)

If you want to test the game without Arduino:
- Edit `src/graphics/game_window.py` line 40
- Change `test_mode=False` to `test_mode=True`
- Run: `python main.py`
- Use SPACE key to roll dice

## Step 4: Using the Game

### Controls:
- **SPACE key**: Roll dice (also works with Arduino input)
- **Arduino**: Automatically sends roll commands when players press buttons on their devices
- **Close window**: Click X or press ESC to quit

### Game Flow:
1. Game starts at GO position
2. Arduino sends "go" signal to player devices via NRF
3. When player presses button, Arduino receives "ROLL" via NRF
4. Arduino sends "P1,Roll" to Python via Serial
5. Python game rolls dice and moves player
6. Python sends property name back to Arduino
7. Process repeats

## Troubleshooting

### "Could not find Arduino port"
- Make sure Arduino is connected via USB
- Check that Arduino IDE can see the port (Tools → Port)
- Try specifying port manually (see Option B above)
- On Mac, you may need to install USB drivers

### "Failed to connect to Arduino"
- Make sure Arduino code is uploaded successfully
- Check Serial Monitor shows "Arduino Ready"
- Verify baud rate is 9600 (matches in both Arduino and Python)
- Try unplugging and replugging USB cable
- Close Serial Monitor in Arduino IDE (only one program can use Serial at a time)

### Game runs but no Arduino input
- Check Serial Monitor in Arduino IDE is closed
- Verify Arduino is sending "P1,Roll" messages (check Serial Monitor before running Python)
- Make sure NRF modules are properly connected and configured
- Check that player devices are sending "ROLL" messages

### Import errors
- Make sure you're in the project directory
- Run `pip install -r requirements.txt` again
- Check Python version: `python --version` (should be 3.7+)

## Testing Without Hardware

If you don't have Arduino connected, you can test the game in test mode:

1. Edit `src/graphics/game_window.py`
2. Change line 40: `self.input_handler = InputHandler(test_mode=True)`
3. Run `python main.py`
4. Use SPACE key to roll dice

## Next Steps

- Connect player devices with NRF24L01 modules
- Configure player device addresses in `Uno_CODE/nrf.cpp` if needed
- Customize game properties in `src/game_logic/game_state.py`

