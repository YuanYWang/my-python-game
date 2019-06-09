import pygame
from GameOfLifeClass import GameOfLife

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 10
HEIGHT = 10

# This sets the margin between each cell
MARGIN = 1

pygame.init()

gol = GameOfLife(rows=80, cols=100)
gol.setupGliderGun()
# Set the width and height of the screen [width, height]
screenWidth = gol.cols * (WIDTH + MARGIN) + MARGIN
screenHight = gol.rows * (HEIGHT + MARGIN) + MARGIN
size = (screenWidth, screenHight)
screen = pygame.display.set_mode(size)
# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
keepGoing = False
changed = True
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    if keepGoing:
        gol.step()
        changed = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            keepGoing = False
            player_position = pygame.mouse.get_pos()
            x = player_position[0]
            y = player_position[1]
            (row, col) = gol.coordToGridIndex(x=x, y=y, width=WIDTH, height=HEIGHT, margin=MARGIN)
            gol.flipState(row, col)
            changed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                keepGoing = False
                gol.step()
                changed = True
            if event.key == pygame.K_c:
                keepGoing = True
                changed = True
    if changed:
        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
        # --- Drawing code should go here
        for row in range(gol.rows):
            for column in range(gol.cols):
                color = WHITE
                if gol.grid[row][column] == 1:
                    color = GREEN

                (x, y) = gol.gridIndexToCoord(row=row, col=column, width=WIDTH, height=HEIGHT, margin=MARGIN)
                pygame.draw.rect(screen, color, [x, y, WIDTH, HEIGHT])

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    changed = False
    # --- Limit to 60 frames per second
    clock.tick(200)

# Close the window and quit.
pygame.quit()
