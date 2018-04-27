import socket
import binascii
import struct
import sys

class spheres_on_top:

    def __init__(self, obj, levels):
        self.obj = obj
        self.levels = levels

         
        sock = socket.socket()
        sock.connect(('localhost', 8000))
#         sock.send(b'hello, world!')
         
#         data = sock.recv(1024)
#         sock.close()
#          
#         print(data)        
#         pass

        values = (1, b'ab', 2.7)
        packer = struct.Struct(b'I 2s f')
        packed_data = packer.pack(*values)
        
        try:
            # Send data
            sock.sendall(packed_data)
        
        finally:
            sock.close()
    
    def _build_tree(self):
        
        pass
    
    def draw_object(self, canvas):
        pass
    
    
    
