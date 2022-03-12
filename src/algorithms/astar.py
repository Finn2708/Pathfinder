from src.algorithms.algorithm import Algorithm
from src.data import DataGrid
from src.cell import Cell, CellValue
from queue import PriorityQueue
from math import inf
from typing import List, Dict, Tuple


class AStar(Algorithm):
    name: str = "A*"
    open_set: PriorityQueue
    open_set_iterable: List[Cell]

    came_from: Dict[Tuple[int, int], Cell]

    g_score: Dict[Tuple[int, int], float]
    f_score: Dict[Tuple[int, int], float]

    count: int = 0

    def __init__(self, grid: DataGrid):
        """Set up the A* algorithm"""
        super().__init__(grid)

        # Build the graph
        self.find_neighbors(grid)

        # G scores state the cost of the path from start to a node on the graph.
        # Start with infinite cost to all nodes since none are explored yet...
        self.g_score = {cell.pos: inf for row in grid.cells for cell in row}
        # ...except for the start node:
        self.g_score[self.start.pos] = 0

        # F scores state how attractive a path from a node to its neighbor is.
        # f(n) = g(n) + h(n)
        # Initialize to inf as none have been evaluated yet...
        self.f_score = {cell.pos: inf for row in grid.cells for cell in row}
        # ...except for the start node:
        self.f_score[self.start.pos] = self.g_score[self.start.pos] + self.h(self.start, self.goal)

        # Create the heap queue
        self.open_set = PriorityQueue()
        # Count is a tie-breaker in case cells put to the queue have equal cost
        # self.count = 0
        # Data is inserted into the queue as a tuple: (f_score, count, cell)
        self.open_set.put((self.f_score[self.start.pos], self.count, self.start))
        # Create a helper list that stores the same cells as the heap queue
        # This is required because we can't loop over the elements of a heap queue
        self.open_set_iterable = [self.start]

        # Dict of the path
        self.came_from = {}

    def run_algorithm(self, grid: DataGrid):
        """
        A* algorithm to find a path from start to goal

        Reference:
        https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
        """

        # Get the node with lowest f score from the heap queue and update the helper list accordingly
        current = self.open_set.get()[2]
        self.open_set_iterable.remove(current)

        # Mark the current cell as considered, so we can show it in the frontend
        if current != self.start and current != self.goal:
            current.value = CellValue.CONSIDERED

        # Check if we are done
        if current == self.goal:
            print("Path found")
            self.done = True
            # Mark the cells of the successful path
            self.show_path(grid)
            return True

        for neighbor in current.neighbors:
            # Calculate G score of the neighbor when coming from the current node
            tentative_g_score = self.g_score[current.pos] + self.d(current, neighbor)

            # If G score to neighbor (when coming from current node) is smaller than the currently stored G score:
            if tentative_g_score < self.g_score[neighbor.pos]:
                # Update the path and scores
                self.came_from[neighbor.pos] = current
                self.g_score[neighbor.pos] = tentative_g_score
                self.f_score[neighbor.pos] = tentative_g_score + self.h(neighbor, self.goal)
                # If the neighbor isn't currently in the helper list, it's also not in the heap queue
                if neighbor not in self.open_set_iterable:
                    # So we add it to consider it in a future iteration
                    self.count += 1
                    self.open_set.put((self.f_score[neighbor.pos], self.count, neighbor))
                    self.open_set_iterable.append(neighbor)
                    if neighbor is not self.goal:
                        # And mark it's current state for the frontend
                        neighbor.value = CellValue.CONSIDERING

        # If there aren't any more nodes on the heap queue, we were unsuccessful in finding a path
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

    def show_path(self, grid):
        """Mark the discovered cells as path"""
        current = self.goal
        while current.pos in self.came_from:
            current = self.came_from[current.pos]
            if current is not self.start:
                current.value = CellValue.PATH

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