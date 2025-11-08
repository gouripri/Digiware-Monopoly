"""
Board rendering and layout
"""
import pygame

class BoardRenderer:
    def __init__(self, screen):
        self.screen = screen    #init_ to 800
        self.board_size = screen.get_width() - 100 #bc the margin is 50
        self.margin = 50
        self.font = pygame.font.SysFont("monospace", 10)

        self.cell_count= 6     #10x10 board
        self.corner_size = self.board_size // 6 #makes corners 133.33px
        self.cell_size= (self.board_size - 2 * self.corner_size) /self.cell_count

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


