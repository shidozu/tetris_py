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

# Function

def show_score(x, y):
    screen.blit(font.render("Score : " + str(score_value), True, (0, 0, 0)), (x, y))

    
def show_next_block():
    pygame.draw.rect(screen, (0, 0, 0), (575, 100, 100, 100), 3)

    screen.blit(font.render("Next", True, (0, 0, 0)), (600, 60))    

    
def game_over_text():
    screen.blit(over_font.render("Game over!", True, (0, 0, 0)), (270, 30))

def getNewTetromino():
    randomTetromino = random.choice(Tetromino)
    print(randomTetromino)
    return randomTetromino




# game-loop

run = True

while run:
    
    # pause for 100ms for more accuracy
    
    pygame.time.delay(100)
    
    # loop through a list of any keyboard or mouse events
    
    for event in pygame.event.get():
        
        # check for a QUIT event
        if event.type == pygame.QUIT:
            
            # End the game loop
            run = False
    
    keys = pygame.key.get_pressed()  # This will give us a dictonary where each key has a value of 1 or 0. Where 1 is pressed and 0 is not pressed.
    # make sure the character can not move off the screen 
    
    if keys[pygame.K_DOWN]:
        yy += 1
        
    if keys[pygame.K_LEFT]:
        x11 -= 5
        x22 -= 5
    
    if keys[pygame.K_RIGHT]:
        x11 += 5
        x22 += 5        
    
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



    # test
    fallingTetromino = getNewTetromino()

    for n, colornumber in enumerate(fallingTetromino[yy]):
        if colornumber > 0:
            x = n % 4 * gap +250
            y = n // 4 * gap +100
            pygame.draw.rect(screen, (0, 0, 0), (x, y, gap, gap))
            pygame.draw.rect(screen, color[colornumber], (x+1, y+1, gap-2, gap-2))



    # update screen

    pygame.display.update()

# close game

pygame.quit()
