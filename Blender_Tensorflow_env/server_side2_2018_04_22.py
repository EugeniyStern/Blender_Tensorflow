import socket
import tensorflow as tf
import numpy as np
'''
Get numpy data from script client_side2
'''
def Main():
    #     get data from blender
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
    np_coords = a.reshape((a_len3, 3))
    print(np_coords.shape)
    conn.close()
    
    # build constant array of coordinates
    coords = tf.constant(np_coords, name="vects", dtype=tf.float64)
    # print(coords)
    # print(np_coords_n)
    
    
    #Variable for the center of sphere (ball)
    center = tf.Variable([[0.0, 0.0, 0.0]], name='center', dtype=tf.float64)
    
    #this node represents delta vector from center  to coordinate of blender object
    delta = coords - center
    
    #this node represents squared length of the delta vector - Pythagorean theorem
    r2 = delta[ : , 0] * delta[:,0] + delta[ : , 1] * delta[:,1] +  delta[ : , 2] * delta[:,2]
    
    #this node takes the largest squared lendth from the center to most distant point of object
    # we will try to minimize this 
    r_max2 = tf.reduce_max(r2)
    
    init = tf.initialize_all_variables()
    
    
    
    # this is standard part of magic from tensorflow
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = optimizer.minimize(r_max2)
     
    init = tf.initialize_all_variables()
 
    def optimize():
        with tf.Session() as session:
            session.run(init)
            print("starting at", "center:", session.run(center), " radius:", np.sqrt(session.run(r_max2)))
            for step in range(200):  
                session.run(train)
                print("step", step, "center:", session.run(center), " radius:", np.sqrt(session.run(r_max2)))
    
    
    optimize()
    
     
if __name__ == '__main__':
    Main()
