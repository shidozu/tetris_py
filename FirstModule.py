'''
Created on 17.09.2020

@author: Lukas & Renan
'''

import pygame
import random
from pygame import mixer

# Initialize pygame


pygame.init()


# Create a window of 800 width, 750 heigth


screen = pygame.display.set_mode((800, 750))  # optional: RESIZEABLE

# Title and Icon


pygame.display.set_caption("Tetris")
icon = pygame.image.load("tetris.png")
pygame.display.set_icon(icon)

# Background Sound


#mixer.music.load("Tetris.mp3")
#mixer.music.set_volume(0.15)
#mixer.music.play(-1)

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

Tetromino = [I, O, S, Z, J, L, T]

# Color


grid = [0] * 10 * 20
deepskyblue = (0,0,205)
mediumblue =  (0,191,255)
darkorange = (255,140,0)
yellow = (255,255,0)
lawngreen = (124,252,0)
red = (255,0,0)
purple = (128,0,128)

# Variable


width, column, row = 300, 10, 20
gap = width // column
height = gap * row
color = [(0,0,0), deepskyblue, mediumblue, darkorange, yellow, lawngreen, red, purple]
yy=0
tetX = 3
tetY = 0
tetromino_down = pygame.USEREVENT + 1
pygame.time.set_timer(tetromino_down, 500)
pygame.key.set_repeat(1, 100)

# Function

# show score
def show_score(x, y):
    screen.blit(font.render("Score : " + str(score_value), True, (0, 0, 0)), (x, y))

# show next block
def show_next_block():
    pygame.draw.rect(screen, (0, 0, 0), (575, 100, 100, 100), 3)
    screen.blit(font.render("Next", True, (0, 0, 0)), (600, 60))

# show game over text
def game_over_text():
    screen.blit(over_font.render("Game over!", True, (0, 0, 0)), (270, 30))

# get randrom tetromino
def get_new_tetromino():
    random_tetromino = random.choice(Tetromino)
    return random_tetromino

# put tetromio on grid
def tetromino_on_grid():
  for n, color in enumerate(falling_tetromino[yy]):
    if color > 0:
      r = tetY + n // 4
      c = tetX + n % 4
      grid[r*column+c] = color

# make sure the character can not move off the screen
def validity(tetXoff, tetYoff):
    for n, color in enumerate(falling_tetromino[yy]):
      if color > 0:
        r = tetYoff + n // 4
        c = tetXoff + n % 4
        if r >= row or c < 0 or c >= column or grid[r * column + c] > 0:
          return False
    return True

# get randrom tetromino
falling_tetromino = get_new_tetromino()

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
            if validity(tetX, tetY + 1):
                tetY += 1

        if event.type == pygame.KEYDOWN:
            # press button 1 to put tetromino on grid
            if event.key == pygame.K_1:
                tetromino_on_grid()
                tetX = 3
                tetY = 0
            # press button 2 to generate new tetro with check
            if event.key == pygame.K_2:
                saveold_tetromino = falling_tetromino
                falling_tetromino = get_new_tetromino()
                if not validity(tetX, tetY):
                    falling_tetromino = saveold_tetromino
            # press button up to rotate
            if event.key == pygame.K_UP:
                if yy >= 3:
                    yy = 0
                    if not validity(tetX, tetY):
                        yy = 3
                else:
                    yy += 1
                    if not validity(tetX, tetY):
                        yy -= 1
            #press button left to slide left
            if event.key == pygame.K_LEFT:
                if validity(tetX - 1, tetY):
                    tetX -= 1
            #press button right to slide right
            if event.key == pygame.K_RIGHT:
                if validity(tetX + 1, tetY):
                    tetX += 1
            # press button down to slide down
            if event.key == pygame.K_DOWN:
                if validity(tetX, tetY + 1):
                    tetY += 1


    # Background color
    screen.fill((241, 241, 241))

    # field 
    pygame.draw.rect(screen, (0, 0, 0), (245, 95, width+10, height+10), 3)

    # show rectangle that contains the next block
    show_next_block()
    # score
    show_score(80, 50)
    # game over text
    game_over_text()
    # draw falling tetromino
    for n, colornumber in enumerate(falling_tetromino[yy]):
        if colornumber > 0:
            x = n % 4 * gap +250 + tetX * gap
            y = n // 4 * gap +100 + tetY * gap
            pygame.draw.rect(screen, (0, 0, 0), (x, y, gap, gap))
            pygame.draw.rect(screen, color[colornumber], (x+1, y+1, gap-2, gap-2))
    #draw field
    for n, colornumber in enumerate(grid):
        if colornumber > 0:
            x = n % column * gap +250
            y = n // column * gap +100
            pygame.draw.rect(screen, (0, 0, 0), (x, y, gap, gap))
            pygame.draw.rect(screen, color[colornumber], (x+1, y+1, gap-2, gap-2))

    # update screen

    pygame.display.update()

# close game

pygame.quit()
