'''
Created on 17.09.2020

@author: Lukas & Renan
'''

import pygame
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

mixer.music.load("Tetris.mp3")
mixer.music.set_volume(0.15)
mixer.music.play(-1)

# Font

score_value = 0
font = pygame.font.SysFont("arial", 25)

over_font = pygame.font.SysFont("arial", 50)

# Global variables
x1 = 0
x2 = 0
y1 = 0
y2 = 0
x11 = 393
x22 = 394
y11 = 125
y22 = 126

# Funktionen

def blocks(x1, y1, x2, y2): 
    pygame.draw.rect(screen, (0, 0, 0), (x1, y1, 15, 15), 2)
    pygame.draw.rect(screen, (240, 0, 0), (x2, y2, 14, 14))


def show_score(x, y):
    screen.blit(font.render("Score : " + str(score_value), True, (0, 0, 0)), (x, y))

    
def show_next_block():
    pygame.draw.rect(screen, (0, 0, 0), (575, 100, 100, 100), 3)

    screen.blit(font.render("Next", True, (0, 0, 0)), (600, 60))    

    
def game_over_text():
    screen.blit(over_font.render("Game over!", True, (0, 0, 0)), (270, 30))


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
        y11 += 5
        y22 += 5
        
    if keys[pygame.K_LEFT]:
        x11 -= 5
        x22 -= 5
    
    if keys[pygame.K_RIGHT]:
        x11 += 5
        x22 += 5        
    
    # Background color
    screen.fill((241, 241, 241))
    
    # field 
    pygame.draw.rect(screen, (0, 0, 0), (250, 100, 300, 600), 3)
    
    # show rectangle that contains the next block
    show_next_block()
    # score
    show_score(80, 50)
    # game over text
    game_over_text()
    
    # falling block
    blocks(x11, y11, x22, y22)

    # update screen

    pygame.display.update()

# close game

pygame.quit()
