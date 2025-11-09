"""
Dice rolling animation
Alternates between random dice images and transition image
"""
import pygame
import random
import os

class DiceAnimation:
    """Handles dice rolling animation"""
    
    def __init__(self, screen):
        self.screen = screen
        self.dice_images = {}
        self.transition_image = None
        self.is_animating = False
        self.animation_frame = 0
        self.animation_duration = 50  # Number of frames to animate (longer animation)
        self.current_dice_value = 1
        # Position: middle of board (400, 400), then down and right a bit
        self.dice_position = (450, 450)  # Center of board, slightly down and right
        self.dice_size = (100, 100)  # Size of dice display
        
        self._load_dice_images()
    
    def _load_dice_images(self):
        """Load all dice images and transition image"""
        try:
            # Load dice_1.png through dice_6.png
            for i in range(1, 7):
                image_path = f"images/images/dice/dice_{i}.png"
                if os.path.exists(image_path):
                    img = pygame.image.load(image_path)
                    # Scale to dice size
                    self.dice_images[i] = pygame.transform.scale(img, self.dice_size)
                else:
                    print(f"Warning: Dice image not found: {image_path}")
            
            # Load transition image
            transition_path = "images/images/dice/dice_transition.png"
            if os.path.exists(transition_path):
                img = pygame.image.load(transition_path)
                self.transition_image = pygame.transform.scale(img, self.dice_size)
            else:
                print(f"Warning: Transition image not found: {transition_path}")
        except Exception as e:
            print(f"Error loading dice images: {e}")
    
    def start_animation(self):
        """Start the dice rolling animation"""
        self.is_animating = True
        self.animation_frame = 0
        self.current_dice_value = random.randint(1, 6)
    
    def stop_animation(self, final_value=None):
        """Stop the animation and set final dice value"""
        self.is_animating = False
        self.animation_frame = 0
        if final_value is not None:
            self.current_dice_value = final_value
    
    def update(self):
        """Update animation frame"""
        if self.is_animating:
            self.animation_frame += 1
            
            # Change dice value randomly during animation (every 5 frames for slower switching)
            if self.animation_frame % 5 == 0:  # Every 5 frames
                self.current_dice_value = random.randint(1, 6)
            
            # Stop animation after duration
            if self.animation_frame >= self.animation_duration:
                self.is_animating = False
                self.animation_frame = 0
    
    def render(self):
        """Render the dice animation"""
        if not self.dice_images and not self.transition_image:
            return  # No images loaded
        
        x, y = self.dice_position
        
        if self.is_animating:
            # Alternate between dice and transition (slower switching - every 5 frames)
            if self.animation_frame % 10 < 5:  # Show dice for 5 frames
                # Show random dice
                if self.current_dice_value in self.dice_images:
                    self.screen.blit(self.dice_images[self.current_dice_value], (x, y))
            else:
                # Show transition for 5 frames
                if self.transition_image:
                    self.screen.blit(self.transition_image, (x, y))
        else:
            # Show final dice value
            if self.current_dice_value in self.dice_images:
                self.screen.blit(self.dice_images[self.current_dice_value], (x, y))
    
    def get_final_value(self):
        """Get the final dice value after animation"""
        return self.current_dice_value

