import bpy

class CHAOS_OT_Debug_Profiler_Utility_Processor:

    def get_bottom_objects(self,parent_object):
        
        bottom_objects = []
    
        for child in parent_object.children:
            print(child.name)
            if len(child.children) == 0:
                bottom_objects.append(child)
            else:
                bottom_objects.extend(self.get_bottom_objects(child))
                
        return bottom_objects

    def unified_name(self,context):
        for selected_object_parent in bpy.context.selected_objects:
            bottom_objects = self.get_bottom_objects(selected_object_parent)
            for btm_obj in bottom_objects:
                if btm_obj.name.endswith("_lod"):
                    btm_obj.data.name = btm_obj.name

        return {'FINISHED'}