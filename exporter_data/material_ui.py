import bpy
from ..ui import ViewChaosPanel
from bpy.types import Panel

class VIEW3D_PT_Material_Utility(ViewChaosPanel, Panel):
    bl_label = "Material Utility"
    bl_description = "Material材质相关工具"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Create Material")

        box1 = box.box()
        col1 = box1.column(align=True)
        row1 = col1.row(align=True)
        row1.operator("material_operators.create_translucent_material", text="Translucent", icon="MATERIAL")
        row1.operator("material_operators.create_unlit_material", text="Unlit", icon="MATERIAL")

        col2 = box1.column(align=True)
        row2 = col2.row(align=True)
        row2.operator("material_operators.create_opaque_character_hero_material", text="Character Hero", icon="MATERIAL")
        row2.operator("material_operators.create_opaque_character_solider_material", text="Character Solider", icon="MATERIAL")

        col3 = box1.column(align=True)
        row3 = col3.row(align=True)
        row3.operator("material_operators.create_opaque_scene_material", text="Opaque Scene", icon="MATERIAL")
        row3.operator("material_operators.create_opaque_blend_material", text="Opaque Blend", icon="MATERIAL")

        col4 = box1.column(align=True)
        row4 = col4.row(align=True)
        row4.operator("material_operators.create_cheap_subsurface_material", text="Cheap Subsurface", icon="MATERIAL")
        row4.operator("material_operators.create_two_side_foliage_material", text="Two Side Foliage", icon="MATERIAL")

        col5 = box1.column(align=True)
        row5 = col5.row(align=True)
        row5.operator("material_operators.create_subsurface_profile_material", text="Subsurface Profile", icon="MATERIAL")
        row5.operator("material_operators.create_sss_subsurface_profile_material", text="SSS Subsurface Profile CC", icon="MATERIAL")

        col6 = box1.column(align=True)
        row6 = col6.row(align=True)
        row6.operator("material_operators.create_cloth_material", text="Cloth", icon="MATERIAL")
        row6.operator("material_operators.create_emissive_material", text="Emissive", icon="MATERIAL")