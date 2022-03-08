from src.data import DataGrid
from src.interface import Interface
from time import perf_counter, sleep


if __name__ == '__main__':
    data = DataGrid()
    frontend = Interface(data)

    while not frontend.app_quit:
        # Update data in generic data class
        frontend.handle(data)
        if frontend.app_find_path:
            # Choose algorithm
            Algorithm = frontend.choose_algorithm()
            algo = Algorithm()
            algo.setup(data)
            while not algo.done:
                start = perf_counter()
                algo.run_algorithm(data)
                frontend.handle(data)
                end = perf_counter()
                # Render at 60 FPS
                sleep(1 / 60 - end + start)
            frontend.wait_for_input()
            frontend.app_find_path = False
            frontend.reset_view(data)
            del algo
            del Algorithm


