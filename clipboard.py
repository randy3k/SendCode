import sublime
import threading

plat = sublime.platform()

if plat == "windows":
    import win32clipboard


def get_clipboard():
    if plat == "windows":
        win32clipboard.OpenClipboard()
        cb = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
    else:
        cb = sublime.get_clipboard()
    return cb


def set_clipboard(cmd):
    if plat == "windows":
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(cmd)
        win32clipboard.CloseClipboard()
    else:
        sublime.set_clipboard(cmd)


class Clipboard:
    thread = None

    def set_clipboard(self, cmd):
        if not self.thread:
            self.cb = get_clipboard()
        else:
            self.thread.cancel()
            self.thread = None

        set_clipboard(cmd)

    def reset_clipboard(self):
        def _reset_clipboard():
            if self.cb is not None:
                set_clipboard(self.cb)
            self.cb = None
            self.thread = None
        self.thread = threading.Timer(0.5, _reset_clipboard)
        self.thread.start()

if 'clipboard' not in globals():
    clipboard = Clipboard()
