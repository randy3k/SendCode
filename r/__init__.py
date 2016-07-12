import sublime
import os
from ..applescript import execute_applescript
from ..autohotkey import execute_autohotkey_script
from ..clipboard import Clipboard

RAPPLESCRIPT = os.path.join(os.path.dirname(__file__), "r.applescript")
RAHK = os.path.join(os.path.dirname(__file__), "r.ahk")


plat = sublime.platform()

if plat == "osx":
    def send_to_r(cmd):
        execute_applescript(RAPPLESCRIPT, cmd)
elif plat == "windows":
    def send_to_r(cmd, rgui=None):
        Clipboard.set_clipboard(cmd)
        if not rgui:
            rgui = "1"
        execute_autohotkey_script(RAHK, rgui)
        Clipboard.reset_clipboard()
