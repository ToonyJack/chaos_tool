import bpy
from .. import general
from bpy.app.translations import pgettext_tip as tip_
from ..ui import ViewChaosPanel
from bpy.types import Panel

class VIEW3D_PT_chaos_help(ViewChaosPanel, Panel):
    bl_label = "Help"
    bl_description = "帮助"

    def draw(self, context):
        prefs = context.preferences
        view = prefs.view

        layout = self.layout
        col = layout.column()
        col.label(text="Version: " + general.get_addon_version())

        row = col.row(align=True)
        row.operator("help_operators.help_url", text="Tutorials", icon="URL")
        row.operator("help_operators.op_language", text=tip_("Language"), icon="FILE_TEXT")

        col.operator("help_operators.feedback_url", text=tip_("Feedback"), icon="ERROR")