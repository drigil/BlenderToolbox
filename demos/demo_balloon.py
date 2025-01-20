# # if you want to call the toolbox the old way with `blender -b -P demo_XXX.py`, then uncomment these two lines
# import sys, os
# sys.path.append("../../BlenderToolbox/") 
import blendertoolbox as bt
import bpy
import os
import numpy as np
import argparse

cwd = os.getcwd()

# Parse through command line arguments
parser = argparse.ArgumentParser(description="Process some arguments.")

# Add arguments
# parser.add_argument("mesh_path", type=str, nargs="?", default= '../meshes/spot.ply', help="Path to mesh")
# parser.add_argument("output_path", type=str, nargs="?", default= './demo_balloon.png', help="Path to output png")

obj_name = "bimba_head_err_traditional_fixed_normals" # bimba_head_err_traditional, bimba_head_err_traditional_fixed_normals
parser.add_argument("mesh_path", type=str, nargs="?", default= '../meshes/' + obj_name + '.obj', help="Path to mesh")
parser.add_argument("output_path", type=str, nargs="?", default= './' + obj_name + '.png', help="Path to output png")


# Parse the arguments
args = parser.parse_args()

outputPath = os.path.join(cwd, args.output_path) # make it abs path for windows


## initialize blender
print("Initialized")
imgRes_x = 1024
imgRes_y = 1024
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
print("Read in Mesh")
meshPath = args.mesh_path
location = (0.83, -0.09, 0.23) # (UI: click mesh > Transform > Location)
rotation = (58, -15, 77) # (UI: click mesh > Transform > Rotation)
scale = (1.373,1.373,1.373) # (UI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
print("Set Shading")
bpy.ops.object.shade_smooth() 

## subdivision
# bt.subdivision(mesh, level = 2)

# # set material
print("Set Material")
# colorObj(RGBA, H, S, V, Bright, Contrast)
meshColor = bt.colorObj(bt.derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
AOStrength = 0.0
bt.setMat_balloon(mesh, meshColor, AOStrength)

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
print("File Saved")

## save rendering
print("Start Rendering")
bt.renderImage(outputPath, cam)