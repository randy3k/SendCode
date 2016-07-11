import sublime
import re
from .settings import Settings
from .terminal import send_to_terminal
from .iterm import send_to_iterm


class TextSender:

    def __init__(self, view, cmd=None, prog=None):
        self.view = view
        settings = Settings(view)
        if prog:
            self.prog = prog
        else:
            self.prog = settings.get("prog")
        self.bracketed_paste_mode = settings.get("bracketed_paste_mode")

    @classmethod
    def initialize(cls, view, **kwargs):
        syntax = Settings(view).syntax()
        if syntax == "r":
            return RTextSender(view, **kwargs)
        elif syntax == "python":
            return PythonTextSender(view, **kwargs)
        elif syntax == "julia":
            return JuliaTextSender(view, **kwargs)
        else:
            return TextSender(view, **kwargs)

    def send_to_terminal(self, cmd):
        send_to_terminal(cmd.rstrip(), self.bracketed_paste_mode)

    def send_to_iterm(self, cmd):
        send_to_iterm(cmd.rstrip(), self.bracketed_paste_mode)

    def send_text(self, cmd):
        prog = self.prog
        if prog.lower() == "terminal":
            self.send_to_terminal(cmd)
        elif prog.lower() == "iterm":
            self.send_to_iterm(cmd)
        else:
            sublime.message_dialog("%s not supported." % prog)


class RTextSender(TextSender):
    pass


class PythonTextSender(TextSender):

    def send_to_terminal(self, cmd):
        cmd = cmd.rstrip()
        if len(re.findall("\n", cmd)) > 0:
            send_to_terminal(r"%cpaste -q")
            send_to_terminal(cmd)
            send_to_terminal("--")
        else:
            send_to_terminal(cmd)

    def send_to_iterm(self, cmd):
        cmd = cmd.rstrip()
        if len(re.findall("\n", cmd)) > 0:
            send_to_iterm(r"%cpaste -q")
            send_to_iterm(cmd)
            send_to_iterm("--")
        else:
            send_to_iterm(cmd)


class JuliaTextSender(TextSender):
    pass
