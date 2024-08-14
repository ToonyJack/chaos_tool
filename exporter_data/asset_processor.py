import bpy
from mathutils import Vector,Quaternion
from ..utility.utility_processor import CHAOS_OT_Utility_Function
from .material_processor import Material


class MeshData:
     
    def __init__(self):
        self.name : str = ""
        self.chaos_asset_url : str = ""
        self.is_imported : bool = False
        self.geometry = None
        self.materials : list = []


    def get_info_to_object(self, mesh_object : object, is_instance:bool):
        if not is_instance:
            mesh_object["chaos_asset_url"] = self.chaos_asset_url
            mesh_object["is_imported"] = self.is_imported

        if not self.name.endswith("_rigid"):
            for material in self.materials:
                material_type_sketum = material.material_type_switcher[material.shader_type]
                material_asset = bpy.data.materials[material.name]
                material_asset = material_type_sketum.create_shader_template(material_asset)
                material_asset = material.get_info_to_object(material_asset)

                for mat_slot in mesh_object.material_slots:
                    if mat_slot.name.split(".")[0] == material.name:
                        mat_slot.material = material_asset

        return mesh_object
    

    def get_info_to_json(self):
        mesh_data_json_str : dict = dict()
        mesh_data_json_str["is_imported"] = self.is_imported
        mesh_data_json_str["chaos_asset_url"] = self.chaos_asset_url
        material_data_json_str : dict = dict()
        for material in self.materials:
            material_data_json_str[material.name] = material.get_info_to_json()
        mesh_data_json_str["material_slots"] = material_data_json_str
        return mesh_data_json_str
    

    def set_info_from_object(self, object, is_rigidbody):
        self.name = object.data.name
        self.is_imported = object.get("is_imported")
        self.chaos_asset_url = object.get("chaos_asset_url")
        self.geometry = object.data

        if not is_rigidbody:
            for mat_slot in object.material_slots:
                material : Material = Material()
                material.set_info_from_object(mat_slot.material)
                self.materials.append(material)
    

    def set_info_from_json(self, mesh_data_name, mesh_data_json_str):
        self.name = mesh_data_name
        self.is_imported = mesh_data_json_str["is_imported"]
        self.chaos_asset_url = mesh_data_json_str["chaos_asset_url"]
        
        material_slots_json_str : dict = mesh_data_json_str["material_slots"]
        if not mesh_data_name.endswith("_rigid"):
            for material_name, material_data_json_str in material_slots_json_str.items():
                material : Material = Material()
                material.set_info_from_json(material_name, material_data_json_str)
                self.materials.append(material)



class AssetData:

    def __init__(self):
        self.name : str = ""
        self.mesh_data_url : str = ""
        self.chaos_asset_url : str = ""
        self.is_imported : bool = False
        self.mesh_data_array : MeshData = []
    

    def get_info_to_object(self,asset_object):
        asset_object["is_imported"] = self.is_imported
        asset_object["chaos_asset_url"] = self.chaos_asset_url
        asset_object["mesh_data_url"] = self.mesh_data_url
        asset_object["chaos_asset_url"] = self.chaos_asset_url
        
        for mesh_data in self.mesh_data_array:
            asset_mesh_obj : object = bpy.data.objects.new(mesh_data.name, mesh_data.geometry)
            bpy.context.collection.objects.link(asset_mesh_obj)
            asset_mesh_obj.parent = asset_object
            asset_mesh_obj = mesh_data.get_info_to_object(asset_mesh_obj,False)
            
        return asset_object
    

    def get_info_to_json(self):
        asset_data : dict = {}
        asset_data["asset_name"] = self.name
        asset_data["is_imported"] = self.is_imported
        asset_data["chaos_asset_url"] = self.chaos_asset_url
        asset_data["mesh_data_url"] = self.mesh_data_url

        mesh_data_array_json_str : dict = {}
        for mesh_data in self.mesh_data_array:
            mesh_data_json_str : dict = {}
            mesh_data_json_str["chaos_asset_url"] = mesh_data.chaos_asset_url
            mesh_data_json_str["is_imported"] = mesh_data.is_imported

            material_slot_array_json_str : dict = {}
            for material in mesh_data.materials:
                material_slot_json_str : dict = {}
                material_slot_json_str["shader_type"] = material.shader_type
                material_slot_json_str["is_imported"] = material.is_imported
                material_slot_json_str["chaos_asset_url"] = material.chaos_asset_url

                material_parameters_json_str : dict = material.material_parameters.get_material_parameters_to_json()
                material_slot_json_str["material_parameters"] = material_parameters_json_str

                material_slot_array_json_str[material.name] = material_slot_json_str

            mesh_data_json_str["material_slots"] = material_slot_array_json_str
            mesh_data_array_json_str[mesh_data.name] = mesh_data_json_str

        asset_data["lod_data"] = mesh_data_array_json_str
        return asset_data
    

    def set_info_from_object(self, object : object):
        self.name = object.name
        self.is_imported = object.get("is_imported")
        self.mesh_data_url = object.get("mesh_data_url")
        self.chaos_asset_url = object.get("chaos_asset_url")

        mesh_data_array : list = []
        for child in object.children:
            mesh_data : MeshData = MeshData()
            if child.data.name.endswith("_rigid"):
                mesh_data.set_info_from_object(child,True)
                mesh_data_array.append(mesh_data)
            else:
                mesh_data.set_info_from_object(child,False)
                mesh_data_array.append(mesh_data)
        self.mesh_data_array = mesh_data_array
            


    def set_info_from_json(self, asset_data_json_key,asset_data_json_value):
        self.name = asset_data_json_key
        self.chaos_asset_url = asset_data_json_value["chaos_asset_url"]
        self.mesh_data_url = asset_data_json_value["mesh_data_url"]
        self.is_imported = asset_data_json_value["is_imported"]
        
        mesh_data_array : list = []
        mesh_data_array_json_str : dict = asset_data_json_value["lod_data"]

        for mesh_data_key, mesh_data_value in mesh_data_array_json_str.items():
            mesh_data : MeshData = MeshData()
            mesh_data.set_info_from_json(mesh_data_key,mesh_data_value)
            mesh_data_array.append(mesh_data)
        self.mesh_data_array = mesh_data_array



class AssetInstanceData:
    
    def __init__(self):
        self.name : str = ""
        self.location : Vector = Vector((0, 0, 0))
        self.rotation : Quaternion = Quaternion((0, 0, 0, 0))
        self.scale : Vector = Vector((0, 0, 0))
        self.is_imported : bool = False
        self.chaos_asset_url : str = ""
        self.asset_json_url : str = "" 
        #self.asset_data : AssetData = AssetData()

    
    def get_info_to_object(self, asset_instance_object):
        #asset_instance_object = self.asset_data.get_info_to_object(asset_instance_object)
        asset_instance_object.location = self.location
        asset_instance_object.rotation_mode = 'QUATERNION'
        asset_instance_object.rotation_quaternion = self.rotation
        asset_instance_object.scale = self.scale
        asset_instance_object["is_imported"] = self.is_imported
        asset_instance_object["chaos_asset_url"] = self.chaos_asset_url
        asset_instance_object["asset_json_url"] = self.asset_json_url
        return asset_instance_object


    def get_info_to_json(self):
        instance_data : dict = {}
        instance_data["location"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.location)
        instance_data["rotation"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.rotation)
        instance_data["scale"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.scale)
        instance_data["is_imported"] = self.is_imported
        instance_data["chaos_asset_url"] = self.chaos_asset_url
        instance_data["asset_json_url"] = self.asset_json_url
        #instance_data["asset_data"] = self.asset_data.get_info_to_json()
        return instance_data


    def set_info_from_object(self, object : object):
        self.name = object.name
        self.location = object.location
        object.rotation_mode = 'QUATERNION'
        self.rotation = object.rotation_quaternion
        self.scale = object.scale
        self.is_imported = object.get("is_imported")
        self.chaos_asset_url = object.get("chaos_asset_url")
        self.asset_json_url = object.get("asset_json_url")
        #self.asset_data.set_info_from_object(object)


    def set_info_from_json(self,asset_key, asset_value):
        self.name = asset_key
        asset_instance_location_array = asset_value["location"]
        self.location = Vector((asset_instance_location_array[0],asset_instance_location_array[1],asset_instance_location_array[2]))

        asset_instance_rotation_array = asset_value["rotation"]
        self.rotation = Quaternion((asset_instance_rotation_array[0],asset_instance_rotation_array[1],asset_instance_rotation_array[2],asset_instance_rotation_array[3]))

        asset_instance_scale_array = asset_value["scale"]
        self.scale = Vector((asset_instance_scale_array[0],asset_instance_scale_array[1],asset_instance_scale_array[2]))

        self.is_imported = asset_value["is_imported"]
        self.chaos_asset_url = asset_value["chaos_asset_url"]
        self.asset_json_url = asset_value["asset_json_url"]
        #asset_data = asset_value["asset_data"]
        #self.asset_data.set_info_from_json(asset_data)



class PrefabJsonData:

    def __init__(self):
        self.name : str = ""
        self.location : Vector = Vector((0, 0, 0))
        self.rotation : Quaternion = Quaternion((0, 0, 0, 0))
        self.scale : Vector = Vector((0, 0, 0))
        self.chaos_asset_url : str = ""
        self.is_imported : bool = False
        self.asset_instance_array : AssetInstanceData = []


    def get_info_to_json(self):
        prefab_object : dict = {}
        prefab_object["location"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.location)
        prefab_object["rotation"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.rotation)
        prefab_object["scale"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.scale)
        prefab_object["chaos_asset_url"] = self.chaos_asset_url
        prefab_object["is_imported"] = self.is_imported

        instance_objects : dict = {}
        for asset_instance in self.asset_instance_array:
            instance_objects[asset_instance.name] = asset_instance.get_info_to_json()
        prefab_object["asset_instance"] = instance_objects

        return prefab_object


    def get_info_to_object(self, prefab_object):
        prefab_object.location = self.location
        prefab_object.rotation_mode = 'QUATERNION'
        prefab_object.rotation_quaternion = self.rotation
        prefab_object.scale = self.scale
        prefab_object["is_imported"] = self.is_imported
        prefab_object["chaos_asset_url"] = self.chaos_asset_url

        return prefab_object


    def set_info_from_object(self, object : object):
        self.name = object.name
        self.location = object.location
        object.rotation_mode = 'QUATERNION'
        self.rotation = object.rotation_quaternion
        self.scale = object.scale
        self.is_imported = object.get("is_imported")
        self.chaos_asset_url = object.get("chaos_asset_url")
    

    def set_info_from_json(self, prefab_key, prefab_value):
        
        self.name = prefab_key

        prefab_location_array = prefab_value["location"]
        self.location = Vector((prefab_location_array[0],prefab_location_array[1],prefab_location_array[2]))

        prefab_rotation_array = prefab_value["rotation"]
        self.rotation = Quaternion((prefab_rotation_array[0],prefab_rotation_array[1],prefab_rotation_array[2],prefab_rotation_array[3]))

        prefab_scale_array = prefab_value["scale"]
        self.scale = Vector((prefab_scale_array[0],prefab_scale_array[1],prefab_scale_array[2]))

        self.chaos_asset_url = prefab_value["chaos_asset_url"]
        self.is_imported = prefab_value["is_imported"]
        asset_instance_json_data : dict = prefab_value["asset_instance"]
        asset_instance_data_array : list = []

        for asset_key,asset_value in asset_instance_json_data.items():
            asset_instance_data : AssetInstanceData = AssetInstanceData()
            asset_instance_data.set_info_from_json(asset_key, asset_value)
            asset_instance_data_array.append(asset_instance_data)

        self.asset_instance_array = asset_instance_data_array