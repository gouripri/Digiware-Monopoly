"""
Main game window and rendering loop
creates pygame window
"""
import pygame
from src.graphics.board import BoardRenderer
from src.game_logic.game_state import GameState

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
        
        # Create renderers
        self.board_renderer = BoardRenderer(self.screen)
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((255, 255, 255))
            
            # Render board (base layer)
            self.board_renderer.render()
            
            # TODO: Render properties, tokens, etc. on top
            
            pygame.display.flip()
            self.clock.tick(60)