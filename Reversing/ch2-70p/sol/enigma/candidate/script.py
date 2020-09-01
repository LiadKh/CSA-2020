import string
import time

from netcat import Netcat

HOST = "18.156.68.123"
PORT = 80

if __name__ == '__main__':
    flag = "MHD{YX_J_WMVKCCE_TC_KFGHFJVK_SU_JC_YRMQVSHFM_CU_AOAUGE_OOPP_LT_MLWJBIONOCN}"
    flag = ''.join(x for x in flag if x.isalpha())
    to_send = """
    HELLO FIELD AGENT!
    COMMANDS:
        SEND-SECRET-DATA
        GET-SECRET-DATA
        GOODBYE
        """
    dec = ""
    l = []
    to_send = ''.join(x for x in to_send if x.isalpha())
    for c in string.ascii_uppercase:
        loc = to_send.find(c)
        if loc != -1:
            l.append((c, to_send.find(c)))

    for i in range(len(flag)):
        for letter, pos in l:
            nc = Netcat(HOST, PORT)
            nc.read()
            nc.read()
            nc.write("AAAAAAAAAA\n")
            nc.read()
            secret = nc.read().split("\n")[4].strip()
            # print(secret)
            nc.write("A\n")
            nc.read()
            nc.read()
            nc.write(secret + "\n")
            flag_current = nc.read_until("\n")
            flag_current = ''.join(x for x in flag_current if x.isalpha())
            nc.read()
            send_a = pos
            while send_a > len(string.ascii_uppercase):
                send_a -= len(string.ascii_uppercase)
            send_a = 13 - send_a  # GET-SECRET-DATA
            if send_a < 0:
                send_a += len(string.ascii_uppercase)
            s = "AAAAAAAAAAAAAAAAAAAAAAAAA" + "A" * i + "A" * send_a
            # print(s)
            nc.write(s + "\n")
            nc.read()
            res = nc.read()
            res = ''.join(x for x in res if x.isalpha())
            if res[pos] == flag_current[i]:
                dec += letter
                print(dec)
                print((letter, i))
                nc.close()
                break
            # print()
            nc.close()
