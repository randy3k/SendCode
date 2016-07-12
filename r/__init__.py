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
    from ..autohotkey import autohotkey

    RAHK = os.path.join(os.path.dirname(__file__), "r.ahk")

    def send_to_r(cmd, rgui=None):
        clipboard.set_clipboard(cmd)
        if not rgui:
            rgui = "1"
        autohotkey(RAHK, rgui)
        clipboard.reset_clipboard()
else:
    def send_to_r(cmd):
        pass
