import sublime
import sublime_plugin
from .settings import Settings


class SendCodeChooseProgCommand(sublime_plugin.TextCommand):

    def show_quick_panel(self, options, done, **kwargs):
        sublime.set_timeout(
            lambda: self.view.window().show_quick_panel(options, done, **kwargs), 10)

    def normalize(self, prog):
        prog = "R" if prog == "R GUI" else prog
        prog = "RStudio" if prog == "RStudio Desktop" else prog
        prog = prog.lower()
        return prog

    def run(self, edit):
        plat = sublime.platform()
        settings = Settings(self.view)
        syntax = settings.syntax()
        if plat == 'osx':
            app_list = [
                "Terminal", "iTerm", "tmux", "screen"]
            if syntax == "r" or syntax == "rmd" or syntax == "rnw":
                app_list = app_list + [
                    "R GUI", "RStudio Desktop", "Chrome-RStudio", "Safari-RStudio"]
            if syntax in ["r", "python", "julia"]:
                app_list = app_list + ["Chrome-Jupyter", "Safari-Jupyter"]

        elif plat == "windows":
            app_list = ["Cmder", "ConEmu", "tmux", "screen"]
            if syntax == "r" or syntax == "rmd" or syntax == "rnw":
                app_list = app_list + ["R GUI", "RStudio Desktop"]
        elif plat == "linux":
            app_list = ["tmux", "screen", "linux-terminal"]
            if syntax == "r" or syntax == "rmd" or syntax == "rnw":
                app_list = app_list + ["RStudio Desktop"]
        else:
            sublime.error_message("Platform not supported!")

        app_list += ["SublimelyTerminal", "SublimeREPL", "TerminalView"]

        def on_done(action):
            if action == -1:
                return
            else:
                result = app_list[action]
                settings.set("prog", self.normalize(result))

        prog = settings.get("prog")
        try:
            selected_index = [self.normalize(p) for p in app_list].index(prog)
        except:
            selected_index = 0

        self.show_quick_panel(app_list, on_done, selected_index=selected_index)
