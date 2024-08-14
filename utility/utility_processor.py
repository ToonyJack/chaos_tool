import bpy
import os
import shutil
import json
import csv
import glob
from mathutils import Color, Vector,Euler,Quaternion

class CHAOS_OT_Utility_Function:
    
    ### <summary>
    ### Remove Unlink Meshes
    ### </summary>
    ### <param name="copyTextureToNewPath"></param>
    @staticmethod
    def remove_unlink_meshes():
        for mesh in bpy.data.meshes:
            if not mesh.users: 
                bpy.data.meshes.remove(mesh)
    

    ### <summary>
    ### Get File Name
    ### </summary>
    ### <param name="copyTextureToNewPath"></param>
    @staticmethod
    def get_file_name(filepath) -> str:
         return os.path.splitext(os.path.basename(filepath))[0]
    

    ### <summary>
    ### Get All Model Json Files
    ### </summary>
    ### <param name="copyTextureToNewPath"></param>
    @staticmethod
    def get_all_model_json_files(filepath)-> list:
        fbx_file_array : list = glob.glob(filepath + '/' + '*.json')
        return fbx_file_array
    

    ### <summary>
    ### Copy the texture from the current path to the new path
    ### </summary>
    ### <param name="copyTextureToNewPath"></param>
    @staticmethod
    def copy_texture_to_new_path(self, old_filepath,new_path):
        new_path = self.makeFolder(new_path)
        shutil.copy(old_filepath, new_path)


    ### <summary>
    ### Create a folder in the FilePath
    ### </summary>
    ### <param name="makeFolder"></param>
    @staticmethod
    def make_folder(filepath):
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            return filepath
        else:
            return filepath
        

    ### <summary>
    ### Delete all files in the FilePath
    ### </summary>
    ### <param name="removeFiles"></param>
    @staticmethod
    def remove_files(filepath):
        if os.path.isfile(filepath):
        # 如果是文件，则直接删除
            os.remove(filepath)
        elif os.path.isdir(filepath):
            # 如果是文件夹，则递归删除文件夹内的所有文件和文件夹
            for file_name in os.listdir(filepath):
                file_path = os.path.join(filepath, file_name)
                CHAOS_OT_Utility_Function.remove_files(file_path)
            os.rmdir(filepath)


    ### <summary>
    ### Serialize as float array
    ### </summary>
    ### <param name="switchParameterType"></param>
    @staticmethod
    def switch_parameter_type(para_value):
        if isinstance(para_value, float):
            return float(para_value)
        elif isinstance(para_value, Vector):
            if len(para_value) == 3:
                return para_value[0],para_value[1],para_value[2]
            elif len(para_value) == 4:
                return para_value[0],para_value[1],para_value[2],para_value[3]
        elif isinstance(para_value, Euler):
            return para_value[0],para_value[1],para_value[2]
        elif isinstance(para_value, Quaternion):
            return para_value[0],para_value[1],para_value[2],para_value[3]
        elif isinstance(para_value, Color):
            return para_value[0],para_value[1],para_value[2]
        elif len(para_value) == 4:
            return para_value[0],para_value[1],para_value[2],para_value[3]
        else: 
            return 0


    ### <summary>
    ### Read Json File Convert to data file
    ### </summary>
    ### <param name="readJsonFile"></param>
    @staticmethod
    def read_json_file(filepath):
        with open(filepath, 'r') as fp:
            data_file = json.load(fp)
        return data_file


    ### <summary>
    ### write Json File
    ### </summary>
    ### <param name="write_json_file"></param>
    @staticmethod
    def write_json_file(json_data,filepath):
        data = json.dumps(json_data, indent="\t", sort_keys=False)
        with open(filepath, 'w') as outfile:
            outfile.write(data + '\n')
            

    ### <summary>
    ### Create a Json File in the FilePath
    ### </summary>
    ### <param name="createJsonFile"></param>
    @staticmethod
    def create_json_file(filepath):
        save_path = bpy.path.abspath("//")
        filename, extension = os.path.splitext(filepath)
        json_basename = os.path.basename(filename)
        extension = ".json"
        json_name = json_basename + extension
        return os.path.join(save_path, json_name)
    
    
    ### <summary>
    ### Read CSV File in the FilePath
    ### </summary>
    ### <param name="read_csv_file"></param>
    @staticmethod
    def read_csv_file_for_add_list(anim_dirpath, csv_filepath):
        anim_filepath_list = []
        with open(csv_filepath, 'r') as file:
            csv_data = csv.reader(file)
            for row in csv_data:
                anim_filepath = os.path.join(anim_dirpath,''.join(row)) + ".seanim"
                anim_filepath_list.append(anim_filepath)
            return anim_filepath_list
        
    
    ### <summary>
    ### selected all objects
    ### </summary>
    ### <param name="selected_all_objects"></param>
    @staticmethod
    def selected_all_objects(is_selected):
        for obj in bpy.context.scene.objects:
            obj.select_set(is_selected)
            
    
    ### <summary>
    ### delect scene data
    ### </summary>
    ### <param name="delect_scene_data"></param>
    @staticmethod 
    def delect_scene_data():
        for obj in bpy.context.scene.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
            
        for action in bpy.data.actions:
            bpy.data.actions.remove(action)
            
        for armature in bpy.data.armatures:
            bpy.data.armatures.remove(armature)
            
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
            
    
    @staticmethod       
    def get_plugins_dirpath():
        plugin_path = os.path.join(os.path.join(bpy.utils.user_resource('SCRIPTS'),"addons"),"chaos_tool")
        return plugin_path
    
    
    @staticmethod       
    def get_option_json_filepath(option_json_name):
        plugins_dirpath = CHAOS_OT_Utility_Function.get_plugins_dirpath()
        export_data_dirpath = os.path.join(plugins_dirpath,"exporter_data")
        static_option_json_filepath = os.path.join(os.path.join(export_data_dirpath,"options"), option_json_name)
        return static_option_json_filepath



class CHAOS_OT_Node_Utility_Function:

    def __init__(self):
        self.default_texture_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"texture")

    def create_texture_node(self, label_name, nodes):
        texture_node = nodes.new(type="ShaderNodeTexImage")
        texture_node.label = label_name
        texture_node["is_imported"] = False
        texture_node["chaos_asset_url"] = ""
        texture_node["texture_source_url"] = ""
        return texture_node

    def create_mapping_node(self, label_name, nodes,links):
        uv_texture_node = nodes.new(type="ShaderNodeUVMap")
        texture_mapping_node = nodes.new(type="ShaderNodeMapping")
        texture_mapping_node.label = label_name
        links.new(uv_texture_node.outputs['UV'], texture_mapping_node.inputs['Vector'])
        return texture_mapping_node
    
    def create_color_node(self,label_name,nodes):
        color_node = nodes.new(type="ShaderNodeRGB")
        color_node.outputs['Color'].default_value = Vector((1.0,1.0,1.0,1.0))
        color_node.label = label_name
        return color_node

    def create_value_node(self,label_name,nodes):
        value_node = nodes.new(type="ShaderNodeValue")
        value_node.label = label_name
        value_node.outputs[0].default_value = 1.0
        return value_node
    
    def create_utility_node(self,type,nodes):
        node = nodes.new(type=type)
        return node
    
    def create_vector_math_node(self,operation,nodes):
        vector_math_node = nodes.new(type="ShaderNodeVectorMath")
        vector_math_node.operation = operation
        return vector_math_node
    
    def create_value_mix_node(self,nodes):
        value_mix_node = nodes.new(type="ShaderNodeMix")
        value_mix_node.data_type = "FLOAT"
        return value_mix_node
    
    def create_value_math_node(self,operation,nodes):
        value_math_node = nodes.new(type="ShaderNodeMath")
        value_math_node.operation = operation
        return value_math_node
    
    def create_break_vector_node(self,nodes):
        return nodes.new(type="ShaderNodeSeparateXYZ")
    
    def create_decode_normal_node(self,nodes):
        return nodes.new(type="ShaderNodeNormalMap")
    
    def create_color_mix_node(self,blend_type,nodes):
        color_mix_node = nodes.new(type="ShaderNodeMix")
        color_mix_node.data_type = "RGBA"
        color_mix_node.blend_type = blend_type
        return color_mix_node
    
    def create_vector_mix_node(self,nodes):
        color_mix_node = nodes.new(type="ShaderNodeMix")
        color_mix_node.data_type = "VECTOR"
        return color_mix_node
    
    def create_combine_vector_node(self,nodes):
        return nodes.new(type="ShaderNodeCombineXYZ")




class CHAOS_OT_Utility_Tools_Processor:
        
    def get_scene_link_mesh_data(self):
        scene_mesh_data_array = {}
        for mesh in bpy.data.meshes:
            if mesh.users:
                index = mesh.name.find("keyword")
                if index != -1:
                    scene_mesh_data_array[mesh.name[:index]] = mesh
        return scene_mesh_data_array
        
                
    def create_chaos_custom_property(self,context):
        for obj in bpy.context.selected_objects:
            #if (obj.get("asset_name") is None and len(obj.children) == 0):
            #    index = obj.data.name.find("_lod0")
            #    if index != -1:
            #        obj["asset_name"] = obj.data.name[:index]
            #if (obj.get("chaos_asset_url") is None):
            #    obj['chaos_asset_url'] = ""
            if (obj.get("mesh_data_url") is None and obj.parent is None):
                if obj.children[0].name.endswith("_lod0"):
                    obj['mesh_data_url'] = os.path.join('C:\\chaos_integrated_tools\\blender_data_analysis\\model\\fbx_model', obj.name) + '.fbx'

            if obj.get("is_imported") is None:
                obj['is_imported'] = False
                
            for mat_slot in obj.material_slots:
                if mat_slot.material.get("is_imported") is None:
                    mat_slot.material['is_imported'] = False

            if obj.get("chaos_asset_url") is None:
                obj['chaos_asset_url'] = ""

            if obj.type == "MESH":
                for mat_slot in obj.material_slots:
                    if mat_slot.material.get("chaos_asset_url")  is None:
                        mat_slot.material["chaos_asset_url"] = ""
                    if mat_slot.material.get("shader_type")  is None:
                        mat_slot.material["shader_type"] = ""
                
            if obj.get("asset_json_url") is None and obj.parent is None:
                if obj.children[0].name.endswith("_lod0"):
                    obj['asset_json_url'] = os.path.join('C:\\chaos_integrated_tools\\blender_data_analysis\\model\\fbx_model', obj.name) + '.json'

            if obj.get("asset_json_url") is None and len(obj.children) == 0:
                index = obj.data.name.find("_lod0")
                if index != -1 and not obj.name == obj.data.name:
                    obj['asset_json_url'] = os.path.join('C:\\chaos_integrated_tools\\blender_data_analysis\\prefabs\\fbx_model', obj.data.name[:index]) + '.json'
        return {'FINISHED'}


    def clear_all_mesh_data(self,context):
        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
        return {'FINISHED'}
    
    def clear_unlink_mesh_data(self,context):
        for mesh in bpy.data.meshes:
            if not mesh.users:
                 bpy.data.meshes.remove(mesh)
        return {'FINISHED'}

    def clear_all_material_data(self,context):
        for obj in bpy.context.selected_objects:
            if len(obj.material_slots) > 0:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.material_slot_remove()
                obj.select_set(False)

        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
        return {'FINISHED'}

    def clear_unlink_material_data(self,context):
        for material in bpy.data.materials:
            if not material.users:
                bpy.data.materials.remove(material)
        return {'FINISHED'}