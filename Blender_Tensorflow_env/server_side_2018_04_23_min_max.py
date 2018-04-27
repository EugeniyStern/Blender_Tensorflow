import socket
import tensorflow as tf
import numpy as np
'''
Get numpy data from script client_side2
'''
def Main():
    #     get data from blender
    host = "localhost"
    port = 9000
     
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
#         print(a)
            
    a_len3 = (int)(a.shape[0]/3)
    np_coords = a.reshape((a_len3, 3))
    print(np_coords.shape)
    conn.close()
    
    # build constant array of coordinates
    coords = tf.constant(np_coords, name="vects", dtype=tf.float64)
     
    #Variable for the center of sphere (ball)
    n_of_balls = 12
    centers_np = np.empty(shape=(n_of_balls,3), dtype=np.float32)

    for i in range(centers_np.shape[0]):
        centers_np[i,0] = np.power(-1,i) * 1
#         i * n_of_balls
        centers_np[i,1] = i * 0.2 / n_of_balls - 0.5
        centers_np[i,2] = np.power(-1,(int)(i/2)) * 1
        
    centers = tf.Variable(centers_np, name='centers', dtype=tf.float64)
    
    #this node represents delta vector from center  to coordinate of blender object
    #delta is an array of tensors for each pair coordinate-center
    delta = [t - centers for t in tf.unstack(coords)]
    
    #this node represents squared length of the delta vector - Pythagorean theorem
    r2 = [ d[ : , 0] * d[:,0] + d[ : , 1] * d[:,1] +  d[ : , 2] * d[:,2] for d in delta ]

    #this node takes the largest squared length from the center to most distant point of object
    # we will try to minimize this 
    r_min2_all= [tf.reduce_min(r2_e) for r2_e in r2 ]    
    
    r_max2 = tf.reduce_max(tf.stack(r_min2_all, 0))
    
    
    
    # this is standard part of magic from tensorflow
    learning_rate_placeholder = tf.placeholder(tf.float32, [], name='learning_rate')
    optimizer = tf.train.AdagradOptimizer(learning_rate=learning_rate_placeholder)
    train = optimizer.minimize(r_max2)
     
    init = tf.global_variables_initializer()
 
    def optimize_and_return_data():
        session = tf.Session()
        session.run(init)
        
        for step in range(30000):  
            if step < 500:
                learning_rate = 2e-1
            if step < 1000:
                learning_rate = 1e-2
            if step < 4000:
                learning_rate = 1e-3    
            if step < 9000:
                learning_rate = 1e-4           
            if step < 12000:
                learning_rate = 5e-5  
            learning_rate = 1
            session.run(train, feed_dict={learning_rate_placeholder: learning_rate})
            print("step", step, " radius:", np.sqrt(session.run(r_max2)))
            print(session.run(centers))    
    
    
    
        #send data back to blender
        port = 9010
        mySocket = socket.socket()
        mySocket.connect((host,port))
        
        res_data = np.empty(shape=(n_of_balls * 4))
        for i in range(n_of_balls):
            res_data[i*4 + 0] = session.run(centers)[i][0]
            res_data[i*4 + 1] = session.run(centers)[i][1]
            res_data[i*4 + 2] = session.run(centers)[i][2]  
            res_data[i*4 + 3] = np.sqrt(session.run(r_max2))                 
            
        
        message =  res_data.tostring()
        mySocket.send(message)               
        mySocket.close()
    
    
    
    optimize_and_return_data()
     
if __name__ == '__main__':
    Main()
