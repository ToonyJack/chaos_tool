import bpy
from ..ui import ViewChaosPanel
from bpy.types import Panel

class VIEW3D_PT_ExporterData(ViewChaosPanel, Panel):
    bl_label = "Export"
    bl_description = "export data,导出数据"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box.label(text="Export Data To Json", icon="EXPORT")
        box1 = box.box()
        col1 = box1.column(align=True)
        col1.operator("exporter_data_operators.export_cc4_data_to_json", text="Export CC4 Data")

        box2 = box.box()
        col2 = box2.column(align=True)
        col2.operator("exporter_data_operators.export_blender_scene_data_to_json", text="Export Scene Data")

        box3 = box.box()
        col3 = box3.column(align=True)
        col3.label(text="Link Prefab Data")
        row = col3.row(align=True)
        row.operator("exporter_data_operators.export_blender_prefabs_data_to_json", text="Export Prefabs Data")
        row.operator("importer_data_operators.import_chaos_prefabs_asset_data", text="Import Prefabs Data ")

        box4 = box.box()
        col4 = box4.column(align=True)
        col4.label(text="Link Model Data")
        row1= col4.row(align=True)
        row1.operator("exporter_data_operators.export_blender_model_data_to_json", text="Export Model Data")
        row1.operator("importer_data_operators.import_chaos_model_asset_data", text="Import Model Data")