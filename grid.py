"""
An object representing a grid on the screen.
"""
import pygame

class Grid:
    """
    Constructor for the Grid class.
    """
    def __init__(self, screen: pygame.Surface,
                 row_count: int, col_count :int, scn_width: int, scn_height: int) -> None:

        self.screen = screen
        self.row_count = row_count
        self.col_count = col_count
        self.scn_width = scn_width
        self.scn_height = scn_height
        self.cell_width = scn_width // col_count
        self.cell_height = scn_height // row_count
        self.grid_col = (0, 0, 0)

    def draw_grid(self, visible=True):
        """
        Creates a grid on the pygame screen surface.
        """
        if visible:
            colour = (0, 0, 0)
        else:
            colour = (255, 255, 255)

        for row in range(self.row_count + 1):
            pygame.draw.line(self.screen, colour,
                             (0, row * self.cell_height), (self.scn_width, row * self.cell_height))
        for col in range(self.col_count + 1):
            pygame.draw.line(self.screen, colour,
                             (col * self.cell_width, 0), (col * self.cell_width, self.scn_height))

    def cell_fill(self, col: int, row: int, color: tuple) -> None:
        """
        Fills the inside of a specified cell with a specified color.
        
        :param col: Column number of the cell (0-indexed)
        :param row: Row number of the cell (0-indexed)
        :param color: Color to fill the cell (R, G, B)
        """
        # Calculate the top-left corner of the cell
        x = col * self.cell_width
        y = row * self.cell_height
        
        # Calculate the width and height of the cell excluding the border
        width = self.cell_width - 1
        height = self.cell_height - 1
        
        # Draw the filled rectangle
        pygame.draw.rect(self.screen, color, (x + 1, y + 1, width, height))

    def get_colour(self, col: int, row: int) -> str:
        """
        Returns the color of the specified cell.
        
        :param col: Column number of the cell (0-indexed)
        :param row: Row number of the cell (0-indexed)
        :return: Color of the cell (R, G, B, A)
        """
        # Calculate the top-left corner of the cell
        x = col * self.cell_width
        y = row * self.cell_height

        # Get the color of the pixel at the top-left corner of the cell
        colour = self.screen.get_at((x + 1, y + 1))

        if colour == (255, 255, 255, 255):  # White
            return 'white'
        elif colour == (0, 0, 0, 255):  # Black
            return 'black'
        else:  # Default to red for any other color
            return 'red'
