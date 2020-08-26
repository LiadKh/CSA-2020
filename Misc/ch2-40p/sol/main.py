import os

from PIL import Image

if __name__ == '__main__':

    # number of images (455846) = 1438 * 317
    WIDTH = 1438
    HEIGHT = 317
    PIXEL = 24
    result = Image.new('RGB', (HEIGHT, WIDTH))

    pos = 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            print(pos)
            im = Image.open(os.getcwd() + '/frames/image-' + str(pos + 1) + ".jpeg")
            result.putpixel((i, j), eval(str(im.getdata()[0])))
            pos += 1
    result.save('result.jpg')