import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from . import exporter_data_processor
from . import importer_data_processor

class CHAOS_OT_Export_CC4_Data_To_Json(Operator,ExportHelper):
    bl_idname = "exporter_data_operators.export_cc4_data_to_json"
    bl_label = "Export"
    bl_description = "导出CC4数据"

    filename_ext = ".fbx"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):

        exporter_cc4_data_processor = exporter_data_processor.CHAOS_OT_Export_CC4_Data_to_Json_Processor()

        return exporter_cc4_data_processor.export_cc4_data(context,self.filepath)
    

class CHAOS_OT_Export_Blender_Scene_Data_To_Json(Operator):
    bl_idname = "exporter_data_operators.export_blender_scene_data_to_json"
    bl_label = "Export"
    bl_description = "导出Blender场景数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        exporter_blender_data_processor = exporter_data_processor.CHAOS_OT_Export_Blender_Data_to_Json_Processor()

        return exporter_blender_data_processor.export_blender_scene_data(context)
    

class CHAOS_OT_Export_Blender_Prefabs_Data_To_Json(Operator):
    bl_idname = "exporter_data_operators.export_blender_prefabs_data_to_json"
    bl_label = "Export"
    bl_description = "导出Blender prefabs数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        exporter_blender_data_processor = exporter_data_processor.CHAOS_OT_Export_Blender_Data_to_Json_Processor()

        return exporter_blender_data_processor.export_blender_prefabs_data(context)


class CHAOS_OT_Export_Blender_Model_Data_To_Json(Operator):
    bl_idname = "exporter_data_operators.export_blender_model_data_to_json"
    bl_label = "Export"
    bl_description = "导出Blender模型数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        exporter_blender_data_processor = exporter_data_processor.CHAOS_OT_Export_Blender_Data_to_Json_Processor()

        return exporter_blender_data_processor.export_blender_model_data(context)
    

class CHAOS_OT_Import_Chaos_Prefabs_Asset_Data(Operator):
    bl_idname = "importer_data_operators.import_chaos_prefabs_asset_data"
    bl_label = "Import"
    bl_description = "导入Chaos Prefab数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        importer_chaos_asset_processer = importer_data_processor.CHAOS_OT_Import_Chaos_Prefabs_Asset_Data_Processpr()

        return importer_chaos_asset_processer.create_chaos_prefab_asset_for_add_scene(context)
    

class CHAOS_OT_Import_Chaos_Model_Asset_Data(Operator):
    bl_idname = "importer_data_operators.import_chaos_model_asset_data"
    bl_label = "Import"
    bl_description = "导入Chaos Model数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        importer_chaos_asset_processer = importer_data_processor.CHAOS_OT_Import_Chaos_Prefabs_Asset_Data_Processpr()

        return importer_chaos_asset_processer.create_chaos_model_asset_for_add_scene(context)