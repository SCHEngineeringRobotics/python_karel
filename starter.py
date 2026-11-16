"""
Instructions
0) Students will need to make sure they are running in a virtual environment with Python 3.14+
1) Students will need to install one library to play sound
    click on terminal and type the following command
    pip install pygame-ce
2) Write your own code in the student_solution function below
3) Run the program, hit the Draw Scene Button and then Run Solution

Inherited Attributes
    self.scene - SceneBuilder Object with Useful Functions and Attributes
    self.avatar - MazeAvatar Object with Useful Functions and Attributes
    
Inherited Basic Functions
    self.move_avatar_forward()
    self.turn_avatar_left()

    self.put_beeper()
    self.pick_beeper()
    self.count_ground_beepers()
    self.count_avatar_beepers()

    self.check_front_wall()
    self.check_right_wall()
    self.check_left_wall()

    self.check_north_wall():
    self.check_east_wall():
    self.check_south_wall():
    self.check_west_wall():

    self.is_avatar_at_goal():
    self.did_actions_fail(color_str):

Inherited Map Functions
    self.get_avatar_location():
    self.get_avatar_orientation(color_str):
    self.get_map_cell():
    self.get_map_goal_position():

Inherited Map Decoration Functions
    self.highlight_right_wall(color), where color can be string (e.g. "blue") or hex code (e.g. #9D2235)
    self.paint_the_ground(color), where color can be string (e.g. "blue") or hex code (e.g. #9D2235)
    self.paint_map_ground(color), where color can be string (e.g. "blue") or hex code (e.g. #9D2235)
"""


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

        #Create a Maze of the selected size (max value 100)
        number_of_rows = 10
        number_of_cols = 10
        #self.create_maze(number_of_rows, number_of_cols)

        # Create a Karel World from a Formatted Text File
        # Three stater worlds (Fill the Pothole) are in the package (i.e. "World1.txt", "World2.txt", and "World3.txt")
        # One starter world (Light Up Post) are in the package (i.e. "World4.txt")
        self.create_karel_world("World1.txt")
    #helper function to turn avatar right when needed
    def turn_avatar_right(self):
        self.turn_avatar_left()
        self.turn_avatar_left()
        self.turn_avatar_left()

    def student_solution(self):
        #comment out whichever one isn't being used
        self.pothole_world_solution()
        #self.maze_solution()


    def pothole_world_solution(self):
        #loop check if there is open space in front of avatar, executes solution loop
        while not self.check_front_wall():
            # check beeper at current position
            self.pick_beeper()
            #check if there is a wall to the right
            if self.check_right_wall():
                self.move_avatar_forward()
                sleep(self.solution_period / 1000.0)
            #if there is a pothole, fills it with beeper and continues on
            else:
                self.turn_avatar_right()
                sleep(self.solution_period / 1000.0)
                self.move_avatar_forward()
                sleep(self.solution_period / 1000.0)
                self.put_beeper()
                sleep(self.solution_period / 1000.0)
                self.turn_avatar_left()
                sleep(self.solution_period / 1000.0)
                self.turn_avatar_left()
                sleep(self.solution_period / 1000.0)
                self.move_avatar_forward()
                sleep(self.solution_period / 1000.0)
                self.check_right_wall()
                sleep(self.solution_period / 1000.0)
                self.turn_avatar_right()
                sleep(self.solution_period / 1000.0)
                self.move_avatar_forward()
                sleep(self.solution_period / 1000.0)
        #check for pothole before last wall. if there is one, fills it
        if self.check_front_wall and not self.check_right_wall():
            self.turn_avatar_right()
            sleep(self.solution_period / 1000.0)
            self.move_avatar_forward()
            sleep(self.solution_period / 1000.0)
            self.put_beeper()
            sleep(self.solution_period / 1000.0)
            self.turn_avatar_left()
            sleep(self.solution_period / 1000.0)
            self.turn_avatar_left()
            sleep(self.solution_period / 1000.0)
            self.move_avatar_forward()
            sleep(self.solution_period / 1000.0)
            self.turn_avatar_right()
            sleep(self.solution_period / 1000.0)
        # Add your code here
        print("Starting Student Solution")
        # Move Forward 1 Spot
        self.move_avatar_forward()
        # Pause for Visualization
        sleep(self.solution_period/1000.0)
        # Turn Avatar to its Left
        self.turn_avatar_left()
        # Pause for Visualization
        sleep(self.solution_period/1000.0)
        # Move Forward 1 Spot
        self.move_avatar_forward()
        # Put Down 1 Beeper from Avatar Backpack
        self.put_beeper()

    def maze_solution(self):
        #runs loop until the avatar finds its way to the goal
        while not self.is_avatar_at_goal():
            #highlights right wall as algorithm is executed for visual on avatar's path
            self.highlight_right_wall()
            #moves avatar forward if it can go forward
            if not self.check_front_wall():
                self.move_avatar_forward()
                sleep(self.solution_period / 1000.0)
            """if there is a wall to the right and front of the avatar, 
            it turns left, which will turn it around if in a dead end"""
            if self.check_front_wall() and self.check_right_wall():
                self.turn_avatar_left()
                sleep(self.solution_period / 1000.0)
            #allows the avatar to hug the right wall till the end of the maze
            if not self.check_right_wall():
                self.turn_avatar_right()
                sleep(self.solution_period / 1000.0)



    def keyboard_event(self, event):
        # You can modify this with function handles to bind functions to key press
        if not self.is_student_running:
            keyboard_switch = {
                'Up': self.move_avatar_forward,
                'Down': None,
                'Left': self.turn_avatar_left,
                'Right': self.turn_avatar_right,
            }
            func = keyboard_switch.get(event.keysym, None)
            if func is not None:
                func()

if __name__ == "__main__":
    # execute only if run as a script
    StudentWorld()
