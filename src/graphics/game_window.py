"""
Main game window and rendering loop
"""
import pygame

class GameWindow:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Monopoly")
        self.clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((255, 255, 255))
            # TODO: Render board, properties, tokens, etc.
            pygame.display.flip()
            self.clock.tick(60)

