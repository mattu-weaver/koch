# pylint: disable=E1101
# pylint: disable=W0621
# pylint: disable=E0401
import pygame
import numpy as np
import random
import toml

cfg = toml.load('config.toml')

WIDTH = cfg['DISPLAY']['WIDTH']
HEIGHT = cfg['DISPLAY']['HEIGHT']
BACKGROUND_COLOR = cfg['DISPLAY']['BACKGROUND']
FOREGROUND_COLOR = cfg['DISPLAY']['FOREGROUND']
SIDES = cfg['FRACTAL']['SIDES']
HIGH_ITERATIONS = cfg['FRACTAL']['HIGH_ITERATIONS']
LOW_ITERATIONS = cfg['FRACTAL']['LOW_ITERATIONS']
SIZE = cfg['FRACTAL']['SIZE']
DELAY = cfg['FRACTAL']['DELAY']
FONTSIZE = cfg['DISPLAY']['FONTSIZE']
RANDOMISE = cfg['FRACTAL']['RANDOM']
RANDOMNESS_FACTOR = cfg['FRACTAL']['RANDOM_FACTOR']

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coastal measurement")

def koch_snowflake_points(iterations, start, end, randomise=False, randomness_factor=0.1):
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
            
            # Apply randomness
            if randomise:
                x2 += randomness_factor * (random.random() - 0.5) * dx
                y2 += randomness_factor * (random.random() - 0.5) * dy
                x3 += randomness_factor * (random.random() - 0.5) * dx
                y3 += randomness_factor * (random.random() - 0.5) * dy
                x4 += randomness_factor * (random.random() - 0.5) * dx
                y4 += randomness_factor * (random.random() - 0.5) * dy

            new_points.extend([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
        new_points.append(points[-1])
        points = np.array(new_points)
    return points

def draw_koch_snowflake(screen, points, delay=DELAY):
    """
    Render the snowflake
    screen: the pygame screen
    points: the points of the snowflake
    delay: the delay between each segment being drawn
    """
    total_sides = len(points) - 1
    total_length = 0
    for i in range(total_sides):
        pygame.draw.line(screen, FOREGROUND_COLOR, points[i], points[i + 1])
        pygame.display.flip()
        pygame.time.delay(delay)
        segment_length = np.linalg.norm(np.array(points[i + 1]) - np.array(points[i]))
        total_length += segment_length
    return total_sides, total_length

def update_progress(screen, high_sides, high_perimeter, low_sides, low_perimeter):
    """
    Displays the number of sides and perimeters of the high and low iteration shapes.
    screen: the pygame screen
    high_sides: the number of sides of the high iteration shape
    high_perimeter: the perimeter of the high iteration shape
    low_sides: the number of sides of the low iteration shape
    low_perimeter: the perimeter of the low iteration shape
    """
    font = pygame.font.SysFont('Arial', FONTSIZE)
    text_high_sides = font.render(f'High Iterations Sides: {high_sides}', True, FOREGROUND_COLOR)
    text_high_perimeter = font.render(f'High Iterations Perimeter: {high_perimeter:.2f}', True, FOREGROUND_COLOR)
    text_low_sides = font.render(f'Low Iterations Sides: {low_sides}', True, FOREGROUND_COLOR)
    text_low_perimeter = font.render(f'Low Iterations Perimeter: {low_perimeter:.2f}', True, FOREGROUND_COLOR)
    screen.fill(BACKGROUND_COLOR, (0, 0, 400, 100))
    screen.blit(text_high_sides, (10, 10))
    screen.blit(text_high_perimeter, (10, 30))
    screen.blit(text_low_sides, (10, 50))
    screen.blit(text_low_perimeter, (10, 70))

# Main drawing
screen.fill(BACKGROUND_COLOR)

# Generate points for the highest number of iterations
x, y = WIDTH // 4, HEIGHT // 2
initial_points = [
    (x, y - SIZE / np.sqrt(3)),
    (x - SIZE / 2, y + SIZE / (2 * np.sqrt(3))),
    (x + SIZE / 2, y + SIZE / (2 * np.sqrt(3)))
]
high_points = []
for i in range(SIDES):
    start = initial_points[i]
    end = initial_points[(i + 1) % 3]
    high_points.extend(koch_snowflake_points(HIGH_ITERATIONS, start, end, randomise=RANDOMISE, randomness_factor=RANDOMNESS_FACTOR))

# Draw the high iteration shape
high_sides, high_perimeter = draw_koch_snowflake(screen, high_points)

# Selectively draw fewer points for the low iteration shape
low_points = []
step = 4 ** (HIGH_ITERATIONS - LOW_ITERATIONS)
for i in range(0, len(high_points), step):
    low_points.append(high_points[i])
low_points.append(high_points[-1])  # Ensure the last point is included

# Adjust the low points to be drawn on the right side
low_points = [(x + WIDTH // 2, y) for (x, y) in low_points]

# Draw the low iteration shape
low_sides, low_perimeter = draw_koch_snowflake(screen, low_points)

# Update the progress display
update_progress(screen, high_sides, high_perimeter, low_sides, low_perimeter)
pygame.display.flip()

# Main loop to keep the window open
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

pygame.quit()