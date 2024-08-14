import bpy
import os
import json
from . import cc4_material_parameters
from .asset_processor import PrefabJsonData, AssetInstanceData,AssetData
from ..utility.utility_processor import CHAOS_OT_Utility_Function


class CHAOS_OT_Export_Data_Processor:

    def __init__(self):
        self.base_filepath : str = 'C:\\chaos_integrated_tools\\blender_data_analysis'
        self.fbx_filename : str = 'fbx_model'
        self.filename_ext : str = ".fbx"


    @staticmethod
    def exportFBXtoJson(filepath : str, fbx_operator_json_file):
        #read fbx export operator from json data --

        with open(fbx_operator_json_file, 'r') as fp:
            data_file = json.load(fp)

        bpy.ops.export_scene.fbx(
            filepath = filepath,
            use_selection = bool(data_file["use_selection"]),
            use_visible = bool(data_file["use_visible"]),
            use_active_collection = bool(data_file["use_active_collection"]),
            global_scale = float(data_file["global_scale"]),
            apply_unit_scale = bool(data_file["apply_unit_scale"]),
            apply_scale_options = data_file["apply_scale_options"],
            use_space_transform = bool(data_file["use_space_transform"]),
            bake_space_transform = bool(data_file["bake_space_transform"]),
            object_types = set(data_file["object_types"]),
            use_mesh_modifiers = bool(data_file["use_mesh_modifiers"]),
            use_mesh_modifiers_render = bool(data_file["use_mesh_modifiers_render"]),
            mesh_smooth_type = data_file["mesh_smooth_type"],
            colors_type = data_file["colors_type"],
            prioritize_active_color = bool(data_file["prioritize_active_color"]),
            use_subsurf = bool(data_file["use_subsurf"]),
            use_mesh_edges = bool(data_file["use_mesh_edges"]),
            use_tspace = bool(data_file["use_tspace"]),
            use_triangles = bool(data_file["use_triangles"]),
            use_custom_props = bool(data_file["use_custom_props"]),
            add_leaf_bones = bool(data_file["add_leaf_bones"]),
            primary_bone_axis = data_file["primary_bone_axis"],
            secondary_bone_axis = data_file["secondary_bone_axis"],
            use_armature_deform_only = bool(data_file["use_armature_deform_only"]),
            armature_nodetype = data_file["armature_nodetype"],
            bake_anim = bool(data_file["bake_anim"]),
            bake_anim_use_all_bones = bool(data_file["bake_anim_use_all_bones"]),
            bake_anim_use_nla_strips = bool(data_file["bake_anim_use_nla_strips"]),
            bake_anim_use_all_actions = bool(data_file["bake_anim_use_all_actions"]),
            bake_anim_force_startend_keying = bool(data_file["bake_anim_force_startend_keying"]),
            bake_anim_step = float(data_file["bake_anim_step"]),
            bake_anim_simplify_factor = float(data_file["bake_anim_simplify_factor"]),
            path_mode = data_file["path_mode"],
            embed_textures = bool(data_file["embed_textures"]),
            batch_mode = data_file["batch_mode"],
            use_batch_own_dir = bool(data_file["use_batch_own_dir"]),
            axis_forward = data_file["axis_forward"],
            axis_up = data_file["axis_up"]
        )


    @staticmethod
    def export_fbx_model(selected_object : object):
        blob : dict = {}
        selected_object.select_set(True)
        for child in selected_object.children:
            child.select_set(True)

        asset_data : AssetData = AssetData()
        asset_data.set_info_from_object(selected_object)
        export_static_options_json = CHAOS_OT_Utility_Function.get_option_json_filepath("export_static_fbx_options.json")
        CHAOS_OT_Export_Data_Processor.exportFBXtoJson(asset_data.mesh_data_url,export_static_options_json)

        asset_json_str : dict = asset_data.get_info_to_json()
        asset_json_filepath = os.path.join(os.path.dirname(asset_data.mesh_data_url), asset_data.name) + ".json"

        blob[asset_data.name] = asset_json_str
        
        CHAOS_OT_Utility_Function.write_json_file(blob,asset_json_filepath)

        for child in selected_object.children:
            child.select_set(False)
        selected_object.select_set(False)
    

            
class CHAOS_OT_Export_CC4_Data_to_Json_Processor(CHAOS_OT_Export_Data_Processor):

    #global parameter
    skin_type_array = [
            'SKIN_BODY',
            'SKIN_ARM',
            'SKIN_LEG',
            'NAILS'
            ]
    
    eye_type_array = [
        'EYE_RIGHT',
        'EYE_LEFT',
        'CORNEA_RIGHT',
        'CORNEA_RIGHT'
    ]

    cc4_material_cache_parameters = cc4_material_parameters.CC4_Material_Cache_Parameters()

    def getObjectProperties(self, chr_cache,filepath):
        texs = bpy.data.images
        for tex in texs:
            tex_path = os.path.normpath(tex.filepath_raw)
            tex_path = os.path.normpath(tex_path)
        blob = {}
        objectData = {}
        object_caches = chr_cache.object_cache
        name = chr_cache.character_id
        json_data = chr_cache.get_json_data()
        object_json = json_data[name]['Object'][name]['Meshes']
        for obj_cache in object_caches:
            meshes = {}
            if obj_cache.object.type == 'MESH':
                meshes['Material'] = self.getMaterialParameter(object_json,obj_cache,chr_cache)
                objectData[obj_cache.source_name] = meshes
        blob["Meshes Data"] = objectData
        data = json.dumps(blob, indent="\t", sort_keys=False)
        with open(self.createJsonFile(filepath), 'w') as outfile:
            outfile.write(data + '\n')

    def getMaterialParameter(self, object_json, obj_cache, chr_cache):
        materialData = {}
        mat_json = object_json[obj_cache.source_name]['Materials']
        for mat_slot in obj_cache.object.material_slots:

            tex_path = self.get_material_tex_dir(chr_cache,obj_cache.object,mat_slot.material)
            print(tex_path)
            mat_cache = chr_cache.get_material_cache(mat_slot.material)
            material_slot = {}
            materialData[mat_slot.name] = material_slot
            shader_parameter = {}
            name = mat_slot.material.name
            texture_list = []
            if name in mat_json:
                texture_list.append(mat_json[name]['Textures'])
                texture_list.append(mat_json[name]['Resource Textures'])
                if('Custom Shader' in mat_json[name]):
                    texture_list.append(mat_json[name]['Custom Shader']['Image'])
            mat_cache_param_list, merge_mat_type = self.get_material_cacha_from_material_type(mat_cache)
            if mat_cache_param_list and merge_mat_type:
                material_slot["shader_type"] = merge_mat_type
                for mat_cache_param_key,mat_cache_param_key_value in mat_cache_param_list.items(): 
                    shader_parameter.setdefault(mat_cache_param_key,CHAOS_OT_Utility_Function.switch_parameter_type(mat_cache_param_key_value))
                for tex_infos in texture_list:
                    for tex_type,tex_value in dict(tex_infos).items():
                        tex_dir = {}
                        rel_pth = tex_value['Texture Path'][1:]
                        abs_path = os.path.normpath(chr_cache.import_dir + rel_pth)
                        texture_name = os.path.basename(abs_path)
                        new_path = os.path.join(os.path.dirname(self.filepath), 'textures' , mat_slot.material.name)
                        CHAOS_OT_Utility_Function.copy_texture_to_new_path(abs_path, new_path)
                        tex_dir['Texture Path'] =  os.path.join(new_path,texture_name)
                        shader_parameter.setdefault(tex_type,tex_dir)
            material_slot["shader_parameter"] = shader_parameter
        return materialData
    
    def get_material_tex_dir(self,chr_cache,obj,mat):
        object_name = obj.name
        mesh_name = obj.data.name
        material_name = mat.name
        rel_object = os.path.join("textures", chr_cache.import_name, object_name, mesh_name, material_name)
        path_object = os.path.join(chr_cache.import_dir, rel_object)
        rel_character = os.path.join("textures", chr_cache.import_name, chr_cache.import_name, mesh_name, material_name)
        path_character = os.path.join(chr_cache.import_dir, rel_character)
        if os.path.exists(path_object):
            return os.path.normpath(path_object)
        elif os.path.exists(path_character):
            return os.path.normpath(path_character)
        else:
            return os.path.normpath(os.path.join(chr_cache.import_dir,chr_cache.import_name + ".fbm"))
           
    def get_material_cacha_from_material_type(self, mat_cache):
        if mat_cache.material_type == 'SKIN_HEAD':
            return self.cc4_material_cache_parameters.get_cc4_head_parameters(mat_cache),'SKIN_HEAD'
        elif mat_cache.material_type in self.skin_type_array:
            return self.cc4_material_cache_parameters.get_cc4_skin_parameters(mat_cache),'SKIN'
        elif mat_cache.material_type == 'TONGUE':
            return self.cc4_material_cache_parameters.get_cc4_tongue_parameters(mat_cache),'TONGUE'
        elif mat_cache.material_type == 'TEETH_UPPER' or mat_cache.material_type == 'TEETH_LOWER':
            return self.cc4_material_cache_parameters.get_cc4_teeth_parameters(mat_cache),'TEETH'
        elif mat_cache.material_type == 'TEARLINE_RIGHT' or mat_cache.material_type == 'TEARLINE_RIGHT':
            return self.cc4_material_cache_parameters.get_cc4_tearline_parameters(mat_cache),'TEARLINE'
        elif mat_cache.material_type in self.eye_type_array:
            return self.cc4_material_cache_parameters.get_cc4_eye_parameters(mat_cache),'EYE'
        elif mat_cache.material_type == 'OCCLUSION_LEFT' or mat_cache.material_type == 'OCCLUSION_RIGHT':
            return self.cc4_material_cache_parameters.get_cc4_eye_occlusion_parameters(mat_cache),'EYE_OCCLUSION'
        elif mat_cache.material_type == 'HAIR':
            return self.cc4_material_cache_parameters.get_cc4_hair_parameters(mat_cache),'HAIR'
        elif mat_cache.material_type == 'SSS':
            return self.cc4_material_cache_parameters.get_cc4_sss_parameters(mat_cache),'SSS'
        elif mat_cache.material_type == 'DEFAULT' or mat_cache.material_type == 'EYELASH':
            return self.cc4_material_cache_parameters.get_cc4_pbr_parameters(mat_cache),'DEFAULT'
        else:
            return None
        
    def export_cc4_data(self,context,filepath):
        props = bpy.context.scene.CC3ImportProps
        chr_cache = props.get_context_character_cache(context)

        export_static_options_json = CHAOS_OT_Utility_Function.get_option_json_filepath("export_static_fbx_options.json")
        self.exportFBXtoJson(filepath, export_static_options_json)
        self.getObjectProperties(chr_cache,filepath)

        return {'FINISHED'}



class CHAOS_OT_Export_Blender_Data_to_Json_Processor(CHAOS_OT_Export_Data_Processor):

    def __init__(self):
        super().__init__()

        self.scene_filename : str = 'scene'
        self.prefabs_filename : str = 'prefabs'
        self.model_filename : str = 'model'


    def create_unified_mesh_to_export_fbx(self, mesh_data : dict, filepath : str):

        index : int = mesh_data.name.find("_lod0")
        if index != -1:
            filepath = os.path.join(filepath, mesh_data.name[:index]) + self.filename_ext
            selected_empty_obj : object = bpy.data.objects.new(mesh_data.name[:index], None)
            bpy.context.collection.objects.link(selected_empty_obj)

            selected_empty_obj["asset_name"] = mesh_data.name[:index]
            selected_empty_obj["is_imported"] = False
            selected_empty_obj["mesh_data_url"] = filepath
            selected_empty_obj["chaos_asset_url"] = ""


            selected_mesh_obj : object = bpy.data.objects.new(mesh_data.name, mesh_data)
            bpy.context.collection.objects.link(selected_mesh_obj)
            selected_mesh_obj.parent = selected_empty_obj
            selected_mesh_obj["chaos_asset_url"] = ""
            selected_mesh_obj["is_imported"] = False

            CHAOS_OT_Export_Data_Processor.export_fbx_model(selected_empty_obj)
        
            bpy.data.objects.remove(selected_mesh_obj, do_unlink=True)
            bpy.data.objects.remove(selected_empty_obj, do_unlink=True)


    def export_blender_scene_data(self,context):
        
        scene_filepath : str = os.path.join(self.base_filepath, self.scene_filename)
        #self.removeFiles(scene_filepath)

        #is create fbx_model folder
        fbx_filepath : str = CHAOS_OT_Utility_Function.make_folder(os.path.join(scene_filepath, self.fbx_filename))

        blob : dict = {}
        objectData : dict = {}
        selected_meshes_array : dict = {}
        for obj in bpy.context.selected_objects:
            instance_data : dict = {}
            instance_data['mesh_data_url'] = os.path.join(fbx_filepath, obj.data.name) + self.filename_ext
            objectData[obj.name] = instance_data
            selected_meshes_array[obj.data.name] = obj.data
            obj.select_set(False)

        blob["Scene_Data"] = objectData
        data = json.dumps(blob, indent="\t", sort_keys=False)
        with open(os.path.join(scene_filepath, 'scene_data.json'), 'w') as outfile:
            outfile.write(data + '\n')

        #create unified mesh && export fbx
        self.create_unified_mesh_to_export_fbx(selected_meshes_array,fbx_filepath)

        return {'FINISHED'}
    

    def export_blender_prefabs_data(self,context):

        prefabs_filepath : str = os.path.join(self.base_filepath, self.prefabs_filename)
        CHAOS_OT_Utility_Function.remove_files(prefabs_filepath)
        prefabs_json_filepath : str = os.path.join(prefabs_filepath, "prefabs_data.json")
        fbx_filepath : str = CHAOS_OT_Utility_Function.make_folder(os.path.join(prefabs_filepath, self.fbx_filename))
        
        prefab_json_data_array : list = []
        
        blob : dict = {}
        selected_meshes_array : set = set()
        for obj in bpy.context.selected_objects:
            if obj.parent is None:
                new_prefab_json_data : PrefabJsonData = PrefabJsonData()
                new_prefab_json_data.set_info_from_object(obj)
                new_asset_instance_array : list = []
                for child in obj.children:
                    
                    selected_meshes_array.add(child.data)
                    new_asset_instance : AssetInstanceData = AssetInstanceData()
                    new_asset_instance.set_info_from_object(child)
                    new_asset_instance_array.append(new_asset_instance)
                    
                    child.select_set(False)
                obj.select_set(False)
                new_prefab_json_data.asset_instance_array = new_asset_instance_array
                prefab_json_data_array.append(new_prefab_json_data)
        
        for mesh in selected_meshes_array:
            self.create_unified_mesh_to_export_fbx(mesh,fbx_filepath)
        
        prefabData : dict = {}
        for prefab_json_data in prefab_json_data_array:
            prefabData[prefab_json_data.name] = prefab_json_data.get_info_to_json()

        blob["Prefabs_Objects"] = prefabData
        
        CHAOS_OT_Utility_Function.write_json_file(blob,prefabs_json_filepath)
        
        return {'FINISHED'}


    def export_blender_model_data(self,context):
        
        export_static_options_json = CHAOS_OT_Utility_Function.get_option_json_filepath("export_static_fbx_options.json")
        model_filepath : str = os.path.join(self.base_filepath, self.model_filename)
        fbx_filepath : str = os.path.join(model_filepath, self.fbx_filename)
        asset_data_array : list = []
        
        for obj in bpy.context.selected_objects:
            if obj.parent is None:
                asset_data : AssetData = AssetData()
                asset_data.set_info_from_object(obj)
                asset_data_array.append(asset_data)
            obj.select_set(False)

        for obj in bpy.context.scene.objects:
            if obj.parent is None:
                obj.select_set(True)
                for child in obj.children:
                    child.select_set(True)
                fbx_export_filepath = os.path.join(fbx_filepath,obj.name) + self.filename_ext
                self.exportFBXtoJson(fbx_export_filepath,export_static_options_json)
                for child in obj.children:
                    child.select_set(False)
                obj.select_set(False)

        for asset_data in asset_data_array:
            asset_data_json_str : dict = {}
            asset_data_json_str[asset_data.name] = asset_data.get_info_to_json()
            json_export_filepath = os.path.join(fbx_filepath,asset_data.name) + ".json"
            CHAOS_OT_Utility_Function.write_json_file(asset_data_json_str,json_export_filepath)
                
        return {'FINISHED'}