"""
Player tokens rendering
"""
import pygame
import os
from src.utils.position_calculator import PositionCalculator

class TokenRenderer:
    def __init__(self, screen, position_calculator):
        self.screen = screen
        self.position_calc = position_calculator
        self.token_images = {}
        self.token_size = (60, 60)  # Size of token images (increased from 40x40)
        
        # Track visual positions for smooth movement (player_index -> visual_position)
        self.visual_positions = {}  # Maps player to their current visual position
        self.moving_tokens = {}  # Maps player to target position when moving
        self.movement_timers = {}  # Maps player to frame counter (pauses at each space)
        self.frames_per_space = 20  # Number of frames to wait at each space (slower movement)
        
        self._load_token_images()
    
    def _load_token_images(self):
        """Load token images for each player"""
        try:
            # Load image-removebg-preview.png for Player 1 (index 0)
            player1_path = "images/images/tokens/image-removebg-preview.png"
            if os.path.exists(player1_path):
                img = pygame.image.load(player1_path)
                # Scale to token size
                self.token_images[0] = pygame.transform.scale(img, self.token_size)
                print(f"Loaded Player 1 token: {player1_path}")
            else:
                print(f"Warning: Player 1 token image not found: {player1_path}")
            
            # Load image 15.png for Player 2 (index 1)
            player2_path = "images/images/tokens/image 15.png"
            if os.path.exists(player2_path):
                img = pygame.image.load(player2_path)
                # Scale to token size
                self.token_images[1] = pygame.transform.scale(img, self.token_size)
                print(f"Loaded Player 2 token: {player2_path}")
            else:
                print(f"Warning: Player 2 token image not found: {player2_path}")
            
            # Load test.png as default for other players
            default_path = "images/images/tokens/test.png"
            if os.path.exists(default_path):
                img = pygame.image.load(default_path)
                # Scale to token size
                self.token_images['default'] = pygame.transform.scale(img, self.token_size)
            else:
                print(f"Warning: Default token image not found: {default_path}")
        except Exception as e:
            print(f"Error loading token images: {e}")
    
    def update_movements(self):
        """Update token positions for smooth movement animation - pauses at each space"""
        # Move tokens one space at a time toward their target, with pause at each space
        for player_id, target_pos in list(self.moving_tokens.items()):
            current_vis_pos = self.visual_positions.get(player_id, target_pos)
            
            if current_vis_pos != target_pos:
                # Increment timer
                if player_id not in self.movement_timers:
                    self.movement_timers[player_id] = 0
                
                self.movement_timers[player_id] += 1
                
                # Only move to next space after waiting the required frames
                if self.movement_timers[player_id] >= self.frames_per_space:
                    # Reset timer
                    self.movement_timers[player_id] = 0
                    
                    # Move forward one space (always forward movement on board)
                    current_vis_pos += 1
                    
                    # Handle board wrapping (0-27, wraps to 0 after 27)
                    if current_vis_pos > 27:
                        current_vis_pos = 0
                    
                    self.visual_positions[player_id] = current_vis_pos
                    
                    # Check if reached target
                    if current_vis_pos == target_pos:
                        del self.moving_tokens[player_id]
                        if player_id in self.movement_timers:
                            del self.movement_timers[player_id]
            else:
                # Already at target
                del self.moving_tokens[player_id]
                if player_id in self.movement_timers:
                    del self.movement_timers[player_id]
    
    def start_movement(self, player, target_position, start_position=None):
        """
        Start smooth movement animation for a player token
        
        Args:
            player: Player object
            target_position: Target board position (0-27)
            start_position: Starting position (if None, uses current visual position or player.position)
        """
        player_id = id(player)  # Use player object ID as unique identifier
        self.moving_tokens[player_id] = target_position
        self.movement_timers[player_id] = 0  # Reset timer
        
        # Set starting visual position
        if start_position is not None:
            self.visual_positions[player_id] = start_position
        elif player_id not in self.visual_positions:
            # If no visual position exists, use player's current position
            # But player.position might already be updated, so we need the old position
            # Better to pass start_position from game_window
            self.visual_positions[player_id] = player.position
    
    def render_token(self, player, player_index, offset_index=0):
        """
        Render a player token at their current visual position (for smooth movement)
        
        Args:
            player: Player object with position attribute
            player_index: Index of player in players list (0 for Player 1, 1 for Player 2, etc.)
            offset_index: Index for offsetting multiple tokens on same space (0, 1, 2, etc.)
        """
        player_id = id(player)
        # Use visual position if moving, otherwise use actual position
        if player_id in self.visual_positions:
            render_position = self.visual_positions[player_id]
        else:
            render_position = player.position
            self.visual_positions[player_id] = render_position
        
        # Get board position coordinates for visual position
        x, y, w, h = self.position_calc.get_position_rect(render_position)
        
        # Calculate center of the space
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Offset multiple tokens if they're on the same space
        # Arrange tokens in a small grid pattern (only if multiple tokens)
        if offset_index == 0:
            # First token: perfectly centered
            offset_x = 0
            offset_y = 0
        else:
            # Additional tokens: small offset to avoid overlap
            offset_x = (offset_index % 2) * 15 - 7  # -7 or +8
            offset_y = (offset_index // 2) * 15 - 7  # -7 or +8
        
        token_x = center_x - self.token_size[0] // 2 + offset_x
        token_y = center_y - self.token_size[1] // 2 + offset_y
        
        # Get the correct token image for this player
        # Player 1 (index 0) uses image-removebg-preview.png
        # Player 2 (index 1) uses image 15.png
        if player_index == 0 and 0 in self.token_images:
            token_image = self.token_images[0]
        elif player_index == 1 and 1 in self.token_images:
            token_image = self.token_images[1]
        elif 'default' in self.token_images:
            token_image = self.token_images['default']
        else:
            return  # No token image available
        
        # Draw token
        self.screen.blit(token_image, (token_x, token_y))
    
    def render_all_tokens(self, players):
        """
        Render all player tokens, handling multiple tokens on same space
        
        Args:
            players: List of Player objects
        """
        # Group players by position
        position_groups = {}
        for i, player in enumerate(players):
            pos = player.position
            if pos not in position_groups:
                position_groups[pos] = []
            position_groups[pos].append((i, player))
        
        # Render tokens with offsets
        for position, player_list in position_groups.items():
            for offset_index, (player_index, player) in enumerate(player_list):
                self.render_token(player, player_index, offset_index)

