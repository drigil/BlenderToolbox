import bpy

def drawPoints(mesh, \
                ptColor, \
                ptSize, \
                emitType = 'VERT',\
                showMesh = True): 
    # initialize a primitive sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius = 1.0, location = (1e7,1e7,1e7))
    sphere = bpy.context.object
    bpy.ops.object.shade_smooth()
    mat = bpy.data.materials.new(name="sphereMat")
    sphere.data.materials.append(mat)
    sphere.active_material = mat
    mat.use_nodes = True
    tree = mat.node_tree
    tree.nodes.new('ShaderNodeHueSaturation')
    tree.nodes["Hue Saturation Value"].inputs['Color'].default_value = ptColor.RGBA
    tree.nodes["Hue Saturation Value"].inputs['Saturation'].default_value = ptColor.S
    tree.nodes["Hue Saturation Value"].inputs['Value'].default_value = ptColor.V
    tree.nodes["Hue Saturation Value"].inputs['Hue'].default_value = ptColor.H
    tree.links.new(tree.nodes["Hue Saturation Value"].outputs['Color'], tree.nodes['Principled BSDF'].inputs['Base Color'])

    # init particle system
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.particle_system_add()
    bpy.data.particles["ParticleSettings"].frame_start = 0
    bpy.data.particles["ParticleSettings"].frame_end = 0
    bpy.data.particles["ParticleSettings"].render_type = 'OBJECT'
    bpy.data.particles["ParticleSettings"].instance_object = sphere
    bpy.data.particles["ParticleSettings"].particle_size = ptSize
    bpy.data.particles["ParticleSettings"].physics_type = 'NO'
    bpy.data.particles["ParticleSettings"].use_emit_random = False

    if emitType == 'VERT':
        bpy.data.particles["ParticleSettings"].emit_from = emitType
        bpy.data.particles["ParticleSettings"].count = len(mesh.data.vertices)
    elif emitType == 'FACE':
        bpy.data.particles["ParticleSettings"].emit_from = emitType
        bpy.data.particles["ParticleSettings"].count = len(mesh.data.polygons)
        bpy.data.particles["ParticleSettings"].use_even_distribution = False
        bpy.data.particles["ParticleSettings"].userjit = 1
    else:
        print('emitType should be either VERT or FACE\n')
        raise

    # show mesh or not (True or False)
    mesh.show_instancer_for_viewport = showMesh
    mesh.show_instancer_for_render = showMesh