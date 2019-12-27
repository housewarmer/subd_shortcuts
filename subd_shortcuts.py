import bpy


bl_info = {
    "name": "Sub-D Shortcuts",
    "blender": (2, 81, 16),
    "category": "Object",
}

C = bpy.context
D = bpy.data

subd_level = 0

class IncreaseViewSubD(bpy.types.Operator):
    """Increase View SubD level."""
    bl_idname = 'object.increase_view_subd'
    bl_label = 'Increase View SubD'
    bl_options = {'REGISTER', 'UNDO'}

    
    def execute(self, context):
        global subd_level
        AO = context.active_object
        if 'Subdivision' in AO.modifiers.keys():
            mod = AO.modifiers['Subdivision']
            mod.levels += 1
            
            subd_level = mod.levels
        else:
            bpy.ops.object.modifier_add(type='SUBSURF')
            mod = AO.modifiers['Subdivision']
            
            subd_level = mod.levels
        return {'FINISHED'}

class DecreaseViewSubD(bpy.types.Operator):
    """Decrease View SubD level."""
    bl_idname = 'object.decrease_view_subd'
    bl_label = 'Decrease View SubD'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global subd_level
        AO = context.active_object
        if 'Subdivision' in AO.modifiers.keys():
            mod = AO.modifiers['Subdivision']
            if mod.levels > 0: mod.levels -= 1
            
            subd_level = mod.levels
        else:
            bpy.ops.object.modifier_add(type='SUBSURF')
            mod = AO.modifiers['Subdivision']
            mod.levels = 0
            subd_level = mod.levels
        return {'FINISHED'}

class ToggleViewSubD(bpy.types.Operator):
    """Toggle View SubD level."""
    bl_idname = 'object.toggle_subd'
    bl_label = 'Toggle View SubD'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global subd_level
        AO = context.active_object
        if 'Subdivision' in AO.modifiers.keys():
            mod = AO.modifiers['Subdivision']
            if mod.levels > 0: mod.levels = 0
            else: mod.levels = subd_level
        else:
            bpy.ops.object.modifier_add(type='SUBSURF')
            mod = AO.modifiers['Subdivision']
            mod.levels = 1

            subd_level = mod.levels

        return {'FINISHED'}

addon_keymaps = []

def register():
    bpy.utils.register_class(IncreaseViewSubD)
    bpy.utils.register_class(DecreaseViewSubD)
    bpy.utils.register_class(ToggleViewSubD)
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    keys = [
        km.keymap_items.new(IncreaseViewSubD.bl_idname, 'EQUAL', 'PRESS', ctrl=True, shift=False),
        km.keymap_items.new(DecreaseViewSubD.bl_idname, 'MINUS', 'PRESS', ctrl=True, shift=False),
        km.keymap_items.new(ToggleViewSubD.bl_idname, 'TAB', 'PRESS', ctrl=True, shift=False),
    ]
    for k in keys:
        addon_keymaps.append((km, k))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(IncreaseViewSubD)
    bpy.utils.unregister_class(DecreaseViewSubD)
    bpy.utils.unregister_class(ToggleViewSubD)

if __name__ == '__main__':
    register()
