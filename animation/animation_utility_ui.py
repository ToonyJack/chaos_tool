import bpy
from ..ui import ViewChaosPanel
from bpy.types import Panel

class VIEW3D_PT_Import_SEAnim(ViewChaosPanel, Panel):
    bl_label = "Animation"
    bl_description = "Animation Utility Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        chaos = context.scene.chaos
        
        box.label(text="Convert SEAnim", icon="EXPORT")
        box1 = box.box()
        col = box1.column(align=True)
        col.prop(chaos,"global_scale",text="Scale")
        col1 = box1.column(align=True)
        col1.prop(chaos,"tposs_path",text="TPoss")
        col2 = box1.column(align=True)
        col2.prop(chaos,"csv_path",text="CSV")
        col3 = box1.column(align=True)
        col3.prop(chaos,"seanim_source_path",text="SEAnim Source")
        col4 = box1.column(align=True)
        col4.prop(chaos,"fbx_save_path",text="FBX Export")
        col5 = box1.column(align=True)
        col5.operator("animation_utility_operators.import_semain", text="Convert")