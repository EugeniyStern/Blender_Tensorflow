import socket
import numpy as np
'''
Get numpy data from script client_side2
'''
def Main():
    host = "localhost"
    port = 8000
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    a = np.empty((0), dtype = np.float64)
    while True:
        data = conn.recv(1024)
        if not data:
                break
        a = np.append(a,np.fromstring(data))
        print(a)
            
    a_len3 = (int)(a.shape[0]/3)
    coords = a.reshape((a_len3, 3))
    print(coords.shape)
    conn.close()
     
if __name__ == '__main__':
    Main()