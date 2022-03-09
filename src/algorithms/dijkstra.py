from src.algorithms.algorithm import Algorithm
from src.data import DataGrid
from src.cell import Cell, CellValue
from queue import PriorityQueue
from math import inf
from typing import Dict, Tuple, Optional


class Dijkstra(Algorithm):
    start: Cell
    goal: Cell

    dist: Dict[Tuple[int, int], float]
    prev: Dict[Tuple[int, int], Optional[Cell]]
    visited: Dict[Tuple[int, int], bool]

    q: PriorityQueue

    done: bool

    def setup(self, grid: DataGrid) -> None:
        sx, sy = grid.start_pos
        self.start = grid.cells[sx][sy]

        gx, gy = grid.goal_pos
        self.goal = grid.cells[gx][gy]

        self.done = False
        self.find_neighbors(grid)

        # Create a heap queue object
        self.q = PriorityQueue()

        # Set initial distances
        self.dist = {cell.pos: inf for row in grid.cells for cell in row}
        # Define the priority of the start cell and insert into queue
        self.dist[self.start.pos] = 0
        self.q.put((self.dist[self.start.pos], self.start.pos))

        # Save the path in here
        self.prev = {}

        self.visited = {cell.pos: False for row in grid.cells for cell in row}

    def run_algorithm(self, grid: DataGrid):
        # Get lowest
        x, y = self.q.get()[1]
        current = grid.cells[x][y]
        if current != self.start and current != self.goal:
            current.value = CellValue.CONSIDERED
        if not self.visited[current.pos]:
            self.visited[current.pos] = True
            if current == self.goal:
                self.done = True
                return True
            for neighbor in current.neighbors:
                if not self.visited[neighbor.pos]:
                    alt = self.dist[current.pos] + self.d(current.pos, neighbor.pos)
                    if alt < self.dist[neighbor.pos]:
                        self.dist[neighbor.pos] = alt
                        # self.prev[neighbor.pos] = current.pos
                        self.prev[neighbor.pos] = current
                        self.q.put((self.dist[current.pos], neighbor.pos))
                        if neighbor is not self.goal:
                            neighbor.value = CellValue.CONSIDERING
        if self.q.empty():
            self.done = True
            print("No path found")
            return False

    def show_path(self, grid):
        current = self.goal
        while current.pos in self.prev:
            current = self.prev[current.pos]
            if current is not self.start:
                current.value = CellValue.PATH

    @staticmethod
    def d(current, neighbor):
        """Return the weight of the edge from current to neighbor

        --- Not implemented at this point ---
        """
        return 1

    @staticmethod
    def find_neighbors(grid: DataGrid) -> None:
        """Identifies the non-blocked neighbors of every cell in the grid"""
        for col in grid.cells:
            for cell in col:
                # Check if the neighbor exists and is open
                cell.neighbors = []
                # Left
                if cell.x > grid.x_min and not grid.cells[cell.x - 1][cell.y].value == CellValue.WALL:
                    cell.neighbors.append(grid.cells[cell.x - 1][cell.y])
                # Right
                if cell.x < grid.x_max and not grid.cells[cell.x + 1][cell.y].value == CellValue.WALL:
                    cell.neighbors.append(grid.cells[cell.x + 1][cell.y])
                # Up
                if cell.y > grid.y_min and not grid.cells[cell.x][cell.y - 1].value == CellValue.WALL:
                    cell.neighbors.append(grid.cells[cell.x][cell.y - 1])
                # Down
                if cell.y < grid.y_max and not grid.cells[cell.x][cell.y + 1].value == CellValue.WALL:
                    cell.neighbors.append(grid.cells[cell.x][cell.y + 1])