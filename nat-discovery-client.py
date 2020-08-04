#!/usr/bin/python3

import socket

server_address = 'server.address.com'
server_port = 9428
server_key = 'example-key\x00'

def nat_discovery_client(server_address, server_port, server_key):
  bytes_to_send = str.encode(server_key)
  buffer_size = 1024

  udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  udp_client_socket.settimeout(5)
  udp_client_socket.sendto(bytes_to_send, (server_address, server_port))

  try:
    (message, address) = udp_client_socket.recvfrom(buffer_size)
    if len(message) != 5:
      # received something other than 5 bytes
      print('expected 5 bytes, received ' + str(message[2]))
      return None

    if message[4] != 0:
      # 5th byte was not null (string was not null terminated?)
      return None

    address = '.'.join([str(int(message[x])) for x in range(0,4)])
    return address
  except socket.timeout:
    # timed out
    return None

def main():
  print(nat_discovery_client(server_address, server_port, server_key))

if __name__ == '__main__':
  main()
