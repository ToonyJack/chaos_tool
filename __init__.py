# 检查当前是否在 Blender 环境中运行的条件语句。
# 如果是，则重新加载插件的所有模块。以便在运行时编辑器中进行修改，而不必重新启动 Blender。
# 如果不是，则引入必要的模块。
if "bpy" in locals():
    import importlib

    importlib.reload(ui)
    importlib.reload(operators)
    importlib.reload(utility.utility_ui)
    importlib.reload(utility.utility_operators)
    importlib.reload(animation.blender_cc_model.blender_cc_model_ui)
    importlib.reload(animation.blender_cc_model.blender_cc_model_operators)
    importlib.reload(animation.animation_utility_ui)
    importlib.reload(animation.animation_utility_operators)
    importlib.reload(exporter_data.exporter_data_ui)
    importlib.reload(exporter_data.exporter_data_operators)
    importlib.reload(help.help_ui)
    importlib.reload(help.help_operators)

else:
    import math

    import bpy
    from bpy.types import PropertyGroup
    from bpy.props import (
        BoolProperty,
        StringProperty,
        FloatProperty
    )

    from . import (
        ui,
        operators
    )

    from .utility import (
        utility_ui,
        utility_operators
    )
    
    from .animation import(
        animation_utility_operators,
        animation_utility_ui
    )
    
    from .animation.blender_cc_model import(
        blender_cc_model_ui,
        blender_cc_model_operators
    )

    from .debug_profiler import(
        debug_profiler_ui,
        debug_profiler_operators
    )

    from .exporter_data import (
        exporter_data_ui,
        exporter_data_operators,
        material_ui,
        material_operators
    )

    from .help import (
        help_ui,
        help_operators
    )

bl_info = {
    "name": "Chaos Toolbox",
    "author": "Wang JangTao/Shao TingWei",
    "description": "Utilities for assist Chaos Engine asset production",
    "blender": (3, 6, 0),
    "version": (0, 3, 1, 5),
    "location": "View3D > Sidebar > CHAOS Tab",
    "warning": "",
    "category": "Generic",
    "doc_url": "https://chaos-docs.booming-inc.com/docs/category/manage_resource/",
}


# 根据属性值切换Shading的显示模式
def update_toggle_vertex_color(self, context):
    # 未启用顶点颜色的显示
    if not self.toggle_vertex_color:
        # 将当前 3D 视图中的 shading 模式设置为 'MATERIAL'，表示使用材质颜色
        bpy.context.space_data.shading.color_type = "MATERIAL"

    # 启用顶点颜色的显示
    else:
        # 将当前 3D 视图中的 shading 模式设置为 'VERTEX'，表示使用顶点颜色
        bpy.context.space_data.shading.color_type = "VERTEX"


class SceneProperties(PropertyGroup):

    toggle_vertex_color: BoolProperty(
        name="Verter Color",
        description="Path to directory where the files are created",
        default=False,
        # 绑定update函数
        update=update_toggle_vertex_color,
    )
    
    tposs_path: StringProperty(
        name="TPoss FilePath",
        description="Path to directory where the files are created",
        default="",
        maxlen=1024,
        subtype="FILE_PATH",
    )
    
    csv_path: StringProperty(
        name="Anim CSV FilePath",
        description="Path to directory where the files are created",
        default="",
        maxlen=1024,
        subtype="FILE_PATH",
    )
    
    seanim_source_path: StringProperty(
        name="SEAnim Source Directory",
        description="Path to directory where the files are created",
        default="",
        maxlen=1024,
        subtype="DIR_PATH",
    )
    
    fbx_save_path: StringProperty(
        name="FBX Export Directory",
        description="Path to directory where the files are created",
        default="",
        maxlen=1024,
        subtype="DIR_PATH",
    )
    
    global_scale: FloatProperty(
        name="Global Scale",
        description="Export Global Scale",
        subtype='FACTOR',
        default=1,  # 1mm
        min=0.00001,
        max=1,
    )



# 存放所有需要注册的类
classes = [
    SceneProperties,
    ui.VIEW3D_PT_chaos_general,
    ui.VIEW3D_PT_chaos_viewport_display,
    ui.VIEW3D_PT_Utilities,
    ui.VIEW3D_PT_chaos_tools,
    ui.VIEW3D_PT_chaos_addMesh,
    ui.VIEW3D_PT_chaos_rename,
    ui.VIEW3D_PT_TopologyCheck,
    utility_ui.VIEW3D_PT_Utility_Tools,
    material_ui.VIEW3D_PT_Material_Utility,
    debug_profiler_ui.VIEW3D_PT_Debug_Profiler_Utility,
    exporter_data_ui.VIEW3D_PT_ExporterData,
    animation_utility_ui.VIEW3D_PT_Import_SEAnim,
    blender_cc_model_ui.VIEW3D_PT_CCModelProcessorPanel,
    help_ui.VIEW3D_PT_chaos_help,
    ui.VIEW3D_PT_chaos_material_tools,
    operators.CHAOS_OT_Obj_Display_showname,
    operators.CHAOS_OT_Obj_Display_Swith,
    operators.CHAOS_OT_ResetLocation,
    operators.CHAOS_OT_ResetRotation,
    operators.CHAOS_OT_ResetScale,
    operators.CHAOS_OT_ResetAll,
    operators.CHAOS_OT_UnitReset,
    operators.CHAOS_OT_batch_rename,
    operators.CHAOS_OT_RenameObjects,
    operators.CHAOS_OT_Utils_VertexColorRemove,
    operators.CHAOS_OT_Utils_UVMapRenam,
    operators.CHAOS_OT_Utils_Parent_Empty,
    operators.CHAOS_OT_Utils_CleanUp,
    operators.CHAOS_OT_Geo_ConvexHull,
    operators.CHAOS_OT_Geo_BBX,
    operators.CHAOS_OT_Geo_Add_EemptyCube,
    operators.CHAOS_OT_Geo_Add_EemptySphere,
    operators.CHAOS_OT_TopologyCheck_deleteloose,
    operators.CHAOS_OT_Replace_Repeated_Materials,
    operators.CHAOS_OT_DeleteZeroAreaFace,
    operators.CHAOS_OT_DissloveZeroAreaFace,
    operators.CHAOS_OT_Add_Triangulate,
    operators.CHAOS_OT_Select_Non_Manifold,
    utility_operators.CHAOS_OT_Create_Chaos_Custom_Property,
    utility_operators.CHAOS_OT_Clear_All_Mesh_Data,
    utility_operators.CHAOS_OT_Clear_Unlink_Mesh_Data,
    utility_operators.CHAOS_OT_Clear_All_Material_Data,
    utility_operators.CHAOS_OT_Clear_Unlink_Material_Data,
    material_operators.CHAOS_OT_Create_Unlit_Material,
    material_operators.CHAOS_OT_Create_Translucent_Material,
    material_operators.CHAOS_OT_Create_OpaqueCharacterHero_Material,
    material_operators.CHAOS_OT_Create_OpaqueCharacterSolider_Material,
    material_operators.CHAOS_OT_Create_OpaqueScene_Material,
    material_operators.CHAOS_OT_Create_OpaqueBlend_Material,
    material_operators.CHAOS_OT_Create_CheapSubsurface_Material,
    material_operators.CHAOS_OT_Create_TwoSideFoliage_Material,
    material_operators.CHAOS_OT_Create_SubsurfaceProfile_Material,
    material_operators.CHAOS_OT_Create_SSSSubsurfaceProfileMrCC_Material,
    material_operators.CHAOS_OT_Create_Cloth_Material,
    material_operators.CHAOS_OT_Create_Emissive_Material,
    debug_profiler_operators.CHAOS_OT_CHAOS_OT_Unified_Name,
    animation_utility_operators.CHAOS_OT_Import_SEAnim,
    blender_cc_model_operators.CHAOS_OT_ResetRestPoseOperator,
    blender_cc_model_operators.CHAOS_OT_ChangeCCHeadOperator,
    exporter_data_operators.CHAOS_OT_Export_CC4_Data_To_Json,
    exporter_data_operators.CHAOS_OT_Export_Blender_Scene_Data_To_Json,
    exporter_data_operators.CHAOS_OT_Export_Blender_Prefabs_Data_To_Json,
    exporter_data_operators.CHAOS_OT_Export_Blender_Model_Data_To_Json,
    exporter_data_operators.CHAOS_OT_Import_Chaos_Prefabs_Asset_Data,
    exporter_data_operators.CHAOS_OT_Import_Chaos_Model_Asset_Data,
    help_operators.CHAOS_OT_Help_URL,
    help_operators.CHAOS_OT_Language,
    help_operators.CHAOS_OT_Feedback_URL,
]

from bpy.app.handlers import persistent


# 该装饰器标记了持久化的函数，它们会在特定的 Blender 事件发生时执行。
# 即使在脚本加载或重新加载后仍然有效
@persistent
def load_handler_for_preferences(_):
    print("Changing Preference Defaults!")
    from bpy import context

    prefs = context.preferences
    prefs.use_preferences_save = False

    view = prefs.view
    view.ui_scale = 1.35


@persistent
def load_handler_for_startup(_):
    print("Changing Startup Defaults!")

    # Use smooth faces.
    for mesh in bpy.data.meshes:
        for poly in mesh.polygons:
            poly.use_smooth = True

    # Use material preview shading.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    # space.shading.type = 'MATERIAL'
                    space.shading.type = "WIREFRAME"


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.chaos = bpy.props.PointerProperty(type=SceneProperties)
    bpy.app.handlers.depsgraph_update_post.append(operators.selection_change_handler)
    

    bpy.types.Scene.m_biped_skeleton = bpy.props.PointerProperty(name='Bip', description='', options={'ANIMATABLE'}, type=bpy.types.Armature)
    bpy.types.Scene.m_cc_skeleton = bpy.props.PointerProperty(name='CC skeleton', description='', type=bpy.types.Armature)
    bpy.types.Scene.m_target_normal_mesh = bpy.props.PointerProperty(name='target normal mesh', description='', type=bpy.types.Object)
    bpy.types.Scene.m_cc_collection = bpy.props.PointerProperty(name='CC Collection', description='', type=bpy.types.Collection)
    bpy.types.Scene.m_biped_collection = bpy.props.PointerProperty(name='Biped Collection', description='', type=bpy.types.Collection)
    
    bpy.types.Scene.sna_mesh_amount = bpy.props.IntProperty(name='Mesh amount', description='', default=3, subtype='NONE', min=1, max=10)
    
    bpy.types.Scene.sna_ccmesh01 = bpy.props.PointerProperty(name='ccmesh01', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk01 = bpy.props.BoolProperty(name='sk01', description='', default=False)
    bpy.types.Scene.sna_no01 = bpy.props.BoolProperty(name='no01', description='', default=False)
    bpy.types.Scene.sna_ccmesh02 = bpy.props.PointerProperty(name='ccmesh02', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk02 = bpy.props.BoolProperty(name='sk02', description='', default=False)
    bpy.types.Scene.sna_no02 = bpy.props.BoolProperty(name='no02', description='', default=False)
    bpy.types.Scene.sna_ccmesh03 = bpy.props.PointerProperty(name='ccmesh03', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk03 = bpy.props.BoolProperty(name='sk03', description='', default=False)
    bpy.types.Scene.sna_no03 = bpy.props.BoolProperty(name='no03', description='', default=False)
    bpy.types.Scene.sna_ccmesh04 = bpy.props.PointerProperty(name='ccmesh04', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk04 = bpy.props.BoolProperty(name='sk04', description='', default=False)
    bpy.types.Scene.sna_no04 = bpy.props.BoolProperty(name='no04', description='', default=False)
    bpy.types.Scene.sna_ccmesh05 = bpy.props.PointerProperty(name='ccmesh05', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk05 = bpy.props.BoolProperty(name='sk05', description='', default=False)
    bpy.types.Scene.sna_no05 = bpy.props.BoolProperty(name='no05', description='', default=False)
    bpy.types.Scene.sna_ccmesh06 = bpy.props.PointerProperty(name='ccmesh06', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk06 = bpy.props.BoolProperty(name='sk06', description='', default=False)
    bpy.types.Scene.sna_no06 = bpy.props.BoolProperty(name='no06', description='', default=False)
    bpy.types.Scene.sna_ccmesh07 = bpy.props.PointerProperty(name='ccmesh07', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk07 = bpy.props.BoolProperty(name='sk07', description='', default=False)
    bpy.types.Scene.sna_no07 = bpy.props.BoolProperty(name='no07', description='', default=False)
    bpy.types.Scene.sna_ccmesh08 = bpy.props.PointerProperty(name='ccmesh08', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk08 = bpy.props.BoolProperty(name='sk08', description='', default=False)
    bpy.types.Scene.sna_no08 = bpy.props.BoolProperty(name='no08', description='', default=False)
    bpy.types.Scene.sna_ccmesh09 = bpy.props.PointerProperty(name='ccmesh09', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk09 = bpy.props.BoolProperty(name='sk09', description='', default=False)
    bpy.types.Scene.sna_no09 = bpy.props.BoolProperty(name='no09', description='', default=False)
    bpy.types.Scene.sna_ccmesh10 = bpy.props.PointerProperty(name='ccmesh10', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_sk10 = bpy.props.BoolProperty(name='sk10', description='', default=False)
    bpy.types.Scene.sna_no10 = bpy.props.BoolProperty(name='no10', description='', default=False)
        
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.overlay.show_stats = True


def unregister():
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"{cls} - may not be registered")  # debug

    del bpy.types.Scene.chaos


if __name__ == "__main__":
    for f in bpy.app.handlers.depsgraph_update_post:
        if f.__name__ == "selection_change_handler":
            bpy.app.handlers.depsgraph_update_post.remove(f)
    register()
