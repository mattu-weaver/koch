# pylint: disable=E1101
# pylint: disable=W0621
# pylint: disable=E0401
import math
import random
import pygame
import numpy as np
import toml
import time 
import sys

cfg = toml.load('config.toml')

WIDTH = cfg['DISPLAY']['WIDTH']
HEIGHT = cfg['DISPLAY']['HEIGHT']
BCOLOUR = cfg['DISPLAY']['BACKGROUND']
HIGH_FORE = cfg['DISPLAY']['HIGH_FORE']
LOW_FORE = cfg['DISPLAY']['LOW_FORE']
SIDES = cfg['FRACTAL']['SIDES']
HIGH_ITERATIONS = cfg['FRACTAL']['HIGH_ITERATIONS']
SIZE = cfg['FRACTAL']['SIZE']
DELAY = cfg['FRACTAL']['DELAY']
FONTSIZE = cfg['DISPLAY']['FONTSIZE']
RANDOMISE = cfg['FRACTAL']['RANDOM']

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coastal measurement")

last_click_time = 0
click_delay = 3.0

def draw_button(screen, msg, x, y, w, h, ic, ac, action=None):
    global last_click_time
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            current_time = time.time()
            if current_time - last_click_time > click_delay:
                action()
                last_click_time = current_time
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.Font("freesansbold.ttf", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


def reset_flag():
    global is_running
    is_running = True


def koch_snowflake_points(iterations, start, end, randomise=False):
    """
    Determine the position of the points on each 'side'.
    iterations: times each side is subdivided
    start: starting point of the side
    end: ending point of the side
    randomise: whether or not to randomise the snowflake shape
    """
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
            if randomise and random.choice([True, False]):
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


def distance_between_points(p1, p2):
    """
    Calculates the distance between two points.
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def reduce_polygon_resolution(points, x, y):
    """
    Reduces the resolution of a polygon by removing x points out of every y points.
    
    Parameters:
    points (list of tuples): The list of points representing the polygon.
    x (int): The number of points to remove.
    y (int): The interval of points to consider.
    
    Returns:
    list of tuples: The reduced list of points.
    """
    reduced_points = []
    count = 0

    for _, point in enumerate(points):
        if count < x:
            count += 1
        else:
            reduced_points.append(point)
            count = (count + 1) % y

    if reduced_points[0][0] != reduced_points[-1][0] or reduced_points[0][1] != reduced_points[-1][1]:
        reduced_points.append(reduced_points[0])

    return reduced_points

def draw_koch_snowflake(screen, points, pen, delay=DELAY):
    """
    Render the snowflake
    screen: the pygame screen
    points: the points of the snowflake
    delay: the delay between each segment being drawn
    """
    first = points[0]
    second = points[1]
    side_length = distance_between_points(first, second)

    total_sides = len(points) - 1
    perim = side_length * total_sides
    total_length = 0
    for i in range(total_sides):
        pygame.draw.line(screen, pen, points[i], points[i + 1], 2)
        pygame.display.flip()
        pygame.time.delay(delay)
        segment_length = distance_between_points(points[i], points[i + 1])
        total_length += segment_length
    return total_sides, side_length, perim

def update_progress(screen, high_sides, high_len, high_p, low_sides, low_len, low_p):
    """
    Displays the number of sides and perimeters of the high and low iteration shapes.
    screen: the pygame screen
    high_sides: the number of sides of the high iteration shape
    high_perimeter: the perimeter of the high iteration shape
    low_sides: the number of sides of the low iteration shape
    low_perimeter: the perimeter of the low iteration shape
    """
    font = pygame.font.SysFont('Arial', FONTSIZE)
    text_high_sides = font.render(f'High-res side count: {high_sides}', True, HIGH_FORE)
    text_high_len = font.render(f'High-res side length: {high_len:.2f}', True, HIGH_FORE)
    text_high_perim = font.render(f'High-res perimeter: {high_p:.2f}', True, HIGH_FORE)
    text_low_sides = font.render(f'Low-res sides count: {low_sides}', True, LOW_FORE)
    text_low_len = font.render(f'Low-res side length: {low_len:.2f}', True, LOW_FORE)
    text_low_perim = font.render(f'Low-res perimeter: {low_p:.2f}', True, LOW_FORE)
    screen.fill(BCOLOUR, (0, 0, 400, 100))
    screen.blit(text_high_sides, (10, 10))
    screen.blit(text_high_len, (10, 30))
    screen.blit(text_high_perim, (10, 50))
    screen.blit(text_low_sides, (10, 70))
    screen.blit(text_low_len, (10, 90))
    screen.blit(text_low_perim, (10, 110))

# Main drawing
screen.fill(BCOLOUR)

# Generate points for the highest number of iterations
def generate_points(width, height, size, sides, high_iterations, randomise):
    x, y = width // 4, height // 2
    initial_points = [
        (x, y - size / np.sqrt(3)),
        (x - size / 2, y + size / (2 * np.sqrt(3))),
        (x + size / 2, y + size / (2 * np.sqrt(3)))
    ]
    high_points = []
    for i in range(sides):
        start = initial_points[i]
        end = initial_points[(i + 1) % 3]
        segment_points = koch_snowflake_points(high_iterations, start, end, randomise=randomise)
        if i > 0:
            segment_points = segment_points[1:]  # Exclude the first point to avoid duplication
        high_points.extend(segment_points)
    return high_points


pygame.display.flip()

# Main loop to keep the window open
RUNNING = True
is_running = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    if is_running:
        screen.fill(BCOLOUR)
        high_points = generate_points(WIDTH, HEIGHT, SIZE, SIDES, HIGH_ITERATIONS, RANDOMISE)
        high_sides, high_length, high_perim = draw_koch_snowflake(screen, high_points, HIGH_FORE)
        low_points = reduce_polygon_resolution(high_points, 29, 30)
        low_points = [(x + WIDTH // 2, y) for (x, y) in low_points]
        low_sides, low_length, low_perim = draw_koch_snowflake(screen, low_points, LOW_FORE)
        update_progress(screen, high_sides, high_length, high_perim, low_sides, low_length, low_perim)
        is_running = False

    draw_button(screen, "Restart", 10, 730, 100, 50, (0, 255, 0), (0, 200, 0), reset_flag)
    pygame.display.update()

pygame.quit()
