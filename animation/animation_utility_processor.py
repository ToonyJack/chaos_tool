import bpy
import os
from ..exporter_data.exporter_data_processor import CHAOS_OT_Export_Data_Processor
from ..exporter_data.importer_data_processor import CHAOS_OT_Import_Data_Processor
from ..utility.utility_processor import CHAOS_OT_Utility_Function
from .seanim import import_seanim
from bpy_extras.wm_utils.progress_report import ProgressReport


class CHAOS_OT_Import_SEAnimation_Processor:
    
    def load_seanim(self, context):
        CHAOS_OT_Utility_Function.delect_scene_data()
        chaos = context.scene.chaos
        export_anim_option_json_path = CHAOS_OT_Utility_Function.get_option_json_filepath("export_animation_fbx_options.json")
        import_skeletal_option_json_path = CHAOS_OT_Utility_Function.get_option_json_filepath("import_skeletal_fbx_options.json")
        
        export_anim_option_json_str = CHAOS_OT_Utility_Function.read_json_file(export_anim_option_json_path)
        export_anim_option_json_str["global_scale"] = chaos.global_scale
        CHAOS_OT_Utility_Function.write_json_file(export_anim_option_json_str,export_anim_option_json_path)
    
        anim_filepath_list = CHAOS_OT_Utility_Function.read_csv_file_for_add_list(chaos.seanim_source_path, chaos.csv_path)
        
        for anim_filepath in anim_filepath_list:
            
            if not os.path.exists(anim_filepath):
                print(anim_filepath)
            else:
                ##import tpose
                CHAOS_OT_Import_Data_Processor.importFBX(chaos.tposs_path,import_skeletal_option_json_path)
                bpy.ops.object.mode_set(mode='OBJECT')
        
                for ob in bpy.context.scene.objects:
                    if ob.parent is None:
                        ob.select_set(True)
                        if ob.type != 'ARMATURE':
                            return "An armature must be selected!"
                        
                        try:
                            ob.animation_data.action
                        except:
                            ob.animation_data_create()

                        with ProgressReport(context.window_manager) as progress:
                            
                            for bone in ob.pose.bones.data.bones:
                                bone.rotation_mode = 'QUATERNION'

                            progress.enter_substeps(1, os.path.basename(anim_filepath))
                            
                            try:
                                import_seanim.load_seanim(self, context, progress, anim_filepath)
                            except Exception as e:
                                progress.leave_substeps("ERROR: " + repr(e))
                            else:
                                progress.leave_substeps()
                                
                        bpy.ops.object.mode_set(mode='OBJECT')
                        ob.select_set(False)
                        
                CHAOS_OT_Utility_Function.selected_all_objects(True)
                CHAOS_OT_Export_Data_Processor.exportFBXtoJson(os.path.join(chaos.fbx_save_path, os.path.splitext(os.path.basename(anim_filepath))[0]) + ".fbx", export_anim_option_json_path)
                CHAOS_OT_Utility_Function.delect_scene_data()