from PIL import Image, ImageDraw
import numpy as np
from sys import setrecursionlimit

setrecursionlimit(1000000000)

image = "./Mazes/perfect2k_2.png"

ans = []
recursion_count = 0
all_arrays = []


class Node:

    def __init__(self, maze, sp, ep, mother=None):  # sp start point , ep -> end point
        self.maze = maze
        self.sp = sp
        self.cp = sp
        self.ep = ep
        print(f"End point : {self.ep}")
        self.check_maze()
        self.path = []
        self.child = []
        self.mother = mother
        self.finished = False
        self.dead_end = False
        self.move()

    def check_maze(self):
        pass

    def move_next(self):
        global recursion_count, all_arrays
        directions = self.check_around()
        recursion_count += 1
        print(f"Recursion count is : {recursion_count}")
        if len(directions) == 0:
            #  dead end
            self.maze[self.cp[0]][self.cp[1]] = 0
            self.dead_end = True
            self.path.append(self.cp)
            for point in self.path:
                if len(point) != 0:
                    all_arrays.append(list(point))
            self.draw()
            print("Reached dead end")
        elif len(directions) == 1:
            #  move to tile
            i = directions[0]
            self.path.append(self.cp)
            self.maze[self.cp[0]][self.cp[1]] = 0
            self.cp = i
        else:
            n_children = len(directions)
            self.maze[self.cp[0]][self.cp[1]] = 0
            self.path.append(self.cp)
            for i in range(n_children):
                self.child.append(
                    Node(self.maze, directions[i], mother=self, ep=self.ep)
                )
            for point in self.path:
                if len(point) != 0:
                    all_arrays.append(list(point))
            self.draw()
            self.dead_end = True

    def check_if_finished(self):
        if self.cp == self.ep:
            print(f"Current point : {self.cp}\tEnd point : {self.ep}")
            self.finished = True
            self.path.append(self.cp)
            self.trace_back()
            print(f"I have Finished my journey")

    def trace_back(self):
        for pt in self.path:
            ans.append(pt)
        while self.mother:
            for i in self.mother.path:
                ans.append(i)
            self.mother = self.mother.mother

    def move(self):
        while not self.dead_end and not self.finished:
            self.check_if_finished()
            self.move_next()
            self.print_cp()
            print(self.path)

    def print_cp(self):
        print(f"Cp : {self.cp}")

    def check_around(self):
        cp, maze, fn = self.cp, self.maze, []
        print(f"Args : {self.cp} ")
        directions = [cp[0], cp[1] - 1], [cp[0], cp[1] + 1], [cp[0] - 1, cp[1]], [cp[0] + 1, cp[1]]
        for i in directions:
            print(f"I : {i}")
            if 0 <= i[0] < len(maze) and 0 <= i[1] < len(maze[0]) and maze[i[0]][i[1]] == 1:
                print(f"{i} : {maze[i[0]][i[1]]}")
                fn.append(i)

        print(f"Final : {fn}")
        return fn

    @staticmethod
    def draw():
        for pnt in all_arrays:
            im.point([pnt[1], pnt[0]], fill=(0, 225, 0))


def find_one(arr):
    for i in range(len(arr)):
        if arr[i] == 1:
            return i


def paint_line(_image, _fill, points):
    for point in points:
        _image.point([point[1], point[0]], fill=_fill)


if __name__ == '__main__':
    s = Node(maze_data, [0, find_one(maze_data[0])], [len(maze_data) - 1, find_one(maze_data[-1])])
    print(ans)
    print(all_arrays)
    paint_line(im, (0, 0, 225), ans)
    qet.save('./Results/sample_three.png')





