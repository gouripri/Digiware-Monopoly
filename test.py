import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monopoly Layers Example")

# Load or make placeholder surfaces
board_outline = pygame.Surface((WIDTH, HEIGHT))
board_outline.fill((230, 230, 230))  # light gray background

boardwalk = pygame.Surface((80, 80))
boardwalk.fill((50, 100, 200))  # blue block

park_place = pygame.Surface((80, 80))
park_place.fill((80, 80, 150))  # darker blue block

token = pygame.Surface((40, 40))
token.fill((255, 0, 0))  # red token
token_pos = [WIDTH - 60, HEIGHT - 60]

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # DRAWING ORDER (layers)
    screen.fill((255, 255, 255))              # white background
    screen.blit(board_outline, (0, 0))        # base layer
    screen.blit(boardwalk, (WIDTH - 80, HEIGHT - 80))   # boardwalk
    screen.blit(park_place, (WIDTH - 160, HEIGHT - 80)) # park place
    screen.blit(token, token_pos)             # token on top

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
