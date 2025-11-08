"""
Main game window and rendering loop
"""
import pygame
from src.graphics.board import BoardRenderer

class GameWindow:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Monopoly")
        self.clock = pygame.time.Clock()
        self.running = True

        self.board_render = BoardRenderer(self.screen)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((90, 140, 220))
            # TODO: Render board, properties, tokens, etc.
            self.board_render.render()
            pygame.display.flip()
            self.clock.tick(60)

