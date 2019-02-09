import socket

def sendmsg(sock, msg):
    """ A technique to send messages of varying length."""
    message = msg
    if not type(msg) == bytes:
        message = msg.encode('ascii')
    length = len(message)
    if length > 9999:
        raise OverflowError('Message is too large.')
    length = "%.4d" % length
    s = sock.send(length.encode('ascii'))
    if s == 0:
        raise RuntimeError('Socket connection broke!')
    s = sock.send(message)
    if s == 0:
        raise RuntimeError('Socket connection broke!')

def recvmsg(sock):
    """ The complement to sendmsg where we receive messages
        of varying length. """
    length = sock.recv(4)
    if not length or length == 0:
        raise RuntimeError('Socket connection broke!')
    length = int(length.decode('ascii'))
    message = sock.recv(length)
    if message == 0:
        raise RuntimeError('Socket connection broke!')
    return message.decode('ascii')
