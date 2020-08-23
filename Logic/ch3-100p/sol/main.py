from maze import Maze
from netcat import Netcat

HOST = 'maze.csa-challenge.com'
PORT = 80

if __name__ == '__main__':
    nc = Netcat(HOST, PORT)

    nc.read_until('(')
    pos = nc.read_until(')')
    x, y = pos[:len(pos) - 1].split(",")
    nc.read()
    nc.clean()
    index = 0
    maze = Maze(nc, int(x), int(y))
    while True:
        try:
            maze.DFS()
        except RecursionError:
            index += 1
            print("RecursionError" + str(index))
    nc.close()
