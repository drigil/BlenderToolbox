# # if you want to call the toolbox the old way with `blender -b -P demo_XXX.py`, then uncomment these two lines
# import sys, os
# sys.path.append("../../BlenderToolbox/")
import blendertoolbox as bt 
import bpy
import os
import numpy as np
cwd = os.getcwd()

# outputPath = os.path.join(cwd, './cow_head.png') # make it abs path for windows

## initialize blender
imgRes_x = 1024 
imgRes_y = 1024
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
## read mesh (choose either readPLY or readOBJ)
# meshPath = 'C:/Users/anshu/source/repos/Neural-TSpline/output_obj_textured/cow_head_reconstructed.obj'
# meshPath = 'C:/Users/anshu/source/repos/Neural-TSpline/data/cow_head/cow_head/mesh_uv.obj'
model = "bimba_head_texture_neural_003_trimmed" # mesh_uv, bimba_head_err_neural_003, bimba_head_texture_neural_003_trimmed
meshPath = '../meshes/' + model + '.obj'
outputPath = os.path.join(cwd, './' + model + '_texture.png') # make it abs path for windows


# location = (0.457694, 0.216293, 0.121025) # (GUI: click mesh > Transform > Location)
# rotation = (106.883, 6.79254, 255.689) # (GUI: click mesh > Transform > Rotation)

# location = (0.397694, -0.263707, -0.158975) # (GUI: click mesh > Transform > Location)
# rotation = (118.883, 1.7925, 319.69) # (GUI: click mesh > Transform > Rotation)

# location = (0.76769, -0.25371, -0.168975) # (GUI: click mesh > Transform > Location)
# rotation = (131.883, -11.207, 307.689) # (GUI: click mesh > Transform > Rotation)

# location = (0.737694, 0.356293, -0.088975) # (GUI: click mesh > Transform > Location)
# rotation = (119.883, 10.7925, 232.689) # (GUI: click mesh > Transform > Rotation)
# scale = (1.5,1.5,1.5) # (GUI: click mesh > Transform > Scale)

# Full model
location = (0.83, -0.09, 0.23) # (UI: click mesh > Transform > Location)
rotation = (58, -15, 77) # (UI: click mesh > Transform > Rotation)
scale = (1.373,1.373,1.373) # (UI: click mesh > Transform > Scale)

mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() 

## subdivision
# bt.subdivision(mesh, level = 2)

# # set material (TODO: this has some new issue due to new version of Blender)
# colorObj(RGBA, H, S, V, Bright, Contrast)
useless = (0,0,0,1)
meshColor = bt.colorObj(useless, 0.5, 1.0, 1.0, 0.0, 0.0)
# texturePath = '../meshes/spot_by_keenan.png' 
texturePath = 'C:/Users/anshu/source/repos/Neural-TSpline/data/cow_head/cow_head/material_0_rotated_textless.png'
# texturePath = 'C:/Users/anshu/source/repos/Neural-TSpline/output_obj_textured/eikonal.png'

bt.setMat_texture(mesh, texturePath, meshColor)

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