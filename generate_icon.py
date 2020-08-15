import bpy
import random
import math
from pprint import pprint, pformat
import mathutils

################################################################################
# setup
################################################################################

print("heyo")
# bpy.app.debug = True  # set debug mode
bpy.context.preferences.view.show_splash = False  # disable splash
bpy.ops.object.delete()  # delete default cube (starts selected)
random.seed(1234567890)  # pin random seed

################################################################################
# set material color
################################################################################

print("Setting up material")

color = [0x00, 0xC0, 0xD3, 0xFF]
for i, c in enumerate(color):
    color[i] = float(c) / 255

material = bpy.data.materials["Material"]
material.diffuse_color = color
mat_nodes = material.node_tree.nodes
diffuse = mat_nodes["Principled BSDF"]
diffuse.inputs["Base Color"].default_value = color

################################################################################
# generate cubes
################################################################################

print("Setting up cubes")

size = 10
height = 10.0

for i in range(size):
    for j in range(size):
        # create cube
        x = -size // 2 + i + 0.5
        y = -size // 2 + j + 0.5
        z = 0
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))

        # resize cube
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))
        bpy.ops.transform.resize(value=(1, 1, 1.0 + height * random.random()))
        bpy.ops.transform.resize(value=(0.95, 0.95, 1.0))

        # set material
        bpy.ops.object.material_slot_add()
        cube = bpy.context.object
        cube.material_slots[0].material = material

################################################################################
# setup camera
################################################################################

print("Setting up camera")

camera = bpy.data.objects["Camera"]
camera.location = (0, 0, 50)
camera.rotation_euler = (0, 0, 0)
camera.data.type = "ORTHO"
camera.data.ortho_scale = 15

################################################################################
# setup light
################################################################################

print("Setting up light")

light = bpy.data.objects["Light"]
light.location = (5, 5, 5)
rx = math.radians(30.0)
ry = math.radians(0.0)
rz = math.radians(225.0)
eul = mathutils.Euler((rx, ry, rz), "ZXY")

light.rotation_euler = eul
light.data.type = "SUN"
light.data.use_nodes = True
light.data.node_tree.nodes["Emission"].inputs["Strength"].default_value = 0.01

################################################################################
# setup world
################################################################################

bkg_node = scene.world.node_tree.nodes["Background"]
bkg_node.inputs["Color"].default_value = (0.3, 0.3, 0.3, 1.0)

################################################################################
# setup render
################################################################################

print("Setting up render")

scene = bpy.data.scenes["Scene"]
scene.render.resolution_x = 800
scene.render.resolution_y = 800
scene.render.engine = "CYCLES"
scene.render.film_transparent = True
# scene.cycles.use_square_samples = True  # square samples

print("done")
