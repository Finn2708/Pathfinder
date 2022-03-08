import pygame
from typing import Tuple, Type
from src.data import DataGrid
from src.cell import CellValue
from src.algorithms.algorithm import Algorithm
from src.algorithms.astar import AStar


class Interface:
    """Class to handle the user interface"""
    cell_size: int

    screen_width: int
    screen_height: int
    screen_size: Tuple[int, int]
    screen: pygame.Surface

    mouse_state: Tuple[bool, bool, bool]

    app_quit: bool
    app_find_path: bool
    app_chosen_algo: Type[Algorithm]

    def __init__(self, grid: DataGrid):
        self.cell_size = grid.cells[0][0].size

        self.screen_width = grid.cols * self.cell_size
        self.screen_height = grid.rows * self.cell_size
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.mouse_state = (False, False, False)

        self.app_quit = False
        self.app_find_path = False
        self.app_chosen_algo = AStar

    def handle(self, grid):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app_quit = True
                return
            if not self.app_find_path:
                # Allow inputs only while the algorithm is not running
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    # If a change in button state of the mouse is registered, update the buttons
                    self.mouse_state = pygame.mouse.get_pressed()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Press space to start the algorithm
                        self.app_find_path = True
                # Process the mouse inputs
                self.handle_mouse_inputs(grid)
        self.draw_cells(grid)

    def draw_cells(self, grid):
        """Draw all the cells in the grid to the screen"""
        for col in grid.cells:
            for cell in col:
                cell.update_color()
                pygame.draw.rect(self.screen, cell.fill_color, cell.rect)
                pygame.draw.rect(self.screen, cell.border_color, cell.border, 1)
        pygame.display.update()

    def handle_mouse_inputs(self, grid: DataGrid):
        for button, pressed in enumerate(self.mouse_state):
            if pressed:
                x, y = self.get_mouse_pos()
                cell = grid.cells[x][y]
                if button == 0:
                    # Left click draws walls
                    if not cell.start and not cell.goal:
                        cell.value = CellValue.WALL
                elif button == 1:
                    # Middle click to move start / goal
                    if cell.start:
                        grid.remove_start()
                    elif cell.goal:
                        grid.remove_goal()
                    else:
                        if not grid.pos_in_grid(grid.start_pos):
                            grid.set_start((x, y))
                        elif not grid.pos_in_grid(grid.goal_pos):
                            grid.set_goal((x, y))
                elif button == 2:
                    # Right click removes walls
                    if not cell.start and not cell.goal:
                        grid.cells[x][y].value = CellValue.OPEN

    def get_mouse_pos(self):
        """Return mouse position (in cell units)"""
        pos = pygame.mouse.get_pos()
        # Transform window pos to cell pos
        x, y = [coord // self.cell_size for coord in pos]
        return x, y

    @staticmethod
    def choose_algorithm() -> Type[Algorithm]:
        return AStar

    def wait_for_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app_quit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Press space to start the algorithm
                        return


    @staticmethod
    def reset_view(grid: DataGrid):
        for col in grid.cells:
            for cell in col:
                if not cell.start and not cell.goal:
                    cell.value = CellValue.OPEN