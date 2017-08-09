import sublime
import time
from ..clipboard import clipboard

plat = sublime.platform()

if plat == "linux":
    from xdotool import xdotool

    def send_to_gnome_terminal(cmd_list):
        wid = xdotool("search", "--onlyvisible", "--class", "gnome-terminal")
        if not wid:
            raise Exception("gnome-terminal not found.")

        wid = wid.decode("utf-8").strip().split("\n")[-1]

        if isinstance(cmd_list, str):
            cmd_list = [cmd_list]

        sublime_id = xdotool("getactivewindow")

        xdotool("windowfocus", wid)

        for cmd in cmd_list:
            clipboard.set_clipboard(cmd)

            if cmd:
                xdotool("key", "--clearmodifiers", "ctrl+shift+v")
                time.sleep(0.1)
            xdotool("key", "--clearmodifiers", "Return")
            time.sleep(0.1)

            clipboard.reset_clipboard()

        xdotool("windowfocus", sublime_id)


else:
    def send_to_gnome_terminal(cmd):
        pass
