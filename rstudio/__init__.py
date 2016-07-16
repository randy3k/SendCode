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
    import win32gui
    import win32api
    import win32con
    import win32clipboard

    def send_to_rstudio(cmd):
        rid = win32gui.FindWindow("Qt5QWindowIcon", "RStudio")
        # TODO: reset clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(cmd)
        win32clipboard.CloseClipboard()
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        win32api.PostMessage(rid, win32con.WM_KEYDOWN, ord("V"), 0)

        def do_enter():
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.PostMessage(rid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)

        if rid:
            sublime.set_timeout(do_enter, 1)


elif plat == "linux":
    from xdotool import xdotool

    def send_to_rstudio(cmd):
        wid = xdotool("search", "--onlyvisible", "--class", "rstudio")
        if wid:
            wid = wid.decode("utf-8").strip().split("\n")[-1]
            clipboard.set_clipboard(cmd)
            xdotool("key", "--window", wid, "--clearmodifiers", "ctrl+v")
            xdotool("key", "--window", wid, "--clearmodifiers", "Return")
            clipboard.reset_clipboard()
