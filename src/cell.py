from enum import Enum, unique
from dataclasses import dataclass, field
from typing import Tuple
from pygame import Rect
from src.style.colors import Colors


@unique
class CellValue(Enum):
    OPEN = 1
    CONSIDERED = 2
    CONSIDERING = 3
    PATH = 4
    START = 5
    GOAL = 6
    WALL = 7


@dataclass
class Cell:
    # General data
    x: int = field(repr=True, init=True)
    y: int = field(repr=True, init=True)
    pos: Tuple[int, int] = field(repr=False, init=False)
    value: CellValue = field(repr=True, init=False, default=CellValue.OPEN)
    start: bool = field(repr=True, init=False, default=False)
    goal: bool = field(repr=True, init=False, default=False)

    # Visualization
    size: int = field(repr=False, init=False, default=20)
    rect: Rect = field(repr=False, init=False, default=None)
    border: Rect = field(repr=False, init=False, default=None)
    fill_color: Tuple[int, int, int] = field(repr=False, init=False, default=Colors.OPEN)
    border_color: Tuple[int, int, int] = field(repr=False, init=False, default=Colors.GRID)

    def __post_init__(self):
        self.pos = self.x, self.y
        self.rect = Rect(self.x * self.size,
                         self.y * self.size,
                         self.size,
                         self.size)
        self.border = Rect(self.rect)
        self.neighbors = []

    def set_value(self, value: CellValue) -> bool:
        """Update the cells value (unless it's start/goal)"""
        if self.value is not CellValue.START and self.value is not CellValue.GOAL:
            self.value = value
            return True
        return False

    def update_color(self):
        """Update color according to current cell value"""
        if self.value == CellValue.OPEN:
            self.write_color_to_cell(Colors.OPEN, Colors.GRID)

        elif self.value == CellValue.CONSIDERED:
            self.write_color_to_cell(Colors.CONSIDERED, Colors.GRID)

        elif self.value == CellValue.CONSIDERING:
            self.write_color_to_cell(Colors.CONSIDERING, Colors.GRID)

        elif self.value == CellValue.PATH:
            self.write_color_to_cell(Colors.PATH)

        elif self.value == CellValue.START:
            self.write_color_to_cell(Colors.START)

        elif self.value == CellValue.GOAL:
            self.write_color_to_cell(Colors.GOAL)

        elif self.value == CellValue.WALL:
            self.write_color_to_cell(Colors.WALL)

    def write_color_to_cell(self, fill, border=None):
        """"""
        self.fill_color = fill
        self.border_color = fill if border is None else border

    def __lt__(self, other):
        return False
