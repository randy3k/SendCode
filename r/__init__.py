import sublime
import os
from ..applescript import osascript
from ..autohotkey import autohotkey
from ..clipboard import Clipboard

RAPPLESCRIPT = os.path.join(os.path.dirname(__file__), "r.applescript")
RAHK = os.path.join(os.path.dirname(__file__), "r.ahk")


plat = sublime.platform()

if plat == "osx":
    def send_to_r(cmd):
        osascript(RAPPLESCRIPT, cmd)
elif plat == "windows":
    def send_to_r(cmd, rgui=None):
        Clipboard.set_clipboard(cmd)
        if not rgui:
            rgui = "1"
        autohotkey(RAHK, rgui)
        Clipboard.reset_clipboard()
else:
    def send_to_r(cmd):
        pass
