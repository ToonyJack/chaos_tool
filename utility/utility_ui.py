import bpy
from ..ui import ViewChaosPanel
from bpy.types import Panel

class VIEW3D_PT_Utility_Tools(ViewChaosPanel, Panel):
    bl_label = "Utility Tools"
    bl_description = "创建适配chaos的自定义属性"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box1 = box.box()
        col1 = box1.column(align=True)
        col1.operator("utility_operators.create_chaos_custom_property", text="Create Chaos Custom Property")
        col2 = box1.column(align=True)
        col2.operator("utility_operators.clear_all_mesh_data", text="Clear All Mesh Data")
        col3 = box1.column(align=True)
        col3.operator("utility_operators.clear_unlink_mesh_data", text="Clear Unlink Mesh Data")
        col4 = box1.column(align=True)
        col4.operator("utility_operators.clear_all_material_data", text="Clear All Material Data")
        col5 = box1.column(align=True)
        col5.operator("utility_operators.clear_unlink_material_data", text="Clear Unlink Material Data")