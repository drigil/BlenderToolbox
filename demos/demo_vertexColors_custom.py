import blendertoolbox as bt 
import bpy
import os
import numpy as np
cwd = os.getcwd()

model = "bimba_head_err_neural_003" # bimba_head_err_neural, bimba_head_err_traditional
outputPath = os.path.join(cwd, './' + model + '_vertex_colors.png') # make it abs path for windows

## initialize blender
imgRes_x = 1024 
imgRes_y = 1024
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# Enable transparent background
bpy.context.scene.render.film_transparent = True

# Set output format to PNG with RGBA
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

## read mesh (choose either readPLY or readOBJ)
meshPath = '../meshes/' + model + '.obj'
location = (0.83, -0.09, 0.23) # (UI: click mesh > Transform > Location)
rotation = (58, -15, 77) # (UI: click mesh > Transform > Rotation)
scale = (1.373,1.373,1.373) # (UI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() 

## subdivision
# bt.subdivision(mesh, level = 2)

## Create a material that uses vertex colors
material = bpy.data.materials.new(name="VertexColorMaterial")
material.use_nodes = True

# Get the material's node tree
nodes = material.node_tree.nodes
links = material.node_tree.links

# Clear existing nodes
for node in nodes:
    nodes.remove(node)

# Add necessary nodes
output_node = nodes.new(type='ShaderNodeOutputMaterial')
output_node.location = (400, 0)

diffuse_node = nodes.new(type='ShaderNodeBsdfDiffuse')
diffuse_node.location = (200, 0)

attribute_node = nodes.new(type='ShaderNodeAttribute')
attribute_node.location = (0, 0)
attribute_node.attribute_name = "Color"  # "Col" is the default name for vertex colors

# Link the nodes
links.new(attribute_node.outputs["Color"], diffuse_node.inputs["Color"])
links.new(diffuse_node.outputs["BSDF"], output_node.inputs["Surface"])

# Assign the material to the mesh
mesh.data.materials.append(material)

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
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

## save rendering
bt.renderImage(outputPath, cam)
