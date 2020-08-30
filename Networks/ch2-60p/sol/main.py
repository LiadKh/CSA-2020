from arc4 import ARC4

from netcat import Netcat

f = open("./CS-hAcked/dictionary.txt", "r")
words = ["b75aa7537b306a86391733e2e6",
         "6ed101ee76155ffc90da9fb05cf5bb",
         "d51f",
         "494c13",
         "bac2",
         "341b5ebe22cd432c4a7994d4bc4a",
         "3e3217f7e110",
         "75efbf54557ced",
         "4bbd1eebc033fc30",
         "bffdd8b81f0c9c96f055"]
flag = {}
for line in f:
    for i in range(len(words)):
        # 2 bytes per once char
        if len(words[i]) / 2 == len(line):
            if not flag.get(str(i)):
                flag[str(i)] = []
            flag[str(i)].append(line)
            print(i, line)
f.close()

words = []
words_len = 1
for i in range(len(flag)):
    words_len *= len(flag.get(str(i)))

for i in range(words_len):
    words.append([])

rounds = words_len
r_rounds = 1
for i in range(len(flag)):
    w = flag.get(str(i))
    rounds = int(rounds / len(w))
    r_rounds *= len(w)

    for j in range(r_rounds):
        word = w[j % len(w)]
        for k in range(rounds):
            words[j * rounds + k].append(word)
print(words)

for word in words:
    w_to_send = ("".join(map(str, word)))
    arc4 = ARC4(b"csa-mitm-key")
    nc = Netcat("3.126.154.76", 80)
    nc.read()
    print(arc4.encrypt(nc.read()))
    nc.write(bytes(arc4.encrypt(w_to_send)) + b"\n")
    print(arc4.decrypt(nc.read()))
    nc.close()
