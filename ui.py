import bpy.props
from bpy.types import Context, Panel, PropertyGroup
from . import general
from bpy.app.translations import pgettext_tip as tip_
from bpy.props import (
    IntProperty,
    BoolProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
)

class ViewChaosPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Chaos-Toolbox"
    bl_ui_units_x = 400


class VIEW3D_PT_chaos_general(ViewChaosPanel, Panel):
    bl_label = "General"

    def draw_report(self, context):
        layout = self.layout

        #
        info = []
        scene = context.scene
        layer = context.view_layer
        unit = scene.unit_settings

        unit_scale = (
            "1.0"
            if unit.scale_length == 1.0
            else ("< " + str(unit.scale_length) + " >")
        )
        unit_system = (
            "Metric - 公制" if unit.system == "METRIC" else ("< " + unit.system + " >")
        )
        if unit.length_unit == "METERS":
            unit_length = "Meters - 米(m)"
        elif unit.length_unit == "CENTIMETERS":
            unit_length = "Centimeters - 厘米(cm)"
        else:
            unit_length = "< " + unit.length_unit + " >"
        info.append((f'{tip_("Unit Scale")}    : {unit_scale}', ()))
        info.append((f'{tip_("Unit System")} : {unit_system}', ()))
        info.append((f'{tip_("Length")} : {unit_length}', ()))

        general.update(*info)

        if info:
            is_edit = context.edit_object is not None

            layout.label(text=tip_("Units"))
            box = layout.box()
            col = box.column()
            if (
                unit.scale_length == 1.0
                and unit.system == "METRIC"
                and unit.length_unit == "METERS"
            ):
                col.alert = False
            else:
                col.alert = True
            for i, (text, data) in enumerate(info):
                col.label(text=text)

    def draw(self, context):
        layout = self.layout
        # layout.operator("chaos.op_language",text="Language EN/CN", icon="FILE_TEXT")
        self.draw_report(context)
        layout.operator("chaos.op_unit_reset", text="Reset Length Unit to cm/m")
        layout.label(text="Clean Up")
        layout.operator("chaos.op_utils_cleanup", icon="TRASH")


class VIEW3D_PT_chaos_viewport_display(ViewChaosPanel, Panel):
    bl_label = "Viewport Display"
    bl_description = "视图显示设置"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: Context):
        chaos = context.scene.chaos

        layout = self.layout
        box = layout.box()
        box.use_property_split = True
        box.use_property_decorate = False
        space_data = context.space_data
        row = box.row()
        row.operator("view3d.toggle_xray", text="", icon="XRAY")
        row.operator("view3d.toggle_shading", text="", icon="SHADING_WIRE")
        row.prop(space_data.shading, "color_type")

        box.label(text="Guides")
        box.use_property_split = False
        row = box.row()
        row.prop(space_data.overlay, "show_stats", text="Statistics")
        row.prop(space_data.overlay, "show_cursor", text="3D Cursor")

        box.label(text="Geometry")
        box.use_property_split = True
        box.prop(
            space_data.overlay,
            "show_wireframes",
        )
        box.prop(
            chaos,
            "toggle_vertex_color",
        )
        box.prop(space_data.overlay, "show_face_orientation", text="Face Orientation")
        box.prop(space_data.overlay, "show_bones", text="Bones")
        box.prop(space_data.overlay, "show_edge_crease")

        layout.label(text="Select Objects")
        col = layout.column()
        col.operator(
            "chaos.op_objdisplay_showname", text="Show Name", icon="SHADING_RENDERED"
        )
        col.operator(
            "chaos.op_objdisplay_swith",
            text="Display As: Wire/Textured",
            icon="SHADING_RENDERED",
        )


class VIEW3D_PT_Utilities(ViewChaosPanel, Panel):
    bl_label = "Utilities"
    bl_description = "实用程序"

    def draw(self, context):
        layout = self.layout


class VIEW3D_PT_chaos_tools(ViewChaosPanel, Panel):
    bl_label = "Tools"
    bl_description = "工具"
    bl_parent_id = "VIEW3D_PT_Utilities"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        layout.label(text="Reset XForm / Freeze Transform")
        row = layout.row(align=True)
        row.operator("CHAOS.op_reset_location")
        row.operator("CHAOS.op_reset_rotation")
        row.operator("CHAOS.op_reset_scale")

        col = layout.column(align=False)
        col.operator("CHAOS.op_reset_all")
        col.operator(
            "chaos.op_vertex_color_remove", text="Delete Vertex Color", icon="TRASH"
        )
        col.operator("chaos.op_uvmap_rename", text="Rename UV Maps", icon="UV_DATA")
        col.operator(
            "chaos.op_parent_empty", text="Parent to Empty", icon="OUTLINER_OB_EMPTY"
        )


class VIEW3D_PT_chaos_addMesh(ViewChaosPanel, Panel):
    bl_label = tip_("New")
    bl_description = "添加"
    bl_parent_id = "VIEW3D_PT_Utilities"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        layout.label(text="Rigid Body")
        box = layout.box()
        col = box.column(align=False)
        #col.operator("chaos.geo_bbx", text="Bounding Box", icon="MODIFIER")
        col.operator("chaos.geo_convexhull", text="Convex Hull", icon="MODIFIER")
        #row = box.row(align=True)
        #row.operator("chaos.op_add_emptycube", icon="CUBE")
        #row.operator("chaos.op_add_emptysphere", icon="SPHERE")


class VIEW3D_PT_chaos_rename(ViewChaosPanel, Panel):
    bl_label = "Rename"
    bl_description = "名称设置"
    bl_parent_id = "VIEW3D_PT_Utilities"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        col = box.column(align=True)

        col.label(text="Add Tag to Object Name")
        col = box.column(align=True)
        col.operator("chaos.renameobjects", text="Rename Object(s)", icon="EVENT_TAB")

        col = box.column(align=True)
        col.label(text="Find/Replace")
        col.operator("wm.batch_rename")


class VIEW3D_PT_TopologyCheck(ViewChaosPanel, Panel):
    bl_label = "拓扑检查"
    bl_description = "topology check 拓扑检查"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box.label(text="网格错误修复", icon="MODIFIER_DATA")
        box1 = box.box()
        col = box1.column(align=True)
        col.operator("chaos.op_topocheck_deleteloose", text="Delete Loose")
        box2 = box.box()
        col = box2.column(align=True)
        op = col.operator("chaos.select_zero_area_face", text="查找并修复零面积面")

        zeroFaceCount = bpy.context.scene.get("zeroFaceCount", 0)
        if zeroFaceCount == 0:
            box2.label(text="没有零面积面！")
        elif zeroFaceCount > 0:
            box2.label(text=f"零面积面：{zeroFaceCount}")
            col = box2.column(align=True)
            op = col.operator("chaos.disslove_zero_area_face", text="修复")
        elif zeroFaceCount == -1:
            box2.label(text="修复完成！")

        box3 = box.box()
        col = box3.column(align=True)
        col.ui_units_x = 5
        row = col.row(align=True)

        op = col.operator("chaos.add_triangulate", text="三角化")
        col.label(text="仅对 边>4 的面进行处理")

        box4 = box.box()
        col = box4.column(align=True)
        op = col.operator("chaos.select_non_manifold", text="选择非流形")
        # if not bpy.ops.chaos.select_non_manifold.poll():
        #     col.label(text="不支持面选择模式！请切换选择模式")


class VIEW3D_PT_chaos_material_tools(ViewChaosPanel, Panel):
    bl_label = tip_("Material")
    bl_description = "材质工具"
    bl_parent_id = "VIEW3D_PT_Utilities"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        layout.label(text=tip_("替换重复材质（无删除操作）"))
        row = layout.row(align=True)

        row.operator("chaos.replace_repeated_materials", text="替换")
