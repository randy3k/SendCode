import sublime
import threading


class Clipboard:
    thread = None

    def set_clipboard(self, cmd):
        if not self.thread:
            self.cb = sublime.get_clipboard()
        else:
            self.thread.cancel()
            self.thread = None
        sublime.set_clipboard(cmd)

    def reset_clipboard(self):
        def _reset_clipboard():
            if self.cb is not None:
                sublime.set_clipboard(self.cb)
            self.cb = None
            self.thread = None
        self.thread = threading.Timer(0.5, _reset_clipboard)
        self.thread.start()

if 'clipboard' not in globals():
    clipboard = Clipboard()
