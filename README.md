# Maze Pathfinding Algorithms in Python

This project implements various classic search and pathfinding algorithms to solve mazes defined in simple text files, including specified start and end coordinates. It provides a console-based visualization to show the search process and the final found path.

## Features

*   Load mazes from `.txt` files with grid and coordinate specifications.
*   Implement a variety of popular pathfinding algorithms.
*   Show the search process step-by-step (nodes visited) using console visualization.
*   Highlight the final path found (if any) in the console output.
*   Compare different algorithms and their variants.

## Implemented Algorithms

The project includes the following algorithms, with different variants where applicable:

*   **Dijkstra's Algorithm**
*   **A\*** Search:
    *   Manhattan Heuristic
    *   Euclidean Heuristic
    *   Overweight Manhattan Heuristic
    *   Overweight Euclidean Heuristic
*   **Greedy Best-First Search:**
    *   Manhattan Heuristic
    *   Euclidean Heuristic
*   **Breadth-First Search (BFS)**
*   **Depth-First Search (DFS):**
    *   Stack-based Iterator Implementation
    *   Stack-based Naive Implementation
    *   Recursive Implementation
*   **Random Search**

## Getting Started

To set up and run the project (ensure you have Python (3.6+) installed):
.

1.  **Clone the repository:**
    ```bash
    git clone [Repository URL]
    cd [Repository Directory]
    ```
2.  **Run:** Start the `main.py` script and select game settings in a terminal interface. Be prepared to adjust terminal size according to the selected maze.

### Maze File Format

Mazes are defined in simple text files with two main parts: a rectangular grid and start/end point coordinates.

*   **Grid:** Represented by characters:
    *   `X`: Wall (obstacle)
    *   ` `: Open path (traversable space)
*   **Coordinates:** Two separate lines specifying the start and end points:
    *   `start C, R`
    *   `end C, R`
    Where `C` is the column number and `R` is the row number.


Example maze files following this format are included in the `mazes/` directory.

## Demonstration



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.****