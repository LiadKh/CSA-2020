import socket


class Netcat:
    file_name = "sol.txt"

    def __init__(self, ip, port):
        Netcat.write_to_file("////////////////////////////////////////////////////////////////////////////////////")
        Netcat.write_to_file("staring")

        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    @classmethod
    def write_to_file(cls, s):
        f = open(cls.file_name, 'a')
        # print(s)
        f.write(s)
        f.write('\n')
        f.close()

    def read(self, length=1024):
        """ Read 1024 bytes off the socket """
        val = self.socket.recv(length).decode("utf-8")
        Netcat.write_to_file(val)
        return val

    def read_until(self, data):
        """ Read data into the buffer until we have data """

        while not data in self.buff:
            self.buff += self.socket.recv(1024).decode("utf-8")

        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]

        Netcat.write_to_file(rval)

        return rval

    def read_all_none_stop(self):
        Netcat.write_to_file("read none stop")
        while True:
            val = self.socket.recv(1024).decode("utf-8")
            Netcat.write_to_file(val)
            # print(val)
            # time.sleep(1)

    def clean(self):
        Netcat.write_to_file("cleaning")
        Netcat.write_to_file(self.buff)
        temp = self.buff
        self.buff = ""
        return temp

    def write(self, data):
        # Netcat.write_to_file("writing")
        # print(data)
        Netcat.write_to_file(data)
        self.socket.send(str.encode(data))
        # time.sleep(1)

    def close(self):
        Netcat.write_to_file("closing")
        Netcat.write_to_file(self.buff)
        self.socket.close()
