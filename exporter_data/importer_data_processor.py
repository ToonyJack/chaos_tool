from operator import truediv
import bpy
import os
import json
from .asset_processor import PrefabJsonData,AssetData,MeshData
from ..utility.utility_processor import CHAOS_OT_Utility_Function


class CHAOS_OT_Import_Data_Processor:

    @staticmethod
    def importFBX(filepath,fbx_operator_json_file):

        with open(fbx_operator_json_file, 'r') as fp:
            data_file = json.load(fp)

        bpy.ops.import_scene.fbx(
            filepath = filepath,
            use_custom_normals = bool(data_file["use_custom_normals"]),
            use_subsurf = bool(data_file["use_subsurf"]),
            use_custom_props = bool(data_file["use_custom_props"]),
            use_custom_props_enum_as_string = bool(data_file["use_custom_props_enum_as_string"]),
            use_image_search = bool(data_file["use_image_search"]),
            colors_type = data_file["colors_type"],
            global_scale = float(data_file["global_scale"]),
            decal_offset = float(data_file["decal_offset"]),
            bake_space_transform = bool(data_file["bake_space_transform"]),
            use_prepost_rot = bool(data_file["use_prepost_rot"]),
            use_manual_orientation = bool(data_file["use_manual_orientation"]),
            axis_forward = data_file["axis_forward"],
            axis_up = data_file["axis_up"],
            use_anim = bool(data_file["use_anim"]),
            anim_offset = float(data_file["anim_offset"]),
            ignore_leaf_bones = bool(data_file["ignore_leaf_bones"]),
            force_connect_children = bool(data_file["force_connect_children"]),
            automatic_bone_orientation = bool(data_file["automatic_bone_orientation"]),
            primary_bone_axis = data_file["primary_bone_axis"],
            secondary_bone_axis = data_file["secondary_bone_axis"],
        )



class CHAOS_OT_Import_Chaos_Prefabs_Asset_Data_Processpr(CHAOS_OT_Import_Data_Processor):

    def __init__(self):
        super().__init__()
        self.base_filepath = 'C:\\chaos_integrated_tools\\blender_data_analysis'
        self.prefabs_filename = 'prefabs'
        self.model_filename = 'model'
        self.prefabs_json_filename = "prefabs_data.json"
        self.fbx_filename = 'fbx_model'


    def create_unified_mesh_from_import_fbx(self,filepath):
        unified_mesh_array = {}

        asset_data_array : dict = {}
        model_json_file_array = CHAOS_OT_Utility_Function.get_all_model_json_files(filepath)
        for model_json_file in model_json_file_array:
            asset_json_data = CHAOS_OT_Utility_Function.read_json_file(model_json_file)
            for asset_json_key, asset_json_value in asset_json_data.items():
                asset_data : AssetData = AssetData()
                asset_data.set_info_from_json(asset_json_key,asset_json_value)
                asset_data_array[asset_data.name] = asset_data
        
        CHAOS_OT_Utility_Function.remove_unlink_meshes()
        import_static_options_json = CHAOS_OT_Utility_Function.get_option_json_filepath("import_static_fbx_options.json")
        
        for asset_data_key, asset_data_value in asset_data_array.items():
            CHAOS_OT_Import_Data_Processor.importFBX(asset_data_value.mesh_data_url,import_static_options_json)
            #current_model_name = self.getFileName(fbx_file)
            for obj in bpy.context.selected_objects:
                if obj.parent is None:
                    child = obj.children[0]
                    unified_mesh_array[CHAOS_OT_Utility_Function.get_file_name(asset_data_value.mesh_data_url)] = child.children[0].data

                    for mesh_child in child.children:
                        bpy.data.objects.remove(mesh_child, do_unlink=True)
                    bpy.data.objects.remove(child, do_unlink=True)
                    bpy.data.objects.remove(obj, do_unlink=True)

        return unified_mesh_array,asset_data_array
        

    def create_chaos_prefab_asset_for_add_scene(self,context):

        prefabs_json_filepath : str = os.path.join(self.base_filepath, self.prefabs_filename)
        fbx_filepath : str = os.path.join(prefabs_json_filepath, self.fbx_filename)

        unified_mesh_array, asset_data_array = self.create_unified_mesh_from_import_fbx(fbx_filepath)

        json_data = CHAOS_OT_Utility_Function.read_json_file(os.path.join(prefabs_json_filepath,self.prefabs_json_filename))

        prefab_json_data_array : list = []
        prefabs_json_list : dict = json_data["Prefabs_Objects"]

        for prefab_key, prefab_value in prefabs_json_list.items():
            prefab_json_data : PrefabJsonData = PrefabJsonData()
            prefab_json_data.set_info_from_json(prefab_key, prefab_value)
            prefab_json_data_array.append(prefab_json_data)

        for prefab_json_data in prefab_json_data_array:
            prefab_empty_obj : object = bpy.data.objects.new(prefab_json_data.name, None)
            bpy.context.collection.objects.link(prefab_empty_obj)
            prefab_empty_obj.empty_display_type = 'PLAIN_AXES'
            prefab_empty_obj = prefab_json_data.get_info_to_object(prefab_empty_obj)

            for asset_instance in prefab_json_data.asset_instance_array:
                asset_instance_empty_obj : object = bpy.data.objects.new(asset_instance.name, unified_mesh_array[CHAOS_OT_Utility_Function.get_file_name(asset_instance.asset_json_url)])
                bpy.context.collection.objects.link(asset_instance_empty_obj)
                asset_instance_empty_obj = asset_instance.get_info_to_object(asset_instance_empty_obj)
                asset_data : AssetData = asset_data_array[CHAOS_OT_Utility_Function.get_file_name(asset_instance_empty_obj.get("asset_json_url"))]
                mesh_data : MeshData = asset_data.mesh_data_array[0]

                asset_instance_empty_obj = mesh_data.get_info_to_object(asset_instance_empty_obj,True)
                asset_instance_empty_obj.parent = prefab_empty_obj
        
        return {'FINISHED'}


    def create_chaos_model_asset_for_add_scene(self,context):

        fbx_filepath : str = os.path.join(os.path.join(self.base_filepath, self.model_filename), self.fbx_filename)
        import_static_options_json = CHAOS_OT_Utility_Function.get_option_json_filepath("import_static_fbx_options.json")

        asset_data_array : list = []
        model_json_file_array = CHAOS_OT_Utility_Function.get_all_model_json_files(fbx_filepath)
        for model_json_file in model_json_file_array:
            asset_json_data = CHAOS_OT_Utility_Function.read_json_file(model_json_file)
            for asset_json_key, asset_json_value in asset_json_data.items():
                asset_data : AssetData = AssetData()
                asset_data.set_info_from_json(asset_json_key,asset_json_value)
                CHAOS_OT_Import_Data_Processor.importFBX(asset_data.mesh_data_url,import_static_options_json)
                for obj in bpy.context.selected_objects:
                    if len(obj.children) == 0:
                        for mesh_data in asset_data.mesh_data_array:
                            if obj.name == mesh_data.name:
                                mesh_data.geometry = obj.data
                    bpy.data.objects.remove(obj, do_unlink=True)
                asset_data_array.append(asset_data)
        
        for asset_data in asset_data_array:
            asset_empty_obj : object = bpy.data.objects.new(asset_data.name, None)
            bpy.context.collection.objects.link(asset_empty_obj)
            asset_empty_obj.empty_display_type = 'PLAIN_AXES'
            asset_empty_obj = asset_data.get_info_to_object(asset_empty_obj)

        return {'FINISHED'}