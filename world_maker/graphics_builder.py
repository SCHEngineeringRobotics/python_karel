"""
    This module is for creating the avatar and other visualization elements
    for a tkinter Canvas object

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
from math import sin, cos, pi, floor
from world_maker.scene_builder import Orientation


class MazeAvatar:
    def __init__(self, canvas, row, col, cell_size, color):
        # Private
        self.__canvas = canvas
        self._row = row
        self._col = col
        self.cell_size = cell_size
        self.border_size = self.cell_size / 2.0
        self.padding_size = self.cell_size / 10
        self.diameter = self.cell_size - 2 * self.padding_size
        self.__x = self.border_size + self._col * self.cell_size
        self.__y = self.border_size + self._row * self.cell_size
        # Private Graphics
        self.__circle_id = self.__canvas.create_oval(self.__x, self.__y,
                                                     self.__x + self.diameter, self.__y + self.diameter,
                                                     fill=color, outline="", tag="avatar")
        self.__poly_id = self.__canvas.create_polygon(self.__x + 0.75 * self.diameter, self.__y + 0.5 * self.cell_size,
                                                      self.__x + 0.25 * self.diameter,
                                                      self.__y + 0.25 * self.diameter,
                                                      self.__x + 0.25 * self.diameter,
                                                      self.__y + 0.75 * self.diameter,
                                                      fill="black", tag="avatar arrow")
        # Properties
        self._fill = color
        self._orientation = Orientation.EAST

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, color):
        self.__canvas.itemconfig(self.__circle_id, fill=color)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if isinstance(value, Orientation):
            self._orientation = value

    @property
    def position(self):
        return self._row, self._col

    def rotate(self, angle_radian):
        for object_id in self.__canvas.find_withtag("arrow"):
            coordinates = self.__canvas.coords(object_id)
            new_coordinates = []
            for a, b in zip(coordinates[0::2], coordinates[1::2]):
                center_x = self.__x + 0.5 * self.diameter + self.padding_size
                center_y = self.__y + 0.5 * self.diameter + self.padding_size
                new_x = center_x + ((a - center_x) * cos(angle_radian) - (b - center_y) * sin(angle_radian))
                new_y = center_y + ((a - center_x) * sin(angle_radian) + (b - center_y) * cos(angle_radian))
                new_coordinates.append(new_x)
                new_coordinates.append(new_y)
            self.__canvas.coords(object_id, new_coordinates)

    def turn_left(self):
        self.rotate(-pi / 2.0)
        self.orientation = Orientation.next_ccw(self.orientation)

    def move_forward(self):
        switch_move = {
            Orientation.NORTH: (0, -self.cell_size),
            Orientation.EAST: (self.cell_size, 0),
            Orientation.SOUTH: (0, self.cell_size),
            Orientation.WEST: (-self.cell_size, 0),
        }
        next_x, next_y = switch_move.get(self.orientation)
        self.__move(next_x, next_y)
        self._row = self._row + int(next_y / self.cell_size)
        self._col = self._col + int(next_x / self.cell_size)

    def __move_grid(self):
        pass

    def __move(self, delta_x, delta_y):
        self.__x += delta_x
        self.__y += delta_y
        for canvas_id in self.__canvas.find_withtag("avatar"):
            self.__canvas.move(canvas_id, delta_x, delta_y)

    def update_graphics(self, cell_size):
        self.cell_size = cell_size
        self.border_size = self.cell_size / 2.0
        self.padding_size = self.cell_size / 10
        self.diameter = self.cell_size - 2 * self.padding_size
        self.__x = self.border_size + self._col * self.cell_size
        self.__y = self.border_size + self._row * self.cell_size
        self.__canvas.coords(self.__circle_id,
                             self.__x + self.padding_size, self.__y + self.padding_size,
                             self.__x + self.diameter + self.padding_size, self.__y + self.diameter + self.padding_size)
        self.__canvas.coords(self.__poly_id,
                             self.__x + 0.75 * self.diameter + self.padding_size,
                             self.__y + 0.5 * self.diameter + self.padding_size,
                             self.__x + 0.25 * self.diameter + self.padding_size,
                             self.__y + 0.25 * self.diameter + self.padding_size,
                             self.__x + 0.25 * self.diameter + self.padding_size,
                             self.__y + 0.75 * self.diameter + self.padding_size)
        current_orientation = Orientation.EAST
        while current_orientation is not self.orientation:
            self.rotate(-pi / 2.0)
            current_orientation = Orientation.next_ccw(current_orientation)

    def bring_to_top(self):
        self.__canvas.tag_raise(self.__circle_id)
        self.__canvas.tag_raise(self.__poly_id)


class MazeCell:
    def __init__(self, canvas, row, col, cell_size):
        self.__canvas = canvas
        self.row = row
        self.col = col
        self.__update_cell_size(cell_size)
        self.__floor_id = self.__canvas.create_rectangle(self.x + self.wall_size/2.0, self.y + self.wall_size/2.0,
                                                         self.x + self.wall_size/2.0 + self.floor_width, self.y + self.wall_size/2.0 + self.floor_width,
                                                         fill="white", outline="", width=0.0, tag="maze floor")
        self.__north_id = self.__canvas.create_line(self.x - self.wall_size/2.0, self.y,
                                                    self.x + self.cell_size + self.wall_size/2.0, self.y,
                                                    fill="black", width=self.wall_size, tag="maze wall")
        self.__east_id = self.__canvas.create_line(self.x + self.cell_size, self.y - self.wall_size/2.0,
                                                   self.x + self.cell_size, self.y + self.cell_size + self.wall_size/2.0,
                                                   fill="black", width=self.wall_size, tag="maze wall")
        self.__south_id = self.__canvas.create_line(self.x - self.wall_size/2.0, self.y + self.cell_size,
                                                    self.x + self.cell_size + self.wall_size/2.0, self.y + self.cell_size,
                                                    fill="black", width=self.wall_size, tag="maze wall")
        self.__west_id = self.__canvas.create_line(self.x, self.y - self.wall_size/2.0,
                                                   self.x, self.y + self.cell_size + self.wall_size/2.0,
                                                   fill="black", width=self.wall_size, tag="maze wall")

        self.wall_north = True
        self.wall_east = True
        self.wall_south = True
        self.wall_west = True

        # Look to combine switches later
        self.switch_wall_graphics = {
            Orientation.NORTH: self.__north_id,
            Orientation.EAST: self.__east_id,
            Orientation.SOUTH: self.__south_id,
            Orientation.WEST: self.__west_id,
        }

        self.switch_wall = {
            Orientation.NORTH: "wall_north",
            Orientation.EAST: "wall_east",
            Orientation.SOUTH: "wall_south",
            Orientation.WEST: "wall_west",
        }

    def update_from_data(self, data):
        # Update based on data
        self.set_floor_color(data.fill_color)
        self.set_wall_active(Orientation.NORTH, data.wall_north)
        self.set_wall_active(Orientation.EAST, data.wall_east)
        self.set_wall_active(Orientation.SOUTH, data.wall_south)
        self.set_wall_active(Orientation.WEST, data.wall_west)

    def set_floor_color(self, color):
        self.__canvas.itemconfig(self.__floor_id, fill=color)

    def reset_floor_color(self):
        self.__canvas.itemconfig(self.__floor_id, fill="white")

    def is_floor_colored(self):
        return self.__canvas.itemcget(self.__floor_id, "fill") == ""

    def set_wall_color(self, wall_orientation, color):
        if isinstance(wall_orientation, Orientation):
            wall_id = self.switch_wall_graphics.get(wall_orientation)
            self.__canvas.itemconfig(wall_id, fill=color)
            self.__canvas.tag_raise(wall_id)
        else:
            raise ValueError("Input wall_orientation must be instance of Orientation")

    def reset_wall_color(self, wall_orientation):
        if isinstance(wall_orientation, Orientation):
            wall_id = self.switch_wall_graphics.get(wall_orientation)
            self.__canvas.itemconfig(wall_id, fill="black")
        else:
            raise ValueError("Input wall_orientation must be instance of Orientation")

    def reset_all_walls(self):
        self.__canvas.itemconfig(self.__north_id, fill="black")
        self.__canvas.itemconfig(self.__east_id, fill="black")
        self.__canvas.itemconfig(self.__south_id, fill="black")
        self.__canvas.itemconfig(self.__west_id, fill="black")

        self.wall_north = True
        self.wall_east = True
        self.wall_south = True
        self.wall_west = True

    def set_wall_active(self, orientation, is_active):
        if isinstance(orientation, Orientation):
            target_wall = self.switch_wall.get(orientation)
            setattr(self, target_wall, is_active)
            if is_active:
                self.set_wall_color(orientation, "black")
            else:
                self.set_wall_color(orientation, "")
        else:
            raise ValueError("The input was not a valid Orientation")

    def is_wall_intact(self, orientation):
        is_active = False
        if isinstance(orientation, Orientation):
            target_wall = self.switch_wall.get(orientation)
            is_active = getattr(self, target_wall)
        return is_active

    def are_walls_intact(self):
        return self.wall_north and self.wall_east and self.wall_south and self.wall_west

    def __update_cell_size(self, cell_size):
        self.cell_size = cell_size
        self.border_size = cell_size / 2.0
        self.x = self.border_size + self.col * self.cell_size
        self.y = self.border_size + self.row * self.cell_size
        self.wall_size = floor(self.cell_size / 10.0)
        self.floor_width = cell_size - self.wall_size

    def update_graphics(self, cell_size):
        self.__update_cell_size(cell_size)
        self.__canvas.itemconfig(self.__north_id, width=self.wall_size)
        self.__canvas.itemconfig(self.__east_id, width=self.wall_size)
        self.__canvas.itemconfig(self.__south_id, width=self.wall_size)
        self.__canvas.itemconfig(self.__west_id, width=self.wall_size)
        self.__canvas.coords(self.__floor_id, (
                             self.x + self.wall_size/2.0, self.y + self.wall_size/2.0,
                             self.x + self.wall_size/2.0 + self.floor_width,
                             self.y + self.wall_size/2.0 + self.floor_width))
        self.__canvas.coords(self.__north_id, (
                             self.x - self.wall_size/2.0, self.y,
                             self.x + self.cell_size + self.wall_size/2.0, self.y))
        self.__canvas.coords(self.__east_id, (
                             self.x + self.cell_size, self.y - self.wall_size/2.0,
                             self.x + self.cell_size, self.y + self.cell_size + self.wall_size/2.0))
        self.__canvas.coords(self.__south_id, (
                             self.x - self.wall_size/2.0, self.y + self.cell_size,
                             self.x + self.cell_size + self.wall_size/2.0, self.y + self.cell_size))
        self.__canvas.coords(self.__west_id, (
                             self.x, self.y - self.wall_size/2.0,
                             self.x, self.y + self.cell_size + self.wall_size/2.0))
