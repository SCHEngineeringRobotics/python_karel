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

# Students will need to click on terminal and type the following command
# pip install pygame

# Imports
from time import sleep
from world_maker.world_builder import MainWorld


class StudentWorld(MainWorld):
    def __init__(self):
        # The following parameters are editable
        cell_size = 50 # Initial size of each square in the world. You can drag the window to resize

        # This parameter changes the visualization speed for the algorithm that creates the maze
        creation_period = 0 # time in milliseconds

        # This parameter changes the speed at which your personal solution will solve the maze
        solution_period = 40 # time in milliseconds

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
        # self.create_maze(number_of_rows, number_of_cols)

        # Create a Karel World from a Formatted Text File
        # Three stater worlds (Fill the Pothole) are in the package (i.e. "World1.txt", "World2.txt", and "World3.txt")
        # One starter world (Light Up Post) are in the package (i.e. "World4.txt")
        self.create_karel_world("World1.txt")

    def student_solution(self):

        # Goal 1: Karel Pothole Algorithm

        # Loop while there is no wall in front of Karel to keep moving
        while not self.check_front_wall():

            # Check wall on the right
            # If the right is no wall on the right, there is a pothole
            if not self.check_front_wall():
                # False (no wall), go into the pothole and fill
                # Turn right and move down into the hole
                self.turn_avatar_left()
                self.turn_avatar_left()
                self.turn_avatar_left()
                self.move_avatar_forward()

                # Fill the pothole with a beeper
                self.put_beeper()

                # Turn around to go back up
                self.turn_avatar_left()
                self.turn_avatar_left()
                self.move_avatar_forward()

                # Turn right (three left turns) to face East again
                self.turn_avatar_left()
                self.turn_avatar_left()
                self.turn_avatar_left()

            # Move forward to the next spot
                self.move_avatar_forward()

        # After reaching the end, check the last spot and put a beeper if empty
        if not self.beeper_present():
            self.put_beeper()

    


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
