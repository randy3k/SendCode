import sublime
import time
import os
from ..clipboard import clipboard
from subprocess import CalledProcessError

plat = sublime.platform()

if plat == "linux":
    from ..xdotool import xdotool

    def send_to_linux_terminal(wids, cmd_list):
        wid = wids.decode("utf-8").strip().split("\n")[-1]

        if isinstance(cmd_list, str):
            cmd_list = [cmd_list]

        sublime_id = xdotool("getactivewindow")

        if os.environ.get("XDG_SESSION_DESKTOP") == "KDE":
            xdotool("windowactivate", wid)
            time.sleep(0.05)
        else:
            xdotool("windowfocus", wid)

        for cmd in cmd_list:
            clipboard.set_clipboard(cmd)

            if cmd:
                xdotool("key", "ctrl+shift+v")
                time.sleep(0.1)
            xdotool("key", "Return")
            time.sleep(0.1)

            clipboard.reset_clipboard()

        if os.environ.get("XDG_SESSION_DESKTOP") == "KDE":
            xdotool("windowactivate", sublime_id)
        else:
            xdotool("windowfocus", sublime_id)

    def get_linux_wids(window_name, linux_terminal):
        try:
            wids = xdotool("search", "--onlyvisible", "--name", window_name)
            return wids
        except CalledProcessError:
            sublime.status_message("{} (WM_NAME) not found; trying {} (WM_CLASS)"
                                   .format(window_name, linux_terminal))
        except TypeError:
            # We get here if window_name is None, meaning we should just look at WM_CLASS
            pass

        wids = xdotool("search", "--onlyvisible", "--class", linux_terminal)

        if not wids:
            raise Exception("{} not found.".format(linux_terminal))

        return wids

else:
    def send_to_linux_terminal(cmd):
        pass

    def get_linux_wids(cmd):
        pass
