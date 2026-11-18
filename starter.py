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
import queue
from encodings import search_function
from sys import excepthook
# Students will need to click on terminal and type the following command
# pip install pygame

# Imports
from time import sleep

from pip._internal import self_outdated_check

from world_maker.world_builder import MainWorld


class StudentWorld(MainWorld):
    def __init__(self):
        # The following parameters are editable
        cell_size = 50  # Initial size of each square in the world. You can drag the window to resize

        # This parameter changes the visualization speed for the algorithm that creates the maze
        creation_period = 0  # time in milliseconds

        # This parameter changes the speed at which your personal solution will solve the maze
        solution_period = 200  # time in milliseconds

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

    # def student_solution(self):
    #
    #     # Goal 2: implementation of the Right Hand Rule for Maze Solving
    #
    #
    #     # Loop indefinitely until the exit is reached
    #     while True:
    #
    #         # Stop condition: exit the loop if Karel reaches teh final destination which is (9,9)
    #         if self.avatar.position == (9,9):
    #             break
    #
    #         # Check if the right side is open, if it is opened, turn right
    #         if not self.check_right_wall():
    #
    #
    #             # If the right is open, turn right and move forward to hug the wall
    #             self.turn_right()
    #             sleep(self.solution_period / 1000)
    #             self.move_avatar_forward()
    #             sleep(self.solution_period / 1000)
    #
    #         # If the right is blocked, check if the front is open
    #         elif not self.check_front_wall():
    #             # If front is open, just move forward
    #             self.move_avatar_forward()
    #             sleep(self.solution_period / 1000)
    #
    #         # If both the right is blocked, check it the front is open
    #         else:
    #             # Turn left to find a new path
    #             self.turn_avatar_left()
    #             sleep(self.solution_period / 1000)




    def student_solution(self):

        # Directions: North, East, South, West
        directions = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)
        ]

        # Get the starting position
        start = self.avatar.position
        # Get the goal position
        goal = (
            self.scene.goal_cell.row,
            self.scene.goal_cell.col,
        )

        # Get the maze size
        rows = self.scene.number_of_rows
        cols = self.scene.number_of_cols

        # Create a queue for BFS
        q = queue.Queue()
        # Add the starting position
        q.put(start)

        # Remember which places it has visited
        visited = set()
        visited.add(start)

        # Remember the previous position
        parent = {}

        # Remember the direction used to reach each position
        move_direction = {}

        # Explore the maze using BFS
        while not q.empty():
            # Get the current position
            current = q.get()

            # Stop when we find the goal
            if current == goal:
                break

            # Get the current cell
            current_cell = self.scene.scene_data[current [0]][current [1]]

            print("Exploring:", current)

            print("Current position:", current)

            print("North:", current_cell.wall_north)
            print("East:", current_cell.wall_east)
            print("South:", current_cell.wall_south)
            print("West:", current_cell.wall_west)

            print("East cell west wall:", self.scene.scene_data[0][1].wall_west)
            print("South cell north wall:", self.scene.scene_data[1][0].wall_north)

            # Check all four directions
            for direction in range(4):

                row_change, col_change = directions[direction]

                next_cell = (
                    current[0] + row_change,
                    current[1] + col_change
        )

                # Skip places outside the maze
                if (next_cell [0] < 0 or
                    next_cell [0] >= rows or
                    next_cell [1] < 0 or
                    next_cell [1] >= cols):
                    continue

                # Skip places we already visited
                if next_cell in visited:
                    continue

                # Check the wall in this direction
                if direction == 0:
                    wall = current_cell.wall_north

                elif direction == 1:
                    wall = current_cell.wall_east

                elif direction == 2:
                    wall = current_cell.wall_south

                else:
                    wall = current_cell.wall_west

                # Don't move through a wall
                if wall:
                    continue

                # Remember this place
                visited.add(next_cell)

                # Remember the previous position
                parent[next_cell] = current

                # Remember the direction
                move_direction[next_cell] = direction

                # Add the new place to the queue
                q.put(next_cell)

            # Stop if the goal cannot be reached
            print("Total visited:", len(visited))
            print("Goal:", goal)
            print("Last visited cells:", list(visited) [-10:])

            if goal not in visited:
                print("No path found")
                return

            # Build the shortest path backwards
            path = []
            current = goal

            while current != start:
                path.append(move_direction[current])
                current = parent[current]

            # Reverse the path
            path.reverse()

            print("Start:", start)
            print("Goal:", goal)
            print("Path length:", len(path))

            # Get the avatar's starting direction
            current_direction = self.avatar.orientation

            # Follow the shortest path
            for direction in path:
                # Face the correct direction
                self.face_direction(current_direction, direction)
                # Move forward
                self.move_avatar_forward()
                # Update the current direction
                current_direction = direction

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
