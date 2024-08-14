from typing import Set
import bpy

from bpy.types import Context, Event


def main(context):
    for ob in context.scene.objects:
        print(ob)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    # idname为代码中调用这个操作符所使用的名字
    bl_idname = "object.simple_operator"
    # label是在Blender中显示的名字
    bl_label = "Simple Object Operator"

    # @classmethod 是 Python 中的装饰器，用于定义一个类方法，绑定到类而不是实例，可以直接通过类名调用
    @classmethod
    # 检测作用域，防止在错误的地方执行函数导致报错
    def poll(cls, context):
        return context.active_object is not None
    
    # 在用户调用这个Operator时会自动触发invoke()方法
    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        # 获取到当前场景的窗口管理器对象
        wm = context.window_manager
        # 使用当前的窗口管理器 (wm) 来显示确认对话框，并将操作符本身 (self) 以及触发操作的事件 (event) 传递给对话框
        return wm.invoke_confirm(self, event)

    # Operator具体执行的代码部分
    def execute(self, context):
        main(context)
        # 返回值有'FINISHED'、'CANCELLED'、'RUNNING_MODAL'、'PASS_THROUGH'，这些状态用于告知 Blender 执行操作的结果
        return {'FINISHED'}

# 注册自定义类
def register():
    bpy.utils.register_class(SimpleOperator)

# 注销自定义类
def unregister():
    bpy.utils.unregister_class(SimpleOperator)

# 如果作为主函数加载，则继续下面的一系列操作
if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()