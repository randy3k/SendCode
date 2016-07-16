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

    import win32gui
    import win32api
    import win32con
    import win32gui_struct

    def send_to_r(cmd):

        rid = win32gui.FindWindow("Rgui", None)
        if not rid:
            rid = win32gui.FindWindow("Rgui Workspace", None)

        if rid:
            clipboard.set_clipboard(cmd + "\n")
            mid = win32gui.GetMenu(rid)
            buf, extras = win32gui_struct.EmptyMENUITEMINFO()
            win32gui.GetMenuItemInfo(mid, 1, True, buf)
            eid = win32gui_struct.UnpackMENUITEMINFO(buf).hSubMenu
            buf, extras = win32gui_struct.EmptyMENUITEMINFO()
            win32gui.GetMenuItemInfo(eid, 1, True, buf)
            pid = win32gui_struct.UnpackMENUITEMINFO(buf).wID
            win32api.PostMessage(rid, win32con.WM_SETFOCUS, pid, 0)
            sublime.set_timeout(lambda: win32api.PostMessage(rid, win32con.WM_COMMAND, pid, 0), 50)
            clipboard.reset_clipboard()

else:
    def send_to_r(cmd):
        pass
