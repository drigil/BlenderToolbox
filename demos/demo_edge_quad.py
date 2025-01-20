import blendertoolbox as bt 
import bpy
import os
import numpy as np
cwd = os.getcwd()

model = "bimba_simplified_original_scaled" # bimba_head_err_neural, bimba_head_err_traditional, bimba_head_err_original, bimba_head_err_traditional_regularized_003, bimba_head_err_neural_003
outputPath = os.path.join(cwd, './' + model + '_wireframe_overlay.png') # make it abs path for windows

## initialize blender
imgRes_x = 1024 # recommend > 1080 
imgRes_y = 1024 # recommend > 1080 
numSamples = 100 # recommend > 200
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
meshPath = '../meshes/' + model + '.obj'

location = (1.03, 0, 0.91) # (UI: click mesh > Transform > Location)
rotation = (63, -7, 81) # (UI: click mesh > Transform > Rotation)
scale = (0.802883,0.802883,0.802883) # (UI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading for mesh (solid shading)
bpy.ops.object.shade_smooth()

# Duplicate the mesh for wireframe rendering
solid_mesh_obj = bpy.context.object
wireframe_mesh_obj = solid_mesh_obj.copy()
wireframe_mesh_obj.data = solid_mesh_obj.data.copy()  # Copy the mesh data
bpy.context.collection.objects.link(wireframe_mesh_obj)  # Link the duplicate mesh to the collection

# Set the original mesh (solid) to be solid and apply the material
solid_mesh_obj.display_type = 'SOLID'  # Solid shading for mesh
solid_material = bpy.data.materials.new(name="Solid_Material")
solid_material.use_nodes = True
solid_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (1, 1, 1, 1)  # Opaque white
solid_material.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 1.0  # Fully opaque
solid_mesh_obj.data.materials.append(solid_material)

# Set the duplicate mesh (wireframe) to wireframe mode
wireframe_mesh_obj.display_type = 'SOLID'  # Wireframe will be drawn on top of the solid object
wireframe_modifier = wireframe_mesh_obj.modifiers.new(name="Wireframe", type='WIREFRAME')
wireframe_modifier.thickness = 0.005  # Adjust the thickness of the wireframe
wireframe_modifier.use_even_offset = True  # Use even offset for consistent wireframe appearance

# Create a wireframe material
wireframe_material = bpy.data.materials.new(name="Wireframe_Material")
wireframe_material.use_nodes = True
wireframe_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)  # Black wireframe color
wireframe_material.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 1.0  # Fully opaque
wireframe_mesh_obj.data.materials.append(wireframe_material)

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation = (3, 0, 2)
lookAtLocation = (0,0,0.5)
focalLength = 45 # (UI: click camera > Object Data > Focal Length)
cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

## set light
lightAngle = (6, -30, -155) 
strength = 2
shadowSoftness = 0.3
sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

## set ambient light
bt.setLight_ambient(color=(0.1,0.1,0.1,1)) 

## set gray shadow to completely white with a threshold 
bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

## save blender file so that you can adjust parameters in the UI
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test_wireframe_overlay.blend')

## save rendering
bt.renderImage(outputPath, cam)
