"""
Main entry point for the Monopoly game
"""
import pygame
from src.graphics.game_window import GameWindow

def main():
    pygame.init()
    game = GameWindow()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()

