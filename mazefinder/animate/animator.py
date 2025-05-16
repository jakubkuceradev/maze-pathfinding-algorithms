"""Modules useful for animating maze exploration."""

import os
from time import sleep
from dataclasses import dataclass, field
from mazefinder.problem import Grid


@dataclass
class Animator:
    """Class used for animating maze exploration."""

    seconds_per_frame: float
    simulation_speed: int = 100
    label: str = ""

    moves_per_frame: int = field(default=1, init=False)
    frame_counter: int = field(default=0, init=False)

    def draw(self, grid):
        """Draw to screen efficiently."""
        os.system("cls" if os.name == "nt" else "clear")
        full_grid = "\n".join("".join(cell.value for cell in row) for row in grid.data)
        print(f"{full_grid}\n{self.label}", flush=True)
        sleep(self.seconds_per_frame)

    def set_frame_interval(self, grid_height, grid_width):
        """Set the frame interval based on grid shape."""
        self.moves_per_frame = max(
            1,
            round(
                grid_height
                * grid_width
                * self.simulation_speed
                * self.seconds_per_frame
                / 60
            ),
        )

    def next_frame(self, grid: Grid):
        """Print the next frame to the terminal after delay."""
        self.frame_counter = (self.frame_counter + 1) % self.moves_per_frame
        if self.frame_counter == 0:
            self.draw(grid)

    def _clear_screen(self):
        """Clear the terminal screen, used for animating."""
        os.system("cls" if os.name == "nt" else "clear")
