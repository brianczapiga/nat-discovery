#!/usr/bin/python3

import socket
import sys
import os
import json

local_ip = '0.0.0.0'
local_port = 9428
buffer_size = 1024
response_key = b'example-key\x00'

# echo -ne "nat-discovery\x00" | nc -vu server.address.com 9428
# server will reply with 5 bytes (ip address null terminated)

def main():
  udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  udp_server_socket.bind((local_ip, local_port))
  sys.stderr.write("Listening on " + local_ip + ":" + str(local_port) + "\n")

  os.chdir('/')
  n = os.fork()
  if not n:
    while True:
      (message, address) = udp_server_socket.recvfrom(buffer_size)

      byteaddress = bytearray([int(x) for x in (address[0].split('.'))])

      if message == response_key:
        udp_server_socket.sendto(byteaddress + b'\x00', address)

  sys.exit(0)

if __name__ == '__main__':
  main()
