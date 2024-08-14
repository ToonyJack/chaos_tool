import bpy
import addon_utils


def get_addon_version():
    for addon in addon_utils.modules():
        if addon.bl_info["name"] == "Chaos Toolbox":
            ver = addon.bl_info["version"]
            addon_version = "%i.%i.%i" % (ver[0], ver[1], ver[2])
            break

    return addon_version if addon_version else "0.0.0"


class Labels:
    """Labels and text blocks"""

    ADDON_NAME_LABEL = "Chaos Toolbox"
    ADDON_NAME = "chaos_tool"
    ADDON_ICO = "PLUGIN"


_data = []


def update(*args):
    _data[:] = args


def info():
    return tuple(_data)


if __name__ == "__main__":
    pass
