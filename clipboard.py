import sublime
import threading


class Clipboard:
    @classmethod
    def set_clipboard(cls, cmd):
        if not cls.thread:
            cls.cb = sublime.get_clipboard()
        else:
            cls.thread.cancel()
            cls.thread = None
        sublime.set_clipboard(cmd)

    @classmethod
    def reset_clipboard(cls):
        def _reset_clipboard():
            if cls.cb is not None:
                sublime.set_clipboard(cls.cb)
            cls.cb = None
            cls.thread = None
        cls.thread = threading.Timer(0.5, _reset_clipboard)
        cls.thread.start()
