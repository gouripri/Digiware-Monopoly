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
            print(f"Connected to Arduino on {self.port}")
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
    
    def set_state(self, state):
        """Set the current game state"""
        self.current_state = state
    
    def get_state(self):
        """Get current game state"""
        return self.current_state
    
    def parse_arduino_message(self, message):
        """
        Parse message from Arduino and extract direction/action.
        MODIFY THIS FUNCTION when you know the Arduino message format.
        
        Args:
            message: Raw string from Arduino Serial
        
        Returns:
            (has_input: bool, direction: int, button_pressed: bool)
            - has_input: True if message contains valid input
            - direction: 1 for clockwise, -1 for counterclockwise, 0 for no rotation
            - button_pressed: True if button was pressed
        """
        message = message.strip().lower()
        
        # TODO: Modify this based on your Arduino message format
        # Examples of what you might receive:
        # - "clockwise" or "cw" or "1"
        # - "counterclockwise" or "ccw" or "-1"
        # - "button" or "press" or "b"
        # - Combined: "cw,button" or "1,1"
        
        has_input = False
        direction = 0
        button_pressed = False
        
        # Example parsing (adjust based on your Arduino format):
        if "clockwise" in message or "cw" in message or message == "1":
            has_input = True
            direction = 1
        elif "counterclockwise" in message or "ccw" in message or message == "-1":
            has_input = True
            direction = -1
        
        if "button" in message or "press" in message or "b" in message:
            has_input = True
            button_pressed = True
        
        return has_input, direction, button_pressed
    
    def read_input(self):
        """
        Read input from Serial (non-blocking).
        
        Returns: (has_input: bool, direction: int, button_pressed: bool)
        - has_input: True if new input was received
        - direction: 1 for clockwise, -1 for counterclockwise, 0 for no rotation
        - button_pressed: True if button was pressed
        """
        if self.test_mode:
            # Test mode: return queued test inputs
            if self.test_input_queue:
                return self.test_input_queue.pop(0)
            return False, 0, False
        
        if self.serial_connection is None or not self.serial_connection.is_open:
            return False, 0, False
        
        try:
            # Check if data is available (non-blocking)
            if self.serial_connection.in_waiting > 0:
                # Read line from Serial
                line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                
                if not line:
                    return False, 0, False
                
                # Debounce: ignore inputs too close together
                current_time = time.time()
                if current_time - self.last_input_time < self.input_debounce:
                    return False, 0, False
                self.last_input_time = current_time
                
                # Parse the message using helper function
                has_input, direction, button_pressed = self.parse_arduino_message(line)
                
                if has_input:
                    return True, direction, button_pressed
                
        except Exception as e:
            print(f"Error reading Serial: {e}")
        
        return False, 0, False
    
    def process_input(self, game_state=None):
        """
        Process input and return what action to take.
        
        Args:
            game_state: Current GameState object (optional, for context)
        
        Returns:
            (action: str, data: dict) or None
            Actions: 'buy', 'pass', 'roll_dice', 'select_next', 'select_prev', 'confirm'
        """
        has_input, direction, button_pressed = self.read_input()
        
        if not has_input:
            return None
        
        # Map input to action based on current game state
        if self.current_state == self.STATE_LANDED_ON_PROPERTY:
            # Player just landed on a property
            if direction == 1:  # Clockwise
                return ('select_buy', {})
            elif direction == -1:  # Counterclockwise
                return ('select_pass', {})
            elif button_pressed:  # Button press to confirm
                return ('confirm', {})
        
        elif self.current_state == self.STATE_WAITING_FOR_ROLL:
            # Waiting for player to roll dice
            if button_pressed or direction != 0:  # Button or encoder turn to roll
                return ('roll_dice', {})
        
        elif self.current_state == self.STATE_MENU_NAVIGATION:
            # Navigating a menu
            if direction == 1:  # Clockwise
                return ('select_next', {})
            elif direction == -1:  # Counterclockwise
                return ('select_prev', {})
            elif button_pressed:  # Button to select
                return ('confirm', {})
        
        elif self.current_state == self.STATE_PLAYER_TURN:
            # General player turn actions
            if direction == 1:
                return ('next_action', {})
            elif direction == -1:
                return ('prev_action', {})
            elif button_pressed:
                return ('confirm', {})
        
        return None
    
    # ========== TESTING HELPER FUNCTIONS ==========
    
    def add_test_input(self, direction=0, button_pressed=False):
        """
        Add test input for testing without Arduino.
        Useful for development and testing.
        
        Args:
            direction: 1 for clockwise, -1 for counterclockwise, 0 for none
            button_pressed: True if button was pressed
        """
        self.test_input_queue.append((True, direction, button_pressed))
    
    def simulate_clockwise_turn(self):
        """Helper: Simulate clockwise encoder turn"""
        self.add_test_input(direction=1, button_pressed=False)
    
    def simulate_counterclockwise_turn(self):
        """Helper: Simulate counterclockwise encoder turn"""
        self.add_test_input(direction=-1, button_pressed=False)
    
    def simulate_button_press(self):
        """Helper: Simulate button press"""
        self.add_test_input(direction=0, button_pressed=True)
    
    def clear_test_inputs(self):
        """Clear all queued test inputs"""
        self.test_input_queue = []

