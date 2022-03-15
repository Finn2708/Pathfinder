from src.algorithms.algorithm import Algorithm
from src.data import DataGrid
from src.cell import Cell, CellValue
from queue import Queue
from typing import List


class BreadthFirstSearch(Algorithm):
    name: str = "Breadth First Search"
    queue: Queue

    explored: List[Cell]

    def __init__(self, grid: DataGrid):
        """Set up the Breadth First Search algorithm"""
        super().__init__(grid)
        self.find_neighbors(grid)
        self.queue = Queue()
        self.explored = [self.start]
        self.queue.put(self.start)

        self.done = False

    def run_algorithm(self, grid: DataGrid) -> bool:
        """
        Breadth First Search (BFS) algorithm to find a path from start to goal

        Reference:
        https://en.wikipedia.org/wiki/Breadth-first_search
        """
        current = self.queue.get()
        current.set_value(CellValue.CONSIDERED)
        if current is self.goal:
            self.done = True
            self.show_path(grid)
            print("Path found")
            return True
        for neighbor in current.neighbors:
            if neighbor not in self.explored:
                self.explored.append(neighbor)
                self.queue.put(neighbor)
                neighbor.set_value(CellValue.CONSIDERING)

        if self.queue.empty():
            self.done = True
            print("No path found")
            return True

        return False

    def show_path(self, grid: DataGrid):
        """Mark the path"""
        current = self.goal
        while current is not self.start:
            if current is not self.start and current is not self.goal:
                current.value = CellValue.PATH
            # Find first appearance of neighbors in visited:
            for cell in self.explored:
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