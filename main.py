# pylint: disable=E1101
# pylint: disable=W0621
# pylint: disable=E0401

import random
import pygame
import toml
from grid import Grid
from ant import Ant


def adjust_window_size(width: int, height: int, rows: int, cols: int) -> tuple:
    """
    Adjust the window size a little to accommodate whole rows and columns.
    """
    row_width = width // cols
    col_height = height // rows

    # Adjust window size to fit the grid
    width = cols * row_width
    height = rows * col_height

    return (width + 1, height + 1)


cfg = toml.load('config.toml')

ROW_COUNT = cfg['DISPLAY']['ROWS']
COL_COUNT = cfg['DISPLAY']['COLUMNS']
SCREEN_WIDTH, SCREEN_HEIGHT = adjust_window_size(
    cfg['DISPLAY']['WIDTH'], cfg['DISPLAY']['HEIGHT'], ROW_COUNT, COL_COUNT)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Langton's Ant")

grid = Grid(screen, ROW_COUNT, COL_COUNT, SCREEN_WIDTH, SCREEN_HEIGHT)
ant = Ant(5, 5, grid)
screen.fill((255, 255, 255))
grid.draw_grid(False)
ant.initialise_ant(COL_COUNT//2, ROW_COUNT//2)
pygame.display.flip()

# Main loop to keep the window open
RUNNING_STATUS = True

while RUNNING_STATUS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING_STATUS = False

    ant.move()

    #pygame.time.wait(500)
    pygame.display.update()

pygame.quit()
