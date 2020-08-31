import codecs
from zlib import crc32

from netcat import Netcat

enc_xor = b"CSA"

get_flag = "474554202f466c61672e6a706720485454502f312e310d0a557365722d4167656e743a204d6f7a696c6c612f352e30202857696e646f7773204e542031302e303b2057696e36343b2078363429204170706c655765624b69742f3533372e333620284b48544d4c2c206c696b65204765636b6f29204368726f6d652f37342e302e333732392e313639205361666172692f3533372e33360d0a486f73743a207777772e7475746f7269616c73706f696e742e636f6d0d0a4163636570742d4c616e67756167653a20656e2d75730d0a436f6e6e656374696f6e3a204b6565702d416c6976650d0a0d0a"

if __name__ == '__main__':
    nc = Netcat('52.28.255.56', 1080)
    nc.write(b"\x5a\x01\xfe\xdd\x74\x9c\x2e")
    response = nc.read()

    print("response: ", response.hex())
    after_version_chars = response[2]

    need_to_xor = response[3:6]
    print("before xor: " + need_to_xor.hex())

    current_checksum = response[6:]
    print("current checksum: " + current_checksum.hex())
    # 5a2cd2331fa90bb96a
    result = bytes()
    for i in range(len(need_to_xor)):
        result += bytes([int(hex(need_to_xor[i]), 16) ^ int(hex(enc_xor[i]), 16)])
    print("after xor: ", result.hex())
    need_checksum = (b"\x5a" + bytes([after_version_chars]) + result)
    print("need checksum: ", need_checksum.hex())

    checksum = format(crc32(need_checksum), "x")
    print("current checksum: ", checksum)
    full_message = bytes(need_checksum.hex() + checksum, encoding="utf-8")
    print("full message: ", full_message)
    as_str = ""
    for i in range(0, len(full_message), 2):
        as_str += full_message[i:i + 2].decode()
    print(as_str)
    new_mes = codecs.decode(as_str, 'hex')
    print("message to send: ", new_mes)
    nc.write(new_mes)
    nc.write(b"\x5a\x01\x00\x01\xc0\xa8\xad\x14\x00\x50\x62\x4A\x30\x63")
    print("response: ", nc.read().hex())
    nc.write(codecs.decode(get_flag, 'hex'))
    pic = b""
    try:
        while True:
            pic += nc.read()
    finally:
        flag = open('Flag.jpg', 'wb')
        flag.write(pic)
        flag.close()
        nc.close()
