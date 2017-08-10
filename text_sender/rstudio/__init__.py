import sublime
import os
from ..clipboard import clipboard

plat = sublime.platform()

if plat == "osx":
    from ..applescript import osascript

    RSTUDIOAPPLESCRIPT = os.path.join(os.path.dirname(__file__), "rstudio.applescript")

    def send_to_rstudio(cmd):
        osascript(RSTUDIOAPPLESCRIPT, cmd)

elif plat == "windows":
    from .. import winauto

    def send_to_rstudio(cmd):
        rid = winauto.find_rstudio()
        clipboard.set_clipboard(cmd)
        winauto.paste_to_rstudio(rid)
        clipboard.reset_clipboard()

elif plat == "linux":
    from xdotool import xdotool

    def send_to_rstudio(cmd):
        wid = xdotool("search", "--onlyvisible", "--class", "rstudio")
        if wid:
            wid = wid.decode("utf-8").strip().split("\n")[-1]
            clipboard.set_clipboard(cmd)
            xdotool("key", "--window", wid, "ctrl+v")
            xdotool("key", "--window", wid, "--clearmodifiers", "Return")
            clipboard.reset_clipboard()
