"""
Created on 17.09.2020

@author: Lukas Rombach & Renan Uerpmann
"""

import pygame
import random
from pygame import mixer


# Functions


def show_score(screen, font, score_value, x, y):
    """ Function to display the player's score on the screen
        screen - the window, where the text is displayed on
        font - the font of the score text
        score_value - the amount of points the player achieved
        x - the x-position of the score on the screen
        y - the y-position of the score on the screen
    """
    
    screen.blit(font.render("Score : " + str(score_value), True, (0, 0, 0)), (x, y))


def show_time(screen, font, running_time, x, y):
    """ Function to display the time of the current game on the screen
        screen - the window, where the text is displayed on
        font - the font of the timer text
        running_time - the amount of time the game is running
        x - the x-position of the timer on the screen
        y - the y-position of the timer on the screen
    """
    # Calculate the amount of minutes off the running time
    minutes = str(running_time // 60000).zfill(2)
    # Calculate the amount of seconds off the running time
    seconds = str(int(running_time % 60000 // 1000)).zfill(2)
    screen.blit(font.render("Zeit : " + str(minutes) + ":" + str(seconds), True, (0, 0, 0)), (x, y))


def show_number_lines(screen, font, lines, x, y):
    """ Function to display the number of cleared lines by the player
        screen - the window, where the text is displayed on
        font - the font of the lines text
        lines - the amount of lines cleared by the player
        x - the x-Position of the text on the screen
        y - the y-Position of the text on the screen
    """
    
    screen.blit(font.render("Reihen: " + str(lines), True, (0, 0, 0)), (x, y))


def show_next_block(screen, font, gap):
    """ Function to display a rectangle field for the tetrominos forecast
        screen - the window, where the text is displayed on
        font - the font of the lines text
        gap - size of the block
    """
    pygame.draw.rect(screen, (0, 0, 0), (575, 100, gap * 4 + 10, gap * 4 + 10), 3)
    screen.blit(font.render("Next", True, (0, 0, 0)), (600, 60))


def game_over_text(screen, over_font):
    """ Function to display a 'Game over' message when the game is over
        screen - the window, where the text is displayed on
        over_font - the font of the 'Game over' message
    """
    
    screen.blit(over_font.render("Game over!", True, (0, 0, 0)), (270, 30))


def get_new_tetromino(all_tetrominos):
    """ Function to get random tetromino
        all_tetrominos - all tetrominos in a list
        return - returns random tetromino
    """
    
    random_tetrominos = random.choice(all_tetrominos)
    return random_tetrominos


def tetromino_on_grid(falling_tetromino, grids, column, tet_x, tet_y):
    """ Function to save the tetromino on the playfield
        falling-tetrominos - current tetromino
        grids - the playfield
        column - the number of columns on the playing field
        tet_x - the x-Position of the tetromino
        tet_y - the y-Position of the tetromino
    """
    
    for n, color_number in enumerate(falling_tetromino):
        if color_number > 0:
            # Calculate column position
            column_pos = tet_x + n % 4
            # Calculate row position
            row_pos = tet_y + n // 4
            # Calculates position for the playing field for the color number
            grids[row_pos * column + column_pos] = color_number


def validity(falling_tetromino, grids, tet_x, tet_y, row, column):
    """ Function to check the validity from the tetromino
        falling_tetromino -  current tetromino
        grids - the playfield
        tet_x - the x-Position of the tetromino
        tet_y - the y-Position of the tetromino
        row - the number of row on the playing field
        column - the number of columns on the playing field
        return - returns true or false
    """
    
    for n, color_number in enumerate(falling_tetromino):
        if color_number > 0:
            # Calculate column position
            column_pos = tet_x + n % 4
            # Calculate row position
            row_pos = tet_y + n // 4
            # Return false if not valid position
            if row_pos >= row or column_pos < 0 or column_pos >= column or grids[row_pos * column + column_pos] > 0:
                return False
    return True


def draw_struture(color, screen, struct, gaps, columns, off_x, off_y, tet_x, tet_y):
    """ Function to display tetromino, grid or forecast tetromino
        color - the tetromino color list
        screen - the window, where the text is displayed on
        struct - the tetromino, grid or forecast
        gaps - size of the block
        column - the number of columns on the playing field
        off_x - the x offset for the struct position
        off_y - the y offset for the struct position
        tet_x - the y-Position of the tetromino
        tet_y - the x-Position of the tetromino
    """

    for n, color_number in enumerate(struct):
        if color_number > 0:
            # Calculate x position
            x = n % columns * gaps + off_x + gaps * tet_x
            # Calculate y position
            y = n // columns * gaps + off_y + gaps * tet_y
            # Draws a black rectangle block
            pygame.draw.rect(screen, (0, 0, 0), (x, y, gaps, gaps))
            # Draws a smaller colorised rectangle block to see the border
            pygame.draw.rect(screen, color[color_number], (x + 1, y + 1, gaps - 2, gaps - 2))


def delete_line(grid, column):
    """ Function to delete and count the full row from the playing field
        grid - the playfield
        column - the number of columns on the playing field
        return - returns counted lines
    """
    # Block counter
    ig = 0
    # Line counter
    line = 0
    # Checks the complete playing field
    for n in range(200):
        # Calculates column position
        x = n % column
        # If a new line beginns sets block counter 0
        if x == 0:
            ig = 0
        # If a block found, increase block counter
        if grid[n] != 0:
            ig += 1
        # If a line is full, delete the line
        if ig == 10:
            # Delete line
            del grid[n - 9:n + 1]
            # Add new line filled with zeros
            for nl in range(column):
                grid.insert(0, 0)
            # Count line
            line += 1
    return line


def main():
    
    # Initialize pygame
    pygame.init()

    # Create a window of 800 width, 750 heigth
    screen = pygame.display.set_mode((800, 750))

    # Title and Icon
    # Set a caption for the game window
    pygame.display.set_caption("Tetris")
    # Load an icon for the game window
    icon = pygame.image.load("tetris.png")
    # Set the icon
    pygame.display.set_icon(icon)

    # Background Sound
    # Load the music file
    mixer.music.load("Tetris.mp3")
    # Set the music volume to 0.15
    mixer.music.set_volume(0.15)
    # Loop the music
    mixer.music.play(-1)

    # Font
    # Font for different screen texts
    font = pygame.font.SysFont("arial", 25)
    # Font for the 'Game over' message
    over_font = pygame.font.SysFont("arial", 50)

    # Declare and initialize all tetromino shape with all rotation
    i_tet = ((0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0),
             (0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0),
             (0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0),
             (0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0))

    o_tet = ((0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0),
             (0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0),
             (0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0),
             (0, 0, 0, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0))

    s_tet = ((0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0),
             (0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 0),
             (0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 0),
             (0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 0, 0))

    z_tet = ((0, 0, 0, 0, 6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0),
             (0, 0, 0, 0, 0, 0, 6, 0, 0, 6, 6, 0, 0, 6, 0, 0),
             (0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 0, 6, 6, 0),
             (0, 0, 0, 0, 0, 6, 0, 0, 6, 6, 0, 0, 6, 0, 0, 0))

    j_tet = ((0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0),
             (0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0),
             (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0),
             (0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0))

    l_tet = ((0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0),
             (0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0),
             (0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 3, 0, 0, 0),
             (0, 0, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0))

    t_tet = ((0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0),
             (0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 7, 0, 0, 7, 0, 0),
             (0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0),
             (0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 0, 0, 0, 7, 0, 0))

    all_tetromino = (i_tet, o_tet, s_tet, z_tet, j_tet, l_tet, t_tet)

    # Color

    deep_sky_blue = (0, 0, 205)
    medium_blue = (0, 191, 255)
    dark_orange = (255, 140, 0)
    yellow = (255, 255, 0)
    lawn_green = (124, 252, 0)
    red = (255, 0, 0)
    purple = (128, 0, 128)

    # Variable

    WIDTH, COLUMN, ROW = 300, 10, 20
    GAP = WIDTH // COLUMN
    HEIGHT = GAP * ROW
    COLOR = [(0, 0, 0), deep_sky_blue, medium_blue, dark_orange, yellow, lawn_green, red, purple]
    grid = [0] * 10 * 20
    rotation = 0
    tet_x = 3
    tet_y = 0
    speed = 900
    tetromino_down = pygame.USEREVENT + 1
    increase_speed = pygame.USEREVENT + 2
    pygame.time.set_timer(tetromino_down, speed)
    pygame.time.set_timer(increase_speed, 30000)
    pygame.key.set_repeat(1, 120)
    # Variable to hold the player's number of cleared lines
    number_of_lines = 0
    # Variable to hold the player's score
    score_value = 0

    # Get randrom tetromino
    next_tetromino = get_new_tetromino(all_tetromino)
    falling_tetromino = get_new_tetromino(all_tetromino)
    game_over_bool = False

    # Game-loop

    run = True
    # Get start time
    start_time = pygame.time.get_ticks()
    while run:
        if not game_over_bool:
            # if not game over, display time
            counting_time = pygame.time.get_ticks() - start_time
        # Loop through a list of any keyboard or mouse events

        for event in pygame.event.get():

            # Check for a QUIT event
            if event.type == pygame.QUIT:

                # End the game loop
                run = False

            if event.type == tetromino_down:
                # Check if valid
                if validity(falling_tetromino[rotation], grid, tet_x, tet_y + 1, ROW, COLUMN):
                    # Tetromino one down
                    tet_y += 1
                else:
                    # Check if game over
                    if not game_over_bool:
                        # Save current tetromino on playing field
                        tetromino_on_grid(falling_tetromino[rotation], grid, COLUMN, tet_x, tet_y)
                        # Put the Tetromino position on start
                        tet_x = 3
                        tet_y = 0
                        rotation = 0
                        # Assign next tetromino
                        falling_tetromino = next_tetromino
                        # Assign random tetromino
                        next_tetromino = get_new_tetromino(all_tetromino)
                        # Temp variable to calculate score
                        number_of_lines_tmp = 0
                        # Delete full lines
                        number_of_lines_tmp += delete_line(grid, COLUMN)
                        # Increase line counter
                        number_of_lines += number_of_lines_tmp
                        # Increase the player's score counter
                        score_value += (number_of_lines_tmp * number_of_lines_tmp) * 10

                        # If tetromino stuck on start position then is game over
                        if not validity(falling_tetromino[rotation], grid, tet_x, tet_y, ROW, COLUMN) and tet_x == 3 and tet_y == 0:
                            # Set game over
                            game_over_bool = True
                            # Stop game music
                            pygame.mixer.music.stop()
                            # Reset next tetromino
                            next_tetromino = falling_tetromino

            # Increase the game speed
            if event.type == increase_speed:
                if speed != 200:
                    speed -= 50
                pygame.time.set_timer(tetromino_down, speed)

            if event.type == pygame.KEYDOWN:

                # Press button up to rotate
                if event.key == pygame.K_UP and not game_over_bool:
                    if rotation >= 3:
                        rotation = 0
                        # If not valid then reset
                        if not validity(falling_tetromino[rotation], grid, tet_x, tet_y, ROW, COLUMN):
                            rotation = 3
                    else:
                        rotation += 1
                        # If not valid then reset
                        if not validity(falling_tetromino[rotation], grid, tet_x, tet_y, ROW, COLUMN):
                            rotation -= 1
                # Press button left to slide left
                if event.key == pygame.K_LEFT and not game_over_bool:
                    if validity(falling_tetromino[rotation], grid, tet_x - 1, tet_y, ROW, COLUMN):
                        tet_x -= 1
                # Press button right to slide right
                if event.key == pygame.K_RIGHT and not game_over_bool:
                    if validity(falling_tetromino[rotation], grid, tet_x + 1, tet_y, ROW, COLUMN):
                        tet_x += 1
                # Press button down to slide down
                if event.key == pygame.K_DOWN and not game_over_bool:
                    if validity(falling_tetromino[rotation], grid, tet_x, tet_y + 1, ROW, COLUMN):
                        tet_y += 1

                # Allows the player to mute/unmute the game music
                if event.key == pygame.K_m and not game_over_bool:
                    if mixer.music.get_volume() > 0:
                        mixer.music.set_volume(0)
                    else:
                        mixer.music.set_volume(0.15)

                # Start new game
                if event.key == pygame.K_n:
                    # Load the music file
                    mixer.music.load("Tetris.mp3")
                    # Set the music volume to 0.15
                    mixer.music.set_volume(0.15)
                    # Loop the music
                    mixer.music.play(-1)
                    # Reset playing field
                    grid = [0] * 10 * 20
                    # Reset number of lines
                    number_of_lines = 0
                    # Reset score value
                    score_value = 0
                    # Reset speed
                    speed = 900
                    pygame.time.set_timer(tetromino_down, speed)
                    # Reset start time
                    start_time = pygame.time.get_ticks()
                    # Put the Tetromino position on start
                    tet_x = 3
                    tet_y = 0
                    rotation = 0
                    # Assign next tetromino
                    falling_tetromino = next_tetromino
                    # Assign random tetromino
                    next_tetromino = get_new_tetromino(all_tetromino)
                    game_over_bool = False

                if event.key == pygame.K_ESCAPE:
                    # Quit game
                    pygame.quit()
                    quit()

        # Background color
        screen.fill((241, 241, 241))

        # Field
        pygame.draw.rect(screen, (0, 0, 0), (245, 95, WIDTH + 10, HEIGHT + 10), 3)

        # Show rectangle that contains the next block
        show_next_block(screen, font, GAP)

        # Display the score
        show_score(screen, font, score_value, 80, 50)

        # Game over text
        if game_over_bool:
            game_over_text(screen, over_font)

        # Forecast tetromino
        draw_struture(COLOR, screen, next_tetromino[0], GAP, 4, 580, 105, 0, 0)

        # Draw falling tetromino
        if not game_over_bool:
            draw_struture(COLOR, screen, falling_tetromino[rotation], GAP, 4, 250, 100, tet_x, tet_y)

        # Draw field
        draw_struture(COLOR, screen, grid, GAP, COLUMN, 250, 100, 0, 0)

        # Display the timer
        show_time(screen, font, counting_time, 80, 100)

        # Display the amount of cleared lines
        show_number_lines(screen, font, number_of_lines, 80, 150)

        # Update screen
        pygame.display.update()

    pygame.quit()


# close game
main()
