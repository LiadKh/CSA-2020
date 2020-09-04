import os
from enum import Enum

from PIL import Image, ImageDraw


class Move(Enum):
    UP = 1
    DOWN = -1
    RIGHT = 1
    LEFT = -1
    DONT_MOVE = 0


FOLDER = "Modify"
MAP_FILE_NAME = 'game-map.jpg'


def get_file_name(number):
    return "Recordings/" + str(number) + ".BIN"


def get_file_name_mod(number):
    return FOLDER + "/" + str(number) + ".jpg"


if __name__ == '__main__':

    try:
        os.mkdir(FOLDER)
    except OSError:
        print("Creation of the directory %s failed" % FOLDER)
    else:
        print("Successfully created the directory %s " % FOLDER)

    for i in range(1, 17):
        moves = []
        with open(get_file_name(i), 'rb') as fp:
            while True:
                current_byes = fp.read(8)
                if not current_byes:
                    break
                x = Move.RIGHT.value if current_byes[4] == 129 else Move.LEFT.value if current_byes[
                                                                                           4] == 127 else Move.DONT_MOVE.value
                y = Move.UP.value if current_byes[6] == 129 else Move.DOWN.value if current_byes[
                                                                                        4] == 127 else Move.DONT_MOVE.value
                moves.append((current_byes[0], x, y))

        pos = (720, 610)
        with Image.open(MAP_FILE_NAME) as im:
            draw = ImageDraw.Draw(im)
            for count, x, y in moves:
                new_pos = (pos[0] - (count * x) * 1.7, pos[1] - (count * y) * 2)
                draw.line([pos, new_pos], width=3)
                pos = new_pos
            im.save(get_file_name_mod(i), "JPEG")
