import bpy
from bpy_types import Operator
import time

from .animation_utility_processor import CHAOS_OT_Import_SEAnimation_Processor


class CHAOS_OT_Import_SEAnim(Operator):
    bl_idname = "animation_utility_operators.import_semain"
    bl_label = "Import"
    bl_description = "导入SEAnim"

    @classmethod
    def poll(self, context):
        return True
    
    
    def execute(self, context):
        seanim_processor = CHAOS_OT_Import_SEAnimation_Processor()
        start_time = time.process_time()
        result = seanim_processor.load_seanim(context)
        
        #seanim_processor.load_seanim(context)
        
        if not result:
            self.report({'INFO'}, "Import finished in %.4f sec." %
                        (time.process_time() - start_time))
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, result)
            return {'FINISHED'}
        #return {'FINISHED'}