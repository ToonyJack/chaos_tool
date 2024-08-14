import bpy
from ...ui import ViewChaosPanel
from bpy.types import Panel

class VIEW3D_PT_CCModelProcessorPanel(ViewChaosPanel, Panel):
    """init"""
    bl_label = "CC模型加工"
    bl_description = "CC,Bip模型替换"
    bl_options = {"DEFAULT_CLOSED"}


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        row = layout.row()
        layout.prop(data = scene, property = "m_cc_skeleton",icon='ARMATURE_DATA')
        layout.prop(data = scene, property = "m_biped_skeleton",icon='ARMATURE_DATA')
        layout.prop(data = scene, property = "m_target_normal_mesh",icon='MESH_DATA')
        layout.prop(data = scene, property = "m_cc_collection",icon='OUTLINER_COLLECTION')
        layout.prop(data = scene, property = "m_biped_collection",icon='OUTLINER_COLLECTION')

        layout.separator(factor=1.0)
        box_holder = layout.box()
        box_holder.alert = False
        box_holder.enabled = True
        box_holder.use_property_split = False
        box_holder.use_property_decorate = False
        box_holder.alignment = 'Expand'.upper()
        box_holder.scale_x = 1.0
        box_holder.scale_y = 1.0

        box_C0357 = box_holder.box()
        box_C0357.alert = False
        box_C0357.enabled = True
        box_C0357.use_property_split = False
        box_C0357.use_property_decorate = False
        box_C0357.alignment = 'Center'.upper()
        box_C0357.scale_x = 1.0
        box_C0357.scale_y = 1.0
        box_C0357.prop(bpy.context.scene, 'sna_mesh_amount', text='Mesh amount', icon_value=0, emboss=True)
        
        mesh_count = max(0, min( bpy.context.scene.sna_mesh_amount, 10))
        for i in range(1, mesh_count + 1):  # Loop from 1 to 10
            prop_name = f"sna_ccmesh{i:02d}"
            prop_sk_name = f"sna_sk{i:02d}"
            prop_no_name = f"sna_no{i:02d}"

            split = layout.split(factor=0.5, align=False)
            split.alert = False
            split.enabled = True
            split.use_property_split = False
            split.use_property_decorate = False
            split.scale_x = 1.0
            split.scale_y = 1.0
            split.alignment = 'CENTER'

            split.prop(bpy.context.scene, prop_name, text='', icon_value=0, emboss=True)

            row = split.row(heading='', align=True)
            row.alert = False
            row.enabled = True
            row.use_property_split = False
            row.use_property_decorate = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            row.alignment = 'CENTER'

            row.prop(bpy.context.scene, prop_sk_name, text=' skin', icon_value=201, emboss=True, toggle=False)
            row.prop(bpy.context.scene, prop_no_name, text=' normal', icon_value=638, emboss=True, toggle=False)


        """ ACTION_TWEAK """
        layout.operator(operator = "blender_cc_operator.reset_restpose_operator", text = "Reset RestPose",icon='ACTION_TWEAK')
        layout.operator(operator = "blender_cc_operator.change_cc_head_operator", text = "Change CC Head",icon='HOOK')
