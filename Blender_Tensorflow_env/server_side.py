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
    coords = tf.constant(np_coords, name="vects", dtype=tf.float32)
     
    #Variable for the center of sphere (ball)
    n_of_balls = 12
    centers_np = np.empty(shape=(n_of_balls,3), dtype=np.float32)

    for i in range(centers_np.shape[0]):
        centers_np[i,0] = np.random.random_sample()*2.0 - 1.0
#         i * n_of_balls
        centers_np[i,1] = np.random.random_sample()*2.0 - 1.0
        centers_np[i,2] = np.random.random_sample()*2.0 - 1.0
        
    centers = tf.Variable(centers_np, name='centers', dtype=tf.float32)
    
    #this node represents delta vector from center  to coordinate of blender object
    #delta is an array of tensors for each  Coordinate x CenterS
    delta = [t - centers for t in tf.unstack(coords)]
    
    #this node represents squared length of the delta vector - Pythagorean theorem
    r2 = [ d[ : , 0] * d[:,0] + d[ : , 1] * d[:,1] +  d[ : , 2] * d[:,2] for d in delta ]


    deltaC_array = [tf.div(1.0, ( 0.01 
                            + tf.square(centers[i,0] - centers[j,0])
                            + tf.square(centers[i,1] - centers[j,1])
                            + tf.square(centers[i,2] - centers[j,2])) ) for i in range(n_of_balls) for j in range(n_of_balls)]


#     print(deltaC_array)
    deltaC = tf.stack(deltaC_array)
        
#     for i in range(n_of_balls):    
#         for j in range(n_of_balls):
#             deltaC[i,j] = tf.div(1.0,0.01 )
#                              + (centers[i,0] - centers[j,0])**2 
#                              + (centers[i,1] - centers[j,1])**2
#                              + (centers[i,2] - centers[j,2])**2  )
#     for i in range(n_of_balls):
#         deltaC[i,j] = tf.constant(0.0)
            
    l_div_r2 = [tf.div(-1.0, t + 0.35) for t in r2]
    
    r_max2 = tf.reduce_sum(tf.stack(l_div_r2, 0)) + tf.reduce_sum(deltaC)
    
    r2_st  = tf.stack(r2)
    
#     r_rad  = [tf.reduce_min(t)    for t in r2 ]
    
#     r_rad_sum = tf.reduce_sum( tf.stack(r_rad))
    
    # this is standard part of magic from tensorflow
    learning_rate_placeholder = tf.placeholder(tf.float32, [], name='learning_rate')
    optimizer = tf.train.AdagradOptimizer(learning_rate=learning_rate_placeholder)
    train_centers = optimizer.minimize(r_max2)
     
#     train_radiuses  = optimizer.minimize(r_rad_sum)
    init = tf.global_variables_initializer()
 
    def optimize_and_return_data():
        session = tf.Session()
        session.run(init)
        
        for step in range(300):  
#             if step < 500:
#                 learning_rate = 2e-1
#             if step < 1000:
#                 learning_rate = 1e-2
#             if step < 4000:
#                 learning_rate = 1e-3    
#             if step < 9000:
#                 learning_rate = 1e-4           
#             if step < 12000:
#                 learning_rate = 5e-5  
            learning_rate = 1
            session.run(train_centers, feed_dict={learning_rate_placeholder: learning_rate})
            print("step", step, " r_max2:", session.run(r_max2))
            print(session.run(centers), session.run(deltaC))
            
        
        centers_np = session.run(centers)
        radius = np.empty((n_of_balls), dtype = np.float32)
        
    
        r2_np_cross = session.run(r2_st)
        print(r2_np_cross.shape)
        #send data back to blender
        port = 9010
        mySocket = socket.socket()
        mySocket.connect((host,port))
        
        res_data = np.empty(shape=(n_of_balls * 4))
        for i in range(n_of_balls):
            res_data[i*4 + 0] = centers_np[i][0]
            res_data[i*4 + 1] = centers_np[i][1]
            res_data[i*4 + 2] = centers_np[i][2]  
            res_data[i*4 + 3] = radius[i]                 
            
        
        message =  res_data.tostring()
        mySocket.send(message)               
        mySocket.close()
    
    
    
    optimize_and_return_data()
     
if __name__ == '__main__':
    Main()
