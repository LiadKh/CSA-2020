import time
from enum import Enum
from netcat import Netcat
import math
from sympy import symbols, solve


class Maze:
    MAX_TO_ASK = 10
    file_name = "sol.txt"

    @classmethod
    def write_to_file(cls, s):
        f = open(cls.file_name, 'a')
        # print(s)
        f.write(s)
        f.write('\n')
        f.close()

    def __init__(self, nc: Netcat, x: int, y: int):
        print("starting point: (" + str(x) + ", " + str(y) + ")")
        self.nc = nc
        self.x = x
        self.y = y
        self.maze = {}
        self.moves = 0
        self.equations = []

    def move(self, direction, remove=False):
        # print(self.get_pos())
        # print(self.x, self.y)

        old_options = self.get_options(self.x, self.y)
        options = old_options[:]

        # print("MOVE")
        # print(options)
        # print(direction)
        # print("(" + str(self.x) + ", " + str(self.y) + ") -> " + direction)
        # print(self.maze)
        Maze.write_to_file(str(options))

        if remove:
            if direction in options:
                options.remove(direction)
            self.maze[(self.x, self.y)] = options

        Maze.write_to_file("(" + str(self.x) + ", " + str(self.y) + ") -> " + direction)

        self.nc.write(direction)
        self.move_x_y(direction)

        print(self.nc.read_until(MazeKeys.COMMAND_INFO.value))

    def get_pos(self):
        self.nc.write(MazeKeys.POSITION.value)
        return tuple(map(int, self.nc.read_until(MazeKeys.COMMAND_INFO.value).split('\n')[0][1:-1].split(',')))

    def DFS(self, come_from=None):
        print("come_from", come_from)
        options = self.get_options(self.x, self.y)[:]
        options_old = options[:]
        if not come_from:
            for direction in options:
                self.move(direction, True)
                self.DFS(direction)
                # self.move((self.opposite_direction(direction)))
        else:
            if len(options) == 1:
                self.move(options[0], True)  # go back
            else:
                if self.opposite_direction(come_from) in options:
                    options.remove(self.opposite_direction(come_from))
                for direction in options:
                    if not self.visited_in(direction):
                        self.moves += 1
                        self.move(direction, True)
                        if self.moves >= Maze.MAX_TO_ASK:
                            self.moves = 0
                            self.ask()
                        self.DFS(direction)
                self.move(self.opposite_direction(come_from), True)

    def move_x_y(self, direction):
        if direction == MazeKeys.UP.value:
            self.y += 1
        elif direction == MazeKeys.DOWN.value:
            self.y -= 1
        elif direction == MazeKeys.LEFT.value:
            self.x -= 1
        if direction == MazeKeys.RIGHT.value:
            self.x += 1

    @staticmethod
    def opposite_direction(direction):
        return {
            MazeKeys.UP.value: MazeKeys.DOWN.value,
            MazeKeys.DOWN.value: MazeKeys.UP.value,
            MazeKeys.RIGHT.value: MazeKeys.LEFT.value,
            MazeKeys.LEFT.value: MazeKeys.RIGHT.value,
        }[direction]

    def get_options(self, x, y):
        options = self.maze.get((x, y))
        if options:
            return options
        self.nc.write(MazeKeys.OPTIONS.value)
        # self.nc.clean()
        options = self.nc.read_until(MazeKeys.NEW_LINE.value)
        print(self.nc.read_until(MazeKeys.COMMAND_INFO.value))
        # print(options)
        options = options.split(',')
        direction_dic = {k.strip(): int(v) for k, v in list(map(lambda o: o.split('='), options))}
        options = [k for k, v in direction_dic.items() if v]
        self.maze[(self.x, self.y)] = options
        return options
        # print(self.opt)

    def read(self):
        v = int(self.nc.read_until(MazeKeys.COMMAND_INFO.value).split('\n')[0])
        if v == 0:
            print(v)
        return v

    def ask(self):
        Maze.write_to_file("ASK DISTANCE")
        self.nc.write(MazeKeys.ASK.value)
        temp = self.nc.read_until(MazeKeys.COMMAND_INFO.value)
        print(temp)

        if temp.startswith(MazeKeys.DISTANCE.value):
            distance = int(temp[len(MazeKeys.DISTANCE.value):-len(MazeKeys.COMMAND_INFO.value)])
            pos = self.get_pos()
            print("distance " + str(distance))
            print("pos " + str(pos))
            self.equations.append([pos, distance])
        if len(self.equations) >= 2:
            self.solve()

    def visited_in(self, direction):
        x = self.x
        y = self.y
        if direction == MazeKeys.UP.value:
            y += 1
        elif direction == MazeKeys.DOWN.value:
            y -= 1
        elif direction == MazeKeys.LEFT.value:
            x -= 1
        if direction == MazeKeys.RIGHT.value:
            x += 1
        return self.maze.get((x, y)) is not None

    def solve(self):
        for i in range(len(self.equations)):
            for j in range(i + 1, len(self.equations)):
                (x1, y1), dis1 = self.equations[i]
                print((x1, y1), dis1)
                (x2, y2), dis2 = self.equations[j]
                print((x2, y2), dis2)

                x, y = symbols('x y')
                x, y = solve([x1 ** 2 - 2 * x1 * x + x ** 2 + y1 ** 2 - 2 * y1 * y + y ** 2 - dis1,
                              x2 ** 2 - 2 * x2 * x + x ** 2 + y2 ** 2 - 2 * y2 * y + y ** 2 - dis2],
                             [x, y])[1]
                try:
                    sol = (int(x), int(y))
                    print("sollllllllllllllll ", sol)
                    self.nc.write(MazeKeys.SOLUTION.value)
                    print(self.nc.read())
                    time.sleep(5)
                    self.nc.write(str(sol))
                    print(self.nc.read())
                    print(self.nc.read())
                    print(self.nc.read())
                    exit(1)
                except:
                    print("opsssssss ")
                    pass


class MazeKeys(Enum):
    UP = 'u'
    DOWN = 'd'
    LEFT = 'l'
    RIGHT = 'r'
    SOLUTION = 's'
    POSITION = 'c'
    OPTIONS = 'i'
    ASK = 'g'
    COMMAND_INFO = "> What is your command?\n"
    SOLUTION_INFO = "What is your solution?"
    DISTANCE = "Your distance from the treasure is √"
    NEW_LINE = "\n"
    FAR_WAY = "far far away"
