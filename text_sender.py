import sublime
import re
from .settings import Settings
from .terminal import send_to_terminal
from .iterm import send_to_iterm
from .r import send_to_r
from .rstudio import send_to_rstudio
from .conemuc import send_to_conemu
from .tmux import send_to_tmux


class TextSender:

    def __init__(self, view, cmd=None, prog=None):
        self.view = view
        self.settings = Settings(view)
        if prog:
            self.prog = prog
        else:
            self.prog = self.settings.get("prog")
        self.bracketed_paste_mode = self.settings.get("bracketed_paste_mode")

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

    def send_to_conemu(self, cmd):
        send_to_conemu(cmd.rstrip())

    def send_to_tmux(self, cmd):
        tmux = self.settings.get("tmux", "tmux")
        send_to_tmux(cmd.rstrip(), tmux)

    def send_text(self, cmd):
        prog = self.prog
        if prog.lower() == "terminal":
            self.send_to_terminal(cmd)
        elif prog.lower() == "iterm":
            self.send_to_iterm(cmd)
        elif prog.lower() == "cmder" or prog.lower() == "conemu":
            self.send_to_conemu(cmd)
        elif prog.lower() == "tmux":
            self.send_to_tmux(cmd)
        else:
            sublime.message_dialog("%s is not supported for current syntax." % prog)


class RTextSender(TextSender):

    def send_text(self, cmd):
        prog = self.prog
        if prog.lower() == "r":
            self.send_to_r(cmd)
        elif prog.lower() == "r64":
            self.send_to_r(cmd, "x64")
        elif prog.lower() == "r32":
            self.send_to_r(cmd, "i386")
        elif prog.lower() == "rstudio":
            self.send_to_rstudio(cmd)
        else:
            super(RTextSender, self).send_text(cmd)

    if sublime.platform() == "osx":
        def send_to_r(self, cmd):
            send_to_r(cmd)
    elif sublime.platform() == "windows":
        def send_to_r(self, cmd, rgui):
            rgui = self.settings.get("rgui", rgui)
            send_to_r(cmd, rgui)
    else:
        def send_to_r(self, cmd):
            pass

    def send_to_rstudio(self, cmd):
        send_to_rstudio(cmd.rstrip())


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

    def send_to_conemu(self, cmd):
        cmd = cmd.rstrip()
        if len(re.findall("\n", cmd)) > 0:
            send_to_conemu(r"%cpaste -q")
            send_to_conemu(cmd.rstrip())
            send_to_conemu("--")
        else:
            send_to_conemu(cmd)

    def send_to_tmux(self, cmd):
        tmux = self.settings.get("tmux", "tmux")
        cmd = cmd.rstrip()
        if len(re.findall("\n", cmd)) > 0:
            send_to_tmux(r"%cpaste -q", tmux)
            send_to_tmux(cmd.rstrip(), tmux)
            # send ctrl-D instead of "--" since `set-buffer` does not work properly
            send_to_tmux("\x04", tmux)
        else:
            send_to_tmux(cmd, tmux)


class JuliaTextSender(TextSender):
    pass
