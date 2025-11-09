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
    
    self.check_front_wall()
    self.check_right_wall()
    self.check_left_wall()
    
    self.highlight_right_wall()
    self.paint_the_ground(color), where color can be string (e.g. "blue) or hex code (e.g. #9D2235)
"""

# Students will need to click on terminal and type the following command
# pip install simpleaudio
# pip install importlib_resources

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
        self.create_karel_world("World4.txt")

        # One starter world (Light Post) are in the package (i.e. "World4.txt")

    def student_solution(self):
        # Delete the pass statement and add your code here
        # To see your solution you can use the sleep command (i.e. sleep(1) to sleep 1 second)
        print("Starting Student Solution")

        self.move_avatar_forward()
        sleep(self.solution_period/1000.0)
        self.turn_avatar_left()
        sleep(self.solution_period/1000.0)
        self.move_avatar_forward()
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
