"""Module necessary for CLI functionality."""

from pathlib import Path
import sys
from typing import Callable
from mazefinder.search import (
    bfs,
    iterator_dfs,
    stack_dfs,
    recursive_dfs,
    dijkstra,
    greedy_manhattan,
    greedy_euclidean,
    a_star_manhattan,
    a_star_euclidean,
    a_star_overweight_manhattan,
    a_star_overweight_euclidean,
    random_search,
)
from mazefinder.animate import Animator
from mazefinder.problem import load_problem


A_STAR_ALGORITHMS = {
    "1": ("A* (Manhattan)", a_star_manhattan),
    "2": ("A* (Euclidean)", a_star_euclidean),
    "3": ("A* (Overweight Manhattan)", a_star_overweight_manhattan),
    "4": ("A* (Overweight Euclidean)", a_star_overweight_euclidean),
}

GREEDY_ALGORITHMS = {
    "1": ("Greedy (Manhattan)", greedy_manhattan),
    "2": ("Greedy (Euclidean)", greedy_euclidean),
}

DFS_ALGORITHMS = {
    "1": ("Stack-based iterator DFS", iterator_dfs),
    "2": ("Stack-based naive DFS", stack_dfs),
    "3": ("Recursive DFS", recursive_dfs),
}

SEARCH_ALGORITHMS = {
    "1": ("A*", A_STAR_ALGORITHMS),
    "2": ("Greedy", GREEDY_ALGORITHMS),
    "3": ("DFS", DFS_ALGORITHMS),
    "4": ("BFS", bfs),
    "5": ("Dijkstra", dijkstra),
    "6": ("Random", random_search),
}

def compress_path(path: list) -> list:
    "Cut the middle of path thats too long."
    if len(path) > 10:
        return path[:5] + ["..."] + path[-6:]
    return path


def solve_maze(file_path: str, search_strategy: Callable, animator: Animator):
    """Solve a maze from file."""
    problem = load_problem(file_path)
    animator.set_frame_interval(len(problem.grid.data), len(problem.grid.data[0]))
    animator.draw(problem.grid)
    path, cells_visited = search_strategy(problem, animator)
    if path:
        animator.draw(problem.grid)
    return path, cells_visited


def get_map_files(folder_paths):
    """Scan multiple folders for .txt files"""
    all_files = []
    for folder in folder_paths:
        folder_path = Path(folder)
        folder_path.mkdir(exist_ok=True)
        files = list(folder_path.glob("*.txt"))
        all_files.extend(files)
    return all_files


def display_menu(options, title):
    """Display a numbered menu and return user's choice"""
    print(f"\n{title}:")
    for key, value in options.items():
        print(f"{key}. {value[0]}")
    while True:
        choice = input("Enter your choice (number): ").strip()
        if choice in options:
            return choice
        print("Invalid choice. Please try again.")


MAP_FOLDERS = ("mazes", )
SECONDS_PER_FRAME_DEFAULT = 0.1
SIMULATION_SPEED_DEFAULT = 10


def main():
    """Run the CLI application."""

    map_files = get_map_files(MAP_FOLDERS)
    if not map_files:
        print(f"No map files found in {MAP_FOLDERS} directories.")
        print("Please add some .txt files with graph edges (format: 'v w' per line)")
        sys.exit(1)

    map_options = {
        str(i + 1): (f"{f.parent.name}/{f.name}", f) for i, f in enumerate(map_files)
    }

    while True:
        print("\n=== Graph Search CLI ===")

        # Map selection
        map_choice = display_menu(map_options, "Select a map")
        map_name, map_path = map_options[map_choice]
        print(f"Selected map: {map_name}")

        # Algorithm selection
        algorithm_choice = display_menu(SEARCH_ALGORITHMS, "Select a search algorithm")
        algorithm_name, algorithm_options = SEARCH_ALGORITHMS[algorithm_choice]
        print(f"Selected algorithm: {algorithm_name}")

        if isinstance(algorithm_options, dict):
            # Variant selection
            variant_choice = display_menu(
                algorithm_options, "Select a search algorithm variant"
            )
            variant_name, variant_func = algorithm_options[variant_choice]
            print(f"Selected variant: {variant_name}")
        else:
            variant_name, variant_func = algorithm_name, algorithm_options

        seconds_per_frame = input(
            f"Set seconds per animated frame (default {SECONDS_PER_FRAME_DEFAULT}): "
        ).strip()
        seconds_per_frame = (
            float(seconds_per_frame)
            if seconds_per_frame
            else float(SECONDS_PER_FRAME_DEFAULT)
        )

        simulation_speed = input(
            f"Set simulation speed (default {SIMULATION_SPEED_DEFAULT}): "
        ).strip()
        simulation_speed = (
            float(simulation_speed)
            if simulation_speed
            else float(SIMULATION_SPEED_DEFAULT)
        )

        path, nodes_visited = solve_maze(
            map_path,
            variant_func,
            Animator(
                seconds_per_frame,
                simulation_speed,
                f"{map_name}: {variant_name}",
            ),
        )

        print(f"Nodes visited: {nodes_visited}")
        if path:
            print(
                f"Path length: {len(path)}\nPath: {" -> ".join((str(position) for position in compress_path(path)))}"
            )

        if input("\nRun again? (y/n): ").lower() != "y":
            break


main()
