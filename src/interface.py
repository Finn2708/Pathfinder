import pygame
from typing import List, Tuple, Type
from src.data import DataGrid
from src.cell import CellValue
from src.style.colors import Colors
from src.algorithms.algorithm import Algorithm


class Button:
    def __init__(self, name, x, y, algo, size=(200, 100), color=Colors.GRID, text_color=Colors.WALL):
        self.name = name
        self.x = x - (size[0] / 2)
        self.y = y - (size[1] / 2)
        self.algo = algo
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, size[0], size[1])
        self.text_color = text_color
        pygame.font.init()
        self.font = pygame.font.Font(None, 25)
        self.text = self.font.render(self.name, True, self.text_color)

    def render_text(self):
        self.text = self.font.render(self.name, True, self.text_color)

    def check_event(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return self.algo

    def update(self, surface: pygame.Surface):
        surface.fill(pygame.Color("black"), self.rect)
        surface.fill(self.color, self.rect.inflate(-4, -4))
        text_rect = self.text.get_rect(center=self.rect.center)
        surface.blit(self.text, text_rect)


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

    def handle(self, grid):
        """Process events and update the display"""
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
                    elif event.key == pygame.K_r:
                        grid.reset_all()
                # Process the mouse inputs
                self.handle_mouse_inputs(grid)
        self.draw_cells(grid)
        pygame.display.update()

    def draw_cells(self, grid):
        """Draw all the cells in the grid to the screen"""
        for col in grid.cells:
            for cell in col:
                cell.update_color()
                pygame.draw.rect(self.screen, cell.fill_color, cell.rect)
                pygame.draw.rect(self.screen, cell.border_color, cell.border, 1)

    def handle_mouse_inputs(self, grid: DataGrid):
        """Process mouse clicks"""
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

    def choose_algorithm(self, algorithms: List[Type[Algorithm]]) -> Type[Algorithm]:
        # TODO: Dynamically place buttons depending on the number of algorithms

        # Screen center
        center = self.screen.get_width() / 2, self.screen.get_height() / 2
        buttons = []
        for i, algo in enumerate(algorithms):
            buttons.append(Button(algo.name, center[0], center[1] + 200 - i*200, algo))

        chosen = None
        while not chosen:
            for event in pygame.event.get():
                for button in buttons:
                    ret = button.check_event(event)
                    if ret:
                        chosen = ret
            for button in buttons:
                button.update(self.screen)
            pygame.display.update()
        return chosen

    def wait_for_input(self):
        """Wait for user input [SPACE]"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app_quit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

    def reset_view(self, grid: DataGrid):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app_quit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        grid.reset()
                        return
                    elif event.key == pygame.K_r:
                        grid.reset_all()
                        return
