from src.algorithms.algorithm import Algorithm
from src.data import DataGrid
from src.cell import Cell, CellValue
from queue import PriorityQueue
from math import inf
from typing import Dict, Tuple


class AStar(Algorithm):

    start: Cell
    goal: Cell

    open_set: PriorityQueue

    came_from: Dict[Tuple[int, int], Cell]

    g_score: Dict[Tuple[int, int], float]
    f_score: Dict[Tuple[int, int], float]

    count: int
    done: bool

    def setup(self, grid: DataGrid):
        sx, sy = grid.start_pos
        self.start = grid.cells[sx][sy]

        gx, gy = grid.goal_pos
        self.goal = grid.cells[gx][gy]

        self.open_set = PriorityQueue()

        self.find_neighbors(grid)

        # Set of discovered nodes
        self.count = 0
        self.open_set.put((0, self.count, self.start))  # prio, node
        self.open_set_iterable = [self.start]

        # List
        self.came_from = {}

        # Map with default values of inf
        self.g_score = {cell.pos: inf for row in grid.cells for cell in row}
        self.g_score[self.start.pos] = 0

        # Map with default values of inf
        self.f_score = {cell.pos: inf for row in grid.cells for cell in row}
        self.f_score[self.start.pos] = self.h(self.start, self.goal)

        self.done = False


    def run_algorithm(self, grid: DataGrid):
        """
        A* algorithm to find a path from start to goal

        Reference:
        https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
        """

        # Get node with lowest f score from heap queue
        current = self.open_set.get()[2]
        if current != self.start and current != self.goal:
            current.value = CellValue.CONSIDERED
        self.open_set_iterable.remove(current)

        if current == self.goal:
            print("Path found")
            self.done = True
            self.reconstruct_path(grid, current)
            return True

        for neighbor in current.neighbors:
            # Calc g score: cost of the path to current node
            tentative_g_score = self.g_score[current.pos] + self.d(current, neighbor)

            # If cost of the path to current is smaller than cost of the path to neighbor
            if tentative_g_score < self.g_score[neighbor.pos]:
                self.came_from[neighbor.pos] = current
                self.g_score[neighbor.pos] = tentative_g_score
                self.f_score[neighbor.pos] = tentative_g_score + self.h(neighbor, self.goal)
                if neighbor not in self.open_set_iterable:
                    self.count += 1
                    self.open_set.put((self.f_score[neighbor.pos], self.count, neighbor))
                    self.open_set_iterable.append(neighbor)
                    if neighbor is not self.goal:
                        neighbor.value = CellValue.CONSIDERING

        if self.open_set.empty():
            self.done = True
            print("No path found")
            return False

    @staticmethod
    def d(current, neighbor):
        """Return the weight of the edge from current to neighbor

        --- Not implemented at this point ---
        """
        return 1

    @staticmethod
    def h(n1, n2):
        """Return the Manhattan distance of two nodes"""
        return abs(n1.x - n2.x) + abs(n1.y - n2.y)

    def reconstruct_path(self, grid: DataGrid, current: Cell):
        """Mark the discovered cells as path"""
        while current.pos in self.came_from:
            current = self.came_from[current.pos]
            if current is not self.start:
                current.value = CellValue.PATH

    def show_path(self, grid):
        pass

    @staticmethod
    def find_neighbors(grid: DataGrid):
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