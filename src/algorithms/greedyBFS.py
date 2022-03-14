from src.algorithms.algorithm import Algorithm
from src.data import DataGrid
from src.cell import Cell, CellValue
from queue import PriorityQueue
from typing import List


class GreedyBFS(Algorithm):
    name: str = "Greedy BFS"
    queue: PriorityQueue

    visited: List[Cell]

    def __init__(self, grid: DataGrid):
        """Set up the Greedy Best First Search algorithm"""
        super().__init__(grid)

        self.find_neighbors(grid)

        self.done = False

        self.visited = []

        self.queue = PriorityQueue()
        self.queue.put((self.h(self.start, self.goal), self.start))

    def run_algorithm(self, grid: DataGrid):
        """
        Greedy Best First Search (BFS) algorithm to find a path from start to goal

        Reference:
        https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS
        """
        _, current = self.queue.get()

        if current not in self.visited:
            self.visited.append(current)
            if current == self.goal:
                self.done = True
                self.show_path(grid)
                print("Path found")
                return True
            for neighbor in current.neighbors:
                # Queue any new neighbors according to their score
                if neighbor not in self.visited:
                    neighbor.set_value(CellValue.CONSIDERING)
                    self.queue.put((self.h(neighbor, self.goal), neighbor))
            current.set_value(CellValue.CONSIDERED)

        if self.queue.empty():
            self.done = True
            print("No path found")

    @staticmethod
    def d(current, neighbor):
        """Return the weight of the edge from current to neighbor

        --- Not implemented at this point ---
        """
        return 1

    @staticmethod
    def h(n1: Cell, n2: Cell):
        """Return the Manhattan distance of two nodes"""
        return abs(n1.x - n2.x) + abs(n1.y - n2.y)

    def show_path(self, grid: DataGrid):
        """Mark the path"""
        current = self.goal
        while current is not self.start:
            if current is not self.start and current is not self.goal:
                current.value = CellValue.PATH
            # Find first appearance of neighbors in visited:
            for cell in self.visited:
                if cell in current.neighbors:
                    current = cell
                    break

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