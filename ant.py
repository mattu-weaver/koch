"""
An object representing a Langton any on the screen.
"""
import random

class Ant:
    """
    Represents a Langton ant.
    """
    ANT_COLOUR = (255, 0, 0)

    def __init__(self, col, row, grid) -> None:
        self.row = row
        self.col = col
        self.grid = grid
        self.cell_colour = None
        self.direction = None
        self.cell_rgb = None

    def move(self) -> None:
        """
        Draws an ant on the screen.
        """
        # flip the colour of the current cell
        if self.cell_colour == 'white':
            self.grid.cell_fill(self.col, self.row, (0, 0, 0))
            self.cell_colour = 'black'
        else:
            self.grid.cell_fill(self.col, self.row, (255, 255, 255))
            self.cell_colour = 'white'
   
        # Set the destination cell
        if self.direction == 'up':
            if self.row == 0:
                self.row = self.grid.row_count - 2

            self.row = max(min(self.row - 1, self.grid.row_count - 2), 2)
        elif self.direction == 'down':
            self.row = max(min(self.row + 1, self.grid.row_count - 2), 2)
        elif self.direction == 'left':
            self.col = max(min(self.col - 1, self.grid.col_count - 2), 2)
        else:
            self.col = max(min(self.col + 1, self.grid.col_count - 2), 2)

        # Get the colour of the destination cell
        self.cell_colour = self.grid.get_colour(self.col, self.row)

        # Move the ant
        self.grid.cell_fill(self.col, self.row, self.ANT_COLOUR)


        # Update the ant's direction
        self.set_direction()
        


    def set_direction(self):
        """
        Updates the direction of the ant based on the color of the cell.
        """
        if self.cell_colour == 'white':
            if self.direction == 'up':
                self.direction = 'right'
            elif self.direction == 'right':
                self.direction = 'down'
            elif self.direction == 'down':
                self.direction = 'left'
            else:
                self.direction = 'up'
        else:
            if self.direction == 'up':
                self.direction = 'left'
            elif self.direction == 'left':
                self.direction = 'down'
            elif self.direction == 'down':
                self.direction = 'right'
            else:
                self.direction = 'up'


    def initialise_ant(self, col=None, row=None) -> None:
        """
        Initializes the ant at a random position on the grid.
        """
        self.col = col
        self.row = row

        # Set a random direction
        self.direction = random.choice(['up', 'down', 'left', 'right'])

        if col is None:
            self.col = random.randint(0, self.grid.col_count - 1)

        if row is None:
            self.row = random.randint(0, self.grid.row_count - 1)

        # get the cell colour before placing the ant
        self.cell_colour = self.grid.get_colour(self.col, self.row)
       #self.draw_ant(self.col, self.row)
