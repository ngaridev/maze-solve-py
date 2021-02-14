from setup import maze_data as md, im, qet
from app import find_one, paint_line
from args import args
from os import mkdir
from os import path, getcwd

"""
Instead of recursion we are using one big loop and a large collection of arrays

The approach is similar but instead of creating a new object @ every split
the one father Node creates a branch >> It would be faster if we could run multiple threads

For every loop in the main loop we move a single-step per array/'path'

Once an array reaches a dead end we call of the movement

"""""


class Node:

    def __init__(self, maze_data, starting_point, end_point):
        self.maze_data = maze_data
        self.starting_point = starting_point
        self.end_point = end_point
        self.save_point = f"\\{str(__file__).split('.')[0]}"
        self.all_arrays = [[self.starting_point]]
        self.reached_final_point = False
        self.potentials = []
        self.setup()
        self.start()

    def setup(self):
        print(f"Starting operation on {args.Image}.png")
        print("#" * 30 + "\n\n")
        print(f"Start point : {self.starting_point}")
        print(f"End point : {self.end_point}")

    def start(self):
        while not self.reached_final_point:
            for array in self.all_arrays:
                if self.move(array):
                    break
        print("#" * 30 + "Search complete" + "#" * 30 + "\n")
        self.trace_back()

    def check_fend(self, array):
        print(f"Final point : {self.end_point}\t:\t{array[-1]}")
        if array[-1] == self.end_point:
            return True
        return False

    def trace_back(self):
        _offset, read_co = 0, 1
        final_array = [self.potentials[-1]]
        print("Tracing Back\n\n")
        while final_array[-1][0] != self.starting_point:
            print(f"Path no : {_offset}")
            for i in range(read_co, len(self.potentials) + 1):
                arr = self.potentials[-i]
                print(f"Array[0] : {arr[-1]}\t, final_array[-1][-1] : {final_array[-1][0]}")
                if arr[-1] == final_array[-1][0]:
                    print("#" * 30 + " Found " + "#" * 30)
                    final_array.append(arr)
            _offset += 1

        # flattening the final path
        final_path = []
        for path in final_array:
            for point in path:
                final_path.append(point)

        print(f"Final path")
        for n, path_found in enumerate(final_path):
            print(f"{n} : {path_found}")

        paint_line(im, (225, 0, 0), final_path)
        self.save_solution()

    def check_solution(self):
        if not len(self.all_arrays):
            return True
        return False

    def move(self, path_array):
        print(f"Current position : {path_array[-1]}")
        possible_directions = self.check_around(path_array)
        print(f"Path Array : {path_array}\n")

        # print(f"Possible Directions : {possible_directions}")
        self.maze_data[path_array[-1][0], path_array[-1][1]] = 0  # we mark area we've passed through already
        if self.check_solution():
            print("Solution unavailable")
            for path in self.all_arrays:
                paint_line(_image=im, _fill=[0, 0, 225], points=path)
            return True

        if self.check_fend(path_array):
            self.maze_data[path_array[-1][0], path_array[-1][1]] = 0  # we mark area we've passed through already
            self.reached_final_point = True
            self.potentials.append(path_array)
            # print(f"Final point reached")
            print(f"Potentials")
            for point in self.potentials:
                print(point)
            return True

        if len(possible_directions) == 0:
            # dead-end reached
            # paint dead-end path on image
            # remove array from all_array
            print("#" * 30 + "Dead point reached" + "#" * 30 + "\n")
            self.all_arrays.remove(path_array)
            paint_line(im, (0, 225, 100), path_array)

        elif len(possible_directions) == 1:
            path_array.append(possible_directions[0])
        else:
            # we create more arrays
            print("#" * 30 + "Split point reached" + "#" * 30 + "\n")
            self.all_arrays.remove(path_array)
            self.potentials.append(path_array)
            for possibility in possible_directions:
                self.all_arrays.append([path_array[-1], possibility])
        return False

    def check_around(self, array):
        cp, maze_d, fn = array[-1], self.maze_data, []
        all_directions = [[cp[0] - 1, cp[1]], [cp[0] + 1, cp[1]], [cp[0], cp[1] + 1], [cp[0], cp[1] - 1], ]
        # print(f"All directions : {all_directions}")
        for direction in all_directions:
            if 0 <= direction[0] < len(maze_d) and 0 <= direction[1] < len(maze_d[0]) and maze_d[direction[0], direction[1]] == 1:
                fn.append(direction)
        return fn

    def print_maze(self):
        for row in self.maze_data:
            print(row)

    def save_solution(self):
        if not path.exists(path.join(getcwd() + self.save_point)):
            print(f"Creating new directory : {path.join(getcwd() + self.save_point)}")
            mkdir(path.join(getcwd() + self.save_point))
        try:
            qet.save(path.join(getcwd() + self.save_point + f"\\{args.Save}.png"))
            print("Image ready")
        except FileNotFoundError:
            print(f"Error occurred saving the file")


if __name__ == '__main__':
    sp, en = [0, find_one(md[0])], [len(md) - 1, find_one(md[-1])]
    root = Node(maze_data=md, starting_point=sp, end_point=en)
