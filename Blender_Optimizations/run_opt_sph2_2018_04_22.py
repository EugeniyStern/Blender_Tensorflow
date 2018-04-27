import bpy
import bmesh
import math
import numpy as np


# import pydevd
import socket


object = bpy.context.object

# pydevd.settrace()
# print(object.name)

       
link = False 
with bpy.data.libraries.load("C:\\eclipse\\blender_models\\study\\fish.blend",link=link) as (df, dt):
    dt.objects = df.objects #['girl_hair']


#link object to current scene
scene = bpy.context.scene
for obj in dt.objects:
    if obj is not None:
       scene.objects.link(obj)

obj = bpy.data.objects['fish_a']

#NewSphere = send_structure_using_packer.spheres_on_top(obj, 3)

if obj.mode == 'EDIT':
    bm = bmesh.from_edit_mesh(obj.data)
    vertices = bm.verts

else:
    vertices = obj.data.vertices

# =====================================================
# Magic is here
# =====================================================

apply_modifiers = True
settings = 'RENDER'
mesh = obj.to_mesh(scene,apply_modifiers,settings)

verts = [obj.matrix_world * vert.co for vert in mesh.vertices] 

# =====================================================
# Blender to Numpy
# =====================================================
verts_np = np.empty(shape=(len(mesh.vertices),3), dtype=np.float64)  

for i in range(len(mesh.vertices)):
    verts_np[i,0] = verts[i][0]
    verts_np[i,1] = verts[i][1]
    verts_np[i,2] = verts[i][2] 

host = 'localhost'
port = 8000
 
mySocket = socket.socket()
mySocket.connect((host,port))

message =  verts_np.tostring()
mySocket.send(message)               
mySocket.close()

