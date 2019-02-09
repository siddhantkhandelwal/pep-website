#! /usr/bin/python3

import socket

import config
import socklib

def requestUpdate(sock):
    request = 'Update requested.'
    socklib.sendmsg(sock, request)
    response = socklib.recvmsg(sock)
    print(response)

    status = socklib.recvmsg(sock)
    print('status:\n %s' % status)

    output = socklib.recvmsg(sock)
    print('output:\n %s' % output)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((config.HOST, config.PORT))
        requestUpdate(sock)

    except Exception as e:
        print("Exception: {}".format(e))

    finally:
        sock.close()
