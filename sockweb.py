import socket

HOST, PORT = "", 8888

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ls.bind((HOST, PORT))
ls.listen(10)

while True:
    cc, ca = ls.accept()
    req = cc.recv(1524)
    print req

    res = '''HTTP/1.1 200 OK
Content-Length: 5

[]22222222222222222'''
    print res
    cc.sendall(res)
