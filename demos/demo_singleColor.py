# # if you want to call the toolbox the old way with `blender -b -P demo_XXX.py`, then uncomment these two lines
# import sys, os
# sys.path.append("../../BlenderToolbox/")
import blendertoolbox as bt 
import bpy
import os
import numpy as np
cwd = os.getcwd()

model = "bimba_head_err_neural_003" # bimba_head_err_neural, bimba_head_err_traditional, bimba_head_err_original, bimba_head_err_traditional_regularized_003, bimba_head_err_neural_003
outputPath = os.path.join(cwd, './' + model + '.png') # make it abs path for windows

## initialize blender
imgRes_x = 512 # 1024, 1024, 512
imgRes_y = 512 # 1024, 390, 512
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)
bpy.context.scene.render.film_transparent = True

## read mesh (choose either readPLY or readOBJ)
meshPath = '../meshes/' + model + '.obj'

# Full model
location = (0.83, -0.09, 0.23) # (UI: click mesh > Transform > Location)
rotation = (58, -15, 77) # (UI: click mesh > Transform > Rotation)
scale = (1.373,1.373,1.373) # (UI: click mesh > Transform > Scale)

# Eye zoom in
location = (2.12, 0.15, 0.92) # (UI: click mesh > Transform > Location)
rotation = (53, -46, 51) # (UI: click mesh > Transform > Rotation)
scale = (1.373,1.373,1.373) # (UI: click mesh > Transform > Scale)

# Ear zoom in
location = (2.3, 0.15, 0.99) # (UI: click mesh > Transform > Location)
rotation = (47, -9, 123) # (UI: click mesh > Transform > Rotation)
scale = (1.373,1.373,1.373) # (UI: click mesh > Transform > Scale)


mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() 

## subdivision
# bt.subdivision(mesh, level = 2)

# # set material (TODO: this has some new issue due to new version of Blender)
lightGreen = (144./255, 238./255, 144./255, 1)
meshColor = bt.colorObj(lightGreen, 0.5, 1.0, 1.0, 0.0, 2.0) #  derekBlue, coralRed, lightGreen
AOStrength = 0.0
bt.setMat_singleColor(mesh, meshColor, AOStrength)

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