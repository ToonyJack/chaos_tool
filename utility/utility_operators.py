import bpy
from bpy.types import Operator
from . import utility_processor

class CHAOS_OT_Create_Chaos_Custom_Property(Operator):
    bl_idname = "utility_operators.create_chaos_custom_property"
    bl_label = ""
    bl_description = "创建适配chaos的自定义属性"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        utility_tools_processor = utility_processor.CHAOS_OT_Utility_Tools_Processor()

        return utility_tools_processor.create_chaos_custom_property(context)


class CHAOS_OT_Clear_All_Mesh_Data(Operator):
    bl_idname = "utility_operators.clear_all_mesh_data"
    bl_label = ""
    bl_description = "删除所有的mesh数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        utility_tools_processor = utility_processor.CHAOS_OT_Utility_Tools_Processor()

        return utility_tools_processor.clear_all_mesh_data(context)
    

class CHAOS_OT_Clear_Unlink_Mesh_Data(Operator):
    bl_idname = "utility_operators.clear_unlink_mesh_data"
    bl_label = ""
    bl_description = "删除未使用的mesh数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        utility_tools_processor = utility_processor.CHAOS_OT_Utility_Tools_Processor()

        return utility_tools_processor.clear_unlink_mesh_data(context)


class CHAOS_OT_Clear_All_Material_Data(Operator):
    bl_idname = "utility_operators.clear_all_material_data"
    bl_label = ""
    bl_description = "删除所有的材质球数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        utility_tools_processor = utility_processor.CHAOS_OT_Utility_Tools_Processor()

        return utility_tools_processor.clear_all_material_data(context)


class CHAOS_OT_Clear_Unlink_Material_Data(Operator):
    bl_idname = "utility_operators.clear_unlink_material_data"
    bl_label = ""
    bl_description = "删除未使用的材质球数据"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        utility_tools_processor = utility_processor.CHAOS_OT_Utility_Tools_Processor()

        return utility_tools_processor.clear_unlink_material_data(context)