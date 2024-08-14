import bpy,webbrowser
from bpy.types import Operator

class CHAOS_OT_Language(Operator):
    bl_label = "Language"
    bl_idname = "help_operators.op_language"
    bl_description = "界面语言切换:中(CN)/英文(EN)"

    def execute(self, context):
        prefs = bpy.context.preferences
        prefs.use_preferences_save = False
        prefs.view.use_translate_interface = True
        if prefs.view.language == "en_US":
            prefs.view.language = "zh_HANS"
            prefs.view.use_translate_new_dataname = 0
        else:
            prefs.view.language = "en_US"
        return {"FINISHED"}

class CHAOS_OT_Help_URL(Operator):
    """帮助文档"""

    bl_idname = "help_operators.help_url"
    bl_label = "Help"
    bl_description = "在网页浏览器中打开网站"

    def execute(self, context):
        # help
        
        return webbrowser.open("https://chaos-docs.booming-inc.com/docs/other_tools/plugins/blender_chaos_toolox")


class CHAOS_OT_Feedback_URL(Operator):
    """错误反馈"""

    bl_idname = "help_operators.feedback_url"
    bl_label = "Bug Feedback"
    bl_description = "在网页浏览器中打开工具反馈页面"

    def execute(self, context):
        # feedback
        webbrowser.open("https://boomingtech.feishu.cn/share/base/form/shrcnu3d4z5Lrw0mjHXbakzAnob")