from dataclasses import dataclass, field
from typing import List, Tuple
from src.cell import Cell, CellValue


@dataclass
class DataGrid:
    """Class for keeping track of individual cells"""
    cells: List[List[Cell]] = field(repr=False, init=False, default=None)

    rows: int = field(repr=True, init=True, default=30)
    cols: int = field(repr=True, init=True, default=30)

    x_min: int = field(repr=False, init=False, default=0)
    x_max: int = field(repr=False, init=False)

    y_min: int = field(repr=False, init=False, default=0)
    y_max: int = field(repr=False, init=False)

    start_pos: Tuple[int, int] = field(repr=True, init=False)
    goal_pos:  Tuple[int, int] = field(repr=True, init=False)

    def __post_init__(self) -> None:
        """This code is executed at the end of the automatically generated __init__"""
        # Create cells and assign them to the grid
        self.create_cells()

        # Set grid bounds
        self.x_max = self.cols - 1
        self.y_max = self.rows - 1

        # Set start and goal position
        self.start_pos = (2, 2)
        self.goal_pos = (self.cols - 3, self.rows - 3)
        self.set_start(self.start_pos)
        self.set_goal(self.goal_pos)

    def create_cells(self) -> None:
        """Create a data cell on the 2D grid for each square"""
        self.cells = []
        for col in range(self.cols):
            self.cells.append([])
            for row in range(self.rows):
                self.cells[col].append(Cell(col, row))

    def set_start(self, pos: (int, int)) -> bool:
        """Set start_pos if pos is in the grid"""
        if self.pos_in_grid(pos):
            self.start_pos = pos
            x, y = pos
            self.cells[x][y].value = CellValue.START
            self.cells[x][y].start = True
            return True
        return False

    def remove_start(self):
        x, y = self.start_pos
        self.cells[x][y].value = CellValue.OPEN
        self.cells[x][y].start = False
        self.start_pos = (-10, -10)

    def set_goal(self, pos: (int, int)) -> bool:
        """Set goal_pos if pos is in the grid"""
        if self.pos_in_grid(pos):
            self.goal_pos = pos
            x, y = pos
            self.cells[x][y].value = CellValue.GOAL
            self.cells[x][y].goal = True
            return True
        return False

    def remove_goal(self):
        x, y = self.goal_pos
        self.cells[x][y].value = CellValue.OPEN
        self.cells[x][y].goal = False
        self.goal_pos = (-10, -10)

    def pos_in_grid(self, coords: (int, int)) -> bool:
        """Return True if coords are in the grid"""
        x, y = coords
        if self.x_min <= x <= self.x_max:
            if self.y_min <= y <= self.y_max:
                return True
        return False

    def reset(self):
        """Reset open cells to initial state"""
        for col in self.cells:
            for cell in col:
                if not (cell.value == CellValue.WALL
                        or cell.value == CellValue.START
                        or cell.value == CellValue.GOAL):
                    cell.value = CellValue.OPEN

    def reset_all(self):
        """Reset all cells to initial state"""
        for col in self.cells:
            for cell in col:
                cell.value = CellValue.OPEN
        start_pos = (2, 2)
        goal_pos = (self.cols - 3, self.rows - 3)
        self.set_start(start_pos)
        self.set_goal(goal_pos)
