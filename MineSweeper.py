import pygame
import MineSweeperClass

WHITE = (255, 255, 255)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 0

tilePicDict = {}
tilePicDict['Covered'] =  pygame.transform.scale(pygame.image.load(r'minesweeper pics\facingDown.png'),(WIDTH,HEIGHT))
tilePicDict['Marked'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\flagged.png'),(WIDTH,HEIGHT))
tilePicDict['Mine'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\bomb.png'),(WIDTH,HEIGHT))
tilePicDict['0'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\0.png'),(WIDTH,HEIGHT))
tilePicDict['1'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\1.png'),(WIDTH,HEIGHT))
tilePicDict['2'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\2.png'),(WIDTH,HEIGHT))
tilePicDict['3'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\3.png'),(WIDTH,HEIGHT))
tilePicDict['4'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\4.png'),(WIDTH,HEIGHT))
tilePicDict['5'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\5.png'),(WIDTH,HEIGHT))
tilePicDict['6'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\6.png'),(WIDTH,HEIGHT))
tilePicDict['7'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\7.png'),(WIDTH,HEIGHT))
tilePicDict['8'] = pygame.transform.scale(pygame.image.load(r'minesweeper pics\8.png'),(WIDTH,HEIGHT))

pygame.init()

ms = MineSweeperClass.MineSweeperGrid(rows=25,cols=40,mines=160)
# Set the width and height of the screen [width, height]
screenWidth = ms.cols * (WIDTH+MARGIN) + MARGIN
screenHight = ms.rows * (HEIGHT+MARGIN)+MARGIN
size = (screenWidth, screenHight)
screen = pygame.display.set_mode(size)
# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
success = False
change = True
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                ms.revert()
                change = True
                ms.fail = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not ms.fail and not success:
            player_position = pygame.mouse.get_pos()
            x = player_position[0]
            y = player_position[1]
            (row,col) = ms.coordToGridIndex(x=x,y=y,width=WIDTH,height=HEIGHT,margin=MARGIN)
            rightClick = event.button == 3
            leftClick = event.button == 1
            mouse_pressed = pygame.mouse.get_pressed()
            if not ms.firstClick and (mouse_pressed[0] and mouse_pressed[2]) or mouse_pressed[1]:
                if row >=0 and row < ms.rows and col>=0 and col<ms.cols:
                    ms.openMultiTile(row,col)
            elif ms.firstClick and leftClick & row >=0 and row < ms.rows and col>=0 and col<ms.cols:
                ms.openFirstTile(row,col)
            elif leftClick and row >=0 and row < ms.rows and col>=0 and col<ms.cols:
                ms.openTile(row,col)
            elif rightClick & row >=0 and row < ms.rows and col>=0 and col<ms.cols:
                if ms.grid[row][col].marked:
                    ms.grid[row][col].marked = False #was marked, now un marked
                    ms.mineUnMarked += 1
                else:
                    if ms.grid[row][col].covered:
                        ms.grid[row][col].marked = True #was unmarked, now marked
                        ms.mineUnMarked -= 1
                print(ms.mineUnMarked)
                change = True
            else:
                change = False
                break
        break

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    if not success and change:
        if not ms.fail:
            screen.fill(WHITE)
            ms.makeBackup()
        else:
            screen.fill(RED)
        # --- Drawing code should go here
        for row in range(ms.rows):
            for column in range(ms.cols):
                (x,y) = ms.gridIndexToCoord(row=row,col=column,width=WIDTH,height=HEIGHT,margin=MARGIN)
                screen.blit(tilePicDict[ms.grid[row][column].printObjAsDictKey()],(x,y))

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    if not success:
        success = ms.success()
    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()