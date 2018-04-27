import bpy
import bmesh
import math
import numpy as np
import mathutils
import pydevd
import socket

import bgl
import blf
import bpy_extras.image_utils as img_utils

pydevd.settrace()
import send_structure_using_packer

object = bpy.context.object

pydevd.settrace()
print(object.name)

       
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
# Magic results to 
# =====================================================

# for edge in mesh.edges:
#     print(verts[vert].x, verts[vert].y, verts[vert].y)

# =====================================================
# Output to image for tests
# =====================================================


# Get the render image
path = "C:\\ws3_ox\\DebugBlender_test_a\\src\\aa.png"
try:
    result = bpy.data.images['Render Result']
    if result.has_data is False:
        bpy.ops.render.render()
        result = bpy.data.images['Render Result']
except:
    bpy.ops.render.render()
    result = bpy.data.images['Render Result']





# Save and reload
result.save_render(path)
img = img_utils.load_image(path)





viewport_info = bgl.Buffer(bgl.GL_INT, 4)
bgl.glGetIntegerv(bgl.GL_VIEWPORT, viewport_info)

scene = bpy.context.scene
render_scale = scene.render.resolution_percentage / 100

WIDTH  = int(scene.render.resolution_x * render_scale)
HEIGHT = int(scene.render.resolution_y * render_scale)

# Load image on memory
img.gl_load(0, bgl.GL_NEAREST, bgl.GL_NEAREST)
tex = img.bindcode

# Create output image (to apply texture)
out = bpy.data.images.new("output", WIDTH, HEIGHT)
buffer = bgl.Buffer(bgl.GL_FLOAT, WIDTH * HEIGHT * 4)

bgl.glDisable(bgl.GL_SCISSOR_TEST) # if remove this line, get blender screenshot not image 
bgl.glViewport(0, 0, WIDTH, HEIGHT)

bgl.glMatrixMode(bgl.GL_PROJECTION)
bgl.glLoadIdentity()
bgl.gluOrtho2D(0, WIDTH, 0, HEIGHT)

# 
bgl.glLineWidth(10)
bgl.glBegin(bgl.GL_LINES)

bgl.glColor4f(1.0, 0.0, 0.0, 1.0)
#bgl.glTexCoord2f(0.0, 0.0)
bgl.glVertex2f(0.0, 0.0)
#bgl.glTexCoord2f(1.0, 1.0)
bgl.glVertex2f(WIDTH, HEIGHT)

bgl.glEnd()

bgl.glLineWidth(1)
bgl.glColor4f(1, 1.0, 0.0, 1)  
for poly in mesh.polygons:
    bgl.glBegin(bgl.GL_LINES)
    for vert in poly.vertices:
        bgl.glVertex2f((int)(200 + 80 * verts[vert].x),(int)(400 + 80 * verts[vert].y))
    bgl.glEnd()

bgl.glColor4f(0, 1.0, 1.0, 1)  
for edge in mesh.edges:
    bgl.glBegin(bgl.GL_LINES)
    for vert in edge.vertices:
        bgl.glVertex2f((int)(500 + 80 * verts[vert].x),(int)(400 + 80 * verts[vert].y))
    bgl.glEnd()
    
    
# Draw a Text
font_id = 0
bgl.glColor4f(1.0, 1.0, 0.0, 1.0)
blf.size(font_id, 18, 72)
blf.position(font_id, 0.5, 0.5, 0)
blf.draw(font_id, "Hello World")   

#
bgl.glFinish()
bgl.glReadPixels(0, 0, WIDTH, HEIGHT , bgl.GL_RGBA, bgl.GL_FLOAT, buffer) # read image data
out.pixels = buffer[:] # Assign image data
img.gl_free() # free opengl image memory

#reset
bgl.glEnable(bgl.GL_SCISSOR_TEST)
# restore opengl defaults
bgl.glLineWidth(1)
bgl.glDisable(bgl.GL_BLEND)
bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

