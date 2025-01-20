import bpy
import bmesh

def count_extraordinary_vertices(face):
    """
    Count the extraordinary vertices of a face.
    An extraordinary vertex is one that does not have 4 connected edges.
    """
    extraordinary_count = 0
    for vert in face.verts:
        if len(vert.link_edges) != 4:
            extraordinary_count += 1
    return extraordinary_count

# Get the active object (assuming it's a quad mesh)
obj = bpy.context.active_object

if obj and obj.type == 'MESH':
    # Ensure we're in Object Mode before creating a BMesh
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create a BMesh representation
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # List to store faces that meet the criteria
    extraordinary_faces = []
    
    # Detect faces with more than one extraordinary vertex
    for face in bm.faces:
        if len(face.verts) == 4:  # Only consider quads
            extraordinary_count = count_extraordinary_vertices(face)
            if extraordinary_count > 1:
                extraordinary_faces.append(face)

    if extraordinary_faces:
        # Deselect all elements first
        for face in bm.faces:
            face.select = False
        
        # Select the faces with more than one extraordinary vertex
        for face in extraordinary_faces:
            face.select = True
        
        # Update the mesh in Edit Mode
        bm.to_mesh(obj.data)
        bm.free()
        
        # Switch to Edit Mode and focus on the selection
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.reveal()  # Ensure hidden faces are shown
        bpy.ops.mesh.select_mode(type="FACE")
        
        # Popup to indicate success
        bpy.context.window_manager.popup_menu(
            lambda self, context: self.layout.label(text=f"Highlighted {len(extraordinary_faces)} face(s) with more than one extraordinary vertex."),
            title="Extraordinary Faces Found",
            icon='INFO'
        )
    else:
        bm.free()
        # Popup to indicate no extraordinary faces found
        bpy.context.window_manager.popup_menu(
            lambda self, context: self.layout.label(text="No faces with more than one extraordinary vertex found."),
            title="No Extraordinary Faces",
            icon='INFO'
        )
else:
    # If no valid object is selected, show an error
    bpy.context.window_manager.popup_menu(
        lambda self, context: self.layout.label(text="Please select a valid mesh object."),
        title="Error",
        icon='ERROR'
    )
