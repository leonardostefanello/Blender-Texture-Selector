# -------------------- IMPORTS --------------------

import bpy

# -------------------- INFORMATION --------------------

bl_info = {
    "name": "Texture Selector",
    "author": "Moonlight_",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "3D Viewport > Sidebar > Texture Selector",
    "description": "Select all objects with the same Base Color texture file.",
    "doc_url": "github.com/leonardostefanello/Blender-Texture-Selector/blob/main/README.md",
    "tracker_url": "github.com/leonardostefanello/Blender-Texture-Selector/issues",
}

# -------------------- SETUP --------------------

class OBJECT_OT_SelectByTexture(bpy.types.Operator):
    bl_idname = "object.select_by_texture"
    bl_label = "Select Objects by Texture"

    def execute(self, context):
        props = context.scene.select_texture_props
        texture_name = props.texture_name
        mode = props.mode
        
        # Deselect all objects first
        bpy.ops.object.select_all(action='DESELECT')
        selected_count = 0  # Counter for selected objects

        # Loop through all objects in the scene
        for obj in bpy.data.objects:
            # Check if the object is visible or selected based on the mode
            if mode == 'VISIBLE' and not obj.visible_get():
                continue
            if mode == 'SELECTED' and not obj.select_get():
                continue

            # Check if the object has a mesh
            if obj.type == 'MESH':
                # Loop through the object's materials
                for slot in obj.material_slots:
                    if slot.material and slot.material.use_nodes:
                        for node in slot.material.node_tree.nodes:
                            # Look for an Image Texture node
                            if node.type == 'TEX_IMAGE':
                                # Check the image name
                                if node.image and texture_name in node.image.name:
                                    # Select the object if the texture matches
                                    obj.select_set(True)
                                    selected_count += 1  # Increment the counter
                                    break

        # Update the counter property
        props.selected_count = selected_count
        return {'FINISHED'}

class SelectTextureProperties(bpy.types.PropertyGroup):
    texture_name: bpy.props.StringProperty(
        name="Texture",
        description="Enter the name of the base color texture file (without extension)",
        default=""
    )
    mode: bpy.props.EnumProperty(
        name="Mode",
        description="Select how to choose objects",
        items=[
            ('VISIBLE', "Visible", "Select only visible objects"),
            ('SELECTED', "Selected", "Select only among selected objects"),
        ],
        default='VISIBLE'
    )
    selected_count: bpy.props.IntProperty(
        name="Selected Count",
        description="Number of selected objects",
        default=0
    )

class OBJECT_PT_SelectTexturePanel(bpy.types.Panel):
    bl_label = "Select Objects by Texture"
    bl_idname = "OBJECT_PT_select_texture_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Texture Selector'

    def draw(self, context):
        layout = self.layout
        props = context.scene.select_texture_props

        layout.prop(props, "texture_name")
        layout.prop(props, "mode")

        row = layout.row()
        row.operator("object.select_by_texture", text="Select Objects")

        # Display the count of selected objects
        layout.label(text=f"Selected Objects: {props.selected_count}")

def register():
    bpy.utils.register_class(OBJECT_OT_SelectByTexture)
    bpy.utils.register_class(SelectTextureProperties)
    bpy.utils.register_class(OBJECT_PT_SelectTexturePanel)
    bpy.types.Scene.select_texture_props = bpy.props.PointerProperty(type=SelectTextureProperties)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SelectByTexture)
    bpy.utils.unregister_class(SelectTextureProperties)
    bpy.utils.unregister_class(OBJECT_PT_SelectTexturePanel)
    del bpy.types.Scene.select_texture_props

if __name__ == "__main__":
    register()

# -------------------- END --------------------