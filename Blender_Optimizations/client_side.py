'''

 Look into client_side2


'''


import socket
import binascii
import struct
import numpy as np
# sock = socket.socket()
# sock.connect(('localhost', 8000))
# sock.send(b'hello, world!')
#  
# data = sock.recv(1024)
# sock.close()
#  
# print(data)

sock = socket.socket()
sock.connect(('localhost', 8000))

np_coords = np.empty((5,3), dtype = np.float64)
for i in range(5):
    for j in range(3):
        np_coords[i,j] = i + j * 0.1
        
np_string = np_coords.tostring()

values = (len(np_string), b'ab', 2.7)
packer = struct.Struct(b'I 2s f')
packed_data = packer.pack(*values)



try:
    # Send data
    sock.sendall(packed_data)
    sock.send(np_string.encode())
finally:
    sock.close()