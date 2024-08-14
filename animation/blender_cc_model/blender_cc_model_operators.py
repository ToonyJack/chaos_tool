import bpy
from bpy.types import Operator
from . import blender_cc_model_processor

class CHAOS_OT_ResetRestPoseOperator(Operator):
    bl_idname = "blender_cc_operator.reset_restpose_operator"
    bl_label = "Process Button"

    def execute(self, context):

        # Call the button callback function
        cc_blender_processor = blender_cc_model_processor.CHAOS_OT_CC_Blender_Processor()

        return cc_blender_processor.reset_rest_pose_callback(context)
    
#############################################################################
# -------------------------- Change CC Head -------------------------------- 

class CHAOS_OT_ChangeCCHeadOperator(Operator):
    bl_idname = "blender_cc_operator.change_cc_head_operator"
    bl_label = "Process Button"

    def execute(self, context):

        # Call the button callback function 
        cc_blender_processor = blender_cc_model_processor.CHAOS_OT_CC_Blender_Processor()
        
        return cc_blender_processor.change_cc_head_callback(context)