import bpy
from bpy.types import Operator
from . import debug_profiler_processor

class CHAOS_OT_CHAOS_OT_Unified_Name(Operator):
    bl_idname = "debug_profiler_operators.unified_name"
    bl_label = "Unified Name"
    bl_description = "统一名称"

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        debug_profiler_utility_processor = debug_profiler_processor.CHAOS_OT_Debug_Profiler_Utility_Processor()

        return debug_profiler_utility_processor.unified_name(context)