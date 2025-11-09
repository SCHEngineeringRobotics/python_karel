"""
   This class builds the main world and provides the interface for the student
   world class to implement and visualize a solution.

    Copyright [2020] [Daniel A. Jacobs]

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Tkinter Imports
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tk_font

import threading  # Threading for Student
import time  # Time and Sleep Control

from abc import ABC, abstractmethod  # Import Abstract Base Class
import random  # Random Number Generator
from importlib_resources import files
import os  # Operating System to Check for File

# File management
import importlib_resources
import world_maker.resources

# My Packages
from world_maker import graphics_builder as graphics
from world_maker import scene_builder as scene

# Test Import Sound
sound_available = False
try:
    import simpleaudio as sa

    congrats_source = importlib_resources.files(world_maker.resources).joinpath("congrats.wav")
    if congrats_source.is_file():
        sound_available = True
    else:
        print("World Maker Audio File: Congrats.wav could not be found")
finally:
    pass

class MainWorld(ABC):

    @abstractmethod
    def __init__(self, cell_size, creation_period, solution_period, seed=time.time()):
        # Attributes
        self.__CELL_SIZE_MIN = 6
        self.__CELL_SIZE_MAX = 100

        #  *** GUI Information ***
        self.__root = tk.Tk()

        # Keybinding
        self.__root.bind("<Key>", self.keyboard_event)

        # Fonts
        heading_font = tk_font.Font(family='Arial', size=24, weight=tk_font.BOLD)
        btn_font = tk_font.Font(family='Arial', size=16, weight=tk_font.BOLD)

        # parameters
        self.frame_width = 150
        self.label_width = 18
        self.border_width = 5
        self.padding = 2

        # Left Frame
        self.frame_left = tk.Frame(master=self.__root, width=self.frame_width)
        self.frame_left.pack(side=tk.LEFT)

        # Status Frame
        self.frm_status = tk.Frame(master=self.frame_left, relief=tk.GROOVE, borderwidth= self.border_width, width=self.frame_width)
        self.lbl_status = tk.Label(self.frm_status, text="Avatar", font=heading_font)
        self.lbl_status.pack()
        self.lbl_orientation = tk.Label(self.frm_status, text="Orientation : EAST", width=self.label_width, font=btn_font)
        self.lbl_orientation.pack()
        self.lbl_position = tk.Label(self.frm_status, text="Position : (0 , 0)", width=self.label_width, font=btn_font)
        self.lbl_position.pack()
        self.lbl_beepers_held = tk.Label(self.frm_status, text="# Beepers : 0", width=self.label_width, font=btn_font)
        self.lbl_beepers_held.pack()
        self.frm_status.pack()

        # Button Frame
        self.frm_button = tk.Frame(master=self.frame_left, relief=tk.GROOVE, borderwidth=self.border_width, width=self.frame_width)

        label = tk.Label(self.frm_button, text="Controls", font=heading_font)
        label.pack(pady=self.padding)
        self.btn_move_forward = tk.Button(self.frm_button, text="Move Forward", foreground="blue", background="white",
                                          font=btn_font, width=self.label_width)
        self.btn_move_forward.pack(pady=self.padding)
        self.btn_move_forward.bind("<Button-1>", lambda event: self.move_avatar_forward())

        self.btn_turn_left = tk.Button(self.frm_button, text="Turn Left", foreground="blue", background="white",
                                       font=btn_font, width=self.label_width)
        self.btn_turn_left.pack(pady=self.padding)
        self.btn_turn_left.bind("<Button-1>", lambda event: self.turn_avatar_left())

        self.btn_put_beeper = tk.Button(self.frm_button, text="Put Beeper", foreground="blue", background="white",
                                          font=btn_font, width=self.label_width)
        self.btn_put_beeper.pack(pady=self.padding)
        self.btn_put_beeper.bind("<Button-1>", lambda event: self.put_beeper())

        self.btn_pick_beeper = tk.Button(self.frm_button, text="Pick Beeper", foreground="blue", background="white",
                                       font=btn_font, width=self.label_width)
        self.btn_pick_beeper.pack(pady=self.padding)
        self.btn_pick_beeper.bind("<Button-1>", lambda event: self.pick_beeper())

        self.btn_make_maze = tk.Button(self.frm_button, text="Draw Scene", foreground="blue", background="white",
                                       font=btn_font, width=self.label_width)
        self.btn_make_maze.pack(pady=self.padding)
        self.btn_make_maze.bind("<Button-1>", lambda event: self.run_scene_generation())

        # could this be toggle button, disabled while running and reset pop when ready?
        self.btn_student = tk.Button(self.frm_button, text="Run Solution", foreground="blue", background="white",
                                     font=btn_font, width=self.label_width)
        self.btn_student.pack(pady=self.padding)
        self.btn_student.bind("<Button-1>", lambda event: self.run_student_solution())
        label = tk.Label(self.frm_button, text="Created by Daniel Jacobs\n Copyright 2020-2025")
        label.pack()

        self.frm_button.pack()

        # Dialog Frame
        self.frm_dialog = tk.Frame(master=self.frame_left, relief=tk.GROOVE, borderwidth= self.border_width, width=self.frame_width)

        self.lbl_dialog = tk.Label(self.frm_dialog, text="Dialog", font=heading_font)
        self.lbl_dialog.pack()
        self.msg_text = tk.Text(self.frm_dialog, height=4, width=self.label_width+2, font=btn_font)
        self.msg_text.delete('1.0', tk.END)
        self.msg_text.insert(tk.END, "Everything looks ok!\nKeep Going!\n\n")
        self.msg_text.pack()
        self.frm_dialog.pack()

        # Right Frame
        self.FRAME_RIGHT_PAD = 15
        self.frm_right = tk.Frame(master=self.__root, relief=tk.FLAT, borderwidth= self.border_width*2, padx=self.FRAME_RIGHT_PAD, pady=self.FRAME_RIGHT_PAD)
        self.frm_right.bind("<Configure>", lambda event: self.resize_event(event))
        self.frm_right.pack(fill=tk.BOTH, expand=tk.TRUE)

        # Thread for Maze Generator
        self.__maze_thread = None
        self.is_maze_created = False

        # Thread for Student Solution
        self.__student_thread = None
        self.is_student_running = False

        # Thread for Sound
        self.__sound_thread = None
        self.is_sound_running = False

        self.sound_player = None
        if sound_available:
            self.congrats_data = congrats_source.read_bytes()
            self.sound_wave = sa.WaveObject(self.congrats_data, 2, 2, 44100)

        self.do_goal_check = False

        # Initialize
        # Inefficient but hides complexity of super.__init__ from first timers
        self.number_of_rows = 0
        self.number_of_cols = 0

        self.creation_period = creation_period
        self.solution_period = solution_period
        self.scene = None

        cell_size = max(self.__CELL_SIZE_MIN, min(cell_size, self.__CELL_SIZE_MAX))
        if (cell_size % 2) == 1:
            self.cell_size = cell_size - 1
        else:
            self.cell_size = cell_size

        self.border_size = self.cell_size / 2.0

        self.canvas_width = (self.number_of_cols + 1) * self.cell_size
        self.canvas_height = (self.number_of_rows + 1) * self.cell_size

        # Canvas Frame
        self.canvas = tk.Canvas(self.frm_right, background="white", width=self.canvas_width, height=self.canvas_height)

        # Create Canvas Frame Widgets
        self.canvas.pack(side=tk.LEFT)

        self.avatar = None

        # Keep record if any move action failed
        self.action_failed = False

        # Use Random Seed
        random.seed(seed)

    def create_maze(self, number_of_rows, number_of_cols):
        # Set Attributes
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols

        # Avatar (initialize to 0,0)
        self.avatar = graphics.MazeAvatar(self.canvas, 0, 0, self.cell_size, "orange")

        # Scene Info
        self.scene = scene.MazeBuilder(self.canvas, self.avatar, self.number_of_rows, self.number_of_cols, self.cell_size, self.creation_period)
        self.scene.build_scene()

        self.canvas_width = (self.number_of_cols + 1) * self.cell_size
        self.canvas_height = (self.number_of_rows + 1) * self.cell_size
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)

        # Check Goal
        self.do_goal_check = True

        # Draw GUI (blocking)
        self.__root.mainloop()  # Blocking until window close

    def create_karel_world(self, world_filename):
        # Check for World Template
        world_source = importlib_resources.files(world_maker.resources).joinpath(world_filename)
        if world_source.is_file():
            world_text = world_source.read_text()
        elif os.path.isfile(world_filename):
            try:
                file_id = open(world_filename)
                world_text = file_id.read()
                file_id.close()
            except FileNotFoundError:
                print("File %s cannot be opened." % world_filename)
        else:
            ImportError("Filename %s was not found in the package or on the patch" % world_filename)

        # Avatar (initialize to 0,0)
        self.avatar = graphics.MazeAvatar(self.canvas, 0, 0, self.cell_size, "orange")

        # Scene Info
        self.scene = scene.KarelSceneBuilder(self.canvas, self.avatar, self.cell_size, world_text)
        self.scene.build_scene()
        self.run_scene_generation()

        # Update Gui
        self.lbl_position.config(text="Position : (%i , %i)" % (self.avatar.position[1],self.avatar.position[0]))
        self.lbl_beepers_held.config(text="# Beepers : %i" % self.avatar.num_beepers)

        # Set Attributes
        self.number_of_rows = self.scene.number_of_rows
        self.number_of_cols = self.scene.number_of_cols
        self.canvas_width = (self.number_of_cols + 1) * self.cell_size
        self.canvas_height = (self.number_of_rows + 1) * self.cell_size
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)

        # Draw GUI (blocking)
        self.__root.mainloop()  # Blocking until window close

    @abstractmethod
    def student_solution(self):
        pass

    def run_student_solution(self):
        # Warp to start and then run

        if not self.is_student_running and self.is_maze_created:
            self.btn_student.config(state=tk.DISABLED)
            self.is_student_running = True
            self.__student_thread = threading.Thread(target=self.student_solution)
            self.__student_thread.daemon = True
            self.__student_thread.start()
            self.__root.after(1000, self.student_check)

    def student_check(self):
        if self.__student_thread.is_alive():
            self.__root.after(1000, self.student_check)
        else:
            self.btn_student.config(state=tk.NORMAL)
            self.is_student_running = False

    def run_scene_generation(self):
        if not self.is_maze_created:
            self.is_maze_created = True
            self.__maze_thread = threading.Thread(target=self.scene.render)
            self.__maze_thread.daemon = True
            self.__maze_thread.start()
            self.btn_make_maze.config(state=tk.DISABLED)

    def run_sound_thread(self):
        if sound_available and (not self.sound_player or not self.sound_player.is_playing()):
            self.__sound_thread = threading.Thread(target=self.play_goal_sound)
            self.__sound_thread.daemon = False
            self.__sound_thread.start()

    def play_goal_sound(self):
        #self.sound_player = self.sound_wave.play()
        pass

    @staticmethod
    def __show_goal_dialog():
        messagebox.showinfo("Congratulations", "Your avatar reached the goal!!")

    def keyboard_event(self, event):
        if not self.is_student_running:
            keyboard_switch = {
                'Up': self.move_avatar_forward,
                'Down': None,
                'Left': self.turn_avatar_left,
                'Right': None,
            }
            func = keyboard_switch.get(event.keysym, None)
            if func is not None:
                func()

    def resize_event(self, event):
        frame_border_size = self.frm_right.cget("bd")
        frame_padding_size = self.FRAME_RIGHT_PAD
        canvas_border_size = int(self.canvas.cget("bd")) + int(self.canvas.cget("highlightthickness"))
        new_canvas_width = event.width - 2 * canvas_border_size - 2 * frame_border_size - 2 * frame_padding_size
        new_canvas_height = event.height - 2 * canvas_border_size - 2 * frame_border_size - 2 * frame_padding_size

        new_cell_size = min(new_canvas_width / (self.number_of_cols + 1), new_canvas_height / (self.number_of_rows + 1))
        self.canvas.config(width=new_cell_size * (self.number_of_cols + 1),
                           height=new_cell_size * (self.number_of_rows + 1))
        if new_cell_size in range(self.__CELL_SIZE_MIN, self.__CELL_SIZE_MAX + 1):
            self.cell_size = new_cell_size

        self.avatar.update_graphics(new_cell_size)
        self.scene.update_graphics(new_cell_size)

    def move_avatar_forward(self):
        # Move Avatar
        move_succeeded = False
        row, col = self.avatar.position
        current_cell = self.scene.scene_data[row][col]
        if not current_cell.is_wall_active(self.avatar.orientation):
            move_succeeded = True
            self.avatar.move_forward()

        # Update Dialog Box
        if move_succeeded:
            self.msg_text.delete('1.0', tk.END)
            self.msg_text.insert(tk.END, "Everything looks ok!\nKeep Going!\n\n")
        else:
            self.msg_text.config(fg="red")
            self.msg_text.delete('1.0', tk.END)
            self.msg_text.insert(tk.END, "You ran into a wall!\n\n")
            self.action_failed = True

        self.lbl_position.config(text="Position : (%i , %i)" % (self.avatar.position[1],self.avatar.position[0]))
        if self.is_avatar_at_goal() and self.do_goal_check and move_succeeded:
            self.__root.after(10, self.run_sound_thread)
            self.__root.after(10, self.__show_goal_dialog)

    def turn_avatar_left(self):
        self.avatar.turn_left()
        self.lbl_orientation.config(text="Orientation : %s" % self.avatar.orientation.name)
        self.msg_text.config(fg="black")
        self.msg_text.delete('1.0', tk.END)
        self.msg_text.insert(tk.END, "Everything looks ok!\nKeep Going!\n\n")

    def put_beeper(self):
        if self.avatar.num_beepers > 0:
            self.avatar.num_beepers -= 1
            row, col = self.avatar.position
            current_cell = self.scene.scene_graphics[row][col]
            current_cell.increment_beepers()
            self.lbl_beepers_held.config(text="# Beepers : %i" % self.avatar.num_beepers)

    def pick_beeper(self):
        row, col = self.avatar.position
        current_cell = self.scene.scene_graphics[row][col]
        if current_cell.num_beepers > 0:
            current_cell.decrement_beepers()
            self.avatar.num_beepers += 1
            self.lbl_beepers_held.config(text="# Beepers : %i" % self.avatar.num_beepers)

    def check_front_wall(self):
        row, col = self.avatar.position
        current_cell = self.scene.scene_data[row][col]
        return getattr(current_cell, current_cell.switch_wall[self.avatar.orientation])

    def check_right_wall(self):
        right_orientation = graphics.Orientation.next_cw(self.avatar.orientation)
        row, col = self.avatar.position
        current_cell = self.scene.scene_data[row][col]
        return getattr(current_cell, current_cell.switch_wall[right_orientation])

    def check_left_wall(self):
        left_orientation = graphics.Orientation.next_ccw(self.avatar.orientation)
        row, col = self.avatar.position
        current_cell = self.scene.scene_data[row][col]
        return getattr(current_cell, current_cell.switch_wall[left_orientation])

    def highlight_right_wall(self):
        right_orientation = graphics.Orientation.next_cw(self.avatar.orientation)
        row, col = self.avatar.position
        current_cell = self.scene.scene_graphics[row][col]
        if getattr(current_cell, current_cell.switch_wall[right_orientation]):
            current_cell.set_wall_color(right_orientation, "red")

    def paint_the_ground(self, color_str):
        row, col = self.avatar.position
        current_cell = self.scene.scene_graphics[row][col]
        current_cell.set_floor_color(color_str)

    def is_avatar_at_goal(self):
        return self.avatar.position == (self.number_of_rows-1, self.number_of_cols-1)

    def did_actions_fail(self):
        return self.action_failed
