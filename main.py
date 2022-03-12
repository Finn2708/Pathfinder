from src.data import DataGrid
from src.interface import Interface
from src.algorithms.astar import AStar
from src.algorithms.dijkstra import Dijkstra
import pygame.time


if __name__ == '__main__':
    # Add additional algorithms to this list:
    algorithms = [Dijkstra, AStar]

    # Set up the data container
    data = DataGrid()
    # Start the user interface
    frontend = Interface(data)

    while not frontend.app_quit:
        # Let the user draw a labyrinth
        frontend.handle(data)

        # Space bar was pressed?
        if frontend.app_find_path:
            # Choose the algorithm from algorithms list
            Algorithm = frontend.choose_algorithm(algorithms)

            # Dynamically create the algorithm object and set up any requirements
            algo = Algorithm(data)
            # algo.setup(data)

            clock = pygame.time.Clock()
            while not algo.is_done() and not frontend.app_quit:
                algo.run_algorithm(data)
                frontend.handle(data)
                clock.tick(240)

            if algo.is_done():
                # Display the result
                frontend.handle(data)

            frontend.app_find_path = False
            frontend.reset_view(data)
            del algo
            del Algorithm


