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
from shutil import posix
# Students will need to click on terminal and type the following command
# pip install pygame

# Imports
from time import sleep
from world_maker.world_builder import MainWorld


class StudentWorld(MainWorld):
    def __init__(self):

        cell_size = 50


        creation_period = 0


        solution_period = 250


        seed = 1884

        """
            Do not modify the super().__init__() command.
            This MazeMain class is a subclass of the MazeCreator class where I have implemented the maze builder.
            In object oriented programming, this is called abstraction. I have hidden the abstract details to leave you
            only with the key information need to interact with the program
        """
        super().__init__(cell_size, creation_period, solution_period, seed)

        # Create a Maze of the selected size (max value 100)
        number_of_rows = 3
        number_of_cols = 3
        self.create_maze(number_of_rows, number_of_cols)



    def student_solution(self):


        # Choose the pzzlue
        self.solve_puzzle()
        # self.solve_potholes()


    def turn_right(self):
        for i in range(3):
            self.turn_avatar_left()


    def turn_around(self):
        for i in range(2):
            self.turn_avatar_left()


    def solve_puzzle(self):

        # Directions: North, East, South, West
        directions = [
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1)
        ]

        # i start here
        row = 0
        col = 0
        facing = 1

        #
        rows = 3
        cols = 3

        visited = {(row, col)}
        dead_ends = []
        stack = []

        # Remember how we reached each square
        parents = {}


        open_counts = {}

        def turn_to(direction):
            nonlocal facing

            # Calculate LEFT turns
            turns = (facing - direction) % 4

            for i in range(turns):
                self.turn_avatar_left()

            facing = direction

        def move_to(target_row, target_col):          #target funtion and also it adds to the blacklist
            nonlocal row, col

            dr = target_row - row
            dc = target_col - col

            direction = directions.index((dr, dc))

            turn_to(direction)

            if not self.check_front_wall():  #we gotta check our paramerters before the main funciton cus like walls n stuff
                self.move_avatar_forward()
                row = target_row
                col = target_col
                return True

            return False

        # DEPTH FIRST SEARCH
        while True:

            current = (row, col)


            if current not in open_counts:

                count = 0

                for direction in range(4):

                    dr, dc = directions[direction]
                    nr = row + dr
                    nc = col + dc

                    if 0 <= nr < rows and 0 <= nc < cols:

                        turn_to(direction)

                        if not self.check_front_wall():
                            count += 1

                open_counts[current] = count

                # A real dead end has only one exit
                if count == 1 and current != (0, 0):
                    dead_ends.append(current)
                    self.paint_the_ground("red")
                else:
                    self.paint_the_ground("blue")

            moved = False

            # Explore unvisited neighboring squares
            for direction in range(4):

                dr, dc = directions[direction]
                nr = row + dr
                nc = col + dc

                if not (0 <= nr < rows):         #yeah man couldnt tell you how this works
                    continue

                if not (0 <= nc < cols):
                    continue

                if (nr, nc) in visited:       #the github guy did this
                    continue

                turn_to(direction)

                if not self.check_front_wall():

                    # Save current position
                    stack.append(current)

                    parents[(nr, nc)] = current

                    self.move_avatar_forward()

                    row = nr
                    col = nc

                    visited.add((row, col))

                    moved = True
                    break

            if not moved:       #every other condition falls under here uhhh I hope

                # All reachable squares explored
                if not stack:
                    break

                # Backtrack
                previous = stack.pop()

                move_to(previous[0], previous[1])

            sleep(self.solution_period / 1000.0)

        print("Exploration complete!")
        print("Visited squares:", visited)      #wow look how professinaol I am
        print("Dead ends:", dead_ends)

        # BUILD PATH FROM START TO FINISH
        finish = (rows - 1, cols - 1)

        if finish not in visited:
            print("Finish not reachable")
            return

        path = []
        position = finish

        while position != (0, 0):
            path.append(position)
            position = parents[position]

        path.append((0, 0))
        path.reverse()

        print("Solution path:", path)

        # Character is back at the start
        # Follow the discovered solution        wow these comments are soooooooog good
        for next_row, next_col in path[1:]:

            move_to(next_row, next_col)

            self.paint_the_ground("green")

            sleep(self.solution_period / 1000.0)

        print("maze solved!")





    def solve_potholes(self):
        print("Solving Potholes")

        while not self.check_front_wall():


            # COMPUTER, LOOK TO THE RIGHT
            if not self.check_right_wall():

                self.pick_beeper()
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
