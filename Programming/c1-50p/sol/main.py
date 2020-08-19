from collections import Counter
import socket

HOST = '3.123.155.56'  # Standard loopback interface address (localhost)
PORT = 2222        # Port to listen on (non-privileged ports are > 1023)



def shared_chars(s1, s2):
    return sum((Counter(s1) & Counter(s2)).values())


# print(shared_chars('rac', 'carts'))
if __name__ == '__main__':
    text_file = open("words.txt", "r")
    lines = text_file.read().split('\n')
    # for v in lines:
    #     print(v)
    text_file.close()
    while True:
        word = input("Enter word: ")
        print(word)
        good = input("Good: ")
        print(good)

        lines = [v for v in lines if shared_chars(v, word) >= int(good)]
        if len(lines) == 1:
            break
    print("SOL: ",lines)
