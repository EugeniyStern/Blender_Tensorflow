'''

 Look into server_side2


'''

import binascii
import socket
import struct
import sys
import tensorflow as tf

# Create a TCP/IP socket

hello = tf.constant('Hello, TensorFlow!')

# Start tf session
sess = tf.Session()

# Run the op
print(sess.run(hello))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8000)
sock.bind(server_address)
sock.listen(1)

unpacker = struct.Struct(b'I 2s f')

while True:
    connection, client_address = sock.accept()
    try:
        data = connection.recv(unpacker.size)
        unpacked_data = unpacker.unpack(data)
        print(unpacked_data)
        
    finally:
        data = connection.recv(unpacked_data[0]).decode()
        print(data.encode())        
        connection.close()


