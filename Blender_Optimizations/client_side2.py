import socket
import numpy as np

'''
Send numpy data to script serv_side2
'''

np_coords = np.empty((5000,3), dtype = np.float64)

def Main():
        host = 'localhost'
        port = 8000
         
        mySocket = socket.socket()
        mySocket.connect((host,port))

        for i in range(5000):
            for j in range(3):
                np_coords[i,j] = i + j * 0.1

        message =  np_coords.tostring()
        mySocket.send(message)               
        mySocket.close()
 
if __name__ == '__main__':
    Main()