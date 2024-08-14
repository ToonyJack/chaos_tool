# -*- coding: UTF-8 -*-

from bpy.app.translations import pgettext_iface as _
import bpy, bmesh, webbrowser, re
from bpy.types import Context, Operator
from bpy.props import (
    IntProperty,
    BoolProperty,
    StringProperty,
    EnumProperty,
)
from bpy.app.translations import pgettext_tip as tip_
from . import general, globalData
from bpy_extras.io_utils import ExportHelper
import bpy.utils.previews


class CHAOS_OT_ResetLocation(Operator):
    bl_label = "Location"
    bl_idname = "chaos.op_reset_location"
    bl_description = "重置选择的mesh对象位置"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selobjs = context.selected_objects

        if len(selobjs) > 0:
            for obj in selobjs:
                if obj.type != "MESH":
                    # obj.location = (0, 0, 0)
                    obj.select_set(False)
            bpy.ops.object.transform_apply(
                location=True, rotation=False, scale=False, isolate_users=True
            )
        self.report({"INFO"}, "Reset Location.")
        return {"FINISHED"}


class CHAOS_OT_ResetRotation(Operator):
    bl_label = "Rotation"
    bl_idname = "chaos.op_reset_rotation"
    bl_description = "重置选择的mesh对象旋转"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selobjs = context.selected_objects
        if len(selobjs) > 0:
            for obj in selobjs:
                if obj.type != "MESH":
                    # obj.location = (0, 0, 0)
                    obj.select_set(False)
            bpy.ops.object.transform_apply(
                location=False, rotation=True, scale=False, isolate_users=True
            )
        self.report({"INFO"}, "Reset Rotation.")
        return {"FINISHED"}


class CHAOS_OT_ResetScale(Operator):
    bl_label = "Scale"
    bl_idname = "chaos.op_reset_scale"
    bl_description = "重置选择的mesh对象比例"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selobjs = context.selected_objects
        if len(selobjs) > 0:
            for obj in selobjs:
                if obj.type != "MESH":
                    obj.select_set(False)
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True, isolate_users=True
            )
        self.report({"INFO"}, "Reset Scale.")
        return {"FINISHED"}


class CHAOS_OT_ResetAll(Operator):
    bl_label = "Reset Transform"
    bl_idname = "chaos.op_reset_all"
    bl_description = "重置选择Mesh对象的变换(transform)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selobjs = context.selected_objects
        if len(selobjs) > 0:
            for obj in selobjs:
                if obj.type != "MESH":
                    obj.select_set(False)
            bpy.ops.object.transform_apply(
                location=True, rotation=True, scale=True, isolate_users=True
            )
        self.report({"INFO"}, "Reset Scale.")
        return {"FINISHED"}


class CHAOS_OT_Utils_UVMapRenam(Operator):
    bl_idname = "chaos.op_uvmap_rename"
    bl_label = "UV Maps Rename"
    bl_description = "重命名UV贴图名称，使所选Mesh对象的UV贴图名称保持一致"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        message = ""
        for obj in bpy.context.selected_objects:
            if obj.type != "MESH":
                continue
            message += obj.name + "/"
            for i in range(len(obj.data.uv_layers)):
                obj.data.uv_layers[i].name = "UVMap_" + str(i)
                print(obj.data.uv_layers[i].name)
        message = "< " + message + "> has UV layer."
        self.report({"INFO"}, message + "\nUV layer rename successfully.")
        return {"FINISHED"}


class CHAOS_OT_Obj_Display_showname(Operator):
    bl_idname = "chaos.op_objdisplay_showname"
    bl_label = "Show Name"
    bl_description = "在视图中显示选择的对象名称"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        message = ""
        for obj in bpy.context.selected_objects:
            message += obj.name + "/"
            if obj.show_name:
                obj.show_name = False
            else:
                obj.show_name = True
        message = "< " + message + "> name is displayed."
        self.report({"INFO"}, message + "\n Show Name Successfully.")
        return {"FINISHED"}


class CHAOS_OT_Obj_Display_Swith(Operator):
    bl_idname = "chaos.op_objdisplay_swith"
    bl_label = "Display Mode: Wire/Solid"
    bl_description = "切换选择对象的显示模式：线框/实体"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        message = ""
        for obj in bpy.context.selected_objects:
            if obj.type != "MESH":
                continue
            message += obj.name + "/"
            if obj.display_type == "WIRE":
                obj.display_type = "TEXTURED"
            else:
                obj.display_type = "WIRE"
        message = "< " + message + "> has UV layer."
        self.report({"INFO"}, message + "\nUV layer rename successfully.")
        return {"FINISHED"}


class CHAOS_OT_Utils_VertexColorRemove(Operator):
    bl_idname = "chaos.op_vertex_color_remove"
    bl_label = "Remove Vertex Color"
    bl_description = "删除Mesh的所有顶点颜色属性"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if obj.type != "MESH":
                continue
            message = "<" + obj.name + "> has vertex colours."
            if len(obj.data.color_attributes) > 0:
                self.report({"INFO"}, message)
            while obj.data.color_attributes:
                obj.data.color_attributes.remove(obj.data.color_attributes[0])
        self.report({"INFO"}, "顶点颜色删除成功\nVertex color deleted successfully.")
        return {"FINISHED"}


class CHAOS_OT_batch_rename(Operator):
    bl_label = "rename"
    bl_idname = "chaos.op_batch_rename"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        self.batch_rename
        self.report({"INFO"}, "Complete the renaming of the selection!")
        return {"FINISHED"}


class CHAOS_OT_UnitReset(Operator):
    bl_label = "Unit Reset"
    bl_idname = "chaos.op_unit_reset"
    bl_description = "重置长度单位厘米(Centimeters)/米(Meters)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        unit_length = bpy.context.scene.unit_settings.length_unit
        if unit_length == "METERS":
            bpy.context.scene.unit_settings.system = "METRIC"
            bpy.context.scene.unit_settings.scale_length = 1.0
            bpy.context.scene.unit_settings.length_unit = "CENTIMETERS"
        else:
            bpy.context.scene.unit_settings.system = "METRIC"
            bpy.context.scene.unit_settings.scale_length = 1.0
            bpy.context.scene.unit_settings.length_unit = "METERS"
        self.report({"INFO"}, "Reset Scene Unit : length is centimeters.")
        return {"FINISHED"}


class CHAOS_OT_RenameObjects(Operator):
    bl_idname = "chaos.renameobjects"
    bl_label = "Rename Object(s)"
    bl_description = (
        "重命名'网格'和'空物体'对象, 并且名称中添加特定标记, \n例如:lod, rigid, occluder, dummy, detection.\n"
    )
    bl_description += "--------------------------------------------------------\n"
    bl_description += "多个选择对象命名:\n命名顺序按照倒序命名，即最后一个选择对象的序号为0"

    tag_occluder: BoolProperty(
        name="Add Tag: Occluder", description="为对象名称添加'Occluder'标记"
    )
    tag_rigid: BoolProperty(name="Add Tag: Rigid Body", description="为对象名称添加'Rigid'标记")
    tag_lod0: BoolProperty(name="Add Tag: LOD", description="为对象名称添加'LOD'标记")
    action: EnumProperty(
        name="Add Tag",
        description="选择一个标记类型",
        items=[
            ("LOD", "LOD", "命名样式: OBJECTNAME_lod#"),
            ("RIGID", "Rigid Body", "命名样式: OBJECTNAME_rigid##"),
            # ('OCCLUDER',      'Occluder',                     'Name Pattern: OBJECTNAME_occluder'),
            ("DUMMY", "Dummy Body", "命名样式: OBJECTNAME_dummy##"),
            ("DETECTION", "Attack Detection Body", "命名样式: detection_##_OBJECTNAME"),
            (
                "DETECTION_DIR",
                "Direction Detection Body",
                "命名样式: detection_##_frame_OBJECTNAME",
            ),
        ],
    )

    use_set_name: BoolProperty(
        name="Set Name:", description="允许使用自定义的对象名称", default=True
    )
    convert_lowercase: BoolProperty(
        name="Convert to Lowercase", default=True, description="转换所有大写字符为小写字符"
    )
    set_name: StringProperty(name="", description="自定义对象名称")

    find_replace: BoolProperty(name="Find / Replace", description="查找/替换")
    find: StringProperty(name="", description="查找...")
    replace: StringProperty(name="", description="替换为...")

    items = []

    def indexstr(self, count, index):
        length = len(str(index))
        string = ""
        if length < count:
            for i in range(length, count):
                string += "0"
        return string + str(index)

    def draw(self, ctx):
        if len(self.items) > 1:
            box = self.layout.box()
            row = box.row(align=True)
            row.prop(self, "use_set_name")
            spl = row.split(factor=2.2, align=False)
            row = spl.row(align=False)
            if self.use_set_name:
                row.enabled = True
            else:
                row.enabled = False
            row.scale_x = 1.425
            row.prop(self, "set_name")
            row1 = box.row(align=True)
            row1.prop(self, "find_replace")
            row1.prop(self, "find")
            row1.prop(self, "replace")

            col = box.column(align=True)
            col.use_property_split = True
            col.use_property_decorate = False
            col.prop(self, "convert_lowercase")
            col.prop(self, "action")
        elif len(self.items) == 1:
            box = self.layout.box()
            box.use_property_split = True
            box.use_property_decorate = False
            col = box.column(align=True)

            col.prop(self, "set_name")
            col.prop(self, "convert_lowercase")
            col.prop(self, "tag_occluder")
            col.prop(self, "tag_rigid")
            col.prop(self, "tag_lod0")

    def execute(self, context):
        if len(self.items) > 1:
            Index = 0
            for obj in self.items:
                NewName = obj.name
                if self.action == "LOD":
                    NewName = self.newname_by_tag(
                        self,
                        name=obj.name,
                        Index=Index,
                        use_suffix="lod",
                        digit_length=1,
                    )
                    Index += 1
                elif self.action == "RIGID":
                    NewName = self.newname_by_tag(
                        self, name=obj.name, Index=Index, use_suffix="rigid"
                    )
                    Index += 1
                elif self.action == "DUMMY":
                    NewName = self.newname_by_tag(
                        self, name=obj.name, Index=Index, use_suffix="dummy"
                    )
                    Index += 1
                elif self.action == "DETECTION":
                    NewName = self.newname_by_tag(
                        self, name=obj.name, Index=Index, use_prefix="detection_"
                    )
                    Index += 1
                elif self.action == "DETECTION_DIR":
                    NewName = self.newname_by_tag(
                        self, name=obj.name, Index=Index, use_prefix="detection_frame"
                    )
                    Index += 1
                obj.name = NewName
        elif len(self.items) == 1:
            NewName = self.set_name
            if self.tag_occluder:
                NewName = NewName + "_occluder"
            if self.tag_rigid:
                NewName = NewName + "_rigid"
            if self.tag_lod0:
                NewName = NewName + "_lod0"
            if self.convert_lowercase:
                NewName = NewName.lower()
            self.items[0].name = NewName

        return {"FINISHED"}

    @staticmethod
    def newname_by_tag(
        self,
        name="",
        use_prefix="",
        use_suffix="",
        use_digits=True,
        digit_length=2,
        Index=0,
    ):
        NewName = name
        if self.use_set_name:
            NewName = self.set_name

        if use_prefix:
            prefix, dir = use_prefix.split("_")
            prefix = "" if use_prefix == "" else (prefix + "_")
            if use_digits:
                prefix += self.indexstr(digit_length, Index)

            if len(dir) > 0:
                NewName = prefix + "_" + dir + "_" + NewName
            else:
                NewName = prefix + "_" + NewName

        if use_suffix:
            suffix = "" if use_suffix == "" else ("_" + use_suffix)
            NewName = NewName + suffix
            if use_digits:
                NewName += self.indexstr(digit_length, Index)
            # Index += 1
        # Find and Replace #
        if self.find_replace:
            NewName = NewName.replace(self.find, self.replace)
        if self.convert_lowercase:
            NewName = NewName.lower()

        NewName = NewName.strip()
        return NewName

    @classmethod
    def poll(cls, context):
        bpy.app.handlers.depsgraph_update_post.append(selection_change_handler)
        return len(get_ordered_selection_objects()) > 0

    def invoke(self, context, event):
        self.items = get_ordered_selection_objects()

        if len(self.items) == 1:
            if bpy.context.active_object == None:
                bpy.context.view_layer.objects.active = self.items[0]
            self.set_name = cleanup_name_tag(name=self.items[0].name)
            wm = context.window_manager
            return wm.invoke_props_dialog(self)
        elif len(self.items) > 1:
            self.set_name = cleanup_name_tag(name=self.items[0].name)
            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=400)
        else:
            self.report({"ERROR"}, "请重新选择对象，再次执行重命名操作。")
            for obj in bpy.context.selected_objects:
                obj.select_set(False)
        return {"RUNNING_MODAL"}


def cleanup_name_tag(name):
    newname = name.split(".")[0]
    splitname = newname.split("_")
    if len(splitname) == 1:
        return newname
    else:
        newname = newname.lower()
        pattern = re.compile(
            r"_occluder|_lod\d*|_rigid\d*|_dummy\d*|detection_\d*_frame_|detection_\d*_"
        )
        newname = pattern.sub("", newname)
        return newname


def get_ordered_selection_objects():
    tagged_objects = []
    for o in bpy.data.objects:
        order_index = o.get("selection_order", -1)
        if order_index >= 0:
            tagged_objects.append((order_index, o))
    tagged_objects = sorted(tagged_objects, key=lambda item: item[0])
    return [o for i, o in tagged_objects]


def clear_order_flag(obj):
    try:
        del obj["selection_order"]
    except KeyError:
        pass


def update_selection_order():
    if not bpy.context.selected_objects:
        for o in bpy.data.objects:
            clear_order_flag(o)
        return
    selection_order = get_ordered_selection_objects()
    idx = 0
    for o in selection_order:
        if not o.select_get():
            selection_order.remove(o)
            clear_order_flag(o)
        else:
            o["selection_order"] = idx
            idx += 1
    for o in bpy.context.selected_objects:
        if o not in selection_order:
            o["selection_order"] = len(selection_order)
            selection_order.append(o)


def selection_change_handler(scene):
    if bpy.context.mode != "OBJECT":
        return
    is_selection_update = any(
        not u.is_updated_geometry
        and not u.is_updated_transform
        and not u.is_updated_shading
        for u in bpy.context.view_layer.depsgraph.updates
    )
    if is_selection_update:
        update_selection_order()


def geo_proxymesh_node_group():
    geo_proxymesh = bpy.data.node_groups.new(
        type="GeometryNodeTree", name="Geo_ProxyMesh"
    )

    # initialize geo_proxymesh nodes
    # node Reroute
    reroute = geo_proxymesh.nodes.new("NodeReroute")
    # node Separate XYZ.001
    separate_xyz_001 = geo_proxymesh.nodes.new("ShaderNodeSeparateXYZ")

    # node Transform Geometry.001
    transform_geometry_001 = geo_proxymesh.nodes.new("GeometryNodeTransform")
    # Translation
    transform_geometry_001.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_001.inputs[3].default_value = (1.0, 0.0, 1.0)

    # node Combine XYZ.004
    combine_xyz_004 = geo_proxymesh.nodes.new("ShaderNodeCombineXYZ")
    # X
    combine_xyz_004.inputs[0].default_value = 0.0
    # Z
    combine_xyz_004.inputs[2].default_value = 0.0

    # node Transform Geometry.002
    transform_geometry_002 = geo_proxymesh.nodes.new("GeometryNodeTransform")
    # Translation
    transform_geometry_002.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry_002.inputs[3].default_value = (0.0, 1.0, 1.0)

    # node Combine XYZ.007
    combine_xyz_007 = geo_proxymesh.nodes.new("ShaderNodeCombineXYZ")
    # Y
    combine_xyz_007.inputs[1].default_value = 0.0
    # Z
    combine_xyz_007.inputs[2].default_value = 0.0

    # node Convex Hull.002
    convex_hull_002 = geo_proxymesh.nodes.new("GeometryNodeConvexHull")

    # node Transform Geometry
    transform_geometry = geo_proxymesh.nodes.new("GeometryNodeTransform")
    # Translation
    transform_geometry.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    transform_geometry.inputs[3].default_value = (1.0, 1.0, 0.0)

    # node Curve Line.001
    curve_line_001 = geo_proxymesh.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line_001.mode = "POINTS"
    # Direction
    curve_line_001.inputs[2].default_value = (0.0, 0.0, 1.0)
    # Length
    curve_line_001.inputs[3].default_value = 1.0

    # node Transform Geometry.004
    transform_geometry_004 = geo_proxymesh.nodes.new("GeometryNodeTransform")
    # Translation
    transform_geometry_004.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_004.inputs[2].default_value = (
        0.0,
        -1.5707963705062866,
        1.5707963705062866,
    )
    # Scale
    transform_geometry_004.inputs[3].default_value = (1.0, 1.0, 1.0)

    # node Bounding Box
    bounding_box = geo_proxymesh.nodes.new("GeometryNodeBoundBox")

    # node Curve Line
    curve_line = geo_proxymesh.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.mode = "POINTS"
    # Direction
    curve_line.inputs[2].default_value = (0.0, 0.0, 1.0)
    # Length
    curve_line.inputs[3].default_value = 1.0

    # node Convex Hull
    convex_hull = geo_proxymesh.nodes.new("GeometryNodeConvexHull")

    # node Separate XYZ.004
    separate_xyz_004 = geo_proxymesh.nodes.new("ShaderNodeSeparateXYZ")

    # node Separate XYZ.005
    separate_xyz_005 = geo_proxymesh.nodes.new("ShaderNodeSeparateXYZ")

    # node Separate XYZ.002
    separate_xyz_002 = geo_proxymesh.nodes.new("ShaderNodeSeparateXYZ")

    # node Separate XYZ.003
    separate_xyz_003 = geo_proxymesh.nodes.new("ShaderNodeSeparateXYZ")

    # node Bounding Box.002
    bounding_box_002 = geo_proxymesh.nodes.new("GeometryNodeBoundBox")

    # node Bounding Box.001
    bounding_box_001 = geo_proxymesh.nodes.new("GeometryNodeBoundBox")

    # node Curve Line.002
    curve_line_002 = geo_proxymesh.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line_002.mode = "POINTS"
    # Direction
    curve_line_002.inputs[2].default_value = (0.0, 0.0, 1.0)
    # Length
    curve_line_002.inputs[3].default_value = 1.0

    # geo_proxymesh inputs
    # input Geometry
    geo_proxymesh.interface.new_socket("Geometry", description='', in_out='INPUT', socket_type="NodeSocketGeometry", parent=None)
    geo_proxymesh.interface.items_tree[0].attribute_domain = "POINT"


    # input Target Object
    geo_proxymesh.interface.new_socket("Target Object", description='', in_out='INPUT', socket_type="NodeSocketObject", parent=None)
    geo_proxymesh.interface.items_tree[1].attribute_domain = "POINT"

    # input Type
    geo_proxymesh.interface.new_socket("Type", description='', in_out='INPUT', socket_type="NodeSocketInt", parent=None)
    geo_proxymesh.interface.items_tree[2].default_value = 1
    geo_proxymesh.interface.items_tree[2].min_value = 1
    geo_proxymesh.interface.items_tree[2].max_value = 5
    geo_proxymesh.interface.items_tree[2].attribute_domain = "POINT"
    geo_proxymesh.interface.items_tree[2].description = "1 边界盒 2 凸包 3 X轴 4 Y轴  5 Z轴 "

    # input Poly Expand
    geo_proxymesh.interface.new_socket("Poly Expand", description='', in_out='INPUT', socket_type="NodeSocketFloat", parent=None)
    geo_proxymesh.interface.items_tree[3].default_value = 0.05
    geo_proxymesh.interface.items_tree[3].min_value = 0.0
    geo_proxymesh.interface.items_tree[3].max_value = 2.0
    geo_proxymesh.interface.items_tree[3].attribute_domain = "POINT"

    # node Group Input
    group_input = geo_proxymesh.nodes.new("NodeGroupInput")

    # node Mesh to Curve
    mesh_to_curve = geo_proxymesh.nodes.new("GeometryNodeMeshToCurve")
    # Selection
    mesh_to_curve.inputs[1].default_value = True

    # node Bounding Box.003
    bounding_box_003 = geo_proxymesh.nodes.new("GeometryNodeBoundBox")

    # initialize switch_geometry_4 node group
    def switch_geometry_4_node_group():
        switch_geometry_4 = bpy.data.node_groups.new(
            type="GeometryNodeTree", name="switch Geometry 4"
        )

        # initialize switch_geometry_4 nodes
        # node Switch.001
        switch_001 = switch_geometry_4.nodes.new("GeometryNodeSwitch")
        switch_001.input_type = "GEOMETRY"

        # node Compare.001
        compare_001 = switch_geometry_4.nodes.new("FunctionNodeCompare")
        compare_001.data_type = "INT"
        compare_001.operation = "GREATER_THAN"
        compare_001.mode = "ELEMENT"
        # A
        compare_001.inputs[0].default_value = 0.0
        # B
        compare_001.inputs[1].default_value = 0.0
        # B_INT
        compare_001.inputs[3].default_value = 2
        # A_VEC3
        compare_001.inputs[4].default_value = (0.0, 0.0, 0.0)
        # B_VEC3
        compare_001.inputs[5].default_value = (0.0, 0.0, 0.0)
        # A_COL
        compare_001.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
        # B_COL
        compare_001.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
        # A_STR
        compare_001.inputs[8].default_value = ""
        # B_STR
        compare_001.inputs[9].default_value = ""
        # C
        compare_001.inputs[10].default_value = 0.8999999761581421
        # Angle
        compare_001.inputs[11].default_value = 0.08726649731397629
        # Epsilon
        compare_001.inputs[12].default_value = 0.0010000000474974513

        # node Compare.002
        compare_002 = switch_geometry_4.nodes.new("FunctionNodeCompare")
        compare_002.data_type = "INT"
        compare_002.operation = "GREATER_THAN"
        compare_002.mode = "ELEMENT"
        # A
        compare_002.inputs[0].default_value = 0.0
        # B
        compare_002.inputs[1].default_value = 0.0
        # B_INT
        compare_002.inputs[3].default_value = 3
        # A_VEC3
        compare_002.inputs[4].default_value = (0.0, 0.0, 0.0)
        # B_VEC3
        compare_002.inputs[5].default_value = (0.0, 0.0, 0.0)
        # A_COL
        compare_002.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
        # B_COL
        compare_002.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
        # A_STR
        compare_002.inputs[8].default_value = ""
        # B_STR
        compare_002.inputs[9].default_value = ""
        # C
        compare_002.inputs[10].default_value = 0.8999999761581421
        # Angle
        compare_002.inputs[11].default_value = 0.08726649731397629
        # Epsilon
        compare_002.inputs[12].default_value = 0.0010000000474974513

        # switch_geometry_4 outputs
        # output Output
        switch_geometry_4.interface.new_socket("Output", description='', in_out='OUTPUT', socket_type="NodeSocketGeometry", parent=None)
        switch_geometry_4.interface.items_tree[0].attribute_domain = "POINT"

        # node Group Output
        group_output = switch_geometry_4.nodes.new("NodeGroupOutput")

        # node Switch.002
        switch_002 = switch_geometry_4.nodes.new("GeometryNodeSwitch")
        switch_002.input_type = "GEOMETRY"
        

        # switch_geometry_4 inputs
        # input input number
        switch_geometry_4.interface.new_socket("Input Number", description='', in_out='INPUT', socket_type="NodeSocketInt", parent=None)
        switch_geometry_4.interface.items_tree[1].default_value = 1
        switch_geometry_4.interface.items_tree[1].min_value = 1
        switch_geometry_4.interface.items_tree[1].max_value = 4
        switch_geometry_4.interface.items_tree[1].attribute_domain = "POINT"

        # input BBX
        switch_geometry_4.interface.new_socket("BBX", description='', in_out='INPUT', socket_type="NodeSocketGeometry", parent=None)
        switch_geometry_4.interface.items_tree[2].attribute_domain = "POINT"

        # input Convex Hull
        switch_geometry_4.interface.new_socket("Convex Hull", description='', in_out='INPUT', socket_type="NodeSocketGeometry", parent=None)
        switch_geometry_4.interface.items_tree[3].attribute_domain = "POINT"

        # input X Axis
        switch_geometry_4.interface.new_socket("X Axis", description='', in_out='INPUT', socket_type="NodeSocketGeometry", parent=None)
        switch_geometry_4.interface.items_tree[4].attribute_domain = "POINT"

        # input Y Axis
        switch_geometry_4.interface.new_socket("Y Axis", description='', in_out='INPUT', socket_type="NodeSocketGeometry", parent=None)
        switch_geometry_4.interface.items_tree[5].attribute_domain = "POINT"

        # input Z Axis
        switch_geometry_4.interface.new_socket("Z Axis", description='', in_out='INPUT', socket_type="NodeSocketGeometry", parent=None)
        switch_geometry_4.interface.items_tree[6].attribute_domain = "POINT"

        # node Group Input
        group_input_1 = switch_geometry_4.nodes.new("NodeGroupInput")

        # node Switch.003
        switch_003 = switch_geometry_4.nodes.new("GeometryNodeSwitch")
        switch_003.input_type = "GEOMETRY"

        # node Compare.003
        compare_003 = switch_geometry_4.nodes.new("FunctionNodeCompare")
        compare_003.data_type = "INT"
        compare_003.operation = "GREATER_THAN"
        compare_003.mode = "ELEMENT"
        # A
        compare_003.inputs[0].default_value = 0.0
        # B
        compare_003.inputs[1].default_value = 0.0
        # B_INT
        compare_003.inputs[3].default_value = 4
        # A_VEC3
        compare_003.inputs[4].default_value = (0.0, 0.0, 0.0)
        # B_VEC3
        compare_003.inputs[5].default_value = (0.0, 0.0, 0.0)
        # A_COL
        compare_003.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
        # B_COL
        compare_003.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
        # A_STR
        compare_003.inputs[8].default_value = ""
        # B_STR
        compare_003.inputs[9].default_value = ""
        # C
        compare_003.inputs[10].default_value = 0.8999999761581421
        # Angle
        compare_003.inputs[11].default_value = 0.08726649731397629
        # Epsilon
        compare_003.inputs[12].default_value = 0.0010000000474974513

        # node Switch
        switch = switch_geometry_4.nodes.new("GeometryNodeSwitch")
        switch.input_type = "GEOMETRY"

        # node Compare
        compare = switch_geometry_4.nodes.new("FunctionNodeCompare")
        compare.data_type = "INT"
        compare.operation = "GREATER_THAN"
        compare.mode = "ELEMENT"
        # A
        compare.inputs[0].default_value = 0.0
        # B
        compare.inputs[1].default_value = 0.0
        # B_INT
        compare.inputs[3].default_value = 1
        # A_VEC3
        compare.inputs[4].default_value = (0.0, 0.0, 0.0)
        # B_VEC3
        compare.inputs[5].default_value = (0.0, 0.0, 0.0)
        # A_COL
        compare.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
        # B_COL
        compare.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
        # A_STR
        compare.inputs[8].default_value = ""
        # B_STR
        compare.inputs[9].default_value = ""
        # C
        compare.inputs[10].default_value = 0.8999999761581421
        # Angle
        compare.inputs[11].default_value = 0.08726649731397629
        # Epsilon
        compare.inputs[12].default_value = 0.0010000000474974513

        # Set locations

        # Set dimensions

        # initialize switch_geometry_4 links
        # compare.Result -> switch.Switch
        switch_geometry_4.links.new(compare.outputs[0], switch.inputs[0])
        # compare_001.Result -> switch_001.Switch
        switch_geometry_4.links.new(compare_001.outputs[0], switch_001.inputs[0])
        # switch.Output -> switch_001.False
        switch_geometry_4.links.new(switch.outputs[0], switch_001.inputs[2])
        # compare_002.Result -> switch_002.Switch
        switch_geometry_4.links.new(compare_002.outputs[0], switch_002.inputs[0])
        # switch_001.Output -> switch_002.False
        switch_geometry_4.links.new(switch_001.outputs[0], switch_002.inputs[2])
        # group_input_1.input number -> compare.A
        switch_geometry_4.links.new(group_input_1.outputs[0], compare.inputs[2])
        # group_input_1.input number -> compare_001.A
        switch_geometry_4.links.new(group_input_1.outputs[0], compare_001.inputs[2])
        # group_input_1.input number -> compare_002.A
        switch_geometry_4.links.new(group_input_1.outputs[0], compare_002.inputs[2])
        # group_input_1.BBX -> switch.False
        switch_geometry_4.links.new(group_input_1.outputs[1], switch.inputs[2])
        # group_input_1.Convex Hull -> switch.True
        switch_geometry_4.links.new(group_input_1.outputs[2], switch.inputs[3])
        # group_input_1.X Axis -> switch_001.True
        switch_geometry_4.links.new(group_input_1.outputs[3], switch_001.inputs[3])
        # group_input_1.Y Axis -> switch_002.True
        switch_geometry_4.links.new(group_input_1.outputs[4], switch_002.inputs[3])
        # compare.Result -> switch.Switch
        switch_geometry_4.links.new(compare.outputs[0], switch.inputs[1])
        # compare_001.Result -> switch_001.Switch
        switch_geometry_4.links.new(compare_001.outputs[0], switch_001.inputs[1])
        # group_input_1.BBX -> switch.False
        switch_geometry_4.links.new(group_input_1.outputs[1], switch.inputs[14])
        # switch.Output -> switch_001.False
        switch_geometry_4.links.new(switch.outputs[6], switch_001.inputs[14])
        # group_input_1.Convex Hull -> switch.True
        switch_geometry_4.links.new(group_input_1.outputs[2], switch.inputs[15])
        # group_input_1.X Axis -> switch_001.True
        switch_geometry_4.links.new(group_input_1.outputs[3], switch_001.inputs[15])
        # compare_002.Result -> switch_002.Switch
        switch_geometry_4.links.new(compare_002.outputs[0], switch_002.inputs[1])
        # switch_001.Output -> switch_002.False
        switch_geometry_4.links.new(switch_001.outputs[6], switch_002.inputs[14])
        # group_input_1.Y Axis -> switch_002.True
        switch_geometry_4.links.new(group_input_1.outputs[4], switch_002.inputs[15])
        # compare_003.Result -> switch_003.Switch
        switch_geometry_4.links.new(compare_003.outputs[0], switch_003.inputs[0])
        # compare_003.Result -> switch_003.Switch
        switch_geometry_4.links.new(compare_003.outputs[0], switch_003.inputs[1])
        # switch_002.Output -> switch_003.False
        switch_geometry_4.links.new(switch_002.outputs[6], switch_003.inputs[14])
        # group_input_1.Z Axis -> switch_003.True
        switch_geometry_4.links.new(group_input_1.outputs[5], switch_003.inputs[15])
        # group_input_1.input number -> compare_003.A
        switch_geometry_4.links.new(group_input_1.outputs[0], compare_003.inputs[2])
        # switch_003.Output -> group_output.Output
        switch_geometry_4.links.new(switch_003.outputs[6], group_output.inputs[0])
        return switch_geometry_4

    switch_geometry_4 = switch_geometry_4_node_group()

    # node Group
    group = geo_proxymesh.nodes.new("GeometryNodeGroup")
    group.node_tree = bpy.data.node_groups["switch Geometry 4"]

    # node Convex Hull.003
    convex_hull_003 = geo_proxymesh.nodes.new("GeometryNodeConvexHull")

    # node Value
    value = geo_proxymesh.nodes.new("ShaderNodeValue")

    value.outputs[0].default_value = 1.0
    # node Viewer
    viewer = geo_proxymesh.nodes.new("GeometryNodeViewer")
    viewer.domain = "AUTO"
    # Value
    viewer.inputs[1].default_value = 0.0
    # Value_002
    viewer.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    # Value_003
    viewer.inputs[4].default_value = 0
    # Value_004
    viewer.inputs[5].default_value = False

    # geo_proxymesh outputs
    # output Geometry
    geo_proxymesh.outputs.new("NodeSocketGeometry", "Geometry")
    geo_proxymesh.outputs[0].attribute_domain = "POINT"

    # node Group Output
    group_output_1 = geo_proxymesh.nodes.new("NodeGroupOutput")

    # node Set Shade Smooth
    set_shade_smooth = geo_proxymesh.nodes.new("GeometryNodeSetShadeSmooth")
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = False

    # node Combine XYZ.002
    combine_xyz_002 = geo_proxymesh.nodes.new("ShaderNodeCombineXYZ")
    # X
    combine_xyz_002.inputs[0].default_value = 0.0
    # Y
    combine_xyz_002.inputs[1].default_value = 0.0

    # node Combine XYZ.003
    combine_xyz_003 = geo_proxymesh.nodes.new("ShaderNodeCombineXYZ")
    # X
    combine_xyz_003.inputs[0].default_value = 0.0
    # Y
    combine_xyz_003.inputs[1].default_value = 0.0

    # node Separate XYZ
    separate_xyz = geo_proxymesh.nodes.new("ShaderNodeSeparateXYZ")

    # node Combine XYZ.005
    combine_xyz_005 = geo_proxymesh.nodes.new("ShaderNodeCombineXYZ")
    # X
    combine_xyz_005.inputs[0].default_value = 0.0
    # Z
    combine_xyz_005.inputs[2].default_value = 0.0

    # node Mesh to Curve.002
    mesh_to_curve_002 = geo_proxymesh.nodes.new("GeometryNodeMeshToCurve")
    # Selection
    mesh_to_curve_002.inputs[1].default_value = True

    # node Combine XYZ.006
    combine_xyz_006 = geo_proxymesh.nodes.new("ShaderNodeCombineXYZ")
    # Y
    combine_xyz_006.inputs[1].default_value = 0.0
    # Z
    combine_xyz_006.inputs[2].default_value = 0.0

    # node Transform Geometry.003
    transform_geometry_003 = geo_proxymesh.nodes.new("GeometryNodeTransform")
    # Translation
    transform_geometry_003.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    transform_geometry_003.inputs[2].default_value = (1.5707963705062866, 0.0, 0.0)
    # Scale
    transform_geometry_003.inputs[3].default_value = (1.0, 1.0, 1.0)

    # node Mesh to Curve.001
    mesh_to_curve_001 = geo_proxymesh.nodes.new("GeometryNodeMeshToCurve")
    # Selection
    mesh_to_curve_001.inputs[1].default_value = True

    # node Object Info
    object_info = geo_proxymesh.nodes.new("GeometryNodeObjectInfo")
    object_info.transform_space = "RELATIVE"
    # As Instance
    object_info.inputs[1].default_value = False

    # node Extrude Mesh.001
    extrude_mesh_001 = geo_proxymesh.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh_001.mode = "FACES"
    # Selection
    extrude_mesh_001.inputs[1].default_value = True
    # Offset
    extrude_mesh_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Individual
    extrude_mesh_001.inputs[4].default_value = False

    # node Convex Hull.001
    convex_hull_001 = geo_proxymesh.nodes.new("GeometryNodeConvexHull")

    # node Triangulate.001
    triangulate_001 = geo_proxymesh.nodes.new("GeometryNodeTriangulate")
    triangulate_001.quad_method = "SHORTEST_DIAGONAL"
    triangulate_001.ngon_method = "BEAUTY"
    # Selection
    triangulate_001.inputs[1].default_value = True
    # Minimum Vertices
    triangulate_001.inputs[2].default_value = 4

    # node Triangulate.002
    triangulate_002 = geo_proxymesh.nodes.new("GeometryNodeTriangulate")
    triangulate_002.quad_method = "SHORTEST_DIAGONAL"
    triangulate_002.ngon_method = "BEAUTY"
    # Selection
    triangulate_002.inputs[1].default_value = True
    # Minimum Vertices
    triangulate_002.inputs[2].default_value = 4

    # node Curve to Mesh.002
    curve_to_mesh_002 = geo_proxymesh.nodes.new("GeometryNodeCurveToMesh")
    # Fill Caps
    curve_to_mesh_002.inputs[2].default_value = True

    # node Curve to Mesh.001
    curve_to_mesh_001 = geo_proxymesh.nodes.new("GeometryNodeCurveToMesh")
    # Fill Caps
    curve_to_mesh_001.inputs[2].default_value = True

    # node Curve to Mesh
    curve_to_mesh = geo_proxymesh.nodes.new("GeometryNodeCurveToMesh")
    # Fill Caps
    curve_to_mesh.inputs[2].default_value = True

    # node Triangulate.003
    triangulate_003 = geo_proxymesh.nodes.new("GeometryNodeTriangulate")
    triangulate_003.quad_method = "SHORTEST_DIAGONAL"
    triangulate_003.ngon_method = "BEAUTY"
    # Selection
    triangulate_003.inputs[1].default_value = True
    # Minimum Vertices
    triangulate_003.inputs[2].default_value = 4

    # #Set locations
    # #Set dimensions

    # initialize geo_proxymesh links
    # transform_geometry.Geometry -> convex_hull.Geometry
    geo_proxymesh.links.new(transform_geometry.outputs[0], convex_hull.inputs[0])
    # reroute.Output -> bounding_box.Geometry
    geo_proxymesh.links.new(reroute.outputs[0], bounding_box.inputs[0])
    # reroute.Output -> transform_geometry.Geometry
    geo_proxymesh.links.new(reroute.outputs[0], transform_geometry.inputs[0])
    # bounding_box.Min -> separate_xyz.Vector
    geo_proxymesh.links.new(bounding_box.outputs[1], separate_xyz.inputs[0])
    # bounding_box.Max -> separate_xyz_001.Vector
    geo_proxymesh.links.new(bounding_box.outputs[2], separate_xyz_001.inputs[0])
    # group_input.Target Object -> object_info.Object
    geo_proxymesh.links.new(group_input.outputs[1], object_info.inputs[0])
    # mesh_to_curve.Curve -> curve_to_mesh.Profile Curve
    geo_proxymesh.links.new(mesh_to_curve.outputs[0], curve_to_mesh.inputs[1])
    # curve_line.Curve -> curve_to_mesh.Curve
    geo_proxymesh.links.new(curve_line.outputs[0], curve_to_mesh.inputs[0])
    # separate_xyz.Z -> combine_xyz_002.Z
    geo_proxymesh.links.new(separate_xyz.outputs[2], combine_xyz_002.inputs[2])
    # combine_xyz_002.Vector -> curve_line.Start
    geo_proxymesh.links.new(combine_xyz_002.outputs[0], curve_line.inputs[0])
    # separate_xyz_001.Z -> combine_xyz_003.Z
    geo_proxymesh.links.new(separate_xyz_001.outputs[2], combine_xyz_003.inputs[2])
    # combine_xyz_003.Vector -> curve_line.End
    geo_proxymesh.links.new(combine_xyz_003.outputs[0], curve_line.inputs[1])
    # transform_geometry_001.Geometry -> convex_hull_001.Geometry
    geo_proxymesh.links.new(
        transform_geometry_001.outputs[0], convex_hull_001.inputs[0]
    )
    # reroute.Output -> bounding_box_001.Geometry
    geo_proxymesh.links.new(reroute.outputs[0], bounding_box_001.inputs[0])
    # reroute.Output -> transform_geometry_001.Geometry
    geo_proxymesh.links.new(reroute.outputs[0], transform_geometry_001.inputs[0])
    # bounding_box_001.Min -> separate_xyz_002.Vector
    geo_proxymesh.links.new(bounding_box_001.outputs[1], separate_xyz_002.inputs[0])
    # bounding_box_001.Max -> separate_xyz_003.Vector
    geo_proxymesh.links.new(bounding_box_001.outputs[2], separate_xyz_003.inputs[0])
    # curve_line_001.Curve -> curve_to_mesh_001.Curve
    geo_proxymesh.links.new(curve_line_001.outputs[0], curve_to_mesh_001.inputs[0])
    # combine_xyz_004.Vector -> curve_line_001.Start
    geo_proxymesh.links.new(combine_xyz_004.outputs[0], curve_line_001.inputs[0])
    # combine_xyz_005.Vector -> curve_line_001.End
    geo_proxymesh.links.new(combine_xyz_005.outputs[0], curve_line_001.inputs[1])
    # separate_xyz_002.Y -> combine_xyz_004.Y
    geo_proxymesh.links.new(separate_xyz_002.outputs[1], combine_xyz_004.inputs[1])
    # separate_xyz_003.Y -> combine_xyz_005.Y
    geo_proxymesh.links.new(separate_xyz_003.outputs[1], combine_xyz_005.inputs[1])
    # transform_geometry_002.Geometry -> convex_hull_002.Geometry
    geo_proxymesh.links.new(
        transform_geometry_002.outputs[0], convex_hull_002.inputs[0]
    )
    # reroute.Output -> bounding_box_002.Geometry
    geo_proxymesh.links.new(reroute.outputs[0], bounding_box_002.inputs[0])
    # reroute.Output -> transform_geometry_002.Geometry
    geo_proxymesh.links.new(reroute.outputs[0], transform_geometry_002.inputs[0])
    # bounding_box_002.Min -> separate_xyz_004.Vector
    geo_proxymesh.links.new(bounding_box_002.outputs[1], separate_xyz_004.inputs[0])
    # bounding_box_002.Max -> separate_xyz_005.Vector
    geo_proxymesh.links.new(bounding_box_002.outputs[2], separate_xyz_005.inputs[0])
    # curve_line_002.Curve -> curve_to_mesh_002.Curve
    geo_proxymesh.links.new(curve_line_002.outputs[0], curve_to_mesh_002.inputs[0])
    # combine_xyz_006.Vector -> curve_line_002.Start
    geo_proxymesh.links.new(combine_xyz_006.outputs[0], curve_line_002.inputs[0])
    # combine_xyz_007.Vector -> curve_line_002.End
    geo_proxymesh.links.new(combine_xyz_007.outputs[0], curve_line_002.inputs[1])
    # separate_xyz_004.X -> combine_xyz_006.X
    geo_proxymesh.links.new(separate_xyz_004.outputs[0], combine_xyz_006.inputs[0])
    # separate_xyz_005.X -> combine_xyz_007.X
    geo_proxymesh.links.new(separate_xyz_005.outputs[0], combine_xyz_007.inputs[0])
    # triangulate_003.Mesh -> group.X Axis
    geo_proxymesh.links.new(triangulate_003.outputs[0], group.inputs[3])
    # group_input.Type -> group.input number
    geo_proxymesh.links.new(group_input.outputs[2], group.inputs[0])
    # mesh_to_curve_001.Curve -> transform_geometry_003.Geometry
    geo_proxymesh.links.new(
        mesh_to_curve_001.outputs[0], transform_geometry_003.inputs[0]
    )
    # transform_geometry_003.Geometry -> curve_to_mesh_001.Profile Curve
    geo_proxymesh.links.new(
        transform_geometry_003.outputs[0], curve_to_mesh_001.inputs[1]
    )
    # mesh_to_curve_002.Curve -> transform_geometry_004.Geometry
    geo_proxymesh.links.new(
        mesh_to_curve_002.outputs[0], transform_geometry_004.inputs[0]
    )
    # transform_geometry_004.Geometry -> curve_to_mesh_002.Profile Curve
    geo_proxymesh.links.new(
        transform_geometry_004.outputs[0], curve_to_mesh_002.inputs[1]
    )
    # bounding_box_003.Bounding Box -> group.BBX
    geo_proxymesh.links.new(bounding_box_003.outputs[0], group.inputs[1])
    # triangulate_001.Mesh -> group.Z Axis
    geo_proxymesh.links.new(triangulate_001.outputs[0], group.inputs[5])
    # triangulate_002.Mesh -> group.Y Axis
    geo_proxymesh.links.new(triangulate_002.outputs[0], group.inputs[4])
    # object_info.Geometry -> extrude_mesh_001.Mesh
    geo_proxymesh.links.new(object_info.outputs[3], extrude_mesh_001.inputs[0])
    # reroute.Output -> convex_hull_003.Geometry
    geo_proxymesh.links.new(reroute.outputs[0], convex_hull_003.inputs[0])
    # reroute.Output -> bounding_box_003.Geometry
    geo_proxymesh.links.new(reroute.outputs[0], bounding_box_003.inputs[0])
    # extrude_mesh_001.Mesh -> reroute.Input
    geo_proxymesh.links.new(extrude_mesh_001.outputs[0], reroute.inputs[0])
    # group_input.Poly Expand -> extrude_mesh_001.Offset Scale
    geo_proxymesh.links.new(group_input.outputs[3], extrude_mesh_001.inputs[3])
    # curve_to_mesh.Mesh -> viewer.Geometry
    geo_proxymesh.links.new(curve_to_mesh.outputs[0], viewer.inputs[0])
    # convex_hull_002.Convex Hull -> mesh_to_curve_002.Mesh
    geo_proxymesh.links.new(convex_hull_002.outputs[0], mesh_to_curve_002.inputs[0])
    # convex_hull_001.Convex Hull -> mesh_to_curve_001.Mesh
    geo_proxymesh.links.new(convex_hull_001.outputs[0], mesh_to_curve_001.inputs[0])
    # convex_hull.Convex Hull -> mesh_to_curve.Mesh
    geo_proxymesh.links.new(convex_hull.outputs[0], mesh_to_curve.inputs[0])
    # convex_hull_003.Convex Hull -> group.Convex Hull
    geo_proxymesh.links.new(convex_hull_003.outputs[0], group.inputs[2])
    # value.Value -> viewer.Value
    geo_proxymesh.links.new(value.outputs[0], viewer.inputs[2])
    # curve_to_mesh.Mesh -> triangulate_001.Mesh
    geo_proxymesh.links.new(curve_to_mesh.outputs[0], triangulate_001.inputs[0])
    # curve_to_mesh_001.Mesh -> triangulate_002.Mesh
    geo_proxymesh.links.new(curve_to_mesh_001.outputs[0], triangulate_002.inputs[0])
    # curve_to_mesh_002.Mesh -> triangulate_003.Mesh
    geo_proxymesh.links.new(curve_to_mesh_002.outputs[0], triangulate_003.inputs[0])
    # group.Output -> set_shade_smooth.Geometry
    geo_proxymesh.links.new(group.outputs[0], set_shade_smooth.inputs[0])
    # set_shade_smooth.Geometry -> group_output_1.Geometry
    geo_proxymesh.links.new(set_shade_smooth.outputs[0], group_output_1.inputs[0])
    return geo_proxymesh

def geo_proxymesh_convexhull():
    geo_proxymesh = bpy.data.node_groups.new(
        type="GeometryNodeTree", name="Geo_ProxyMesh"
    )

    convex_hull = geo_proxymesh.nodes.new("GeometryNodeConvexHull")

    object_info = geo_proxymesh.nodes.new("GeometryNodeObjectInfo")
    object_info.transform_space = "RELATIVE"
    # As Instance
    object_info.inputs[1].default_value = False

    # node Extrude Mesh
    extrude_mesh = geo_proxymesh.nodes.new("GeometryNodeExtrudeMesh")
    extrude_mesh.mode = "FACES"
    # Selection
    extrude_mesh.inputs[1].default_value = True
    # Offset
    extrude_mesh.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Individual
    extrude_mesh.inputs[4].default_value = False

    # node Group Input
    group_input = geo_proxymesh.nodes.new("NodeGroupInput")

    geo_proxymesh.interface.new_socket("Geometry", description="", in_out= "INPUT", socket_type="NodeSocketGeometry", parent=None)
    geo_proxymesh.interface.items_tree[0].attribute_domain = "POINT"
    # input Target Object
    geo_proxymesh.interface.new_socket("Target Object", description="", in_out= "INPUT", socket_type="NodeSocketObject", parent=None)
    geo_proxymesh.interface.items_tree[1].attribute_domain = "POINT"
    # input Poly Expand
    geo_proxymesh.interface.new_socket("Poly Expand", description="", in_out= "INPUT", socket_type="NodeSocketFloat", parent=None)
    geo_proxymesh.interface.items_tree[2].default_value = 0.05
    geo_proxymesh.interface.items_tree[2].min_value = 0.0
    geo_proxymesh.interface.items_tree[2].max_value = 2.0
    geo_proxymesh.interface.items_tree[2].attribute_domain = "POINT"


    # node Set Shade Smooth
    set_shade_smooth = geo_proxymesh.nodes.new("GeometryNodeSetShadeSmooth")
    # Selection
    set_shade_smooth.inputs[1].default_value = True
    # Shade Smooth
    set_shade_smooth.inputs[2].default_value = False

    # node Group Output
    geo_proxymesh.interface.new_socket("Geometry", description="", in_out= "OUTPUT", socket_type="NodeSocketGeometry", parent=None)
    geo_proxymesh.interface.items_tree[0].attribute_domain = "POINT"
    
    group_output = geo_proxymesh.nodes.new("NodeGroupOutput")
    
    geo_proxymesh.links.new(extrude_mesh.outputs[0], convex_hull.inputs[0])
    geo_proxymesh.links.new(group_input.outputs[1], object_info.inputs[0])
    geo_proxymesh.links.new(group_input.outputs[2], extrude_mesh.inputs[3])
    geo_proxymesh.links.new(object_info.outputs[3], extrude_mesh.inputs[0])
    geo_proxymesh.links.new(convex_hull.outputs[0], set_shade_smooth.inputs[0])
    geo_proxymesh.links.new(set_shade_smooth.outputs[0], group_output.inputs[0])

    return geo_proxymesh


class Geo_ProxyMesh:
    def modifiers_result(self, context):
        depsgraph = context.evaluated_depsgraph_get()
        obj = context.object
        evaluated_object = obj.evaluated_get(depsgraph)
        mesh = bpy.data.meshes.new_from_object(evaluated_object, depsgraph=depsgraph)
        obj.modifiers.clear()
        if obj.mode == "OBJECT":
            obj.data = mesh
        else:
            bm = bmesh.from_edit_mesh(obj.data)
            bm.clear()
            bm.from_mesh(mesh)
            bmesh.update_edit_mesh(obj.data)
        # print("-------modifiers_result------")


class CHAOS_OT_Geo_BBX(Geo_ProxyMesh, Operator):
    bl_idname = "chaos.geo_bbx"
    bl_label = "Bounding Box"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "为激活物体生成边界框，并设置边界框网格显示模式为线框"

    def execute(self, context):
        self.modifiers_result(context)
        return {"FINISHED"}

    def draw(self, context):
        box = self.layout.box()
        col = box.column(align=True)
        col.prop(
            data=context.active_object.modifiers["Geo_ProxyMesh"],
            property='["Socket_2"]',
            text="Expand",
            slider=1,
        )

    def invoke(self, context, event):
        self.items = bpy.context.selected_objects
        if context.active_object:
            # initialize geo_proxymesh node group
            geo_proxymesh = geo_proxymesh_node_group()

            target_name = bpy.context.object.name

            bpy.ops.mesh.primitive_plane_add(
                size=2,
                enter_editmode=False,
                align="WORLD",
                location=(0, 0, 0),
                scale=(1, 1, 1),
            )
            newname = cleanup_name_tag(name=target_name)
            bpy.context.active_object.name = newname + "_BoundingBox"
            bpy.context.object.display_type = "WIRE"

            name = bpy.context.active_object.name
            obj = bpy.data.objects[name]
            mod = obj.modifiers.new(name="Geo_ProxyMesh", type="NODES")
            mod.node_group = geo_proxymesh
            mod["Input_1"] = bpy.data.objects[target_name]

            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=400)
        return {"FINISHED"}


class CHAOS_OT_Geo_ConvexHull(Geo_ProxyMesh, Operator):
    bl_idname = "chaos.geo_convexhull"
    bl_label = "Convex Hull"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "为激活物体生成凸包网格，并设置凸包网格显示模式为线框"

    def execute(self, context):
        self.modifiers_result(context)
        return {"FINISHED"}

    def draw(self, context):
        box = self.layout.box()
        col = box.column(align=True)
        col.prop(
            data=context.active_object.modifiers["Geo_ProxyMesh"],
            property='["Socket_2"]',
            text="Expand",
            slider=1,
        )
        col.label(text="Decimate")
        col.prop(
            data=context.active_object.modifiers["Decimate"],
            property="ratio",
            text="Ratio",
        )

    def invoke(self, context, event):
        self.items = bpy.context.selected_objects
        if context.active_object:
            # initialize geo_proxymesh node group
            #geo_proxymesh = geo_proxymesh_node_group()
            geo_proxymesh = geo_proxymesh_convexhull()

            target_name = bpy.context.object.name

            bpy.ops.mesh.primitive_plane_add(
                size=2,
                enter_editmode=False,
                align="WORLD",
                location=(0, 0, 0),
                scale=(1, 1, 1),
            )
            newname = cleanup_name_tag(name=target_name)
            # bpy.data.meshes[f"{target_name}"].name = newname
            bpy.context.active_object.name = newname + "_ConvexHull"
            bpy.context.object.display_type = "WIRE"

            name = bpy.context.active_object.name
            obj = bpy.data.objects[name]
            mod = obj.modifiers.new(name="Geo_ProxyMesh", type="NODES")
            mod.node_group = geo_proxymesh
            mod["Socket_1"] = bpy.data.objects[target_name]
            print(mod.items())
            mod = obj.modifiers.new(name="Decimate", type="DECIMATE")
            mod.ratio = 0.3

            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=400)
        return {"FINISHED"}


class CHAOS_OT_Utils_Parent_Empty(Operator):
    """
    为选择对象创建父对象(空物体)
    """

    bl_idname = "chaos.op_parent_empty"
    bl_label = "Parent to Empty"
    bl_description = "为选择对象创建父对象(空物体)"
    bl_options = {"REGISTER", "UNDO"}

    set_name: bpy.props.StringProperty(name="", description="Base Name")

    items = []

    def draw(self, context):
        box = self.layout.box()
        row = box.row(align=True)
        row.prop(self, "set_name")

    def execute(self, context):
        selobj = context.selected_objects
        bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
        empty = bpy.context.object
        empty.name = self.set_name
        # empty.name = self.rename()
        message = "select objects <"
        for obj in selobj:
            if obj.type != "MESH" and obj.type != "EMPTY":
                continue
            message += obj.name + "/"
            obj.parent = empty
        self.report({"INFO"}, message + f"> parent object is < {empty.name} >.")
        return {"FINISHED"}

    def invoke(self, context, event):
        self.items = bpy.context.selected_objects
        if context.active_object == None:
            context.view_layer.objects.active = self.items[0]
        if len(self.items) > 0:
            # self.set_name = self.items[0].name
            self.set_name = cleanup_name_tag(name=self.items[0].name)
            wm = context.window_manager
            return wm.invoke_props_dialog(self, width=400)
        return {"FINISHED"}


class Add_Eempty:
    @classmethod
    def add_driver(self, ob, attrib_target, attrib_source, idx):
        d = ob.driver_add(f'["{attrib_target}"]', idx).driver
        d.type = "AVERAGE"
        v = d.variables.new()
        t = v.targets[0]
        t.id_type = "OBJECT"
        t.id = ob
        t.data_path = f"{attrib_source}[{idx}]"

        ob.id_properties_ensure()
        property_manager = ob.id_properties_ui(attrib_target)
        property_manager.update(min=-1e39, max=1e39)


class CHAOS_OT_Geo_Add_EemptyCube(Add_Eempty, Operator):
    """
    添加刚体代理对象-立方体
    """

    bl_idname = "chaos.op_add_emptycube"
    bl_label = "Empty Cube"
    bl_description = "添加刚体代理对象-立方体"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.object.empty_add(
            type="CUBE", align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
        )
        context.active_object.name = "EmptyCube.001"
        ob = context.active_object
        prop_name = "size"
        ob[prop_name] = (0.0, 0.0, 0.0)

        self.add_driver(ob, prop_name, "scale", 0)
        self.add_driver(ob, prop_name, "scale", 1)
        self.add_driver(ob, prop_name, "scale", 2)
        return {"FINISHED"}


class CHAOS_OT_Geo_Add_EemptySphere(Add_Eempty, Operator):
    """
    添加刚体代理对象-球体
    """

    bl_idname = "chaos.op_add_emptysphere"
    bl_label = "Empty Sphere"
    bl_description = "添加刚体代理对象-球体"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.object.empty_add(
            type="SPHERE", align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
        )
        context.active_object.name = "EmptySphere.001"
        ob = context.active_object
        prop_name = "size"
        ob[prop_name] = (0.0, 0.0, 0.0)

        self.add_driver(ob, prop_name, "scale", 0)
        self.add_driver(ob, prop_name, "scale", 1)
        self.add_driver(ob, prop_name, "scale", 2)
        return {"FINISHED"}


class CHAOS_OT_Utils_CleanUp(Operator):
    bl_idname = "chaos.op_utils_cleanup"
    bl_description = "清理文件中所有不属于任何对象,并且未被使用的数据块"
    bl_label = "Recursive Unused Data-Blocks"

    def execute(self, context):
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
        return {"FINISHED"}


class CHAOS_OT_TopologyCheck_deleteloose(Operator):
    """删除松散元素"""

    bl_idname = "chaos.op_topocheck_deleteloose"
    bl_label = "Delete Loose"
    bl_description = "删除所有网格对象的松散顶点，边或面"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        message = ""
        count = 0
        # if bpy.ops.object.mode_set.poll():
        #     #print("检测合法,当前context为：" + bpy.ops.object.__name__)
        #     bpy.ops.object.mode_set( mode = 'OBJECT' )
        #     for o in bpy.data.objects:
        #         if (o.type == 'MESH'):
        #             count += 1
        #             bpy.context.view_layer.objects.active = o
        #             if bpy.ops.object.mode_set.poll():
        #                 bpy.ops.object.mode_set(mode='EDIT', toggle=True)
        #             bpy.ops.mesh.select_all(action='SELECT')
        #             bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)
        #             print(o.name)
        #             bpy.ops.object.mode_set( mode = 'OBJECT' )
        #     self.report({"INFO"},"\n delete loose successfully.")
        #     print("总共处理了 %d 个MESH" % count)
        #     return {"FINISHED"}
        # else:
        #     print("无事发生,当前context为：" + bpy.ops.object.__name__)
        #     return {"CANCELLED"}

        objectLists = bpy.context.selected_objects
        print("长度为：%d" % len(objectLists))
        if len(objectLists) == 0:
            self.report({"INFO"}, "请不要啥也不选")
            return {"FINISHED"}
        deleteLooseCount = 0
        deleteLooseSucceedCount = 0
        deleteLooseFailedCount = 0
        self.report({"INFO"}, "----------------------开始处理----------------------")
        for o in objectLists:
            deleteLooseCount += 1
            print(bpy.ops.object.mode_set.poll())
            if o.type == "MESH" and bpy.ops.object.mode_set.poll():
                bpy.context.view_layer.objects.active = o
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action="SELECT")
                bpy.ops.mesh.delete_loose(
                    use_verts=True, use_edges=True, use_faces=False
                )
                bpy.ops.object.mode_set(mode="OBJECT")
                self.report({"INFO"}, f"第{deleteLooseCount}次处理成功,当前对象为：{o.name}")
                print(f"第{deleteLooseCount}次处理成功,当前对象为：{o.name}")
                deleteLooseSucceedCount += 1
            elif o.type == "MESH" and not bpy.ops.object.mode_set.poll():
                self.report(
                    {"INFO"}, f"第{deleteLooseCount}次处理失败,当前对象为：{o.name}，请重新选取该对象再次操作"
                )
                print(f"第{deleteLooseCount}次处理失败,当前对象为：{o.name}，类型为{o.type}")
                deleteLooseFailedCount += 1
            else:
                self.report(
                    {"INFO"}, f"第{deleteLooseCount}次处理失败,当前对象为：{o.name}，类型为{o.type}"
                )
                print(f"第{deleteLooseCount}次处理失败,当前对象为：{o.name}")
                deleteLooseFailedCount += 1
                # return {"CANCELLED"}
        self.report(
            {"INFO"},
            f"-------------结束处理，成功{deleteLooseSucceedCount}个，失败{deleteLooseFailedCount}个-------------",
        )
        return {"FINISHED"}


class CHAOS_OT_Replace_Repeated_Materials(Operator):
    """
    \n替换重复材质
    \n这个函数不会进行删除材质的操作
    """

    bl_idname = "chaos.replace_repeated_materials"
    bl_label = "替换重复材质（无删除操作）"
    bl_description = "将重复的材质替换为原材质"
    bl_options = {"INTERNAL", "UNDO"}

    selectedObjectList = []
    newSelectedObjectList = []
    allObjectList = []

    isUpdateEnabled: BoolProperty(
        name="is Update Enabled",
        description="是否需要更新选择项,False为需要更新",
        default=False,
    )

    objectCount: IntProperty(
        name="objectCount",
        default=0,
    )

    def SearchChildrenObject(ObjectList: bpy.types.BlendDataObjects):
        result = []

        for obj in ObjectList:
            if not obj in CHAOS_OT_Replace_Repeated_Materials.selectedObjectList:
                result.append(obj)
            if obj.children == None:
                pass
            else:
                result.extend(
                    CHAOS_OT_Replace_Repeated_Materials.SearchChildrenObject(
                        obj.children
                    )
                )
        return result

    def data_source_update(self, context):
        for obj in bpy.data.objects:
            obj.select_set(False)
        self.isUpdateEnabled = False

    data_source: EnumProperty(
        name="Source",
        items=(
            ("SELECT", "当前选中项", ""),
            ("ALL", "全部项", ""),
            ("SELECT CHILDREN", "选中所有层级", ""),
        ),
        update=data_source_update,
    )

    def draw(self, context: Context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "data_source", expand=True)
        row = layout.row()

        if self.isUpdateEnabled == False:
            if self.data_source == "SELECT":
                print("对当前选中物体处理")
                # 对当前选中物体处理
                currentObjectList = self.selectedObjectList
                for obj in currentObjectList:
                    obj.select_set(True)
                self.objectCount = len(currentObjectList)
            elif self.data_source == "ALL":
                print("对所有物体处理")
                # 对所有物体处理
                currentObjectList = self.allObjectList
                for obj in currentObjectList:
                    obj.select_set(True)
                self.objectCount = len(currentObjectList)
            elif self.data_source == "SELECT CHILDREN":
                print("对当前选中物体及其子物体处理")
                # 对当前选中物体及其子物体处理
                currentObjectList = self.selectedObjectList
                # 去重
                newCurrentObjectList = list(
                    set(
                        CHAOS_OT_Replace_Repeated_Materials.SearchChildrenObject(
                            currentObjectList
                        )
                    )
                )

                for obj in newCurrentObjectList:
                    obj.select_set(True)
                self.objectCount = len(newCurrentObjectList)
                self.newSelectedObjectList = newCurrentObjectList
            self.isUpdateEnabled = True
        row.label(text=f"将会处理{self.objectCount}个物体")

    def execute(self, context: Context):
        dataSource = self.data_source
        print(f"处理{dataSource}")

        # selectedObjectList = bpy.context.selected_objects
        # allObjectList = bpy.data.objects

        # # 获取所有materials
        # materialList = []
        # materialList = bpy.data.materials

        if dataSource == "SELECT":
            # 对当前选中物体处理
            currentObjectList = bpy.context.selected_objects
        elif dataSource == "ALL":
            # 对所有物体处理
            currentObjectList = self.allObjectList
        if dataSource == "SELECT CHILDREN":
            # 对当前选中物体及其子物体处理
            currentObjectList = self.newSelectedObjectList

        # 定义正则表达式匹配模式
        pattern = re.compile(r"^(.+)\.\d{3}$")
        failList = []
        successList = []

        for objectItem in currentObjectList:
            if objectItem.type != "MESH":
                continue
            elif objectItem.type == "MESH" and objectItem.material_slots:
                # currentMaterialName = objectItem.material_slots
                currentMaterialSlotList = []
                for currentMaterialSlot in objectItem.material_slots:
                    if currentMaterialSlot and currentMaterialSlot.material:
                        currentMaterialSlotList.append(currentMaterialSlot)
                original_names = [
                    pattern.match(s.material.name).group(1)
                    if pattern.match(s.material.name)
                    else s.material.name
                    for s in currentMaterialSlotList
                ]
                for i in range(0, len(currentMaterialSlotList)):
                    if currentMaterialSlotList[i].material.name != original_names[i]:
                        if bpy.data.materials.get(original_names[i]):
                            # print(f"将材质 {objectItem.material_slots[i].material.name} 替换为 {original_names[i]}")
                            successList.append(currentMaterialSlotList[i].material.name)
                            objectItem.material_slots[
                                i
                            ].material = bpy.data.materials.get(original_names[i])
                            # successList.append(objectItem.material_slots[i].material)
                        else:
                            # failList.append(objectItem.material_slots[i].material)
                            failList.append(currentMaterialSlotList[i].material.name)

        self.report({"INFO"}, f"{len(successList)}个材质处理成功")
        # print(f"{len(successList)}个材质处理成功")
        # for item in successList:
        #     print(item)

        # print("--------------------------------------------------------")
        self.report({"INFO"}, f"{len(failList)}个材质处理失败，无法找到基材质")
        # print(f"{len(failList)}个材质处理失败，无法找到基材质")
        # for item in failList:
        #     print(item)

        return {"FINISHED"}

    # 在用户调用这个Operator时会自动触发invoke()方法
    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.selectedObjectList = bpy.context.selected_objects
        self.allObjectList = bpy.data.objects
        # 获取到当前场景的窗口管理器对象
        wm = context.window_manager
        # 使用当前的窗口管理器 (wm) 来显示确认对话框，并将操作符本身 (self) 以及触发操作的事件 (event) 传递给对话框
        return wm.invoke_props_dialog(self, width=400)


class CHAOS_OT_DeleteZeroAreaFace(Operator):
    """
    \n清理零面积的面
    """

    bl_idname = "chaos.select_zero_area_face"
    bl_label = "Zero Area Face"
    bl_description = "选中面积为0的面"
    bl_options = {"INTERNAL", "UNDO"}

    zeroFaceCount: IntProperty(
        name="Count of Zero Face",
        description="零面积面的数量",
        default=0,
    )

    def execute(self, context: Context):
        self.zeroFaceCount = 0
        selectedObjectList = bpy.context.selected_objects
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.reveal()
            bpy.ops.mesh.select_all(action="DESELECT")
        for obj in selectedObjectList:
            bm = bmesh.new()
            if bpy.ops.object.mode_set.poll() and obj.type == "MESH":
                bpy.ops.object.mode_set(mode="EDIT")
                # bpy.ops.mesh.select_mode(type="VERT")

                bm = bmesh.from_edit_mesh(obj.data)

                # 用于确保网格中的面(BMFace)有着正确的查找表(lookup table)
                bm.faces.ensure_lookup_table()

                bpy.ops.mesh.select_mode(type="FACE")
                for i in range(0, len(bm.faces)):
                    area = bm.faces[i].calc_area()
                    if area < 0.0001:
                        self.zeroFaceCount += 1
                        print(bm.faces[i].index)
                        bm.faces[i].select_set(True)

        bpy.context.scene["zeroFaceCount"] = self.zeroFaceCount

        # bpy.ops.mesh.select_all(action="SELECT")

        return {"FINISHED"}


class CHAOS_OT_DissloveZeroAreaFace(Operator):
    bl_idname = "chaos.disslove_zero_area_face"
    bl_label = "Disslove Zero Area Face"
    bl_description = "清理面积为0的面"
    bl_options = {"INTERNAL", "UNDO"}

    # @classmethod
    # def poll(cls, context):
    #     return True

    def execute(self, context):
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.dissolve_degenerate(threshold=0.0001)
            bpy.ops.chaos.select_zero_area_face()
            bpy.context.scene["zeroFaceCount"] = -1

        return {"FINISHED"}


class CHAOS_OT_Add_Triangulate(Operator):
    bl_idname = "chaos.add_triangulate"
    bl_label = "Add Triangulate"
    bl_description = "对大于四边面的模型执行三角化操作 建议保留修改器"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selectedObjects = bpy.context.selected_objects
        for obj in selectedObjects:
            if obj.type == "MESH":
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_add(type="TRIANGULATE")
                obj.modifiers["Triangulate"].min_vertices = 5
                # if bpy.context.space_data.shading.type != "WIREFRAME":
                #     bpy.ops.view3d.toggle_shading(type="WIREFRAME")

        return {"FINISHED"}


class CHAOS_OT_Get_Shape_Key(Operator):
    bl_idname = "chaos.get_shape_key"
    bl_label = "Get Shape Key"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = bpy.context.active_object
        list: bpy.type.shape_keys = obj.data.shape_keys

        return {"FINISHED"}


class CHAOS_OT_Select_Non_Manifold(bpy.types.Operator):
    bl_idname = "chaos.select_non_manifold"
    bl_label = "Select Non Manifold"
    bl_description = "选择模型上的非流形部分"
    bl_options = {"INTERNAL", "UNDO"}

    @classmethod
    def poll(cls, context):
        # if bpy.context.tool_settings.mesh_select_mode[2]:
        #     return True
        return True

    def execute(self, context):
        selectedObjectList = []
        for obj in bpy.context.selected_objects:
            if obj.type == "MESH":
                selectedObjectList.append(obj)

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action="DESELECT")

        for obj in selectedObjectList:
            obj.select_set(True)

        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(type="VERT")
            bpy.ops.mesh.select_non_manifold(
                extend=False,
                use_wire=True,
                use_boundary=True,
                use_multi_face=True,
                use_non_contiguous=True,
                use_verts=True,
            )
            # self.report({"INFO"}, f"当前没有选择物体")

        return {"FINISHED"}


# class MyClassName(bpy.types.Operator):
#     bl_idname = "my_operator.my_class_name"
#     bl_label = "My Class Name"
#     bl_description = "Description that shows in blender tooltips"
#     bl_options = {"REGISTER"}

#     @classmethod
#     def poll(cls, context):
#         return True

#     def invoke(self, context, event):
#         context.window_manager.modal_handler_add(self)
#         return {"RUNNING_MODAL"}

#     def modal(self, context, event):
#         if event.type == "LEFTMOUSE":
#             return {"FINISHED"}

#         if event.type in {"RIGHTMOUSE", "ESC"}:
#             return {"CANCELLED"}

#         return {"RUNNING_MODAL"}
        

 
