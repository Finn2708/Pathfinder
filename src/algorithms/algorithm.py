from abc import ABC, abstractmethod
from src.data import DataGrid
from src.data import Cell


class Algorithm(ABC):
    """Abstract Base Class to implement strategy pattern for algorithms"""

    # Name of the algorithm (displayed in the frontend)
    name: str
    # Current state of the algorithm
    done: bool = False

    # Start and goal cells
    start: Cell
    goal: Cell

    def __init__(self, grid: DataGrid):
        # Get the start and goal cells from the grid
        sx, sy = grid.start_pos
        gx, gy = grid.goal_pos
        self.start = grid.cells[sx][sy]
        self.goal = grid.cells[gx][gy]

    @abstractmethod
    def run_algorithm(self, grid: DataGrid):
        pass

    @abstractmethod
    def show_path(self, grid):
        pass

    def is_done(self):
        """Return true if the algorithm is done"""
        return self.done
