"""
    This class is used to create the data within each scene.  The graphics
    builder is used to render the scene onto the GUI.

    Copyright [2020] [Daniel A. Jacobs]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Native Packages
from abc import ABC, abstractmethod  # Import Abstract Base Class
import random  # Random number generator
import time  # Time and Sleep Command
from enum import IntEnum  # Enumerated Types

# My Packages
from world_maker import graphics_builder as graphics


class SceneBuilder(ABC):
    def __init__(self, canvas, avatar, number_of_rows, number_of_cols, cell_size, creation_period):
        # Public
        self.number_of_rows = max(1, min(number_of_rows, 100))
        self.number_of_cols = max(1, min(number_of_cols, 100))

        self.scene_graphics = []
        self.cell_size = cell_size
        self.creation_period = creation_period
        self.is_rendered = False
        self.visited = []

        # Private
        self._canvas = canvas
        self._avatar = avatar

    @abstractmethod
    def build_scene(self):
        pass

    def render(self):
        # Initialize
        self.scene_graphics = [[graphics.MazeCell(self._canvas, row, col, self.cell_size) for col in range(self.number_of_cols)] for row in range(self.number_of_rows)]
        self._avatar.bring_to_top()
        time.sleep(min(1, self.creation_period / 100.0))

        for cell in self.visited:
            row = cell.row
            col = cell.col
            self.scene_graphics[row][col].update_from_data(self.scene_data[row][col])
            if self.creation_period > 0:
                time.sleep(self.creation_period / 1000.0)

        self.is_rendered = True

    def update_graphics(self, cell_size):
        # Update Graphics
        self.cell_size = cell_size
        if self.is_rendered:
            for row in range(0, self.number_of_rows):
                for col in range(0, self.number_of_cols):
                    self.scene_graphics[row][col].update_graphics(cell_size)


class MazeBuilder(SceneBuilder):
    def __init__(self, canvas, avatar, number_of_rows, number_of_cols, cell_size, creation_period):
        super().__init__(canvas, avatar, number_of_rows, number_of_cols, cell_size, creation_period)

        self.scene_data = []
        for row in range(0, self.number_of_rows):
            row_array = []
            for col in range(0, self.number_of_cols):
                row_array.append(SceneCell(row, col, True, ""))
            self.scene_data.append(row_array)

        self.start_cell = self.scene_data[0][0]
        self.goal_cell = self.scene_data[number_of_rows - 1][number_of_cols - 1]

    def build_scene(self):
        # Initialize
        cell_stack = []

        # Choose Random Cell
        current_cell = self.scene_data[random.randint(0, self.number_of_rows - 1)][
            random.randint(0, self.number_of_cols - 1)]
        self.visited.append(current_cell)
        # Set Neighbor List
        neighbors = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        # While all cells are not visited
        visited_cells = 1
        while visited_cells < self.number_of_rows * self.number_of_cols:
            # Clear stack
            neighbor_stack = []

            # Check all neighbors and add to stack if all walls are intact
            for pair in neighbors:
                if current_cell.row + pair[0] in range(0, self.number_of_rows) and current_cell.col + pair[1] in range(
                        0, self.number_of_cols):
                    test_cell = self.scene_data[current_cell.row + pair[0]][current_cell.col + pair[1]]
                    if test_cell.are_walls_intact():
                        neighbor_stack.append(test_cell)

            # if neighbors exist with full walls
            if len(neighbor_stack) > 0:
                # choose random
                action_cell = neighbor_stack[random.randint(0, len(neighbor_stack) - 1)]
                if action_cell.row == current_cell.row and action_cell.col == (current_cell.col + 1):
                    current_cell.set_wall_active(Orientation.EAST, False)
                    action_cell.set_wall_active(Orientation.WEST, False)
                elif action_cell.row == current_cell.row and action_cell.col == (current_cell.col - 1):
                    current_cell.set_wall_active(Orientation.WEST, False)
                    action_cell.set_wall_active(Orientation.EAST, False)
                elif action_cell.row == (current_cell.row - 1) and action_cell.col == current_cell.col:
                    current_cell.set_wall_active(Orientation.NORTH, False)
                    action_cell.set_wall_active(Orientation.SOUTH, False)
                elif action_cell.row == (current_cell.row + 1) and action_cell.col == current_cell.col:
                    current_cell.set_wall_active(Orientation.SOUTH, False)
                    action_cell.set_wall_active(Orientation.NORTH, False)

                # Push Current Cell and Make Action new Cell
                cell_stack.append(current_cell)
                self.visited.append(action_cell)
                current_cell = action_cell
                visited_cells += 1

            else:
                if cell_stack:
                    current_cell = cell_stack.pop()

        # Set Start and Goal Cell Color
        self.start_cell.set_floor_color("red")
        self.goal_cell.set_floor_color("green")


class KarelSceneBuilder(SceneBuilder):
    def __init__(self, canvas, avatar, cell_size, scene_string_data):
        # Parse File Splitting on NewLine
        file_lines = scene_string_data.split("\n")

        # Parse World First
        world_item = [line for line in file_lines if 'World' in line and '#' not in line]
        if len(world_item) == 1:
            tokens = world_item[0].split()
            number_of_rows = int(tokens[1])
            number_of_cols = int(tokens[2])
            super().__init__(canvas, avatar, number_of_rows, number_of_cols, cell_size, 0)
            self.scene_data = []
            for row in range(0, self.number_of_rows):
                row_array = []
                for col in range(0, self.number_of_cols):
                    next_cell = SceneCell(row, col, False, "")
                    if row == 0:
                        next_cell.set_wall_active(Orientation.NORTH, True)
                    if row == self.number_of_rows-1:
                        next_cell.set_wall_active(Orientation.SOUTH, True)
                    if col == 0:
                        next_cell.set_wall_active(Orientation.WEST, True)
                    if col == self.number_of_cols-1:
                        next_cell.set_wall_active(Orientation.EAST, True)

                    row_array.append(next_cell)
                self.scene_data.append(row_array)
        else:
            ValueError("The Karel World File Must have a Single Row with World #Rows #Cols")

        # Parse Avatar
        avatar_item = [line for line in file_lines if 'Robot' in line and '#' not in line]
        if len(avatar_item) == 1:
            tokens = avatar_item[0].split()
            starting_row = int(tokens[1])
            starting_col = int(tokens[2])
            starting_orientation_enum = int(tokens[3])
            starting_beepers = int(tokens[4])
        else:
            ValueError("The Karel World File Must have a Single Row with Robot StartRow StartCol OrientationNum "
                       "NumBeepers")

        # Parse Beepers
        # beeper_item = [line for line in file_lines if 'Robot' in line and '#' not in line]

        # Parse Walls
        for wall_line in file_lines:
            if 'Wall' in wall_line and '#' not in wall_line:
                tokens = wall_line.split()
                row = int(tokens[1])-1
                col = int(tokens[2])-1
                wall_enum = int(tokens[3])-1
                current_scene_cell = self.scene_data[row][col]
                orientation = Orientation(wall_enum)
                current_scene_cell.set_wall_active(Orientation(wall_enum), True)
                if orientation == Orientation.NORTH and row-1 in range(self.number_of_rows):
                    self.scene_data[row-1][col].set_wall_active(Orientation.SOUTH, True)
                if orientation == Orientation.EAST and col+1 in range(self.number_of_cols):
                    self.scene_data[row][col+1].set_wall_active(Orientation.WEST, True)
                if orientation == Orientation.SOUTH and row+1 in range(self.number_of_rows):
                    self.scene_data[row+1][col].set_wall_active(Orientation.NORTH, True)
                if orientation == Orientation.WEST and col-1 in range(self.number_of_cols):
                    self.scene_data[row][col-1].set_wall_active(Orientation.EAST, True)

    def build_scene(self):
        # Update Canvas with Size
        self.visited = [item for sub in self.scene_data for item in sub]


class SceneCell:
    def __init__(self, row, col, make_walls=True, fill_color=""):
        self.switch_wall = {
            Orientation.NORTH: "wall_north",
            Orientation.EAST: "wall_east",
            Orientation.SOUTH: "wall_south",
            Orientation.WEST: "wall_west",
        }
        self.row = row
        self.col = col

        if make_walls:
            self.wall_north = True
            self.wall_east = True
            self.wall_south = True
            self.wall_west = True
        else:
            self.wall_north = False
            self.wall_east = False
            self.wall_south = False
            self.wall_west = False

        self.fill_color = fill_color

    def set_wall_active(self, wall_orientation, is_wall_active):
        if isinstance(wall_orientation, Orientation):
            target_wall = self.switch_wall.get(wall_orientation)
            setattr(self, target_wall, is_wall_active)
        else:
            raise ValueError("Input wall_orientation must be instance of Orientation")

    def is_wall_active(self, wall_orientation):
        if isinstance(wall_orientation, Orientation):
            target_wall = self.switch_wall.get(wall_orientation)
            return getattr(self, target_wall)
        else:
            raise ValueError("Input wall_orientation must be instance of Orientation")

    def set_all_walls(self, is_wall_active):
        self.wall_north = is_wall_active
        self.wall_east = is_wall_active
        self.wall_south = is_wall_active
        self.wall_west = is_wall_active

    def set_floor_color(self, color_string):
        self.fill_color = color_string

    def are_walls_intact(self):
        return self.wall_north and self.wall_east and self.wall_south and self.wall_west


class Orientation(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def next_ccw(current):
        if isinstance(current, Orientation):
            next_value = (current.value + 3) % Orientation.__len__()
        else:
            raise ValueError("The input was not a valid Orientation")
        return Orientation(next_value)

    @staticmethod
    def next_cw(current):
        if isinstance(current, Orientation):
            next_value = (current.value + 1) % Orientation.__len__()
        else:
            raise ValueError("The input was not a valid Orientation")
        return Orientation(next_value)
