import bpy
from bpy.types import Operator
from .material_processor import CHAOS_OT_Material_Processor

class CHAOS_OT_Create_Unlit_Material(Operator):
    bl_idname = "material_operators.create_unlit_material"
    bl_label = ""
    bl_description = "创建Unlit材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "unlit")


class CHAOS_OT_Create_Translucent_Material(Operator):
    bl_idname = "material_operators.create_translucent_material"
    bl_label = ""
    bl_description = "创建Translucent材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "translucent")
    


class CHAOS_OT_Create_OpaqueCharacterHero_Material(Operator):
    bl_idname = "material_operators.create_opaque_character_hero_material"
    bl_label = ""
    bl_description = "创建OpaqueCharacterHero材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "opaque_character_hero")
    


class CHAOS_OT_Create_OpaqueCharacterSolider_Material(Operator):
    bl_idname = "material_operators.create_opaque_character_solider_material"
    bl_label = ""
    bl_description = "创建OpaqueCharacterSolider材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "opaque_character_solider")
    


class CHAOS_OT_Create_OpaqueScene_Material(Operator):
    bl_idname = "material_operators.create_opaque_scene_material"
    bl_label = ""
    bl_description = "创建OpaqueScene材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "opaque_scene")
    


class CHAOS_OT_Create_OpaqueBlend_Material(Operator):
    bl_idname = "material_operators.create_opaque_blend_material"
    bl_label = ""
    bl_description = "创建OpaqueBlend材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "opaque_blend")
    


class CHAOS_OT_Create_CheapSubsurface_Material(Operator):
    bl_idname = "material_operators.create_cheap_subsurface_material"
    bl_label = ""
    bl_description = "创建CheapSubsurface材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "cheap_subsurface")
    


class CHAOS_OT_Create_TwoSideFoliage_Material(Operator):
    bl_idname = "material_operators.create_two_side_foliage_material"
    bl_label = ""
    bl_description = "创建TwoSideFoliage材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "two_side_foliage")
    


class CHAOS_OT_Create_SubsurfaceProfile_Material(Operator):
    bl_idname = "material_operators.create_subsurface_profile_material"
    bl_label = ""
    bl_description = "创建SubsurfaceProfile材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "subsurface_profile")
    


class CHAOS_OT_Create_SSSSubsurfaceProfileMrCC_Material(Operator):
    bl_idname = "material_operators.create_sss_subsurface_profile_material"
    bl_label = ""
    bl_description = "创建SSSSubsurfaceProfileMrCC材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "sss_subsurface_profile_mr_CC")
    


class CHAOS_OT_Create_Cloth_Material(Operator):
    bl_idname = "material_operators.create_cloth_material"
    bl_label = ""
    bl_description = "创建Cloth材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "cloth_base")
    


class CHAOS_OT_Create_Emissive_Material(Operator):
    bl_idname = "material_operators.create_emissive_material"
    bl_label = ""
    bl_description = "创建Emissive材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "emissive")



class CHAOS_OT_Create_Decal_Material(Operator):
    bl_idname = "material_operators.create_decal_material"
    bl_label = ""
    bl_description = "创建Decal材质球"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        
        material_processor : CHAOS_OT_Material_Processor = CHAOS_OT_Material_Processor()

        return material_processor.create_material(context, "decal")