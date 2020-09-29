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


# show time
def show_time(screen, font, running_time, x, y):
    minutes = str(running_time // 60000).zfill(2)
    seconds = str(int(running_time % 60000//1000)).zfill(2)
    screen.blit(font.render("Zeit : " + str(minutes) + ":" + str(seconds), True, (0, 0, 0)), (x, y))


# show number of cleared lines
def show_number_lines(screen, font, lines, x, y):
    screen.blit(font.render("Reihen: " + str(lines), True, (0, 0, 0)), (x, y))


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
            return True
    return False


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

    # Declare and initialize all tetromino shape with all rotation
    i_tet = [[0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
             [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
             [0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0]]

    o_tet = [[0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0]]

    s_tet = [[0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0],
             [0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 0, 0]]

    z_tet = [[0, 0, 0, 0, 6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 6, 0, 0, 6, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 0, 6, 6, 0],
             [0, 0, 0, 0, 0, 6, 0, 0, 6, 6, 0, 0, 6, 0, 0, 0]]

    j_tet = [[0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]]

    l_tet = [[0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 3, 0, 0, 0],
             [0, 0, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0]]

    t_tet = [[0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 7, 0, 0, 7, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0],
             [0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 0, 0, 0, 7, 0, 0]]

    all_tetromino = [i_tet, o_tet, s_tet, z_tet, j_tet, l_tet, t_tet]

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
    speed = 900
    tetromino_down = pygame.USEREVENT + 1
    pygame.time.set_timer(tetromino_down, speed)
    pygame.key.set_repeat(1, 100)
    number_of_lines = 0
    # get randrom tetromino

    next_tetromino = get_new_tetromino(all_tetromino)
    falling_tetromino = get_new_tetromino(all_tetromino)
    game_over_bool = False

    # game-loop

    run = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while run:
        if not game_over_bool:
            counting_time = pygame.time.get_ticks() - start_time
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
                    if not game_over_bool:
                        tetromino_on_grid(falling_tetromino[yy], grid, COLUMN, tet_x, tet_y)
                        tet_x = 3
                        tet_y = 0
                        yy = 0

                        falling_tetromino = next_tetromino
                        next_tetromino = get_new_tetromino(all_tetromino)
                        pygame.time.set_timer(tetromino_down, speed)

                    if not validity(falling_tetromino[yy], grid, tet_x, tet_y, ROW, COLUMN) and tet_x == 3 and tet_y == 0 and not game_over_bool:
                        game_over_bool = True
                        next_tetromino = falling_tetromino

            if event.type == pygame.KEYDOWN:

                # press button up to rotate
                if event.key == pygame.K_UP and not game_over_bool:
                    if yy >= 3:
                        yy = 0
                        if not validity(falling_tetromino[yy], grid, tet_x, tet_y, ROW, COLUMN):
                            yy = 3
                    else:
                        yy += 1
                        if not validity(falling_tetromino[yy], grid, tet_x, tet_y, ROW, COLUMN):
                            yy -= 1
                # press button left to slide left
                if event.key == pygame.K_LEFT and not game_over_bool:
                    if validity(falling_tetromino[yy], grid, tet_x - 1, tet_y, ROW, COLUMN):
                        tet_x -= 1
                # press button right to slide right
                if event.key == pygame.K_RIGHT and not game_over_bool:
                    if validity(falling_tetromino[yy], grid, tet_x + 1, tet_y, ROW, COLUMN):
                        tet_x += 1
                # press button down to slide down
                if event.key == pygame.K_DOWN and not game_over_bool:
                    if validity(falling_tetromino[yy], grid, tet_x, tet_y + 1, ROW, COLUMN):
                        tet_y += 1

                if event.key == pygame.K_m:
                    if mixer.music.get_volume() > 0:
                        mixer.music.set_volume(0)
                    else:
                        mixer.music.set_volume(0.15)

        # Background color
        screen.fill((241, 241, 241))

        if delete_line(grid, COLUMN):
            number_of_lines += 1
            score_value += 10
            speed -= 100

        # field
        pygame.draw.rect(screen, (0, 0, 0), (245, 95, WIDTH+10, height+10), 3)

        # show rectangle that contains the next block
        show_next_block(screen, font, gap)

        # score
        show_score(screen, font, score_value, 80, 50)

        # game over text
        if game_over_bool:
            game_over_text(screen, over_font)

        # forecast tetromino
        draw_struture(COLOR, screen, next_tetromino[0], gap, 4, 580, 105, 0, 0)

        # draw falling tetromino
        if not game_over_bool:
            draw_struture(COLOR, screen, falling_tetromino[yy], gap, 4, 250, 100, tet_x, tet_y)

        # draw field
        draw_struture(COLOR, screen, grid, gap, COLUMN, 250, 100, 0, 0)

        # timer
        show_time(screen, font, counting_time, 80, 100)

        # lines
        show_number_lines(screen, font, number_of_lines, 80, 150)

        # update screen
        pygame.display.update()

    pygame.quit()


# close game
main()



