"""
Board rendering and layout
"""
import pygame
from src.utils.position_calculator import PositionCalculator

class BoardRenderer:
    def __init__(self, screen):
        self.screen = screen    #init_ to 800
        self.board_size = screen.get_width() - 100 #bc the margin is 50
        self.margin = 50
        self.font = pygame.font.SysFont("monospace", 10)

        self.cell_count= 6     #10x10 board
        self.corner_size = self.board_size // 6 #makes corners 133.33px
        self.cell_size= (self.board_size - 2 * self.corner_size) /self.cell_count

        # Position calculator for testing positions
        self.position_calc = PositionCalculator(
            self.board_size, self.margin, self.corner_size, self.cell_size
        )

        #make the board an actual object
        self.board_surface = pygame.Surface((self.board_size, self.board_size))
        self.board_color = (240,235,210)  # light beige board color
        self.border_color = (0, 0, 0)
        
        # Load board background image
        self.board_background = None
        self._load_board_background()

    def render(self):
        """Render the Monopoly board"""
        # Draw board background image if available
        if self.board_background:
            # Scale background to fit board size
            scaled_bg = pygame.transform.scale(self.board_background, (self.board_size, self.board_size))
            self.screen.blit(scaled_bg, (self.margin, self.margin))
        else:
            # Fallback to colored background if no image
            board_rect = pygame.Rect(
                self.margin,  # x offset
                self.margin,  # y offset
                self.board_size,  # width
                self.board_size  # height
            )
            self.board_surface.fill(self.board_color)
            pygame.draw.rect(self.board_surface, self.border_color,
                             (0, 0, self.board_size, self.board_size), 3)
            self.screen.blit(self.board_surface, (self.margin, self.margin))

        # Position numbers removed

    def draw_corners(self):
        c_size = self.corner_size
        m = self.margin
        color = (0, 0, 0)

        pygame.draw.rect(self.screen, color, (m, m, c_size, c_size), 2)
        # Top-right
        pygame.draw.rect(self.screen, color, (m + self.board_size - c_size, m, c_size, c_size), 2)
        # Bottom-left
        pygame.draw.rect(self.screen, color, (m, m + self.board_size - c_size, c_size, c_size), 2)
        # Bottom-right
        pygame.draw.rect(self.screen, color, (m + self.board_size - c_size, m + self.board_size - c_size, c_size, c_size), 2)

    def draw_tiles(self):
        """Draw tile outlines - currently empty, can add back if needed"""
        pass
    
    def draw_position_numbers(self):
        """Draw position numbers (0-27) on each space for testing/alignment"""
        font = pygame.font.SysFont("monospace", 16)
        
        for position in range(28):
            x, y, w, h = self.position_calc.get_position_rect(position)
            
            # Draw position number (no rectangle background)
            text = font.render(str(position), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
            self.screen.blit(text, text_rect)
    
    def _load_board_background(self):
        """Load the board background image"""
        import os
        try:
            image_path = "images/images/properties/Group 46.png"
            if os.path.exists(image_path):
                self.board_background = pygame.image.load(image_path)
                print(f"Loaded board background: {image_path}")
            else:
                print(f"Warning: Board background image not found: {image_path}")
        except Exception as e:
            print(f"Error loading board background: {e}")


