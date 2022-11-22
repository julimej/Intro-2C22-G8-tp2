import socket
address = ('10.0.0.2', 3000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
f = open('a.txt', 'w+')

while True:
    data, addr = s.recvfrom(1024)
    print ('data', data)
    f.write(str(data))
    f.flush()
f.close()
s.close()