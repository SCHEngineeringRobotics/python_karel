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
        self.create_maze(number_of_rows, number_of_cols)

        # Create a Karel World from a Formatted Text File
        # Three stater worlds (Fill the Pothole) are in the package (i.e. "World1.txt", "World2.txt", and "World3.txt")
        # One starter world (Light Up Post) are in the package (i.e. "World4.txt")
        #  self.create_karel_world("World1.txt")


    def student_solution(self):


        # Choose the pzzlue
        self.solve_maze()
        # self.solve_potholes()


    def turn_right(self):
        for i in range(3):
            self.turn_avatar_left()


    def turn_around(self):
        for i in range(2):
            self.turn_avatar_left()


    def solve_maze(self):
        # Directions: North, East, South, West           this almost works
        directions = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)
        ]

        # Start at the top-left, facing East
        row = 0
        col = 0
        facing = 1

        visited = {(row, col)}
        stack = []

        # Set this to the maze dimensins
        rows = 10
        cols = 10

        while True:

            # Stop at the bottom-right finish
            if row == rows - 1 and col == cols - 1:
                print("Maze Solved!")
                break

            moved = False

            # Try all four directions
            for new_direction in range(4):

                dr, dc = directions[new_direction]
                new_row = row + dr
                new_col = col + dc

                # Skip visited or out-of-bounds cells     yeah this also dont work abnd im scared and idk why
                if not (0 <= new_row < rows):
                    continue

                if not (0 <= new_col < cols):
                    continue

                if (new_row, new_col) in visited:
                    continue

                # Turn toward the chosen direction
                turns = (new_direction - facing) % 4

                for i in range(turns):
                    self.turn_avatar_left()

                facing = new_direction

                # Check whether movement is possible
                if not self.check_front_wall():

                    stack.append((row, col))
                    self.move_avatar_forward()

                    row = new_row
                    col = new_col

                    visited.add((row, col))
                    self.paint_the_ground("blue")

                    moved = True
                    break

            if not moved:

                # No unexplored neighbors = backtrack
                if not stack:
                    print("No path found")
                    break

                previous_row, previous_col = stack.pop()

                # Find direction to previous square.   this is chopped cheese :(
                dr = previous_row - row
                dc = previous_col - col

                back_direction = directions.index((dr, dc))

                turns = (back_direction - facing) % 4

                for i in range(turns):
                    self.turn_avatar_left()

                facing = back_direction

                self.move_avatar_forward()

                row = previous_row
                col = previous_col

                self.paint_the_ground("yellow")

            sleep(self.solution_period / 1000.0)


    def solve_potholes(self):
        print("Solving Potholes")

        while not self.check_front_wall():

            # COMPUTER, LOOK TO THE RIGHT
            if not self.check_right_wall():

                self.turn_right()
                self.move_avatar_forward()

                # Place a beeper in the pothole
                self.put_beeper()

                # Return to main path.    this part actually works I have no idea how but im not touching it
                self.turn_around()
                self.move_avatar_forward()
                self.turn_right()

            # JARVIS, CONTINUE FORWARD
            if not self.check_front_wall():
                self.move_avatar_forward()

            sleep(self.solution_period / 1000.0)

        print("Potholes Completed!")


if __name__ == "__main__":
    # execute only if run as a script
    StudentWorld()
