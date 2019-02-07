#! /usr/bin/python3
# The PEP Updater Client - By Hypro999

import os
import socket

HOST = '139.59.3.240'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	print('PEP portal updater socket attempting connection to %s:%d [process id: %d]' % (HOST, PORT, os.getpid()))
	s.connect((HOST, PORT))
	for _ in range(3):
		data = s.recv(1024)
		print(">>> " + data.decode('ascii'))
