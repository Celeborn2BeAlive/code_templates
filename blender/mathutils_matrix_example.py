import bpy
import mathutils
import math

for x in ['Cube', 'Suzanne']:
    if x in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[x])

bpy.ops.mesh.primitive_monkey_add(
    size=2, enter_editmode=False, location=(0, 0, 0))
suz = bpy.context.active_object

# create a location matrix
mat_loc = mathutils.Matrix.Translation((5.0, 0.0, 0.0))

# create a rotation matrix
mat_rot = mathutils.Matrix.Rotation(math.radians(45.0), 4, 'Z')
mat_rot2 = mathutils.Matrix.Rotation(math.radians(-45.0), 4, 'X')


# initiallay Suzanne and world coordinate system are identical.
suz.matrix_world = suz.matrix_world @ mat_loc
# this rotates around global z-axis
suz.matrix_world = mat_rot @ suz.matrix_world
# this rotates around local x-axis then translate along the local z axis
suz.matrix_world = suz.matrix_world @ mat_rot2 @ mathutils.Matrix.Translation(
    (0.0, 0.0, 3.0))
