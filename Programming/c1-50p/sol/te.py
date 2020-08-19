import socket
import time
from collections import Counter

HOST = '3.123.155.56'  # Standard loopback interface address (localhost)
PORT = 2222  # Port to listen on (non-privileged ports are > 1023)


def shared_chars(s1, s2):
    return sum((Counter(s1) & Counter(s2)).values())


class Netcat:
    """ Python 'netcat like' module """

    def __init__(self, ip, port):
        self.buff = b""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length=1024):
        """ Read 1024 bytes off the socket """

        return self.socket.recv(length)

    def read_until(self, data, first=False):
        """ Read data into the buffer until we have data """
        if first:
            time.sleep(5)
        while not str.encode(data) in self.buff:
            self.buff += self.socket.recv(1024)
            print(self.buff)

        if first:
            self.buff = ""
            pass
        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]

        return rval

    def printAll(self):
        while True:
            print(self.socket.recv(1024))
            time.sleep(1)

    def write(self, data):
        self.socket.send(str.encode(data))
        time.sleep(1)

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    nc = Netcat(HOST, PORT)

    text_file = open("words.txt", "r")
    lines = text_file.read().split('\n')
    text_file.close()
    nc.read_until('GO', True)
    for word in lines:
        nc.write(word)
        good = int(nc.read())
        print(word, good)
        lines = [v for v in lines if shared_chars(v, word) >= int(good)]
        if len(lines) == 1:
            break

    print("SOL: ", lines)
    nc.write(lines[0])

    nc.printAll()
    nc.close()
