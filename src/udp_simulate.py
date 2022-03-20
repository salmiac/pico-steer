import struct
import time
import socket

client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.settimeout(0.2)

switch = True

while True:
    # client.sendto(bytes([0x80,0x81, 0x7f, 0xC7, 1, 0, 0x47]), ('255.255.255.255',9999))

    data = bytearray([0x80, 0x81, 0x7e, 0xfd, 0x08])
    wheel_angle_int = 1
    for b in struct.pack('<H', wheel_angle_int):
        data.append(b)
    heading_int = 2
    for b in struct.pack('<H', heading_int):
        data.append(b)
    roll_int = 3
    for b in struct.pack('<H', roll_int):
        data.append(b)

    switch = not switch
    data.append(0b1111_1101 if switch else 0xff)
    data.append(0x80)

    crc = 0
    for byte in data[2:]:
        crc += byte
    crc %= 256
    data.append(crc)
    
    client.sendto(bytes(data), ('255.255.255.255',9999))

    time.sleep(2)

