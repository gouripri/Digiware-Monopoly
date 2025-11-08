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

    def render(self):
        """Render the Monopoly board"""
        # TODO: Implement board rendering
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

        self.draw_corners()
        self.draw_tiles()
        self.draw_position_numbers()  # Show position numbers for testing

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
        color = (0, 0, 0)
        c= self.corner_size
        t = self.cell_size
        margin= self.margin
        # Top edge (left → right, skipping corners)
        for i in range(self.cell_count):
            x = margin + c + i * t
            pygame.draw.rect(self.screen, color, (x, margin, t, c), 2)

        # Bottom edge
        for i in range(self.cell_count):
            x = margin + c + i * t
            pygame.draw.rect(self.screen, color, (x, margin+ self.board_size - c, t, c), 2)

        # Left edge
        for i in range(self.cell_count):
            y = margin + c + i * t
            pygame.draw.rect(self.screen, color, (margin, y, c, t), 2)

        # Right edge
        for i in range(self.cell_count):
            y = margin + c + i * t
            pygame.draw.rect(self.screen, color, (margin+self.board_size - c, y, c, t), 2)
    
    def draw_position_numbers(self):
        """Draw position numbers (0-27) on each space for testing/alignment"""
        font = pygame.font.SysFont("monospace", 16)
        
        for position in range(28):
            x, y, w, h = self.position_calc.get_position_rect(position)
            
            # Draw a colored rectangle to show the position
            color = (100, 200, 255)  # Light blue for visibility
            pygame.draw.rect(self.screen, color, (x, y, w, h), 1)
            
            # Draw position number
            text = font.render(str(position), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
            self.screen.blit(text, text_rect)


