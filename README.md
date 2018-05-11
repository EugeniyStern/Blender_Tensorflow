This is an example of how Blender can be connected to Python script running tensorflow.

The idea is:
1) First script reads and sends geometry of Blender object(s)  to second script using socket.
2) Second script gets data from socket and performs tensorflow magic.
3) Second script returns data to first scripts using socket.
4) First script makes some changes in Blender geometry.

First script(s) - Blender_Optimatazions/run_opt_sph.py, Blender_Optimatazions/run.py

Second script(s) - Blender_Tensorflow_env/server_side.py