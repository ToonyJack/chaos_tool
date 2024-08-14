import bpy
from ..ui import ViewChaosPanel
from bpy.types import Panel

class VIEW3D_PT_Debug_Profiler_Utility(ViewChaosPanel, Panel):
    bl_label = "Debug Profiler"
    bl_description = "导出前Debug Check"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box.label(text="Debug Profiler Utility", icon="EXPORT")
        box1 = box.box()
        col1 = box1.column(align=True)
        col1.operator("debug_profiler_operators.unified_name", text="Unified Name")