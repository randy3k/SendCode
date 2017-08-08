import sublime
import os
from ..clipboard import clipboard

plat = sublime.platform()

if plat == "osx":
    from ..applescript import osascript

    RAPPLESCRIPT = os.path.join(os.path.dirname(__file__), "r.applescript")

    def send_to_r(cmd):
        osascript(RAPPLESCRIPT, cmd)
elif plat == "windows":

    from .. import winauto

    def send_to_r(cmd):
        rid = winauto.find_rgui()
        winauto.bring_rgui_to_top(rid)

        clipboard.set_clipboard(cmd + "\n")
        winauto.paste_to_rgui(rid)
        clipboard.reset_clipboard()

else:
    def send_to_r(cmd):
        pass
