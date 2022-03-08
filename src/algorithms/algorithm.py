from abc import ABC, abstractmethod
from src.data import DataGrid


class Algorithm(ABC):
    """Abstract Base Class to implement strategy pattern for algorithms"""
    done: bool

    @abstractmethod
    def setup(self, grid: DataGrid):
        pass

    @abstractmethod
    def run_algorithm(self, grid: DataGrid):
        pass

    @abstractmethod
    def show_path(self, grid):
        pass