"""
Instructions
0) Install the two libraries needed from the Git Repository
1) Write your own code in the student_solution function below
2) Run the program, hit the Make Maze Button and then Run Solution

Inherited Attributes
    self.scene - SceneBuilder Object with Useful Functions and Attributes
    self.avatar - MazeAvatar Object with Useful Functions and Attributes
    
Inherited Functions
    self.move_avatar_forward()
    self.turn_avatar_left()

    self.put_beeper()
    self.pick_beeper()

    self.check_front_wall()
    self.check_right_wall()
    self.check_left_wall()
    
    self.highlight_right_wall()
    self.paint_the_ground(color), where color can be string (e.g. "blue") or hex code (e.g. #9D2235)
"""
from encodings import search_function
# Students will need to click on terminal and type the following command
# pip install pygame

# Imports
from time import sleep

from pip._internal import self_outdated_check

from world_maker.world_builder import MainWorld


class StudentWorld(MainWorld):
    def __init__(self):
        # The following parameters are editable
        cell_size = 50 # Initial size of each square in the world. You can drag the window to resize

        # This parameter changes the visualization speed for the algorithm that creates the maze
        creation_period = 0 # time in milliseconds

        # This parameter changes the speed at which your personal solution will solve the maze
        solution_period = 200 # time in milliseconds

        # This parameter sets the starting point for the random number generator.
        # We will use the same seed during the workshop so that we all start off solving the same maze.
        seed = 1884

        """
            Do not modify the super().__init__() command.
            This MazeMain class is a subclass of the MazeCreator class where I have implemented the maze builder.
            In object oriented programming, this is called abstraction. I have hidden the abstract details to leave you
            only with the key information need to interact with the program
        """
        super().__init__(cell_size, creation_period, solution_period, seed)

        # Create a Maze of the selected size (max value 100)
        number_of_rows = 10
        number_of_cols = 10
        self.create_maze(number_of_rows, number_of_cols)

        # Create a Karel World from a Formatted Text File
        # Three stater worlds (Fill the Pothole) are in the package (i.e. "World1.txt", "World2.txt", and "World3.txt")
        # One starter world (Light Up Post) are in the package (i.e. "World4.txt")
        # self.create_karel_world("World3.txt")


    def turn_right(self):
        self.turn_avatar_left()
        sleep(self.solution_period / 1000)
        self.turn_avatar_left()
        sleep(self.solution_period / 1000)
        self.turn_avatar_left()
        sleep(self.solution_period / 1000)

    # def student_solution(self):
    #     # Goal 1: Karel Pothole Algorithm
    #
    #     # Move forward one step first
    #     self.move_avatar_forward()
    #     sleep(self.solution_period / 1000)
    #
    #     # Pick up the beeper at this new location
    #     self.pick_beeper()
    #     sleep(self.solution_period / 1000)
    #
    #     # Check if there is a pothole below
    #     if not self.check_right_wall():
    #         # Turn right to face the pothole
    #         self.turn_right()
    #         sleep(self.solution_period / 1000)
    #         # Move down into the pothole
    #         self.move_avatar_forward()
    #         sleep(self.solution_period / 1000)
    #         # Fill the pothole with a beeper
    #         self.put_beeper()
    #         sleep(self.solution_period / 1000)
    #
    #     # Climb out and turn around then go back up
    #         self.turn_avatar_left()
    #         sleep(self.solution_period / 1000)
    #         self.turn_avatar_left()
    #         sleep(self.solution_period / 1000)
    #         self.move_avatar_forward()
    #         sleep(self.solution_period / 1000)
    #
    #     # Use the turn_right function to face East again
    #         self.turn_right()
    #         sleep(self.solution_period / 1000)
    #
    #     # Now, continue the normal loop for the rest of the map
    #     while not self.check_front_wall():
    #         self.move_avatar_forward()
    #         sleep(self.solution_period / 1000)
    #
    #         # Pick up beeper if present
    #         self.pick_beeper()
    #         sleep(self.solution_period / 1000)
    #
    #         # Check for pothole on the right, if no wall, go down to fill it
    #         if not self.check_right_wall():
    #             sleep(self.solution_period / 1000)
    #             self.turn_right()
    #             sleep(self.solution_period / 1000)
    #             self.move_avatar_forward()
    #             sleep(self.solution_period / 1000)
    #             self.put_beeper()
    #             sleep(self.solution_period / 1000)
    #
    #             # Come back up and face right again
    #             self.turn_avatar_left()
    #             sleep(self.solution_period / 1000)
    #             self.turn_avatar_left()
    #             sleep(self.solution_period / 1000)
    #             self.move_avatar_forward()
    #             sleep(self.solution_period / 1000)
    #             self.turn_right()
    #             sleep(self.solution_period / 1000)





    def student_solution(self):

        # Goal 2: implementation of the Right Hand Rule for Maze Solving


        # Loop indefinitely until the exit is reached
        while True:

            # Stop condition: exit the loop if Karel reaches teh final destination which is (9,9)
            if self.avatar.position == (9,9):
                break

            # Check if the right side is open, if it is opened, turn right
            if not self.check_right_wall():


                # If the right is open, turn right and move forward to hug the wall
                self.turn_right()
                sleep(self.solution_period / 1000)
                self.move_avatar_forward()
                sleep(self.solution_period / 1000)

            # If the right is blocked, check if the front is open
            elif not self.check_front_wall():
                # If front is open, just move forward
                self.move_avatar_forward()
                sleep(self.solution_period / 1000)

            # If both the right is blocked, check it the front is open
            else:
                # Turn left to find a new path
                self.turn_avatar_left()
                sleep(self.solution_period / 1000)































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

if __name__ == "__main__":
    # execute only if run as a script
    StudentWorld()

