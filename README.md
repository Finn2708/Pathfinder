# Pathfinder
Yet another 2D Visualization Tool for different path finding algorithms.

Inspired by [Pathfinding Visualizer by Clement Mihailescu](https://clementmihailescu.github.io/Pathfinding-Visualizer/)

## Algorithms:

Individual algorithms are derived from an abstract base class `Algorithm(ABC)` implementing a strategy pattern.

- [A*](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Dijkstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Breadth First Search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Depth First Search](https://en.wikipedia.org/wiki/Depth-first_search)
- [Greedy Best First Search](https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS)

![Alt Text](./media/demo.gif)


## Installation
The GUI uses ```pygame```. Install using pip:
```
pip install -r requirements.txt
```

## Usage
```
py main.py
```

## Controls

- ``Left Click`` - Draw walls

- ``Right-Click`` - Clear walls

- ``Middle-Click`` - Move start / goal

- ``Space`` - Start algorithm / Clear map

- ``r`` - Reset the entire map