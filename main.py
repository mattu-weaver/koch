# pylint: disable=E1101
# pylint: disable=W0621
# pylint: disable=E0401
import random
import toml
import pygame
import numpy as np


cfg = toml.load('config.toml')
pygame.init()

WIDTH = cfg['DISPLAY']['WIDTH']
HEIGHT = cfg['DISPLAY']['HEIGHT']
FOREGROUND_COLOR = cfg['DISPLAY']['FOREGROUND']
BACKGROUND_COLOR = cfg['DISPLAY']['BACKGROUND']
DELAY = cfg['FRACTAL']['DELAY']
ITERATIONS = cfg['FRACTAL']['ITERATIONS']
SIDES = cfg['FRACTAL']['SIDES']
SIZE = cfg['FRACTAL']['SIZE']
FONTSIZE = cfg['DISPLAY']['FONTSIZE']
RANDOMISE = cfg['FRACTAL']['RANDOM']

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coastal measurement")

def koch_snowflake_points(iterations, start, end, randomize=False):
    points = np.array([start, end])
    root3 = np.sqrt(3)
    for _ in range(iterations):
        new_points = []
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x5, y5 = points[i + 1]
            dx = x5 - x1
            dy = y5 - y1
            x2 = x1 + dx / 3
            y2 = y1 + dy / 3
            if randomize and random.choice([True, False]):
                x3 = (x1 + x5) / 2 - root3 * (y1 - y5) / 6
                y3 = (y1 + y5) / 2 - root3 * (x5 - x1) / 6
            else:
                x3 = (x1 + x5) / 2 + root3 * (y1 - y5) / 6
                y3 = (y1 + y5) / 2 + root3 * (x5 - x1) / 6
            x4 = x1 + 2 * dx / 3
            y4 = y1 + 2 * dy / 3

            new_points.extend([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
        new_points.append(points[-1])
        points = np.array(new_points)
    return points

def draw_koch_snowflake(screen, center, iterations, size, delay=DELAY, randomize=False):
    x, y = center
    points = np.array([
        (x, y - size / np.sqrt(3)),
        (x - size / 2, y + size / (2 * np.sqrt(3))),
        (x + size / 2, y + size / (2 * np.sqrt(3)))
    ])
    total_sides = SIDES
    total_length = 0
    for i in range(SIDES):
        start = points[i]
        end = points[(i + 1) % 3]
        koch_points = koch_snowflake_points(iterations, start, end, randomize)
        for j in range(len(koch_points) - 1):
            pygame.draw.line(screen, FOREGROUND_COLOR, koch_points[j], koch_points[j + 1])
            pygame.display.flip()
            pygame.time.delay(delay)
            total_sides += 1
            segment_length = np.linalg.norm(koch_points[j+1] - koch_points[j])
            total_length += segment_length
            update_progress(screen, total_sides, total_length)

def update_progress(screen, total_sides, total_length):
    """
    Displays the number of sides that have been drawn and their total length.
    screen: the pygame screen
    total_sides: the total number of sides that have been drawn
    total_length: the total length of all sides that have been drawn
    """
    font = pygame.font.SysFont('Arial', FONTSIZE)
    text_sides = font.render(f'Total Sides: {total_sides}', True, FOREGROUND_COLOR)
    text_total_length = font.render(f'Total Length: {total_length:.2f}', True, FOREGROUND_COLOR)
    screen.fill(BACKGROUND_COLOR, (0, 0, 200, 100))
    screen.blit(text_sides, (10, 10))
    screen.blit(text_total_length, (10, 50))

# Main drawing
screen.fill(BACKGROUND_COLOR)
draw_koch_snowflake(screen, (WIDTH // 2, HEIGHT // 2), ITERATIONS, SIZE, randomize=RANDOMISE)
pygame.display.flip()

# Main loop to keep the window open
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

pygame.quit()
