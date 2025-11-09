"""
Main game window and rendering loop
creates pygame window
"""
import pygame
from src.graphics.board import BoardRenderer
from src.graphics.dice_animation import DiceAnimation
from src.graphics.tokens import TokenRenderer
from src.game_logic.game_state import GameState
from src.utils.input_handler import InputHandler

class GameWindow:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Monopoly")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game state (stores all game data in memory)
        self.game_state = GameState()
        
        # Initialize all properties on the board
        self.game_state.initialize_all_properties()
        
        # Add single player for presentation
        self.game_state.add_player("Player 1", "test")
        
        # Create renderers
        self.board_renderer = BoardRenderer(self.screen)
        self.dice_animation = DiceAnimation(self.screen)
        
        # Create token renderer (needs position calculator from board renderer)
        self.token_renderer = TokenRenderer(self.screen, self.board_renderer.position_calc)
        
        # Track if we've processed the dice roll for this animation
        self.dice_roll_processed = False
        
        # Initialize Arduino input handler (test_mode=True for testing without Arduino)
        self.input_handler = InputHandler(test_mode=False)  # Set to False when Arduino is connected
        self.input_handler.connect()
        
        # Send initial property name for starting position (GO)
        initial_prop = self.game_state.get_property_at_position(0)
        if initial_prop:
            self.input_handler.send_property_name(initial_prop.name)
        
    def _send_current_property(self):
        """Send the current player's property name to Arduino"""
        current_player = self.game_state.get_current_player()
        if current_player:
            prop = self.game_state.get_property_at_position(current_player.position)
            if prop:
                self.input_handler.send_property_name(prop.name)
    
    def _handle_roll_request(self):
        """Handle a request to roll dice (from keyboard or Arduino)"""
        if not self.dice_animation.is_animating:
            # Get current player
            current_player = self.game_state.get_current_player()
            if current_player:
                # Check if player should skip turn (e.g., in jail)
                should_skip, reason = self.game_state.should_skip_turn(current_player)
                
                if should_skip:
                    # Player skips turn
                    print(reason)
                    # In single player mode, just wait for next roll
                    # self.game_state.next_turn()  # Commented out for single player
                    # Send current player's property name
                    self._send_current_property()
                else:
                    # Player can roll dice
                    if reason:  # Released from jail message
                        print(reason)
                    
                    # Reset processed flag
                    self.dice_roll_processed = False
                    # Start dice animation
                    self.dice_animation.start_animation()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # Press SPACE to trigger dice roll and move player
                    if event.key == pygame.K_SPACE:
                        self._handle_roll_request()
            
            # Check for Arduino input
            arduino_action = self.input_handler.process_input(self.game_state)
            if arduino_action:
                action_name, action_data = arduino_action
                if action_name == 'roll_dice':
                    # In single player mode, always accept roll requests
                    self._handle_roll_request()
            
            # Update animations
            self.dice_animation.update()
            self.token_renderer.update_movements()  # Update token movement animations
            
            # Check if dice animation just finished (only process once)
            if self.dice_animation.just_finished and not self.dice_roll_processed:
                # Mark as processed so we don't do it multiple times
                self.dice_roll_processed = True
                self.dice_animation.just_finished = False
                
                # Get current player
                current_player = self.game_state.get_current_player()
                if current_player:
                    # Roll dice using game state (single die, 1-6)
                    dice_roll = self.game_state.roll_dice(num_dice=1)
                    # Set the animation to show the final value (dice stays visible)
                    self.dice_animation.stop_animation(final_value=dice_roll)
                    
                    # Get starting position before move
                    start_position = current_player.position
                    
                    # Move player based on dice roll (1-6 spaces)
                    new_position, passed_go, landed_on_go, went_to_jail = self.game_state.move_player(current_player, dice_roll)
                    
                    if went_to_jail:
                        print(f"{current_player.name} rolled {dice_roll}, landed on Go to Jail! Sent to Jail (position 7)")
                    else:
                        print(f"{current_player.name} rolled {dice_roll}, moved to position {new_position}")
                    
                    # Start smooth movement animation for the token (from start to target)
                    # If went to jail, animate to position 7
                    self.token_renderer.start_movement(current_player, new_position, start_position=start_position)
                    
                    # Handle landing on property
                    action, prop, message = self.game_state.handle_landing(current_player, new_position)
                    if action == 'buy':
                        print(f"{message}")
                    elif action == 'rent':
                        print(f"{message}")
                    
                    # Send property name to Arduino
                    if prop:
                        self.input_handler.send_property_name(prop.name)
                    else:
                        # Get property at position even if handle_landing returned None
                        prop_at_pos = self.game_state.get_property_at_position(new_position)
                        if prop_at_pos:
                            self.input_handler.send_property_name(prop_at_pos.name)
                    
                    # In single player mode, don't advance turn (always same player)
                    # For presentation: just reset for next roll
                    # self.game_state.next_turn()  # Commented out for single player
                    # Send current player's property name to Arduino
                    self._send_current_property()
            
            self.screen.fill((255, 255, 255))
            
            # Render board (base layer)
            self.board_renderer.render()
            
            # Render tokens (on top of board)
            self.token_renderer.render_all_tokens(self.game_state.players)
            
            # Render dice animation (on top of everything)
            self.dice_animation.render()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # Cleanup: disconnect from Arduino when game closes
        self.input_handler.disconnect()