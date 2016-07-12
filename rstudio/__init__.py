import sublime
import os
from ..applescript import osascript
from ..autohotkey import autohotkey
from ..xdotool import xdotool
from ..clipboard import Clipboard

RSTUDIOAPPLESCRIPT = os.path.join(os.path.dirname(__file__), "rstudio.applescript")
RSTUDIOAHK = os.path.join(os.path.dirname(__file__), "rstudio.ahk")


plat = sublime.platform()

if plat == "osx":
    def send_to_rstudio(cmd):
        osascript(RSTUDIOAPPLESCRIPT, cmd)

elif plat == "windows":
    def send_to_rstudio(cmd):
        Clipboard.set_clipboard(cmd)
        autohotkey(RSTUDIOAHK)
        Clipboard.reset_clipboard()

elif plat == "linux":
    def send_to_rstudio(cmd, xdotool_path=None):
        wid = xdotool("search", "--onlyvisible", "--class", "rstudio", path=xdotool_path)
        if wid:
            wid = wid.decode("utf-8").strip().split("\n")[-1]
            Clipboard.set_clipboard(cmd)
            xdotool("key", "--window", wid, "--clearmodifiers", "ctrl+v", path=xdotool_path)
            xdotool("key", "--window", wid, "--clearmodifiers", "Return", path=xdotool_path)
            Clipboard.reset_clipboard()
