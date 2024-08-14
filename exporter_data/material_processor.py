import bpy
import os
from mathutils import Vector,Color
from ..utility.utility_processor import CHAOS_OT_Utility_Function,CHAOS_OT_Node_Utility_Function


default_texture_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"texture")

class Texture:

    def __init__(self):
        self.texture_source_url : str = ""
        self.chaos_asset_url : str = ""
        self.is_imported : bool = False


    def get_texture_to_object(self, node):
        node.image = bpy.data.images.load(self.texture_source_url)
        node["texture_source_url"] = self.texture_source_url
        node["chaos_asset_url"] = self.chaos_asset_url
        node["is_imported"] = self.is_imported
        return node


    def get_texture_to_json(self):
        texture_data : dict = {}
        texture_data["texture_source_url"] = self.texture_source_url
        texture_data["chaos_asset_url"] = self.chaos_asset_url
        texture_data["is_imported"] = self.is_imported
        return texture_data


    def set_texture_from_object(self, node):
         self.texture_source_url = os.path.abspath(node.image.filepath)
         self.chaos_asset_url = node.get("chaos_asset_url")
         self.is_imported = node.get("is_imported")


    def set_texture_from_json(self, texture_parameters):
        self.texture_source_url = texture_parameters["texture_source_url"]
        self.chaos_asset_url = texture_parameters["chaos_asset_url"]
        self.is_imported = texture_parameters["is_imported"]



class Material:

    def __init__(self):
        self.name : str = ""
        self.shader_type : str = ""
        self.chaos_asset_url : str = ""
        self.is_imported : bool = False
        self.material_parameters = None

        self.material_type_switcher : dict = {
            "unlit" : UnlitMaterial(),
            "translucent" : TranslucentMaterial(),
            "emissive" : EmissiveMaterial(),
            "opaque_character_hero" : OpaqueCharactorHeroMaterial(),
            "opaque_character_solider" : OpaqueCharactorSoliderMaterial(),
            "opaque_scene" : OpaqueSceneMaterial(),
            "opaque_blend" : OpaqueBlendMaterial(),
            "cheap_subsurface" : CheapSubsurfaceMaterial(),
            "two_side_foliage" : TwoSideFoliageMaterial(),
            "subsurface_profile" : SubsurfaceProfileMaterial(),
            "sss_subsurface_profile_mr_CC" : SSSSubsurfaceProfileMrCCMaterial(),
            "cloth_base" : ClothMaterial(),
            "decal" : DecalMaterial()
        }


    def get_info_to_object(self, material):

        material["shader_type"] = self.shader_type
        material["chaos_asset_url"] = self.chaos_asset_url
        material["is_imported"] = self.is_imported
        material = self.material_parameters.get_material_parameters_to_object(material,self.shader_type)

        return material
    

    def get_info_to_json(self):
        material_data_json_str : dict = dict()

        material_data_json_str["shader_type"] = self.shader_type
        material_data_json_str["chaos_asset_url"] = self.chaos_asset_url
        material_data_json_str["is_imported"] = self.is_imported
        material_data_json_str["material_parameters"] = self.material_parameters.get_material_parameters_to_json()

        return material_data_json_str
    

    def set_info_from_object(self, material):
        self.name = material.name
        self.shader_type = material.get("shader_type")
        self.chaos_asset_url = material.get("chaos_asset_url")
        self.is_imported = material.get("is_imported")
        self.material_parameters = self.material_type_switcher[self.shader_type]
        self.material_parameters.set_material_parameters_from_object(material,self.shader_type)
    

    def set_info_from_json(self, material_name, material_data_json_string):
        self.name = material_name
        self.shader_type = material_data_json_string["shader_type"]
        self.is_imported = material_data_json_string["is_imported"]
        self.chaos_asset_url = material_data_json_string["chaos_asset_url"]
        material_parameters_json_str = material_data_json_string["material_parameters"]
        self.material_parameters = self.material_type_switcher[self.shader_type]
        self.material_parameters.set_material_parameters_from_json(material_parameters_json_str)



class UnlitMaterial:

    def __init__(self):
        self.base_color_map : Texture = Texture()
        self.uv_scale_offset : Vector = Vector((0.0,1.0,1.0,0.0))
        self.base_color_multiplier : Vector = Vector((1.0,1.0,1.0,1.0))
        self.use_alpha_clip : bool = False
        self.alpha_clip_value : float = 0.333
        
        self.node_manager = CHAOS_OT_Node_Utility_Function()


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            if node.label == "base_color_map":
                self.base_color_map.set_texture_from_object(node)
            elif node.label == "uv_scale_offset":
                self.uv_scale_offset = Vector((node.inputs[1].default_value[1], node.inputs[3].default_value[0], node.inputs[3].default_value[1], node.inputs[1].default_value[0]))
            elif node.label == "base_color_multiplier":
                self.base_color_multiplier = node.outputs['Color'].default_value
            elif node.label == shader_type:
                self.use_alpha_clip = node.inputs["Use Alpha Clip"].default_value


    def set_material_parameters_from_json(self, material_parameters):
        self.base_color_map.set_texture_from_json(material_parameters["base_color_map"])
        uv_scale_offset = material_parameters["uv_scale_offset"]
        self.uv_scale_offset = Vector((uv_scale_offset[3], uv_scale_offset[1], uv_scale_offset[2], uv_scale_offset[0]))
        base_color_multiplier = material_parameters["base_color_multiplier"]
        self.base_color_multiplier = Vector((base_color_multiplier[0], base_color_multiplier[1], base_color_multiplier[2], base_color_multiplier[3]))
        self.use_alpha_clip = material_parameters["use_alpha_clip"]
        self.alpha_clip_value = material_parameters["alpha_clip_value"]


    def get_material_parameters_to_json(self):
        material_parameters : dict = dict()
        material_parameters["base_color_map"] = self.base_color_map.get_texture_to_json()
        material_parameters["uv_scale_offset"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.uv_scale_offset)
        material_parameters["base_color_multiplier"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.base_color_multiplier)
        material_parameters["use_alpha_clip"] = self.use_alpha_clip
        material_parameters["alpha_clip_value"] = self.alpha_clip_value
        return material_parameters


    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            if node.label == "base_color_map":
                node = self.base_color_map.get_texture_to_object(node)
            elif node.label == "uv_scale_offset":
                node.inputs[3].default_value = Vector((self.uv_scale_offset[1], self.uv_scale_offset[2], 0))
                node.inputs[1].default_value = Vector((self.uv_scale_offset[3], self.uv_scale_offset[0], 0))
            elif node.label == shader_type:
                node.inputs["Use Alpha Clip"].default_value = self.use_alpha_clip
            elif node.label == "base_color_multiplier":
                node.outputs['Color'].default_value = self.base_color_multiplier
        return material


    def create_shader_template(self, material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="UnlitNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "unlit"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs[26])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "unlit"
        return material
        


class OpaqueBase:

    def __init__(self):
        self.base_color_map : Texture = Texture()
        self.normal_map : Texture = Texture()
        self.orm_mask_map : Texture = Texture()

        self.uv_scale_offset : Vector = Vector((0.0,1.0,1.0,0.0))
        self.base_color_multiplier : Vector = Vector((1.0,1.0,1.0,1.0))
        self.use_alpha_clip : bool = False
        self.metallic_scale : float = 1.0
        self.roughness_scale : float = 1.0
        self.specular_value : float = 0.5
        self.ao_influence : float = 1.0
        self.alpha_clip_value : float = 0.333
        
        self.node_manager = CHAOS_OT_Node_Utility_Function()


    def set_opaque_base_parameters_from_object(self, node, shader_type):
        if node.label == "base_color_map":
            self.base_color_map.set_texture_from_object(node)
        elif node.label == "normal_map":
            self.normal_map.set_texture_from_object(node)
        elif node.label == "orm_mask_map":
            self.orm_mask_map.set_texture_from_object(node)
        elif node.label == "uv_scale_offset":
            self.uv_scale_offset = Vector((node.inputs[1].default_value[1], node.inputs[3].default_value[0], node.inputs[3].default_value[1], node.inputs[1].default_value[0]))
        elif node.label == shader_type:
            self.use_alpha_clip = node.inputs["Use Alpha Clip"].default_value
        elif node.label == "metallic_scale":
            self.metallic_scale = node.outputs[0].default_value
        elif node.label == "roughness_scale":
            self.roughness_scale = node.outputs[0].default_value
        elif node.label == "specular_level":
            self.specular_value = node.outputs[0].default_value
        elif node.label == "base_color_multiplier":
            self.base_color_multiplier = node.outputs['Color'].default_value


    def get_opaque_base_parameters_to_object(self,node,shader_type):
        if node.label == "base_color_map":
            node = self.base_color_map.get_texture_to_object(node)
        elif node.label == "normal_map":
            node = self.normal_map.get_texture_to_object(node)
        elif node.label == "orm_mask_map":
            node = self.orm_mask_map.get_texture_to_object(node)
        elif node.label == "uv_scale_offset":
            node.inputs[3].default_value = Vector((self.uv_scale_offset[1], self.uv_scale_offset[2], 0))
            node.inputs[1].default_value = Vector((self.uv_scale_offset[3], self.uv_scale_offset[0], 0))
        elif node.label == shader_type:
            node.inputs["Use Alpha Clip"].default_value = self.use_alpha_clip
        elif node.label == "metallic_scale":
            node.outputs[0].default_value = self.metallic_scale
        elif node.label == "roughness_scale":
            node.outputs[0].default_value = self.roughness_scale
        elif node.label == "specular_level":
            node.outputs[0].default_value = self.specular_value
        elif node.label == "base_color_multiplier":
            node.outputs['Color'].default_value = self.base_color_multiplier

    
    def set_opaque_base_parameters_from_json(self, material_parameters):
        self.base_color_map.set_texture_from_json(material_parameters["base_color_map"])
        self.normal_map.set_texture_from_json(material_parameters["normal_map"])
        self.orm_mask_map.set_texture_from_json(material_parameters["orm_mask_map"])

        uv_scale_offset = material_parameters["uv_scale_offset"]
        self.uv_scale_offset = Vector((uv_scale_offset[3], uv_scale_offset[1], uv_scale_offset[2], uv_scale_offset[0]))

        base_color_multiplier = material_parameters["base_color_multiplier"]
        self.base_color_multiplier = Vector((base_color_multiplier[0], base_color_multiplier[1], base_color_multiplier[2], base_color_multiplier[3]))

        self.use_alpha_clip = material_parameters["use_alpha_clip"]
        self.metallic_scale = material_parameters["metallic_scale"]
        self.roughness_scale = material_parameters["roughness_scale"]
        self.specular_value = material_parameters["specular_value"]
        self.ao_influence = material_parameters["ao_influence"]
        self.alpha_clip_value = material_parameters["alpha_clip_value"]


    def get_opaque_base_parameters_to_json(self):
        material_parameters : dict = {}

        material_parameters["base_color_map"] = self.base_color_map.get_texture_to_json()
        material_parameters["normal_map"] = self.normal_map.get_texture_to_json()
        material_parameters["orm_mask_map"] = self.orm_mask_map.get_texture_to_json()

        material_parameters["uv_scale_offset"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.uv_scale_offset)
        material_parameters["base_color_multiplier"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.base_color_multiplier)
        material_parameters["use_alpha_clip"] = self.use_alpha_clip
        material_parameters["metallic_scale"] = self.metallic_scale
        material_parameters["roughness_scale"] = self.roughness_scale
        material_parameters["specular_value"] = self.specular_value
        material_parameters["ao_influence"] = self.ao_influence
        material_parameters["alpha_clip_value"] = self.alpha_clip_value

        return material_parameters



class TranslucentMaterial(OpaqueBase):

    def __init__(self):
        super().__init__()


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_opaque_base_parameters_from_object(node,shader_type)


    def set_material_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)


    def get_material_parameters_to_json(self):
        return self.get_opaque_base_parameters_to_json()
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_opaque_base_parameters_to_object(node,shader_type)
        return material
    

    def create_shader_template(self, material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="TranslucentNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "translucent"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs['Base Color'])
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "translucent"
        return material



class EmissiveMaterial(OpaqueBase):

    def __init__(self):
        super().__init__()
        self.emissive_map : Texture = Texture()
        self.emissive_color_multiplier : Vector = Vector((1.0, 1.0, 1.0, 1.0))
        self.emissive_intensity : float = 1.0


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_opaque_base_parameters_from_object(node,shader_type)
            if node.label == "emissive_map":
                self.emissive_map.set_texture_from_object(node)
            elif node.label == "emissive_intensity":
                self.emissive_intensity = node.outputs[0].default_value
            elif node.label == "emissive_color_multiplier":
                self.emissive_color_multiplier = node.outputs['Color'].default_value


    def set_material_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)
        self.emissive_map.set_texture_from_json(material_parameters["emissive_map"])
        self.emissive_intensity = material_parameters["emissive_intensity"]
        emissive_color_multiplier = material_parameters["emissive_color_multiplier"]
        self.emissive_color_multiplier = Vector((emissive_color_multiplier[0], emissive_color_multiplier[1], emissive_color_multiplier[2], emissive_color_multiplier[3]))


    def get_material_parameters_to_json(self):
        material_parameters : dict = self.get_opaque_base_parameters_to_json()
        material_parameters["emissive_map"] = self.emissive_map.get_texture_to_json()
        material_parameters["emissive_intensity"] = self.emissive_intensity
        material_parameters["emissive_color_multiplier"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.emissive_color_multiplier)
        return material_parameters
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_opaque_base_parameters_to_object(node, shader_type)
            if node.label == "emissive_map":
                node = self.emissive_map.get_texture_to_object(node)
            elif node.label == "emissive_intensity":
                node.outputs[0].default_value = self.emissive_intensity
            elif node.label == "emissive_color_multiplier":
                node.outputs['Color'].default_value = self.emissive_color_multiplier
        return material
    

    def create_shader_template(self, material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        emissive_texture_node = self.node_manager.create_texture_node("emissive_map",nodes)
        emissive_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        emissive_color_multiplier_node = self.node_manager.create_color_node("emissive_color_multiplier",nodes)
        emissive_intensity_node  = self.node_manager.create_value_node("emissive_intensity",nodes)
        emissive_intensity_node.outputs[0].default_value = 1.0
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], emissive_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="EmissiveNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "emissive"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Emissive Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Emissive Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Emissive Intensity", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(emissive_texture_node.outputs['Color'], group_node.inputs['Emissive Color'])
        links.new(emissive_color_multiplier_node.outputs['Color'], group_node.inputs['Emissive Color Multiplier'])
        links.new(emissive_intensity_node.outputs['Value'], group_node.inputs['Emissive Intensity'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        mix_emissive_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs['Base Color'])
        
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        
        group_node_tree.links.new(group_input.outputs['Emissive Color'], mix_emissive_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Emissive Color Multiplier'], mix_emissive_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_emissive_color_mutilpler_node.outputs[0], bsdf_node.inputs[26])
        group_node_tree.links.new(group_input.outputs['Emissive Intensity'], bsdf_node.inputs[27])
        
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "emissive"
        return material



class OpaqueCharactorHeroMaterial(OpaqueBase):

    def __init__(self):
        super().__init__()

    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_opaque_base_parameters_from_object(node,shader_type)


    def set_material_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)


    def get_material_parameters_to_json(self):
        return self.get_opaque_base_parameters_to_json()
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_opaque_base_parameters_to_object(node,shader_type)
        return material


    def create_shader_template(self,material):

        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="OpaqueCharacterHeroNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "opaque_character_hero"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs['Base Color'])
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "opaque_character_hero"

        return material



class OpaqueCharactorSoliderMaterial(OpaqueBase):

    def __init__(self):
        super().__init__()
        self.use_tint : bool = bool()
        self.tint_map : Texture = Texture()


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_opaque_base_parameters_from_object(node, shader_type)
            if node.label == shader_type:
                self.use_tint = node.inputs["Use Tint"].default_value
            elif node.label == "tint_map":
                self.tint_map.set_texture_from_object(node)


    def set_material_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)
        self.use_tint = material_parameters["use_tint"]
        self.tint_map.set_texture_from_json(material_parameters["tint_map"])


    def get_material_parameters_to_json(self):
        material_parameters : dict = self.get_opaque_base_parameters_to_json()
        material_parameters["use_tint"] = self.use_tint
        material_parameters["tint_map"] = self.tint_map.get_texture_to_json()
        return material_parameters
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_opaque_base_parameters_to_object(node, shader_type)
            if node.label == shader_type:
                node.inputs["Use Tint"].default_value = self.use_tint
            elif node.label == "tint_map":
                node = self.tint_map.get_texture_to_object(node)
        return material
    

    def create_shader_template(self,material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        tint_texture_node = self.node_manager.create_texture_node("tint_map",nodes)
        tint_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], tint_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="OpaqueCharacterSoliderNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "opaque_character_solider"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Tint", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Tint", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(tint_texture_node.outputs['Color'], group_node.inputs['Tint'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])

        tint_color_multiplier_node = self.node_manager.create_color_node("tint_color_multiplier",group_node_tree.nodes)
        tint_color_mix_node = self.node_manager.create_color_mix_node("OVERLAY",group_node_tree.nodes)
        base_tint_color_mix_node = self.node_manager.create_vector_mix_node(group_node_tree.nodes)
        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(group_input.outputs['Base Color'], tint_color_mix_node.inputs[6])
        group_node_tree.links.new(tint_color_multiplier_node.outputs['Color'], tint_color_mix_node.inputs[7])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], base_tint_color_mix_node.inputs[4])
        group_node_tree.links.new(tint_color_mix_node.outputs["Result"], base_tint_color_mix_node.inputs[5])
        group_node_tree.links.new(group_input.outputs['Tint'], base_tint_color_mix_node.inputs[0])
        group_node_tree.links.new(base_tint_color_mix_node.outputs["Result"], bsdf_node.inputs['Base Color'])
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "opaque_character_solider"
        
        return material


    
class OpaqueSceneMaterial(OpaqueBase):

    def __init__(self):
        super().__init__()
        self.use_burn : bool = False
        self.burn_base_color_map : Texture = Texture()
        self.burn : float = 0
        self.burn_map_uv_scale_offset : Vector = Vector((0.0,1.0,1.0,0.0))


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_opaque_base_parameters_from_object(node, shader_type)
            if node.label == shader_type:
                self.use_burn = node.inputs["Use Burn"].default_value
            elif node.label == "burn_base_color_map":
                self.burn_base_color_map.set_texture_from_object(node)
            elif node.label == "burn":
                self.burn = node.outputs[0].default_value
            elif node.label == "burn_map_uv_scale_offset":
                self.burn_map_uv_scale_offset = Vector((node.inputs[3].default_value[1], node.inputs[1].default_value[0], node.inputs[1].default_value[1], node.inputs[3].default_value[0]))


    def set_material_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)
        self.use_burn = material_parameters["use_burn"]
        self.burn_base_color_map.set_texture_from_json(material_parameters["burn_base_color_map"])
        self.burn = material_parameters["burn"]

        burn_map_uv_scale_offset = material_parameters["burn_map_uv_scale_offset"]
        self.burn_map_uv_scale_offset = Vector((burn_map_uv_scale_offset[0], burn_map_uv_scale_offset[1], burn_map_uv_scale_offset[2], burn_map_uv_scale_offset[3]))


    def get_material_parameters_to_json(self):
        material_parameters : dict = self.get_opaque_base_parameters_to_json()
        material_parameters["use_burn"] = self.use_burn
        material_parameters["burn_base_color_map"] = self.burn_base_color_map.get_texture_to_json()
        material_parameters["burn"] = self.burn
        material_parameters["burn_map_uv_scale_offset"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.burn_map_uv_scale_offset)
        return material_parameters
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_opaque_base_parameters_to_object(node, shader_type)
            if node.label == shader_type:
                node.inputs["Use Burn"].default_value = self.use_burn
            elif node.label == "burn_base_color_map":
                node = self.burn_base_color_map.get_texture_to_object(node)
            elif node.label == "burn":
                node.outputs[0].default_value = self.burn
            elif node.label == "burn_map_uv_scale_offset":
                node.inputs[3].default_value = Vector((self.burn_map_uv_scale_offset[3], self.burn_map_uv_scale_offset[0], 0))
                node.inputs[1].default_value = Vector((self.burn_map_uv_scale_offset[1], self.burn_map_uv_scale_offset[2], 0))
        return material
    

    def create_shader_template(self,material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        burn_base_color_texture_node = self.node_manager.create_texture_node("burn_base_color_map",nodes)
        burn_base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        burn_texture_mapping_node = self.node_manager.create_mapping_node("burn_map_uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        burn_node  = self.node_manager.create_value_node("burn",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(burn_texture_mapping_node.outputs['Vector'], burn_base_color_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="OpaqueSceneNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "opaque_scene"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Burn", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Burn Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Burn", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(burn_base_color_texture_node.outputs['Color'], group_node.inputs['Burn Color'])
        links.new(burn_node.outputs['Value'], group_node.inputs['Burn'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        base_burn_color_mix_node = self.node_manager.create_color_mix_node("MIX",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(group_input.outputs['Burn'], base_burn_color_mix_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Burn Color'], base_burn_color_mix_node.inputs[7])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], base_burn_color_mix_node.inputs[6])
        group_node_tree.links.new(base_burn_color_mix_node.outputs["Result"], bsdf_node.inputs['Base Color'])
        
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "opaque_scene"
        return material



class OpaqueBlendMaterial(OpaqueBase):

    def __init__(self):
        super().__init__()
        self.detail_base_color_opacity_map : Texture = Texture()
        self.detail_normal_map : Texture = Texture()
        self.detail_orm_map : Texture = Texture()
        self.mask_edge_noise_map : Texture = Texture()

        self.detail_uv_scale_offset : Vector = Vector((0.0,1.0,1.0,0.0))
        self.detail_base_color_multiplier : Vector = Vector((1.0,1.0,1.0,1.0))
        self.mask_edge_uv_scale_offset : Vector = Vector((0.0,1.0,1.0,0.0))

        self.detail_metallic_scale : float = 1.0
        self.detail_roughness_scale : float = 1.0
        self.detail_ao_influence : float = 1.0
        self.detail_specular_value : float = 0.5
        self.mask_height : float = 0
        self.mask_power : float = 1.0
        self.mask_intensity : float = 1.0
        self.blend_normal_strength : float = 0.5
        self.world_blend_max : float = 2.0


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_opaque_base_parameters_from_object(node, shader_type)
            if node.label == "detail_base_color_opacity_map":
                self.detail_base_color_opacity_map.set_texture_from_object(node)
            elif node.label == "detail_normal_map":
                self.detail_normal_map.set_texture_from_object(node)
            elif node.label == "detail_orm_map":
                self.detail_orm_map.set_texture_from_object(node)
            elif node.label == "mask_edge_noise_map":
                self.mask_edge_noise_map.set_texture_from_object(node)

            elif node.label == "detail_uv_scale_offset":
                self.detail_uv_scale_offset = Vector((node.inputs[3].default_value[1], node.inputs[1].default_value[0], node.inputs[1].default_value[1], node.inputs[3].default_value[0]))
            elif node.label == "detail_base_color_multiplier":
                self.detail_base_color_multiplier = node.outputs['Color'].default_value
            elif node.label == "mask_edge_uv_scale_offset":
                self.mask_edge_uv_scale_offset = Vector((node.inputs[3].default_value[1], node.inputs[1].default_value[0], node.inputs[1].default_value[1], node.inputs[3].default_value[0]))
            
            elif node.label == "detail_metallic_scale":
                self.detail_metallic_scale = node.outputs[0].default_value
            elif node.label == "detail_roughness_scale":
                self.detail_roughness_scale = node.outputs[0].default_value
            elif node.label == "detail_ao_influence":
                self.detail_ao_influence = node.outputs[0].default_value
            elif node.label == "detail_specular_value":
                self.detail_specular_value = node.outputs[0].default_value
            elif node.label == "mask_height":
                self.mask_height = node.outputs[0].default_value
            elif node.label == "mask_power":
                self.mask_power = node.outputs[0].default_value
            elif node.label == "mask_intensity":
                self.mask_intensity = node.outputs[0].default_value
            elif node.label == "blend_normal_strength":
                self.blend_normal_strength = node.outputs[0].default_value
            elif node.label == "world_blend_max":
                self.world_blend_max = node.outputs[0].default_value


    def set_material_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)
        self.detail_base_color_opacity_map.set_texture_from_json(material_parameters["detail_base_color_opacity_map"])
        self.detail_normal_map.set_texture_from_json(material_parameters["detail_normal_map"])
        self.detail_orm_map.set_texture_from_json(material_parameters["detail_orm_map"])
        self.mask_edge_noise_map.set_texture_from_json(material_parameters["mask_edge_noise_map"])

        detail_uv_scale_offset = material_parameters["detail_uv_scale_offset"]
        self.detail_uv_scale_offset = Vector((detail_uv_scale_offset[3], detail_uv_scale_offset[0], detail_uv_scale_offset[1], detail_uv_scale_offset[2]))
        detail_base_color_multiplier = material_parameters["detail_base_color_multiplier"]
        self.detail_base_color_multiplier = Vector((detail_base_color_multiplier[0], detail_base_color_multiplier[1], detail_base_color_multiplier[2], detail_base_color_multiplier[3]))
        mask_edge_uv_scale_offset = material_parameters["mask_edge_uv_scale_offset"]
        self.mask_edge_uv_scale_offset = Vector((mask_edge_uv_scale_offset[3], mask_edge_uv_scale_offset[0], mask_edge_uv_scale_offset[1], mask_edge_uv_scale_offset[2]))

        self.detail_metallic_scale = material_parameters["detail_metallic_scale"]
        self.detail_roughness_scale = material_parameters["detail_roughness_scale"]
        self.detail_ao_influence = material_parameters["detail_ao_influence"]
        self.detail_specular_value = material_parameters["detail_specular_value"]
        self.mask_height = material_parameters["mask_height"]
        self.mask_power = material_parameters["mask_power"]
        self.mask_intensity = material_parameters["mask_intensity"]
        self.blend_normal_strength = material_parameters["blend_normal_strength"]
        self.world_blend_max = material_parameters["world_blend_max"]


    def get_material_parameters_to_json(self):
        material_parameters : dict = self.get_opaque_base_parameters_to_json()
        material_parameters["detail_base_color_opacity_map"] = self.detail_base_color_opacity_map.get_texture_to_json()
        material_parameters["detail_normal_map"] = self.detail_normal_map.get_texture_to_json()
        material_parameters["detail_orm_map"] = self.detail_orm_map.get_texture_to_json()
        material_parameters["mask_edge_noise_map"] = self.mask_edge_noise_map.get_texture_to_json()
        
        material_parameters["detail_uv_scale_offset"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.detail_uv_scale_offset)
        material_parameters["detail_base_color_multiplier"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.detail_base_color_multiplier)
        material_parameters["mask_edge_uv_scale_offset"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.mask_edge_uv_scale_offset)
        
        material_parameters["detail_metallic_scale"] = self.detail_metallic_scale
        material_parameters["detail_roughness_scale"] = self.detail_roughness_scale
        material_parameters["detail_ao_influence"] = self.detail_ao_influence
        material_parameters["detail_specular_value"] = self.detail_specular_value
        material_parameters["mask_height"] = self.mask_height
        material_parameters["mask_power"] = self.mask_power
        material_parameters["mask_intensity"] = self.mask_intensity
        material_parameters["blend_normal_strength"] = self.blend_normal_strength
        material_parameters["world_blend_max"] = self.world_blend_max
        return material_parameters
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_opaque_base_parameters_to_object(node, shader_type)
            if node.label == "detail_base_color_opacity_map":
                node = self.detail_base_color_opacity_map.get_texture_to_object(node)
            elif node.label == "detail_normal_map":
                node = self.detail_normal_map.get_texture_to_object(node)
            elif node.label == "detail_orm_map":
                node = self.detail_orm_map.get_texture_to_object(node)
            elif node.label == "mask_edge_noise_map":
                node = self.mask_edge_noise_map.get_texture_to_object(node)
                
            elif node.label == "detail_uv_scale_offset":
                node.inputs[3].default_value = Vector((self.detail_uv_scale_offset[3], self.detail_uv_scale_offset[0], 0))
                node.inputs[1].default_value = Vector((self.detail_uv_scale_offset[1], self.detail_uv_scale_offset[2], 0))
            elif node.label == "detail_base_color_multiplier":
                node.outputs['Color'].default_value = self.detail_base_color_multiplier
            elif node.label == "mask_edge_uv_scale_offset":
                node.inputs[3].default_value = Vector((self.mask_edge_uv_scale_offset[3], self.mask_edge_uv_scale_offset[0], 0))
                node.inputs[1].default_value = Vector((self.mask_edge_uv_scale_offset[1], self.mask_edge_uv_scale_offset[2], 0))

            elif node.label == "detail_metallic_scale":
                node.outputs[0].default_value = self.detail_metallic_scale
            elif node.label == "detail_roughness_scale":
                node.outputs[0].default_value = self.detail_roughness_scale
            elif node.label == "detail_ao_influence":
                node.outputs[0].default_value = self.detail_ao_influence
            elif node.label == "detail_specular_value":
                node.outputs[0].default_value = self.detail_specular_value
            elif node.label == "mask_height":
                node.outputs[0].default_value = self.mask_height
            elif node.label == "mask_power":
                node.outputs[0].default_value = self.mask_power
            elif node.label == "mask_intensity":
                node.outputs[0].default_value = self.mask_intensity
            elif node.label == "blend_normal_strength":
                node.outputs[0].default_value = self.blend_normal_strength
            elif node.label == "world_blend_max":
                node.outputs[0].default_value = self.world_blend_max
        return material
    

    def create_shader_template(self,material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        ### <summary>
        ### Create Texture Node
        ### </summary>
        ### base texture node
        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))
        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        ### detail texture node
        detail_base_color_opacity_texture_node = self.node_manager.create_texture_node("detail_base_color_opacity_map",nodes)
        detail_base_color_opacity_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        detail_normal_texture_node = self.node_manager.create_texture_node("detail_normal_map",nodes)
        detail_normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))
        detail_orm_texture_node = self.node_manager.create_texture_node("detail_orm_map",nodes)
        detail_orm_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        ### mask edge texture node
        mask_edge_noise_texture_node = self.node_manager.create_texture_node("mask_edge_noise_map",nodes)
        mask_edge_noise_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        ### end------------------
        

        ### <summary>
        ### Create Texture UV Mapping
        ### </summary>
        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        detail_texture_mapping_node = self.node_manager.create_mapping_node("detail_uv_scale_offset",nodes,links)
        mask_edge_texture_mapping_node = self.node_manager.create_mapping_node("mask_edge_uv_scale_offset",nodes,links)
        ### end------------------
        
        
        ### <summary>
        ### Create Float4 Parameters Node
        ### </summary>
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        detail_base_color_multiplier_node = self.node_manager.create_color_node("detail_base_color_multiplier",nodes)
        ### end------------------
        
        
        ### <summary>
        ### Create Float Parameters Node
        ### </summary>
        ### base float parameter node
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        
        ### detail float parameter node
        detail_metallic_scale_node  = self.node_manager.create_value_node("detail_metallic_scale",nodes)
        detail_metallic_scale_node.outputs[0].default_value = 0.0
        detail_roughness_scale_node  = self.node_manager.create_value_node("detail_roughness_scale",nodes)
        detail_roughness_scale_node.outputs[0].default_value = 1.0
        detail_specular_level_node  = self.node_manager.create_value_node("detail_specular_level",nodes)
        detail_specular_level_node.outputs[0].default_value = 0.5
        
        ### mask float parameter node
        mask_height_node  = self.node_manager.create_value_node("mask_height",nodes)
        mask_height_node.outputs[0].default_value = 0.0
        mask_power_node  = self.node_manager.create_value_node("mask_power",nodes)
        mask_power_node.outputs[0].default_value = 1.0
        blend_normal_strength_node  = self.node_manager.create_value_node("blend_normal_strength",nodes)
        blend_normal_strength_node.outputs[0].default_value = 0.5
        world_blend_max_node  = self.node_manager.create_value_node("world_blend_max",nodes)
        world_blend_max_node.outputs[0].default_value = 2.0
        ### end------------------
        
        
        ### <summary>
        ### Link Texture and UV Mapping
        ### </summary>
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(detail_texture_mapping_node.outputs['Vector'], detail_base_color_opacity_texture_node.inputs['Vector'])
        links.new(detail_texture_mapping_node.outputs['Vector'], detail_normal_texture_node.inputs['Vector'])
        links.new(detail_texture_mapping_node.outputs['Vector'], detail_orm_texture_node.inputs['Vector'])
        links.new(mask_edge_texture_mapping_node.outputs['Vector'], mask_edge_noise_texture_node.inputs['Vector'])
        ### end------------------
        
        
        ### <summary>
        ### Create Group Node Tree
        ### </summary>
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="OpaqueBlendNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "opaque_blend"
        group_node.node_tree = group_node_tree

        ### Create input output node
        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        ### <summary>
        ### Create input socket
        ### </summary>
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        
        group_node_tree.interface.new_socket("Detail Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Detail Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Detail Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        
        group_node_tree.interface.new_socket("Mask Edge Noise", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        
        
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Detail Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        
        
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        
        group_node_tree.interface.new_socket("Detail Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Detail Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Detail Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Detail Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        
        group_node_tree.interface.new_socket("Mask Height", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Mask Power", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Blend Normal Strength", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("World Blend Max", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        
        
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)
        ### end------------------


        ### <summary>
        ### Link OutInput Node to Group Input Node
        ### </summary>
        ### link texture node
        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        
        links.new(detail_base_color_opacity_texture_node.outputs['Color'], group_node.inputs['Detail Base Color'])
        links.new(detail_base_color_opacity_texture_node.outputs['Alpha'], group_node.inputs['Detail Opacity Mask'])
        links.new(detail_normal_texture_node.outputs['Color'], group_node.inputs['Detail Normal'])
        links.new(detail_orm_texture_node.outputs['Color'], group_node.inputs['Detail Orm Mask'])
        
        links.new(mask_edge_noise_texture_node.outputs['Color'], group_node.inputs['Mask Edge Noise'])
        
        ### link float4 node
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(detail_base_color_multiplier_node.outputs['Color'], group_node.inputs['Detail Base Color Multiplier'])
        
        ### link float node
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])
        
        links.new(detail_metallic_scale_node.outputs['Value'], group_node.inputs['Detail Metallic Scale'])
        links.new(detail_roughness_scale_node.outputs['Value'], group_node.inputs['Detail Roughness Scale'])
        links.new(detail_specular_level_node.outputs['Value'], group_node.inputs['Detail Specular Level'])
        
        links.new(mask_height_node.outputs['Value'], group_node.inputs['Mask Height'])
        links.new(mask_power_node.outputs['Value'], group_node.inputs['Mask Power'])
        links.new(blend_normal_strength_node.outputs['Value'], group_node.inputs['Blend Normal Strength'])
        links.new(world_blend_max_node.outputs['Value'], group_node.inputs['World Blend Max'])
        ### end------------------


        ### <summary>
        ### Create BSDF Node
        ### </summary>
        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        ### bsdf node end------------------
        
        
        
        ### <summary>
        ### Create BlendWeight Node Tree
        ### </summary>
        blend_weight_group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="BlendWeightNodeTree")
        blend_weight_group_node = self.node_manager.create_utility_node("ShaderNodeGroup",group_node_tree.nodes)
        blend_weight_group_node.label = "BlendWeight"
        blend_weight_group_node.node_tree = blend_weight_group_node_tree

        ### Create input output node
        blend_weight_group_input = self.node_manager.create_utility_node("NodeGroupInput",blend_weight_group_node_tree.nodes)
        blend_weight_group_output = self.node_manager.create_utility_node("NodeGroupOutput",blend_weight_group_node_tree.nodes)

        blend_weight_group_node_tree.interface.new_socket("Base Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        blend_weight_group_node_tree.interface.new_socket("Mask Edge Noise", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        blend_weight_group_node_tree.interface.new_socket("Mask Height", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        blend_weight_group_node_tree.interface.new_socket("Mask Power", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        blend_weight_group_node_tree.interface.new_socket("Blend Normal Strength", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        blend_weight_group_node_tree.interface.new_socket("World Blend Max", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        blend_weight_group_node_tree.interface.new_socket("Result", description='', in_out='OUTPUT', socket_type="NodeSocketFloat", parent=None)

        base_normal_decode_normal_node = self.node_manager.create_decode_normal_node(blend_weight_group_node_tree.nodes)
        rgb_to_bw_node = self.node_manager.create_utility_node("ShaderNodeRGBToBW",blend_weight_group_node_tree.nodes)
        normal_vector_mix_node = self.node_manager.create_vector_mix_node(blend_weight_group_node_tree.nodes)
        normal_vector_mix_node.inputs[4].default_value = Vector((0,0,1))
        normalize_vector_node = self.node_manager.create_vector_math_node("NORMALIZE",blend_weight_group_node_tree.nodes)
        dot_unit_vector_node = self.node_manager.create_vector_math_node("DOT_PRODUCT",blend_weight_group_node_tree.nodes)
        dot_unit_vector_node.inputs[1].default_value = Vector((0,0,1))
        add_1_math_node = self.node_manager.create_value_math_node("ADD", blend_weight_group_node_tree.nodes)
        add_1_math_node.inputs[1].default_value = 1.0
        multiply_0_5_math_node = self.node_manager.create_value_math_node("MULTIPLY", blend_weight_group_node_tree.nodes)
        multiply_0_5_math_node.inputs[1].default_value = 0.5
        world_blend_max_mix_math_node = self.node_manager.create_value_mix_node(blend_weight_group_node_tree.nodes)
        world_blend_max_mix_math_node.inputs[2].default_value = -4
        subtract_mask_noise_math_node = self.node_manager.create_value_math_node("SUBTRACT",blend_weight_group_node_tree.nodes)
        add_mask_height_math_node = self.node_manager.create_value_math_node("ADD",blend_weight_group_node_tree.nodes)
        clamp_value_1_node = self.node_manager.create_utility_node("ShaderNodeClamp",blend_weight_group_node_tree.nodes)
        power_mask_power_math_node = self.node_manager.create_value_math_node("POWER",blend_weight_group_node_tree.nodes)
        clamp_value_2_node = self.node_manager.create_utility_node("ShaderNodeClamp",blend_weight_group_node_tree.nodes)
        
        ### create transform normal to world space group node
        tbn_group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="TransformNormalToWorldSpaceNodeTree")
        tbn_group_node = self.node_manager.create_utility_node("ShaderNodeGroup",blend_weight_group_node_tree.nodes)
        tbn_group_node.label = "TransformNormalToWorldSpace"
        tbn_group_node.node_tree = tbn_group_node_tree
        
        ### Create input output node
        tbn_group_input = self.node_manager.create_utility_node("NodeGroupInput",tbn_group_node_tree.nodes)
        tbn_group_output = self.node_manager.create_utility_node("NodeGroupOutput",tbn_group_node_tree.nodes)
        
        tbn_group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketVector", parent=None)
        tbn_group_node_tree.interface.new_socket("Result", description='', in_out='OUTPUT', socket_type="NodeSocketVector", parent=None)
        
        normal_separate_xyz_node = self.node_manager.create_break_vector_node(tbn_group_node_tree.nodes)
        geometry_node = self.node_manager.create_utility_node("ShaderNodeNewGeometry",tbn_group_node_tree.nodes)
        tn_cross_node = self.node_manager.create_vector_math_node("CROSS_PRODUCT",tbn_group_node_tree.nodes)
        targent_multiply_node = self.node_manager.create_vector_math_node("MULTIPLY", tbn_group_node_tree.nodes)
        binormal_multiply_node = self.node_manager.create_vector_math_node("MULTIPLY", tbn_group_node_tree.nodes)
        normal_normalize_node = self.node_manager.create_vector_math_node("NORMALIZE", tbn_group_node_tree.nodes)
        normal_multiply_node = self.node_manager.create_vector_math_node("MULTIPLY", tbn_group_node_tree.nodes)
        t_add_b_node = self.node_manager.create_vector_math_node("ADD", tbn_group_node_tree.nodes)
        b_add_n_node = self.node_manager.create_vector_math_node("ADD", tbn_group_node_tree.nodes)
        
        tbn_group_node_tree.links.new(tbn_group_input.outputs["Normal"],normal_separate_xyz_node.inputs["Vector"])
        tbn_group_node_tree.links.new(geometry_node.outputs["Tangent"],targent_multiply_node.inputs[0])
        tbn_group_node_tree.links.new(normal_separate_xyz_node.outputs["X"],targent_multiply_node.inputs[1])
        tbn_group_node_tree.links.new(geometry_node.outputs["Normal"],tn_cross_node.inputs[0])
        tbn_group_node_tree.links.new(geometry_node.outputs["Tangent"],tn_cross_node.inputs[1])
        tbn_group_node_tree.links.new(tn_cross_node.outputs["Vector"],binormal_multiply_node.inputs[0])
        tbn_group_node_tree.links.new(normal_separate_xyz_node.outputs["Y"],binormal_multiply_node.inputs[1])
        tbn_group_node_tree.links.new(geometry_node.outputs["Normal"],normal_normalize_node.inputs["Vector"])
        tbn_group_node_tree.links.new(normal_normalize_node.outputs["Vector"],normal_multiply_node.inputs[0])
        tbn_group_node_tree.links.new(normal_separate_xyz_node.outputs["Z"],normal_multiply_node.inputs[1])
        
        tbn_group_node_tree.links.new(targent_multiply_node.outputs["Vector"],t_add_b_node.inputs[0])
        tbn_group_node_tree.links.new(binormal_multiply_node.outputs["Vector"],t_add_b_node.inputs[1])
        tbn_group_node_tree.links.new(t_add_b_node.outputs["Vector"],b_add_n_node.inputs[0])
        tbn_group_node_tree.links.new(normal_multiply_node.outputs["Vector"],b_add_n_node.inputs[1])
        tbn_group_node_tree.links.new(b_add_n_node.outputs["Vector"],tbn_group_output.inputs["Result"])
        ### transform normal to world space group node end
        
        blend_weight_group_node_tree.links.new(blend_weight_group_input.outputs["Mask Edge Noise"], rgb_to_bw_node.inputs["Color"])
        blend_weight_group_node_tree.links.new(blend_weight_group_input.outputs["Base Normal"], base_normal_decode_normal_node.inputs["Color"])
        blend_weight_group_node_tree.links.new(base_normal_decode_normal_node.outputs["Normal"], normal_vector_mix_node.inputs[5])
        blend_weight_group_node_tree.links.new(blend_weight_group_input.outputs["Blend Normal Strength"], normal_vector_mix_node.inputs[0])
        blend_weight_group_node_tree.links.new(normal_vector_mix_node.outputs["Result"], tbn_group_node.inputs["Normal"])
        blend_weight_group_node_tree.links.new(tbn_group_node.outputs["Result"], normalize_vector_node.inputs["Vector"])
        blend_weight_group_node_tree.links.new(normalize_vector_node.outputs["Vector"], dot_unit_vector_node.inputs[0])
        blend_weight_group_node_tree.links.new(dot_unit_vector_node.outputs["Value"], add_1_math_node.inputs[0])
        blend_weight_group_node_tree.links.new(add_1_math_node.outputs["Value"], multiply_0_5_math_node.inputs[0])
        blend_weight_group_node_tree.links.new(multiply_0_5_math_node.outputs["Value"], world_blend_max_mix_math_node.inputs[0])
        blend_weight_group_node_tree.links.new(blend_weight_group_input.outputs["World Blend Max"], world_blend_max_mix_math_node.inputs[3])
        blend_weight_group_node_tree.links.new(world_blend_max_mix_math_node.outputs["Result"], subtract_mask_noise_math_node.inputs[0])
        blend_weight_group_node_tree.links.new(rgb_to_bw_node.outputs["Val"], subtract_mask_noise_math_node.inputs[1])
        blend_weight_group_node_tree.links.new(subtract_mask_noise_math_node.outputs["Value"], add_mask_height_math_node.inputs[0])
        blend_weight_group_node_tree.links.new(blend_weight_group_input.outputs["Mask Height"], add_mask_height_math_node.inputs[1])
        blend_weight_group_node_tree.links.new(add_mask_height_math_node.outputs["Value"], clamp_value_1_node.inputs[0])
        blend_weight_group_node_tree.links.new(clamp_value_1_node.outputs["Result"], power_mask_power_math_node.inputs[0])
        blend_weight_group_node_tree.links.new(blend_weight_group_input.outputs["Mask Power"], power_mask_power_math_node.inputs[1])
        blend_weight_group_node_tree.links.new(power_mask_power_math_node.outputs["Value"], clamp_value_2_node.inputs[0])
        blend_weight_group_node_tree.links.new(clamp_value_2_node.outputs["Result"], blend_weight_group_output.inputs["Result"])
        ### blend weight group node end------------------
        
        
        ### <summary>
        ### Create Base Color Blend Node Tree
        ### </summary>
        base_color_blend_group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="BaseColorBlendNodeTree")
        base_color_blend_group_node = self.node_manager.create_utility_node("ShaderNodeGroup",group_node_tree.nodes)
        base_color_blend_group_node.label = "BaseColorBlend"
        base_color_blend_group_node.node_tree = base_color_blend_group_node_tree
        
        base_color_blend_group_input = self.node_manager.create_utility_node("NodeGroupInput",base_color_blend_group_node_tree.nodes)
        base_color_blend_group_output = self.node_manager.create_utility_node("NodeGroupOutput",base_color_blend_group_node_tree.nodes)
        
        base_color_blend_group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        base_color_blend_group_node_tree.interface.new_socket("Detail Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        base_color_blend_group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        base_color_blend_group_node_tree.interface.new_socket("Detail Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        base_color_blend_group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        base_color_blend_group_node_tree.interface.new_socket("Detail Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        base_color_blend_group_node_tree.interface.new_socket("Blend Weight", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        base_color_blend_group_node_tree.interface.new_socket("Final Color", description='', in_out='OUTPUT', socket_type="NodeSocketColor", parent=None)
        base_color_blend_group_node_tree.interface.new_socket("Final Alpha", description='', in_out='OUTPUT', socket_type="NodeSocketColor", parent=None)
        
        base_color_multiply_node = self.node_manager.create_vector_math_node("MULTIPLY",base_color_blend_group_node_tree.nodes)
        detail_base_color_multiply_node = self.node_manager.create_vector_math_node("MULTIPLY",base_color_blend_group_node_tree.nodes)
        mix_color_node = self.node_manager.create_vector_mix_node(base_color_blend_group_node_tree.nodes)
        mix_value_node = self.node_manager.create_value_mix_node(base_color_blend_group_node_tree.nodes)
        
        base_color_blend_group_node_tree.links.new(base_color_blend_group_input.outputs["Base Color"],base_color_multiply_node.inputs[0])
        base_color_blend_group_node_tree.links.new(base_color_blend_group_input.outputs["Base Color Multiplier"],base_color_multiply_node.inputs[1])
        base_color_blend_group_node_tree.links.new(base_color_blend_group_input.outputs["Detail Base Color"],detail_base_color_multiply_node.inputs[0])
        base_color_blend_group_node_tree.links.new(base_color_blend_group_input.outputs["Detail Base Color Multiplier"],detail_base_color_multiply_node.inputs[1])
        
        base_color_blend_group_node_tree.links.new(base_color_blend_group_input.outputs["Blend Weight"],mix_color_node.inputs[0])
        base_color_blend_group_node_tree.links.new(base_color_multiply_node.outputs["Vector"],mix_color_node.inputs[4])
        base_color_blend_group_node_tree.links.new(detail_base_color_multiply_node.outputs["Vector"],mix_color_node.inputs[5])
        
        base_color_blend_group_node_tree.links.new(base_color_blend_group_input.outputs["Blend Weight"],mix_value_node.inputs[0])
        base_color_blend_group_node_tree.links.new(base_color_blend_group_input.outputs["Opacity Mask"],mix_value_node.inputs[2])
        base_color_blend_group_node_tree.links.new(base_color_blend_group_input.outputs["Detail Opacity Mask"],mix_value_node.inputs[3])
        
        base_color_blend_group_node_tree.links.new(mix_color_node.outputs["Result"],base_color_blend_group_output.inputs["Final Color"])
        base_color_blend_group_node_tree.links.new(mix_value_node.outputs["Result"],base_color_blend_group_output.inputs["Final Alpha"])
        ### Base Color Blend group node end------------------
        
        
        ### <summary>
        ### Create Normal Blend Node Tree
        ### </summary>
        normal_blend_group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="NormalBlendNodeTree")
        normal_blend_group_node = self.node_manager.create_utility_node("ShaderNodeGroup",group_node_tree.nodes)
        normal_blend_group_node.label = "NormalBlend"
        normal_blend_group_node.node_tree = normal_blend_group_node_tree

        ### Create input output node
        normal_blend_group_input = self.node_manager.create_utility_node("NodeGroupInput",normal_blend_group_node_tree.nodes)
        normal_blend_group_output = self.node_manager.create_utility_node("NodeGroupOutput",normal_blend_group_node_tree.nodes)

        normal_blend_group_node_tree.interface.new_socket("Base Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        normal_blend_group_node_tree.interface.new_socket("Detail Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        normal_blend_group_node_tree.interface.new_socket("Blend Weight", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        normal_blend_group_node_tree.interface.new_socket("Result", description='', in_out='OUTPUT', socket_type="NodeSocketVector", parent=None)

        base_decode_normal_node = self.node_manager.create_decode_normal_node(normal_blend_group_node_tree.nodes)
        detail_decode_normal_node = self.node_manager.create_decode_normal_node(normal_blend_group_node_tree.nodes)
        normal_mix_vector_node = self.node_manager.create_vector_mix_node(normal_blend_group_node_tree.nodes)
        ### end------------------
        
        
        ### <summary>
        ### Create BlendAngleCorrectedNormal Node Tree
        ### </summary>
        blend_normal_group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="BlendAngleCorrectedNormalNodeTree")
        blend_normal_group_node = self.node_manager.create_utility_node("ShaderNodeGroup",normal_blend_group_node_tree.nodes)
        blend_normal_group_node.label = "BlendAngleCorrectedNormal"
        blend_normal_group_node.node_tree = blend_normal_group_node_tree
        
        ### Create input output node
        blend_normal_group_input = self.node_manager.create_utility_node("NodeGroupInput",blend_normal_group_node_tree.nodes)
        blend_normal_group_output = self.node_manager.create_utility_node("NodeGroupOutput",blend_normal_group_node_tree.nodes)
        
        blend_normal_group_node_tree.interface.new_socket("Base Normal", description='', in_out='INPUT', socket_type="NodeSocketVector", parent=None)
        blend_normal_group_node_tree.interface.new_socket("Detail Normal", description='', in_out='INPUT', socket_type="NodeSocketVector", parent=None)
        blend_normal_group_node_tree.interface.new_socket("Result", description='', in_out='OUTPUT', socket_type="NodeSocketVector", parent=None)
        
        base_normal_separate_xyz_node = self.node_manager.create_break_vector_node(blend_normal_group_node_tree.nodes)
        base_normal_add_value_math_node = self.node_manager.create_value_math_node("ADD", blend_normal_group_node_tree.nodes)
        base_normal_add_value_math_node.inputs[1].default_value = 1.0
        base_normal_combine_xyz_node = self.node_manager.create_combine_vector_node(blend_normal_group_node_tree.nodes)
        base_normal_multiply_vector_math_node = self.node_manager.create_vector_math_node("MULTIPLY", blend_normal_group_node_tree.nodes)
        base_normal_separate_z_node = self.node_manager.create_break_vector_node(blend_normal_group_node_tree.nodes)
        base_normal_subtract_vector_math_node = self.node_manager.create_vector_math_node("SUBTRACT", blend_normal_group_node_tree.nodes)
        
        detail_normal_separate_xyz_node = self.node_manager.create_break_vector_node(blend_normal_group_node_tree.nodes)
        detail_normal_multiply_x_value_math_node = self.node_manager.create_value_math_node("MULTIPLY", blend_normal_group_node_tree.nodes)
        detail_normal_multiply_x_value_math_node.inputs[1].default_value = -1.0
        detail_normal_multiply_y_value_math_node = self.node_manager.create_value_math_node("MULTIPLY", blend_normal_group_node_tree.nodes)
        detail_normal_multiply_y_value_math_node.inputs[1].default_value = -1.0
        detail_normal_combine_xyz_node = self.node_manager.create_combine_vector_node(blend_normal_group_node_tree.nodes)
        detail_normal_multiply_vector_math_node = self.node_manager.create_vector_math_node("MULTIPLY", blend_normal_group_node_tree.nodes)
        
        dot_vertor_math_node = self.node_manager.create_vector_math_node('DOT_PRODUCT',blend_normal_group_node_tree.nodes)
        
        ### link
        blend_normal_group_node_tree.links.new(blend_normal_group_input.outputs["Base Normal"], base_normal_separate_xyz_node.inputs["Vector"])
        blend_normal_group_node_tree.links.new(base_normal_separate_xyz_node.outputs["X"], base_normal_combine_xyz_node.inputs["X"])
        blend_normal_group_node_tree.links.new(base_normal_separate_xyz_node.outputs["Y"], base_normal_combine_xyz_node.inputs["Y"])
        blend_normal_group_node_tree.links.new(base_normal_separate_xyz_node.outputs["Z"], base_normal_add_value_math_node.inputs[0])
        blend_normal_group_node_tree.links.new(base_normal_add_value_math_node.outputs["Value"], base_normal_combine_xyz_node.inputs["Z"])
        
        blend_normal_group_node_tree.links.new(blend_normal_group_input.outputs["Detail Normal"], detail_normal_separate_xyz_node.inputs["Vector"])
        blend_normal_group_node_tree.links.new(detail_normal_separate_xyz_node.outputs["X"], detail_normal_multiply_x_value_math_node.inputs[0])
        blend_normal_group_node_tree.links.new(detail_normal_separate_xyz_node.outputs["Y"], detail_normal_multiply_y_value_math_node.inputs[0])
        blend_normal_group_node_tree.links.new(detail_normal_multiply_x_value_math_node.outputs["Value"], detail_normal_combine_xyz_node.inputs["X"])
        blend_normal_group_node_tree.links.new(detail_normal_multiply_y_value_math_node.outputs["Value"], detail_normal_combine_xyz_node.inputs["Y"])
        blend_normal_group_node_tree.links.new(detail_normal_separate_xyz_node.outputs["Z"], detail_normal_combine_xyz_node.inputs["Z"])
        
        blend_normal_group_node_tree.links.new(base_normal_combine_xyz_node.outputs["Vector"], dot_vertor_math_node.inputs[0])
        blend_normal_group_node_tree.links.new(detail_normal_combine_xyz_node.outputs["Vector"], dot_vertor_math_node.inputs[1])
        blend_normal_group_node_tree.links.new(base_normal_combine_xyz_node.outputs["Vector"], base_normal_multiply_vector_math_node.inputs[0])
        blend_normal_group_node_tree.links.new(dot_vertor_math_node.outputs["Value"], base_normal_multiply_vector_math_node.inputs[1])
        
        blend_normal_group_node_tree.links.new(detail_normal_combine_xyz_node.outputs["Vector"], detail_normal_multiply_vector_math_node.inputs[0])
        blend_normal_group_node_tree.links.new(base_normal_combine_xyz_node.outputs["Vector"], base_normal_separate_z_node.inputs["Vector"])
        blend_normal_group_node_tree.links.new(base_normal_separate_z_node.outputs["Z"], detail_normal_multiply_vector_math_node.inputs[1])
        
        blend_normal_group_node_tree.links.new(base_normal_multiply_vector_math_node.outputs["Vector"], base_normal_subtract_vector_math_node.inputs[0])
        blend_normal_group_node_tree.links.new(detail_normal_multiply_vector_math_node.outputs["Vector"], base_normal_subtract_vector_math_node.inputs[1])
        
        blend_normal_group_node_tree.links.new(base_normal_subtract_vector_math_node.outputs["Vector"], blend_normal_group_output.inputs["Result"])
        ### blend normal group end------------------

        normal_blend_group_node_tree.links.new(normal_blend_group_input.outputs["Base Normal"], base_decode_normal_node.inputs["Color"])
        normal_blend_group_node_tree.links.new(normal_blend_group_input.outputs["Detail Normal"], detail_decode_normal_node.inputs["Color"])
        normal_blend_group_node_tree.links.new(base_decode_normal_node.outputs["Normal"], blend_normal_group_node.inputs["Base Normal"])
        normal_blend_group_node_tree.links.new(detail_decode_normal_node.outputs["Normal"], blend_normal_group_node.inputs["Detail Normal"])

        normal_blend_group_node_tree.links.new(normal_blend_group_input.outputs["Blend Weight"], normal_mix_vector_node.inputs[0])
        normal_blend_group_node_tree.links.new(base_decode_normal_node.outputs["Normal"], normal_mix_vector_node.inputs[4])
        normal_blend_group_node_tree.links.new(blend_normal_group_node.outputs["Result"], normal_mix_vector_node.inputs[5])

        normal_blend_group_node_tree.links.new(normal_mix_vector_node.outputs["Result"], normal_blend_group_output.inputs["Result"])
        ### normal blend group node end------------------
        
        
        ### <summary>
        ### Create Orm Mask Blend Node Tree
        ### </summary>
        orm_mask_blend_group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="OrmMaskBlendNodeTree")
        orm_mask_blend_group_node = self.node_manager.create_utility_node("ShaderNodeGroup",group_node_tree.nodes)
        orm_mask_blend_group_node.label = "OrmMaskBlend"
        orm_mask_blend_group_node.node_tree = orm_mask_blend_group_node_tree
        
        orm_mask_blend_group_input = self.node_manager.create_utility_node("NodeGroupInput",orm_mask_blend_group_node_tree.nodes)
        orm_mask_blend_group_output = self.node_manager.create_utility_node("NodeGroupOutput",orm_mask_blend_group_node_tree.nodes)
        
        orm_mask_blend_group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Detail Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Detail Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Detail Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Detail Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Blend Weight", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Final Metallic", description='', in_out='OUTPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Final Roughness", description='', in_out='OUTPUT', socket_type="NodeSocketFloat", parent=None)
        orm_mask_blend_group_node_tree.interface.new_socket("Final Specular Level", description='', in_out='OUTPUT', socket_type="NodeSocketFloat", parent=None)
        
        orm_mask_separate_xyz_node = self.node_manager.create_break_vector_node(orm_mask_blend_group_node_tree.nodes)
        detail_orm_mask_separate_xyz_node = self.node_manager.create_break_vector_node(orm_mask_blend_group_node_tree.nodes)
        metallic_multiply_node = self.node_manager.create_value_math_node("MULTIPLY",orm_mask_blend_group_node_tree.nodes)
        roughness_multiply_node = self.node_manager.create_value_math_node("MULTIPLY",orm_mask_blend_group_node_tree.nodes)
        detail_metallic_multiply_node = self.node_manager.create_value_math_node("MULTIPLY",orm_mask_blend_group_node_tree.nodes)
        detail_roughness_multiply_node = self.node_manager.create_value_math_node("MULTIPLY",orm_mask_blend_group_node_tree.nodes)
        mix_metallic_node = self.node_manager.create_value_mix_node(orm_mask_blend_group_node_tree.nodes)
        mix_roughness_node = self.node_manager.create_value_mix_node(orm_mask_blend_group_node_tree.nodes)
        mix_specular_level_node = self.node_manager.create_value_mix_node(orm_mask_blend_group_node_tree.nodes)
        
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Orm Mask"], orm_mask_separate_xyz_node.inputs["Vector"])
        orm_mask_blend_group_node_tree.links.new(orm_mask_separate_xyz_node.outputs["Y"], roughness_multiply_node.inputs[0])
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Roughness Scale"], roughness_multiply_node.inputs[1])
        orm_mask_blend_group_node_tree.links.new(orm_mask_separate_xyz_node.outputs["Z"], metallic_multiply_node.inputs[0])
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Metallic Scale"], metallic_multiply_node.inputs[1])
        
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Detail Orm Mask"], detail_orm_mask_separate_xyz_node.inputs["Vector"])
        orm_mask_blend_group_node_tree.links.new(detail_orm_mask_separate_xyz_node.outputs["Y"], detail_roughness_multiply_node.inputs[0])
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Detail Roughness Scale"], detail_roughness_multiply_node.inputs[1])
        orm_mask_blend_group_node_tree.links.new(detail_orm_mask_separate_xyz_node.outputs["Z"], detail_metallic_multiply_node.inputs[0])
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Detail Metallic Scale"], detail_metallic_multiply_node.inputs[1])
        
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Blend Weight"], mix_metallic_node.inputs[0])
        orm_mask_blend_group_node_tree.links.new(metallic_multiply_node.outputs["Value"], mix_metallic_node.inputs[2])
        orm_mask_blend_group_node_tree.links.new(detail_metallic_multiply_node.outputs["Value"], mix_metallic_node.inputs[3])
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Blend Weight"], mix_roughness_node.inputs[0])
        orm_mask_blend_group_node_tree.links.new(roughness_multiply_node.outputs["Value"], mix_roughness_node.inputs[2])
        orm_mask_blend_group_node_tree.links.new(detail_roughness_multiply_node.outputs["Value"], mix_roughness_node.inputs[3])
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Blend Weight"], mix_specular_level_node.inputs[0])
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Specular Level"], mix_specular_level_node.inputs[2])
        orm_mask_blend_group_node_tree.links.new(orm_mask_blend_group_input.outputs["Detail Specular Level"], mix_specular_level_node.inputs[3])
        
        orm_mask_blend_group_node_tree.links.new(mix_metallic_node.outputs["Result"], orm_mask_blend_group_output.inputs["Final Metallic"])
        orm_mask_blend_group_node_tree.links.new(mix_roughness_node.outputs["Result"], orm_mask_blend_group_output.inputs["Final Roughness"])
        orm_mask_blend_group_node_tree.links.new(mix_specular_level_node.outputs["Result"], orm_mask_blend_group_output.inputs["Final Specular Level"])
        ### end------------------
        
        
        ### <summary>
        ### link group node
        ### </summary>
        group_node_tree.links.new(group_input.outputs["Base Color"],base_color_blend_group_node.inputs["Base Color"])
        group_node_tree.links.new(group_input.outputs["Normal"], normal_blend_group_node.inputs["Base Normal"])
        group_node_tree.links.new(group_input.outputs["Orm Mask"],orm_mask_blend_group_node.inputs["Orm Mask"])
        group_node_tree.links.new(group_input.outputs["Detail Base Color"],base_color_blend_group_node.inputs["Detail Base Color"])
        group_node_tree.links.new(group_input.outputs["Detail Normal"],normal_blend_group_node.inputs["Detail Normal"])
        group_node_tree.links.new(group_input.outputs["Detail Orm Mask"],orm_mask_blend_group_node.inputs["Detail Orm Mask"])
        group_node_tree.links.new(group_input.outputs["Base Color Multiplier"],base_color_blend_group_node.inputs["Base Color Multiplier"])
        group_node_tree.links.new(group_input.outputs["Detail Base Color Multiplier"],base_color_blend_group_node.inputs["Detail Base Color Multiplier"])
        group_node_tree.links.new(group_input.outputs["Metallic Scale"],orm_mask_blend_group_node.inputs["Metallic Scale"])
        group_node_tree.links.new(group_input.outputs["Roughness Scale"],orm_mask_blend_group_node.inputs["Roughness Scale"])
        group_node_tree.links.new(group_input.outputs["Specular Level"],orm_mask_blend_group_node.inputs["Specular Level"])
        group_node_tree.links.new(group_input.outputs["Detail Metallic Scale"],orm_mask_blend_group_node.inputs["Detail Metallic Scale"])
        group_node_tree.links.new(group_input.outputs["Detail Roughness Scale"],orm_mask_blend_group_node.inputs["Detail Roughness Scale"])
        group_node_tree.links.new(group_input.outputs["Detail Specular Level"],orm_mask_blend_group_node.inputs["Detail Specular Level"])
        group_node_tree.links.new(group_input.outputs["Opacity Mask"],base_color_blend_group_node.inputs["Opacity Mask"])
        group_node_tree.links.new(group_input.outputs["Detail Opacity Mask"],base_color_blend_group_node.inputs["Detail Opacity Mask"])
        group_node_tree.links.new(group_input.outputs["Normal"], blend_weight_group_node.inputs["Base Normal"])
        group_node_tree.links.new(group_input.outputs["Mask Edge Noise"], blend_weight_group_node.inputs["Mask Edge Noise"])
        group_node_tree.links.new(group_input.outputs["Mask Height"],blend_weight_group_node.inputs["Mask Height"])
        group_node_tree.links.new(group_input.outputs["Mask Power"],blend_weight_group_node.inputs["Mask Power"])
        group_node_tree.links.new(group_input.outputs["Blend Normal Strength"],blend_weight_group_node.inputs["Blend Normal Strength"])
        group_node_tree.links.new(group_input.outputs["World Blend Max"],blend_weight_group_node.inputs["World Blend Max"])
        
        group_node_tree.links.new(blend_weight_group_node.outputs["Result"],base_color_blend_group_node.inputs["Blend Weight"])
        group_node_tree.links.new(blend_weight_group_node.outputs["Result"],normal_blend_group_node.inputs["Blend Weight"])
        group_node_tree.links.new(blend_weight_group_node.outputs["Result"],orm_mask_blend_group_node.inputs["Blend Weight"])
        
        group_node_tree.links.new(base_color_blend_group_node.outputs["Final Color"],bsdf_node.inputs["Base Color"])
        group_node_tree.links.new(base_color_blend_group_node.outputs["Final Alpha"],bsdf_node.inputs["Alpha"])
        group_node_tree.links.new(normal_blend_group_node.outputs["Result"],bsdf_node.inputs["Normal"])
        group_node_tree.links.new(orm_mask_blend_group_node.outputs["Final Metallic"],bsdf_node.inputs["Metallic"])
        group_node_tree.links.new(orm_mask_blend_group_node.outputs["Final Roughness"],bsdf_node.inputs["Roughness"])
        group_node_tree.links.new(orm_mask_blend_group_node.outputs["Final Specular Level"],bsdf_node.inputs["Specular IOR Level"])
        
        group_node_tree.links.new(bsdf_node.outputs["BSDF"],group_output.inputs["BSDF"])
        
        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "opaque_character_hero"
        return material



class DecalMaterial(OpaqueBase):

    def __init__(self):
        super().__init__()



class OpaqueSubsurfaceBase(OpaqueBase):

    def __init__(self):
        super().__init__()
        self.subsurface_color_map : Texture = Texture()
        self.subsurface_color_multiplier : Vector = Vector((1.0, 1.0, 1.0, 1.0))
        self.density_map : Texture = Texture()
        self.opacity_multiplier : float = 1.0

    
    def set_opaque_subsurface_base_parameters_from_object(self, node, shader_type):
        self.set_opaque_base_parameters_from_object(node,shader_type)
        if node.label == "subsurface_color_map":
            self.subsurface_color_map.set_texture_from_object(node)
        elif node.label == "subsurface_color_multiplier":
            self.subsurface_color_multiplier = node.outputs['Color'].default_value
        elif node.label == "density_map":
            self.density_map.set_texture_from_object(node)
        elif node.label == "opacity_multiplier":
            self.opacity_multiplier = node.outputs[0].default_value


    def set_opaque_subsurface_base_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)
        self.subsurface_color_map.set_texture_from_json(material_parameters["subsurface_color_map"])
        subsurface_color_multiplier = material_parameters["subsurface_color_multiplier"]
        self.subsurface_color_multiplier = Vector((subsurface_color_multiplier[0], subsurface_color_multiplier[1], subsurface_color_multiplier[2], subsurface_color_multiplier[3]))
        self.density_map.set_texture_from_json(material_parameters["density_map"])
        self.opacity_multiplier = material_parameters["opacity_multiplier"]


    def get_opaque_subsurface_base_parameters_to_json(self):
        material_parameters : dict = {}
        material_parameters = self.get_opaque_base_parameters_to_json()
        material_parameters["subsurface_color_map"] = self.subsurface_color_map.get_texture_to_json()
        material_parameters["subsurface_color_multiplier"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.subsurface_color_multiplier)
        material_parameters["density_map"] = self.density_map.get_texture_to_json()
        material_parameters["opacity_multiplier"] = self.opacity_multiplier
        return material_parameters
    

    def get_opaque_subsurface_base_parameters_to_object(self, node, shader_type):
        self.get_opaque_base_parameters_to_object(node,shader_type)
        if node.label == "subsurface_color_map":
            node = self.subsurface_color_map.get_texture_to_object(node)
        elif node.label == "subsurface_color_multiplier":
            node.outputs['Color'].default_value = self.subsurface_color_multiplier
        elif node.label == "density_map":
            node = self.density_map.get_texture_to_object(node)
        elif node.label == "opacity_multiplier":
            node.outputs[0].default_value = self.opacity_multiplier



class CheapSubsurfaceMaterial(OpaqueSubsurfaceBase):

    def __init__(self):
        super().__init__()


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_opaque_subsurface_base_parameters_from_object(node,shader_type)


    def set_material_parameters_from_json(self, material_parameters):
        self.set_opaque_subsurface_base_parameters_from_json(material_parameters)


    def get_material_parameters_to_json(self):
        return self.get_opaque_subsurface_base_parameters_to_json()
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_opaque_subsurface_base_parameters_to_object(node,shader_type)
        return material
    

    def create_shader_template(self, material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        subsurface_color_texture_node = self.node_manager.create_texture_node("subsurface_color_map",nodes)
        subsurface_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        
        density_texture_node = self.node_manager.create_texture_node("density_map",nodes)
        density_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        subsurface_color_multiplier_node = self.node_manager.create_color_node("subsurface_color_multiplier",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        opacity_multiplier_node  = self.node_manager.create_value_node("opacity_multiplier",nodes)
        opacity_multiplier_node.outputs[0].default_value = 1.0
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], subsurface_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], density_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="CheapSubsurfaceNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "cheap_subsurface"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Subsurface Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Subsurface Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Density", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Multiplier", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(subsurface_color_texture_node.outputs['Color'], group_node.inputs['Subsurface Color'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(subsurface_color_multiplier_node.outputs['Color'], group_node.inputs['Subsurface Color Multiplier'])
        links.new(density_texture_node.outputs['Color'], group_node.inputs['Density'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])
        links.new(opacity_multiplier_node.outputs['Value'], group_node.inputs['Opacity Multiplier'])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs['Base Color'])
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "cheap_subsurface"
        return material



class TwoSideFoliageMaterial(OpaqueSubsurfaceBase):

    def __init__(self):
        super().__init__()


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_opaque_subsurface_base_parameters_from_object(node,shader_type)


    def set_material_parameters_from_json(self, material_parameters):
        self.set_opaque_subsurface_base_parameters_from_json(material_parameters)


    def get_material_parameters_to_json(self):
        return self.get_opaque_subsurface_base_parameters_to_json()
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_opaque_subsurface_base_parameters_to_object(node,shader_type)
        return material
    

    def create_shader_template(self, material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        subsurface_color_texture_node = self.node_manager.create_texture_node("subsurface_color_map",nodes)
        subsurface_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        
        density_texture_node = self.node_manager.create_texture_node("density_map",nodes)
        density_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        subsurface_color_multiplier_node = self.node_manager.create_color_node("subsurface_color_multiplier",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        opacity_multiplier_node  = self.node_manager.create_value_node("opacity_multiplier",nodes)
        opacity_multiplier_node.outputs[0].default_value = 1.0
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], subsurface_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], density_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="TwoSideFoliageNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "two_side_foliage"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Subsurface Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Subsurface Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Density", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Multiplier", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(subsurface_color_texture_node.outputs['Color'], group_node.inputs['Subsurface Color'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(subsurface_color_multiplier_node.outputs['Color'], group_node.inputs['Subsurface Color Multiplier'])
        links.new(density_texture_node.outputs['Color'], group_node.inputs['Density'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])
        links.new(opacity_multiplier_node.outputs['Value'], group_node.inputs['Opacity Multiplier'])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs['Base Color'])
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "two_side_foliage"
        return material



class SubsurfaceProfileBase(OpaqueBase):

    def __init__(self):
        super().__init__()
        self.sss_mask_map : Texture = Texture()
        self.sss_thickness_map : Texture = Texture()
        self.sss_strength_scale : float =  1.0


    def set_subsurface_profile_base_parameters_from_object(self, node, shader_type):
        self.set_opaque_base_parameters_from_object(node,shader_type)
        if node.label == "sss_mask_map":
            self.sss_mask_map.set_texture_from_object(node)
        elif node.label == "sss_thickness_map":
            self.sss_thickness_map.set_texture_from_object(node)
        elif node.label == "sss_strength_scale":
            self.sss_strength_scale = node.outputs[0].default_value


    def set_subsurface_profile_base_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)
        self.sss_mask_map.set_texture_from_json(material_parameters["sss_mask_map"])
        self.sss_thickness_map.set_texture_from_json(material_parameters["sss_thickness_map"])
        self.sss_strength_scale = material_parameters["sss_strength_scale"]


    def get_subsurface_profile_base_parameters_to_json(self):
        material_parameters : dict = self.get_opaque_base_parameters_to_json()
        material_parameters["sss_mask_map"] = self.sss_mask_map.get_texture_to_json()
        material_parameters["sss_thickness_map"] = self.sss_thickness_map.get_texture_to_json()
        material_parameters["sss_strength_scale"] = self.sss_strength_scale
        return material_parameters
    

    def get_subsurface_profile_base_parameters_to_object(self, node, shader_type):
        self.get_opaque_base_parameters_to_object(node,shader_type)
        if node.label == "sss_mask_map":
            node = self.sss_mask_map.get_texture_to_object(node)
        elif node.label == "sss_thickness_map":
            node = self.sss_thickness_map.get_texture_to_object(node)
        elif node.label == "sss_strength_scale":
            node.outputs[0].default_value = self.sss_strength_scale



class SubsurfaceProfileMaterial(SubsurfaceProfileBase):

    def __init__(self):
        super().__init__()


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_subsurface_profile_base_parameters_from_object(node,shader_type)


    def set_material_parameters_from_json(self, material_parameters):
        self.set_subsurface_profile_base_parameters_from_json(material_parameters)


    def get_material_parameters_to_json(self):
        return self.get_subsurface_profile_base_parameters_to_json()
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_subsurface_profile_base_parameters_to_object(node,shader_type)
        return material
    

    def create_shader_template(self, material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        sss_mask_texture_node = self.node_manager.create_texture_node("sss_mask_map",nodes)
        sss_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        
        sss_thickness_texture_node = self.node_manager.create_texture_node("sss_thickness_map",nodes)
        sss_thickness_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        sss_strength_scale_node  = self.node_manager.create_value_node("sss_strength_scale",nodes)
        sss_strength_scale_node.outputs[0].default_value = 1.0
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], sss_mask_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], sss_thickness_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="SubsurfaceProfileNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "subsurface_profile"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("SSS Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("SSS Thickness", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("SSS Strength", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(sss_mask_texture_node.outputs['Color'], group_node.inputs["SSS Mask"])
        links.new(sss_thickness_texture_node.outputs['Color'], group_node.inputs["SSS Thickness"])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])
        links.new(sss_strength_scale_node.outputs['Value'], group_node.inputs["SSS Strength"])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs['Base Color'])
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "subsurface_profile"
        return material



class SSSSubsurfaceProfileMrCCMaterial(SubsurfaceProfileBase):

    def __init__(self):
        super().__init__()
        self.use_cc_thickness_map : bool = False
        self.micro_normal_map : Texture = Texture()
        self.micro_roughness_map : Texture = Texture()
        self.micro_normal_mask_map : Texture = Texture()
        self.blend_normal_map : Texture = Texture()
        self.normal_strength : float = 1.0
        self.micro_normal_strength : float = 1.0
        self.blend_normal_strength : float = 1.0
        self.edge_roughness_multiplier : float = 1.0
        self.sss_strength : float = 1.0
        self.sss_contrast : float = 1.0
        self.base_color_brightness : float = 1.0
        self.micro_uv : float = 1.0
        self.micro_roughness_scale : float = 1.0


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_subsurface_profile_base_parameters_from_object(node,shader_type)

            if node.label == "micro_normal_map":
                self.micro_normal_map.set_texture_from_object(node)
            elif node.label == "micro_roughness_map":
                self.micro_roughness_map.set_texture_from_object(node)
            elif node.label == "micro_normal_mask_map":
                self.micro_normal_mask_map.set_texture_from_object(node)
            elif node.label == "blend_normal_map":
                self.blend_normal_map.set_texture_from_object(node)
            elif node.label == shader_type:
                self.use_cc_thickness_map = node.inputs["Use CC Thickness Map"].default_value
            elif node.label == "normal_strength":
                self.normal_strength = node.outputs[0].default_value
            elif node.label == "micro_normal_strength":
                self.micro_normal_strength = node.outputs[0].default_value
            elif node.label == "blend_normal_strength":
                self.blend_normal_strength = node.outputs[0].default_value
            elif node.label == "edge_roughness_multiplier":
                self.edge_roughness_multiplier = node.outputs[0].default_value
            elif node.label == "sss_strength":
                self.sss_strength = node.outputs[0].default_value
            elif node.label == "sss_contrast":
                self.sss_contrast = node.outputs[0].default_value
            elif node.label == "base_color_brightness":
                self.base_color_brightness = node.outputs[0].default_value
            elif node.label == "micro_uv":
                self.micro_uv = node.outputs[0].default_value
            elif node.label == "micro_roughness_scale":
                self.micro_roughness_scale = node.outputs[0].default_value


    def set_material_parameters_from_json(self, material_parameters):
        self.set_subsurface_profile_base_parameters_from_json(material_parameters)

        self.micro_normal_map.set_texture_from_json(material_parameters["micro_normal_map"])
        self.sss_thickness_map.set_texture_from_json(material_parameters["micro_roughness_map"])
        self.micro_normal_mask_map.set_texture_from_json(material_parameters["micro_normal_mask_map"])
        self.blend_normal_map.set_texture_from_json(material_parameters["blend_normal_map"])
        self.use_cc_thickness_map = material_parameters["use_cc_thickness_map"]
        self.normal_strength = material_parameters["normal_strength"]
        self.micro_normal_strength = material_parameters["micro_normal_strength"]
        self.blend_normal_strength = material_parameters["blend_normal_strength"]
        self.edge_roughness_multiplier = material_parameters["edge_roughness_multiplier"]
        self.sss_strength = material_parameters["sss_strength"]
        self.sss_contrast = material_parameters["sss_contrast"]
        self.base_color_brightness = material_parameters["base_color_brightness"]
        self.micro_uv = material_parameters["micro_uv"]
        self.micro_roughness_scale = material_parameters["micro_roughness_scale"]


    def get_material_parameters_to_json(self):
        material_parameters : dict = self.get_subsurface_profile_base_parameters_to_json()

        material_parameters["micro_normal_map"] = self.micro_normal_map.get_texture_to_json()
        material_parameters["micro_roughness_map"] = self.micro_roughness_map.get_texture_to_json()
        material_parameters["micro_normal_mask_map"] = self.micro_normal_mask_map.get_texture_to_json()
        material_parameters["blend_normal_map"] = self.blend_normal_map.get_texture_to_json()
        material_parameters["use_cc_thickness_map"] = self.noruse_cc_thickness_mapmal_strength
        material_parameters["normal_strength"] = self.normal_strength
        material_parameters["micro_normal_strength"] = self.micro_normal_strength
        material_parameters["blend_normal_strength"] = self.blend_normal_strength
        material_parameters["edge_roughness_multiplier"] = self.edge_roughness_multiplier
        material_parameters["sss_strength"] = self.sss_strength
        material_parameters["sss_contrast"] = self.sss_contrast
        material_parameters["base_color_brightness"] = self.base_color_brightness
        material_parameters["micro_uv"] = self.micro_uv
        material_parameters["micro_roughness_scale"] = self.micro_roughness_scale
        return material_parameters
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_subsurface_profile_base_parameters_to_object(node,shader_type)

            if node.label == "micro_normal_map":
                node = self.micro_normal_map.get_texture_to_object(node)
            elif node.label == "micro_roughness_map":
                node = self.micro_roughness_map.get_texture_to_object(node)
            if node.label == "micro_normal_mask_map":
                node = self.micro_normal_mask_map.get_texture_to_object(node)
            elif node.label == "blend_normal_map":
                node = self.blend_normal_map.get_texture_to_object(node)
            elif node.label == shader_type:
                node = node.inputs["Use CC Thickness Map"].default_value = self.use_cc_thickness_map
            elif node.label == "normal_strength":
                node.outputs[0].default_value = self.normal_strength
            elif node.label == "micro_normal_strength":
                node.outputs[0].default_value = self.micro_normal_strength
            elif node.label == "blend_normal_strength":
                node.outputs[0].default_value = self.blend_normal_strength
            elif node.label == "edge_roughness_multiplier":
                node.outputs[0].default_value = self.edge_roughness_multiplier
            elif node.label == "sss_strength":
                node.outputs[0].default_value = self.sss_strength
            elif node.label == "sss_contrast":
                node.outputs[0].default_value = self.sss_contrast
            elif node.label == "base_color_brightness":
                node.outputs[0].default_value = self.base_color_brightness
            elif node.label == "micro_uv":
                node.outputs[0].default_value = self.micro_uv
            elif node.label == "micro_roughness_scale":
                node.outputs[0].default_value = self.micro_roughness_scale
        return material
    

    def create_shader_template(self, material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        micro_normal_texture_node = self.node_manager.create_texture_node("micro_normal_map",nodes)
        micro_normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))
        
        micro_roughness_texture_node = self.node_manager.create_texture_node("micro_roughness_map",nodes)
        micro_roughness_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        
        micro_normal_mask_texture_node = self.node_manager.create_texture_node("micro_normal_mask_map",nodes)
        micro_normal_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        
        blend_normal_texture_node = self.node_manager.create_texture_node("blend_normal_map",nodes)
        blend_normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        normal_strength_node  = self.node_manager.create_value_node("normal_strength",nodes)
        normal_strength_node.outputs[0].default_value = 1.0
        micro_normal_strength_node  = self.node_manager.create_value_node("micro_normal_strength",nodes)
        micro_normal_strength_node.outputs[0].default_value = 1.0
        blend_normal_strength_node  = self.node_manager.create_value_node("blend_normal_strength",nodes)
        blend_normal_strength_node.outputs[0].default_value = 1.0
        edge_roughness_multiplier_node  = self.node_manager.create_value_node("edge_roughness_multiplier",nodes)
        edge_roughness_multiplier_node.outputs[0].default_value = 1.0
        sss_strength_node  = self.node_manager.create_value_node("sss_strength",nodes)
        sss_strength_node.outputs[0].default_value = 1.0
        sss_contrast_node  = self.node_manager.create_value_node("sss_contrast",nodes)
        sss_contrast_node.outputs[0].default_value = 1.0
        base_color_brightness_node  = self.node_manager.create_value_node("base_color_brightness",nodes)
        base_color_brightness_node.outputs[0].default_value = 1.0
        micro_uv_node  = self.node_manager.create_value_node("micro_uv",nodes)
        micro_uv_node.outputs[0].default_value = 1.0
        micro_roughness_scale_node  = self.node_manager.create_value_node("micro_roughness_scale",nodes)
        micro_roughness_scale_node.outputs[0].default_value = 1.0
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], blend_normal_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="SSSSubsurfaceProfileCCNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "sss_subsurface_profile_mr_CC"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Micro Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Micro Normal Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Micro roughness", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Blend Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use CC Thickness Map", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Normal Strength", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Micro Normal Strength", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Blend Normal Strength", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Edge Roughness Multiplier", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("SSS Strength", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("SSS Contrast", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Base Color Brightness", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Micro UV", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Micro Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)


        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(micro_normal_texture_node.outputs['Color'], group_node.inputs['Micro Normal'])
        links.new(micro_normal_mask_texture_node.outputs['Color'], group_node.inputs['Micro Normal Mask'])
        links.new(micro_roughness_texture_node.outputs['Color'], group_node.inputs['Micro roughness'])
        links.new(blend_normal_texture_node.outputs['Color'], group_node.inputs['Blend Normal'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])
        links.new(normal_strength_node.outputs['Value'], group_node.inputs['Normal Strength'])
        links.new(micro_normal_strength_node.outputs['Value'], group_node.inputs['Micro Normal Strength'])
        links.new(blend_normal_strength_node.outputs['Value'], group_node.inputs['Blend Normal Strength'])
        links.new(edge_roughness_multiplier_node.outputs['Value'], group_node.inputs['Edge Roughness Multiplier'])
        links.new(sss_strength_node.outputs['Value'], group_node.inputs['SSS Strength'])
        links.new(sss_contrast_node.outputs['Value'], group_node.inputs['SSS Contrast'])
        links.new(base_color_brightness_node.outputs['Value'], group_node.inputs['Base Color Brightness'])
        links.new(micro_uv_node.outputs['Value'], group_node.inputs['Micro UV'])
        links.new(micro_roughness_scale_node.outputs['Value'], group_node.inputs['Micro Roughness Scale'])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs['Base Color'])
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "sss_subsurface_profile_mr_CC"
        return material



class ClothBase(OpaqueBase):

    def __init__(self):
        super().__init__()
        self.gradient_map : Texture = Texture()
        self.alpha_map : Texture = Texture()
        self.height_map : Texture = Texture()
        self.fuzz_color : Vector = Vector((1.0, 1.0, 1.0, 1.0))
        self.normal_strength : float = 1.0
        self.cloth_mask : float = 1.0
        self.gradient_index : float = 1.0


    def set_cloth_base_parameters_from_object(self, node, shader_type):
        self.set_opaque_base_parameters_from_object(node,shader_type)
        if node.label == "gradient_map":
            self.gradient_map.set_texture_from_object(node)
        elif node.label == "alpha_map":
            self.alpha_map.set_texture_from_object(node)
        elif node.label == "height_map":
            self.height_map.set_texture_from_object(node)

        elif node.label == "fuzz_color":
            self.fuzz_color = node.outputs['Color'].default_value
        elif node.label == "normal_strength":
            self.normal_strength = node.outputs[0].default_value
        elif node.label == "cloth_mask":
            self.cloth_mask = node.outputs[0].default_value
        elif node.label == "gradient_index":
            self.gradient_index = node.outputs[0].default_value


    def set_cloth_base_parameters_from_json(self, material_parameters):
        self.set_opaque_base_parameters_from_json(material_parameters)

        self.gradient_map.set_texture_from_json(material_parameters["gradient_map"])
        self.alpha_map.set_texture_from_json(material_parameters["alpha_map"])
        self.height_map.set_texture_from_json(material_parameters["height_map"])

        fuzz_color = material_parameters["fuzz_color"]
        self.fuzz_color = Vector((fuzz_color[0], fuzz_color[1], fuzz_color[2], fuzz_color[3]))
        self.normal_strength = material_parameters["normal_strength"]
        self.cloth_mask = material_parameters["cloth_mask"]
        self.gradient_index = material_parameters["gradient_index"]


    def get_cloth_base_parameters_to_json(self):
        material_parameters : dict = self.get_opaque_base_parameters_to_json()
        material_parameters["gradient_map"] = self.gradient_map.get_texture_to_json()
        material_parameters["alpha_map"] = self.alpha_map.get_texture_to_json()
        material_parameters["height_map"] = self.height_map.get_texture_to_json()

        material_parameters["fuzz_color"] = CHAOS_OT_Utility_Function.switch_parameter_type(self.fuzz_color)
        material_parameters["normal_strength"] = self.normal_strength
        material_parameters["cloth_mask"] = self.cloth_mask
        material_parameters["gradient_index"] = self.gradient_index
        return material_parameters
    

    def get_cloth_base_parameters_to_object(self, node, shader_type):
        self.get_opaque_base_parameters_to_object(node,shader_type)
        if node.label == "gradient_map":
            node = self.gradient_map.get_texture_to_object(node)
        elif node.label == "alpha_map":
            node = self.alpha_map.get_texture_to_object(node)
        elif node.label == "height_map":
            node = self.height_map.get_texture_to_object(node)

        elif node.label == "fuzz_color":
            node.outputs['Color'].default_value = self.fuzz_color
        elif node.label == "normal_strength":
            node.outputs[0].default_value = self.normal_strength
        elif node.label == "cloth_mask":
            node.outputs[0].default_value = self.cloth_mask
        elif node.label == "gradient_index":
            node.outputs[0].default_value = self.gradient_index



class ClothMaterial(ClothBase):

    def __init__(self):
        super().__init__()


    def set_material_parameters_from_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.set_cloth_base_parameters_from_object(node,shader_type)


    def set_material_parameters_from_json(self, material_parameters):
        self.set_cloth_base_parameters_from_json(material_parameters)


    def get_material_parameters_to_json(self):
        return self.get_cloth_base_parameters_to_json()
    

    def get_material_parameters_to_object(self, material, shader_type):
        for node in material.node_tree.nodes:
            self.get_cloth_base_parameters_to_object(node,shader_type)
        return material
    

    def create_shader_template(self, material):
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        for node in nodes:
            nodes.remove(node)

        base_color_texture_node = self.node_manager.create_texture_node("base_color_map",nodes)
        base_color_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        normal_texture_node = self.node_manager.create_texture_node("normal_map",nodes)
        normal_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_normal_n.tga"))

        orm_mask_texture_node = self.node_manager.create_texture_node("orm_mask_map",nodes)
        orm_mask_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_mask_orm.tga"))
        
        gradient_texture_node = self.node_manager.create_texture_node("gradient_map",nodes)
        gradient_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        
        alpha_texture_node = self.node_manager.create_texture_node("alpha_map",nodes)
        alpha_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))
        
        height_texture_node = self.node_manager.create_texture_node("height_map",nodes)
        height_texture_node.image = bpy.data.images.load(os.path.join(default_texture_path,"default_white_d.tga"))

        texture_mapping_node = self.node_manager.create_mapping_node("uv_scale_offset",nodes,links)
        
        base_color_multiplier_node = self.node_manager.create_color_node("base_color_multiplier",nodes)
        fuzz_color_multiplier_node = self.node_manager.create_color_node("fuzz_color_multiplier",nodes)
        metallic_scale_node  = self.node_manager.create_value_node("metallic_scale",nodes)
        metallic_scale_node.outputs[0].default_value = 0.0
        roughness_scale_node  = self.node_manager.create_value_node("roughness_scale",nodes)
        roughness_scale_node.outputs[0].default_value = 1.0
        specular_level_node  = self.node_manager.create_value_node("specular_level",nodes)
        specular_level_node.outputs[0].default_value = 0.5
        normal_strength_node  = self.node_manager.create_value_node("normal_strength",nodes)
        normal_strength_node.outputs[0].default_value = 1.0
        cloth_mask_node  = self.node_manager.create_value_node("cloth_mask",nodes)
        cloth_mask_node.outputs[0].default_value = 1.0
        gradient_index_node  = self.node_manager.create_value_node("gradient_index",nodes)
        gradient_index_node.outputs[0].default_value = 1.0
        
        links.new(texture_mapping_node.outputs['Vector'], base_color_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], normal_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], orm_mask_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], gradient_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], alpha_texture_node.inputs['Vector'])
        links.new(texture_mapping_node.outputs['Vector'], height_texture_node.inputs['Vector'])
        
        group_node_tree = bpy.data.node_groups.new(type="ShaderNodeTree", name="ClothNodeTree")
        group_node = self.node_manager.create_utility_node("ShaderNodeGroup",nodes)
        group_node.label = "cloth_base"
        group_node.node_tree = group_node_tree

        group_input = self.node_manager.create_utility_node("NodeGroupInput",group_node_tree.nodes)
        group_output = self.node_manager.create_utility_node("NodeGroupOutput",group_node_tree.nodes)
        
        group_node_tree.interface.new_socket("Base Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Use Alpha Clip", description='', in_out='INPUT', socket_type="NodeSocketBool", parent=None)
        group_node_tree.interface.new_socket("Base Color Multiplier", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Normal", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Orm Mask", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Gradient", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Alpha", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Height", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Fuzz Color", description='', in_out='INPUT', socket_type="NodeSocketColor", parent=None)
        group_node_tree.interface.new_socket("Metallic Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Roughness Scale", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Opacity Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Specular Level", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Normal Strength", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Cloth Mask", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("Gradient Index", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
        group_node_tree.interface.new_socket("BSDF", description='', in_out='OUTPUT', socket_type="NodeSocketShader", parent=None)

        links.new(base_color_texture_node.outputs['Color'], group_node.inputs['Base Color'])
        links.new(base_color_texture_node.outputs['Alpha'], group_node.inputs['Opacity Mask'])
        links.new(normal_texture_node.outputs['Color'], group_node.inputs['Normal'])
        links.new(orm_mask_texture_node.outputs['Color'], group_node.inputs['Orm Mask'])
        links.new(gradient_texture_node.outputs['Color'], group_node.inputs['Gradient'])
        links.new(alpha_texture_node.outputs['Color'], group_node.inputs['Alpha'])
        links.new(height_texture_node.outputs['Color'], group_node.inputs['Height'])
        links.new(base_color_multiplier_node.outputs['Color'], group_node.inputs['Base Color Multiplier'])
        links.new(fuzz_color_multiplier_node.outputs['Color'], group_node.inputs['Fuzz Color'])
        links.new(metallic_scale_node.outputs['Value'], group_node.inputs['Metallic Scale'])
        links.new(roughness_scale_node.outputs['Value'], group_node.inputs['Roughness Scale'])
        links.new(specular_level_node.outputs['Value'], group_node.inputs['Specular Level'])
        links.new(normal_strength_node.outputs['Value'], group_node.inputs["Normal Strength"])
        links.new(cloth_mask_node.outputs['Value'], group_node.inputs["Cloth Mask"])
        links.new(gradient_index_node.outputs['Value'], group_node.inputs["Gradient Index"])

        bsdf_node = self.node_manager.create_utility_node("ShaderNodeBsdfPrincipled",group_node_tree.nodes)
        mix_color_mutilpler_node = self.node_manager.create_vector_math_node("MULTIPLY",group_node_tree.nodes)
        separate_color = self.node_manager.create_break_vector_node(group_node_tree.nodes)
        metallic_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        roughness_math_multiplier_node = self.node_manager.create_value_math_node("MULTIPLY",group_node_tree.nodes)
        convert_normal_map_node = self.node_manager.create_decode_normal_node(group_node_tree.nodes)

        group_node_tree.links.new(group_input.outputs['Base Color'], mix_color_mutilpler_node.inputs[0])
        group_node_tree.links.new(group_input.outputs['Base Color Multiplier'], mix_color_mutilpler_node.inputs[1])
        group_node_tree.links.new(mix_color_mutilpler_node.outputs[0], bsdf_node.inputs['Base Color'])
        group_node_tree.links.new(group_input.outputs['Normal'], convert_normal_map_node.inputs['Color'])
        group_node_tree.links.new(convert_normal_map_node.outputs['Normal'], bsdf_node.inputs['Normal'])
        group_node_tree.links.new(group_input.outputs['Orm Mask'], separate_color.inputs['Vector'])
        group_node_tree.links.new(group_input.outputs['Metallic Scale'], metallic_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Z'], metallic_math_multiplier_node.inputs[0])
        group_node_tree.links.new(metallic_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Metallic'])
        group_node_tree.links.new(group_input.outputs['Roughness Scale'], roughness_math_multiplier_node.inputs[1])
        group_node_tree.links.new(separate_color.outputs['Y'], roughness_math_multiplier_node.inputs[0])
        group_node_tree.links.new(roughness_math_multiplier_node.outputs['Value'], bsdf_node.inputs['Roughness'])
        group_node_tree.links.new(group_input.outputs['Specular Level'], bsdf_node.inputs['Specular IOR Level'])
        group_node_tree.links.new(group_input.outputs['Opacity Mask'], bsdf_node.inputs['Alpha'])
        group_node_tree.links.new(bsdf_node.outputs['BSDF'], group_output.inputs['BSDF'])

        output_node = self.node_manager.create_utility_node("ShaderNodeOutputMaterial",nodes)
        links.new(group_node.outputs['BSDF'], output_node.inputs['Surface'])

        material["shader_type"] = "cloth_base"
        return material



class CHAOS_OT_Material_Processor:

    def __init__(self):
        self.material : Material = Material()


    def create_material(self, context, shader_type : str):
        material = bpy.data.materials.new('test')
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                material_sketum = self.material.material_type_switcher.get(shader_type, 'None')
                material = material_sketum.create_shader_template(material)
                obj.data.materials.append(material)
        return {'FINISHED'}
