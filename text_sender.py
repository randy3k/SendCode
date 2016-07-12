import sublime
import re
from .settings import Settings
from .terminal import send_to_terminal
from .iterm import send_to_iterm
from .r import send_to_r
from .rstudio import send_to_rstudio
from .conemu import send_to_conemu
from .tmux import send_to_tmux
from .screen import send_to_screen
from .chrome import send_to_chrome_jupyter, send_to_chrome_rstudio
from .safari import send_to_safari_jupyter, send_to_safari_rstudio


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
        send_to_terminal(cmd, self.bracketed_paste_mode)

    def send_to_iterm(self, cmd):
        send_to_iterm(cmd, self.bracketed_paste_mode)

    def send_to_conemu(self, cmd):
        conemuc_path = self.settings.get("conemu", None)
        send_to_conemu(cmd, conemuc_path)

    def send_to_tmux(self, cmd):
        tmux = self.settings.get("tmux", "tmux")
        send_to_tmux(cmd, tmux, self.bracketed_paste_mode)

    def send_to_screen(self, cmd):
        screen = self.settings.get("screen", "screen")
        send_to_screen(cmd, screen, self.bracketed_paste_mode)

    def send_to_chrome_jupyter(self, cmd):
        send_to_chrome_jupyter(cmd)

    def send_to_safari_jupyter(self, cmd):
        send_to_safari_jupyter(cmd)

    def send_text(self, cmd):
        cmd = cmd.rstrip()
        prog = self.prog.lower()
        if prog == "terminal":
            self.send_to_terminal(cmd)
        elif prog == "iterm":
            self.send_to_iterm(cmd)
        elif prog == "cmder" or prog == "conemu":
            self.send_to_conemu(cmd)
        elif prog == "tmux":
            self.send_to_tmux(cmd)
        elif prog == "screen":
            self.send_to_screen(cmd)
        elif prog == "chrome-jupyter":
            self.send_to_chrome_jupyter(cmd)
        elif prog == "safari-jupyter":
            self.send_to_safari_jupyter(cmd)
        else:
            sublime.message_dialog("%s is not supported for current syntax." % prog)


class RTextSender(TextSender):

    def send_text(self, cmd):
        cmd = cmd.rstrip()
        prog = self.prog.lower()
        if prog == "r":
            self.send_to_r(cmd)
        elif prog == "r64":
            self.send_to_r(cmd, "x64")
        elif prog == "r32":
            self.send_to_r(cmd, "i386")
        elif prog == "rstudio":
            self.send_to_rstudio(cmd)
        elif prog == "chrome-rstudio":
            self.send_to_chrome_rstudio(cmd)
        elif prog == "safari-rstudio":
            self.send_to_safari_rstudio(cmd)
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

    if sublime.platform() == "linux":
        def send_to_rstudio(self, cmd):
            xdotool_path = self.settings.get("xdotool", None)
            send_to_rstudio(cmd, xdotool_path)
    else:
        def send_to_rstudio(self, cmd):
            send_to_rstudio(cmd)

    def send_to_chrome_rstudio(self, cmd):
        send_to_chrome_rstudio(cmd)

    def send_to_safari_rstudio(self, cmd):
        send_to_safari_rstudio(cmd)


class PythonTextSender(TextSender):

    def send_to_terminal(self, cmd):
        if len(re.findall("\n", cmd)) > 0:
            send_to_terminal(r"%cpaste -q")
            send_to_terminal(cmd)
            send_to_terminal("--")
        else:
            send_to_terminal(cmd)

    def send_to_iterm(self, cmd):
        if len(re.findall("\n", cmd)) > 0:
            send_to_iterm(r"%cpaste -q")
            send_to_iterm(cmd)
            send_to_iterm("--")
        else:
            send_to_iterm(cmd)

    def send_to_conemu(self, cmd):
        if len(re.findall("\n", cmd)) > 0:
            send_to_conemu(r"%cpaste -q")
            send_to_conemu(cmd)
            send_to_conemu("--")
        else:
            send_to_conemu(cmd)

    def send_to_tmux(self, cmd):
        tmux = self.settings.get("tmux", "tmux")
        if len(re.findall("\n", cmd)) > 0:
            send_to_tmux(r"%cpaste -q", tmux)
            send_to_tmux(cmd, tmux)
            # send ctrl-D instead of "--" since `set-buffer` does not work properly
            send_to_tmux("\x04", tmux)
        else:
            send_to_tmux(cmd, tmux)

    def send_to_screen(self, cmd):
        if len(re.findall("\n", cmd)) > 0:
            send_to_screen(r"%cpaste -q")
            send_to_screen(cmd)
            send_to_screen("--")
        else:
            send_to_screen(cmd)


class JuliaTextSender(TextSender):
    pass
