"""
Input handler for reading rotary encoder data from Arduino via Serial
Maps hardware input to game actions
"""
import serial
import serial.tools.list_ports
import time

class InputHandler:
    """Handles input from Arduino rotary encoders"""
    
    # Game states
    STATE_WAITING_FOR_ROLL = "waiting_for_roll"
    STATE_LANDED_ON_PROPERTY = "landed_on_property"
    STATE_PLAYER_TURN = "player_turn"
    STATE_MENU_NAVIGATION = "menu_navigation"
    
    def __init__(self, port=None, baud_rate=9600, test_mode=False):
        """
        Initialize input handler with Serial connection
        
        Args:
            port: Serial port name (e.g., '/dev/tty.usbmodem...' on Mac, 'COM3' on Windows)
                   If None, will try to auto-detect
            baud_rate: Serial communication speed (default 9600)
            test_mode: If True, simulates input for testing without Arduino
        """
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None
        self.current_state = self.STATE_WAITING_FOR_ROLL
        self.last_input_time = 0
        self.input_debounce = 0.1  # Minimum time between inputs (seconds)
        self.test_mode = test_mode
        self.test_input_queue = []  # For testing without Arduino
        
    def connect(self):
        """Connect to Arduino via Serial"""
        if self.test_mode:
            print("Input handler in TEST MODE - no Arduino connection needed")
            return True
            
        try:
            if self.port is None:
                # Try to auto-detect Arduino port
                self.port = self._find_arduino_port()
                if self.port is None:
                    print("Could not find Arduino port. Please specify port manually.")
                    return False
            
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=0.1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"✓ Connected to Arduino on {self.port}")
            print(f"  Waiting for messages (e.g., 'P1,Roll')...")
            return True
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")
            return False
    
    def _find_arduino_port(self):
        """Try to find Arduino port automatically"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # Common Arduino identifiers
            if 'arduino' in port.description.lower() or 'usb' in port.description.lower():
                return port.device
        # If no Arduino found, return first available port (for testing)
        if ports:
            return ports[0].device
        return None
    
    def disconnect(self):
        """Close Serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Disconnected from Arduino")
    
    def send_to_arduino(self, message):
        """
        Send a message to Arduino via Serial.
        
        Args:
            message: String message to send to Arduino
        """
        if self.test_mode:
            print(f"[TEST MODE] Would send to Arduino: {message}")
            return
        
        if self.serial_connection is None or not self.serial_connection.is_open:
            return
        
        try:
            # Send message with newline (Arduino typically reads line by line)
            message_with_newline = f"{message}\n"
            self.serial_connection.write(message_with_newline.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to Arduino: {e}")
    
    def send_property_name(self, property_name):
        """
        Send the current property name to Arduino.
        Format: "Property: <name>"
        
        Args:
            property_name: Name of the property the player is on
        """
        if property_name:
            self.send_to_arduino(f"Property: {property_name}")
    
    def set_state(self, state):
        """Set the current game state"""
        self.current_state = state
    
    def get_state(self):
        """Get current game state"""
        return self.current_state
    
    def parse_arduino_message(self, message):
        """
        Parse message from Arduino.
        Format: "Roll", "Buy", "Pass" (single player mode)
        Also supports: "P1,Roll" format for compatibility
        
        Args:
            message: Raw string from Arduino Serial (e.g., "Roll" or "P1,Roll")
        
        Returns:
            (has_input: bool, player_num: int, action: str)
            - has_input: True if message contains valid input
            - player_num: Player number (1 for single player, or from message)
            - action: Action string (e.g., "Roll", "Buy", "Pass") or None
        """
        message = message.strip()
        
        # Parse format: "P1,Roll" or "P2,Buy" etc. (for compatibility)
        if ',' in message:
            parts = message.split(',')
            if len(parts) == 2:
                player_part = parts[0].strip().upper()
                action_part = parts[1].strip()
                
                # Extract player number from "P1", "P2", etc.
                player_num = 0
                if player_part.startswith('P') and len(player_part) > 1:
                    try:
                        player_num = int(player_part[1:])
                    except ValueError:
                        pass
                
                # Return parsed values
                if player_num > 0 and action_part:
                    return True, player_num, action_part
        
        # Single player mode: just action words like "Roll", "Buy", "Pass"
        message_upper = message.upper()
        if message_upper in ["ROLL", "BUY", "PASS"]:
            # Single player mode - always player 1
            return True, 1, message_upper
        
        # Fallback: try to parse old format for backwards compatibility
        message_lower = message.lower()
        has_input = False
        direction = 0
        button_pressed = False
        
        if "clockwise" in message_lower or "cw" in message_lower or message == "1":
            has_input = True
            direction = 1
        elif "counterclockwise" in message_lower or "ccw" in message_lower or message == "-1":
            has_input = True
            direction = -1
        
        if "button" in message_lower or "press" in message_lower or "b" in message_lower:
            has_input = True
            button_pressed = True
        
        # Return old format if found, otherwise no input
        if has_input:
            return True, 0, None  # Old format, no player number
        return False, 0, None
    
    def read_input(self):
        """
        Read input from Serial (non-blocking).
        
        Returns: (has_input: bool, player_num: int, action: str)
        - has_input: True if new input was received
        - player_num: Player number (1, 2, 3, etc.) or 0 if not specified
        - action: Action string (e.g., "Roll", "Buy", "Pass") or None
        """
        if self.test_mode:
            # Test mode: return queued test inputs
            if self.test_input_queue:
                return self.test_input_queue.pop(0)
            return False, 0, None
        
        if self.serial_connection is None or not self.serial_connection.is_open:
            return False, 0, None
        
        try:
            # Check if data is available (non-blocking)
            if self.serial_connection.in_waiting > 0:
                # Read line from Serial
                line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                
                if not line:
                    return False, 0, None
                
                # Debug: print received message
                print(f"[Arduino] Received: '{line}'")
                
                # Debounce: ignore inputs too close together
                current_time = time.time()
                if current_time - self.last_input_time < self.input_debounce:
                    return False, 0, None
                self.last_input_time = current_time
                
                # Parse the message using helper function
                has_input, player_num, action = self.parse_arduino_message(line)
                
                if has_input:
                    print(f"[Arduino] Parsed: player={player_num}, action={action}")
                    return True, player_num, action
                else:
                    print(f"[Arduino] Could not parse message: '{line}'")
                
        except Exception as e:
            print(f"Error reading Serial: {e}")
        
        return False, 0, None
    
    def process_input(self, game_state=None):
        """
        Process input and return what action to take.
        Single player mode: accepts "Roll", "Buy", "Pass" directly.
        
        Args:
            game_state: Current GameState object (optional, for context)
        
        Returns:
            (action: str, data: dict) or None
            Actions: 'roll_dice', 'buy', 'pass', etc.
            data contains: 'player_num' (1-indexed player number)
        """
        has_input, player_num, action = self.read_input()
        
        if not has_input:
            return None
        
        # Single player mode: if we have an action, process it (always for player 1)
        if action:
            action_upper = action.upper()
            
            # In single player mode, always accept actions (only one player)
            if action_upper == "ROLL":
                print(f"[Game] Triggering dice roll for player {player_num}")
                return ('roll_dice', {'player_num': 1})
            elif action_upper == "BUY":
                return ('buy', {'player_num': 1})
            elif action_upper == "PASS":
                return ('pass', {'player_num': 1})
        
        # Multi-player format: "P1,Roll" style messages (for compatibility)
        if player_num > 0 and action:
            action_upper = action.upper()
            
            # Check if this is for the current player
            current_player_index = 0
            if game_state:
                current_player_index = game_state.current_player_index
            
            # Player numbers are 1-indexed, current_player_index is 0-indexed
            if player_num == (current_player_index + 1):
                # This message is for the current player
                if action_upper == "ROLL":
                    return ('roll_dice', {'player_num': player_num})
                elif action_upper == "BUY":
                    return ('buy', {'player_num': player_num})
                elif action_upper == "PASS":
                    return ('pass', {'player_num': player_num})
        
        return None
    
    # ========== TESTING HELPER FUNCTIONS ==========
    
    def add_test_input(self, player_num=0, action=None):
        """
        Add test input for testing without Arduino.
        Useful for development and testing.
        
        Args:
            player_num: Player number (1, 2, 3, etc.) or 0 for old format
            action: Action string (e.g., "Roll", "Buy", "Pass") or None
        """
        self.test_input_queue.append((True, player_num, action))
    
    def simulate_player_roll(self, player_num):
        """Helper: Simulate player rolling dice (e.g., "P1,Roll")"""
        self.add_test_input(player_num=player_num, action="Roll")
    
    def simulate_clockwise_turn(self):
        """Helper: Simulate clockwise encoder turn (old format)"""
        self.add_test_input(player_num=0, action=None)
    
    def simulate_counterclockwise_turn(self):
        """Helper: Simulate counterclockwise encoder turn (old format)"""
        self.add_test_input(player_num=0, action=None)
    
    def simulate_button_press(self):
        """Helper: Simulate button press (old format)"""
        self.add_test_input(player_num=0, action=None)
    
    def clear_test_inputs(self):
        """Clear all queued test inputs"""
        self.test_input_queue = []

