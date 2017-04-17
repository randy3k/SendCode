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
    import win32gui_struct
    import win32api
    import win32con

    def send_to_r(cmd):

        rid = win32gui.FindWindow("Rgui", None)
        if not rid:
            rid = win32gui.FindWindow("Rgui Workspace", None)

        if rid:
            clipboard.set_clipboard(cmd + "\n")

            menuitems = win32gui.GetMenu(rid)
            buf, extras = win32gui_struct.EmptyMENUITEMINFO()
            win32gui.GetMenuItemInfo(menuitems, 0, True, buf)

            if win32gui_struct.UnpackMENUITEMINFO(buf).text == "":
                editid = 2
            else:
                editid = 1
            buf, extras = win32gui_struct.EmptyMENUITEMINFO()
            win32gui.GetMenuItemInfo(menuitems, editid, True, buf)
            editmenu = win32gui_struct.UnpackMENUITEMINFO(buf).hSubMenu

            buf, extras = win32gui_struct.EmptyMENUITEMINFO()
            win32gui.GetMenuItemInfo(editmenu, 1, True, buf)
            pasteid = win32gui_struct.UnpackMENUITEMINFO(buf).wID
            win32api.PostMessage(rid, win32con.WM_SETFOCUS, pasteid, 0)

            sublime.set_timeout(lambda: win32api.PostMessage(rid, win32con.WM_COMMAND, pasteid, 0), 50)
            clipboard.reset_clipboard()

else:
    def send_to_r(cmd):
        pass
