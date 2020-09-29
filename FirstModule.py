'''
Created on 17.09.2020

@author: Lukas & Renan
'''

import pygame
import random
from pygame import mixer


# Function


# show score
def show_score(screen, font, score_value, x, y):
    screen.blit(font.render("Score : " + str(score_value), True, (0, 0, 0)), (x, y))


# show next block
def show_next_block(screen, font, gap):
    pygame.draw.rect(screen, (0, 0, 0), (575, 100, gap*4+10, gap*4+10), 3)
    screen.blit(font.render("Next", True, (0, 0, 0)), (600, 60))


# show game over text
def game_over_text(screen, over_font):
    screen.blit(over_font.render("Game over!", True, (0, 0, 0)), (270, 30))


# get randrom tetromino
def get_new_tetromino(all_tetrominos):
    random_tetrominos = random.choice(all_tetrominos)
    return random_tetrominos


# put tetromio on grid
def tetromino_on_grid(falling_tetromino, grids, column, tet_x, tet_y):
  for n, color in enumerate(falling_tetromino):
    if color > 0:
      r = tet_y + n // 4
      c = tet_x + n % 4
      grids[r*column+c] = color


# make sure the character can not move off the screen
def validity(falling_tetromino, grids, off_tet_x, off_tet_y, row, column):
    for n, color in enumerate(falling_tetromino):
      if color > 0:
        r = off_tet_y + n // 4
        c = off_tet_x + n % 4
        if r >= row or c < 0 or c >= column or grids[r * column + c] > 0:
          return False
    return True


# draw tetromino, grid or forecast
def draw_struture(color, screen, struct, gaps, columns, off_x, off_y, tet_x, tet_y):
    for n, color_number in enumerate(struct):
        if color_number > 0:
            x = n % columns * gaps + off_x + gaps * tet_x
            y = n // columns * gaps + off_y + gaps * tet_y
            pygame.draw.rect(screen, (0, 0, 0), (x, y, gaps, gaps))
            pygame.draw.rect(screen, color[color_number], (x+1, y+1, gaps-2, gaps-2))


# delete full column
def delete_line(grid, column):
    ig = 0
    for n in range(200):
        x = n % column
        if x == 0:
            ig = 0
        if grid[n] != 0:
            ig += 1
        if ig == 10:
            del grid[n - 9:n + 1]
            for nl in range(column):
                grid.insert(0, 0)


def main():
    # Initialize pygame

    pygame.init()
    # Create a window of 800 width, 750 heigth

    screen = pygame.display.set_mode((800, 750))  # optional: RESIZEABLE

    # Title and Icon

    pygame.display.set_caption("Tetris")
    icon = pygame.image.load("tetris.png")
    pygame.display.set_icon(icon)

    # Background Sound

    mixer.music.load("Tetris.mp3")
    mixer.music.set_volume(0.15)
    mixer.music.play(-1)

    # Font

    score_value = 0
    font = pygame.font.SysFont("arial", 25)

    over_font = pygame.font.SysFont("arial", 50)

    # Tetromino

    I = [[0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
         [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
         [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0]]

    O = [[0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0]]

    S = [[0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0],
         [0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 0, 0]]

    Z = [[0, 0, 0, 0, 6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 6, 0, 0, 6, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 0, 6, 6, 0],
         [0, 0, 0, 0, 0, 6, 0, 0, 6, 6, 0, 0, 6, 0, 0, 0]]

    J = [[0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]]

    L = [[0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 3, 0, 0, 0],
         [0, 0, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0]]

    T = [[0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 7, 0, 0, 7, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0],
         [0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 0, 0, 0, 7, 0, 0]]

    all_tetromino = [I, O, S, Z, J, L, T]

    # Color

    grid = [0] * 10 * 20
    deep_sky_blue = (0, 0, 205)
    medium_blue = (0, 191, 255)
    dark_orange = (255, 140, 0)
    yellow = (255, 255, 0)
    lawn_green = (124, 252, 0)
    red = (255, 0, 0)
    purple = (128, 0, 128)

    # Variable

    WIDTH, COLUMN, ROW = 300, 10, 20
    gap = WIDTH // COLUMN
    height = gap * ROW
    COLOR = [(0, 0, 0), deep_sky_blue, medium_blue, dark_orange, yellow, lawn_green, red, purple]
    yy = 0
    tet_x = 3
    tet_y = 0
    tetromino_down = pygame.USEREVENT + 1
    pygame.time.set_timer(tetromino_down, 500)
    pygame.key.set_repeat(1, 100)
    # get randrom tetromino

    next_tetromino = get_new_tetromino(all_tetromino)
    falling_tetromino = get_new_tetromino(all_tetromino)

    # game-loop

    run = True
    clock = pygame.time.Clock()
    while run:
        # loop through a list of any keyboard or mouse events

        for event in pygame.event.get():

            # check for a QUIT event
            if event.type == pygame.QUIT:

                # End the game loop
                run = False

            # tetromino one down
            if event.type == tetromino_down:
                if validity(falling_tetromino[yy], grid, tet_x, tet_y + 1, ROW, COLUMN):
                    tet_y += 1
                else:
                    tetromino_on_grid(falling_tetromino[yy], grid, COLUMN, tet_x, tet_y)
                    tet_x = 3
                    tet_y = 0

                    falling_tetromino = next_tetromino
                    next_tetromino = get_new_tetromino(all_tetromino)
                    delete_line(grid, COLUMN)

            if event.type == pygame.KEYDOWN:
                # press button 1 to put tetromino on grid
                if event.key == pygame.K_1:
                    tetromino_on_grid(falling_tetromino[yy], grid, COLUMN, tet_x, tet_y)
                    tet_x = 3
                    tet_y = 0
                # press button 2 to generate new tetro with check
                if event.key == pygame.K_2:
                    saveold_tetromino = falling_tetromino
                    falling_tetromino = next_tetromino
                    next_tetromino = get_new_tetromino(all_tetromino)
                    if not validity(falling_tetromino[yy], grid, tet_x, tet_y, ROW, COLUMN):
                        falling_tetromino = saveold_tetromino
                # press button up to rotate
                if event.key == pygame.K_UP:
                    if yy >= 3:
                        yy = 0
                        if not validity(falling_tetromino[yy], grid, tet_x, tet_y, ROW, COLUMN):
                            yy = 3
                    else:
                        yy += 1
                        if not validity(falling_tetromino[yy], grid, tet_x, tet_y, ROW, COLUMN):
                            yy -= 1
                # press button left to slide left
                if event.key == pygame.K_LEFT:
                    if validity(falling_tetromino[yy], grid, tet_x - 1, tet_y, ROW, COLUMN):
                        tet_x -= 1
                # press button right to slide right
                if event.key == pygame.K_RIGHT:
                    if validity(falling_tetromino[yy], grid, tet_x + 1, tet_y, ROW, COLUMN):
                        tet_x += 1
                # press button down to slide down
                if event.key == pygame.K_DOWN:
                    if validity(falling_tetromino[yy], grid, tet_x, tet_y + 1, ROW, COLUMN):
                        tet_y += 1

        # Background color
        screen.fill((241, 241, 241))

        # field
        pygame.draw.rect(screen, (0, 0, 0), (245, 95, WIDTH+10, height+10), 3)

        # show rectangle that contains the next block
        show_next_block(screen, font, gap)

        # score
        show_score(screen, font, score_value, 80, 50)

        # game over text
        game_over_text(screen, over_font)

        # forecast tetromino
        draw_struture(COLOR, screen, next_tetromino[0], gap, 4, 580, 105, 0, 0)

        # draw falling tetromino
        draw_struture(COLOR, screen, falling_tetromino[yy], gap, 4, 250, 100, tet_x, tet_y)

        # draw field
        draw_struture(COLOR, screen, grid, gap, COLUMN, 250, 100, 0, 0)

        # update screen
        pygame.display.update()


    pygame.quit()
# close game
main()



