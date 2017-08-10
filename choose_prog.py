import sublime
import sublime_plugin
from .settings import Settings


class SendCodeChooseProgCommand(sublime_plugin.TextCommand):

    def show_quick_panel(self, options, done):
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(options, done), 10)

    def run(self, edit):
        plat = sublime.platform()
        settings = Settings(self.view)
        syntax = settings.syntax()
        if plat == 'osx':
            app_list = [
                "[Reset]", "Terminal", "iTerm", "tmux", "screen"]
            if syntax == "r" or syntax == "rmd" or syntax == "rnw":
                app_list = app_list + [
                    "R GUI", "RStudio Desktop", "Chrome-RStudio", "Safari-RStudio"]
            if syntax in ["r", "python", "julia"]:
                app_list = app_list + ["Chrome-Jupyter", "Safari-Jupyter"]

        elif plat == "windows":
            app_list = ["[Reset]", "Cmder", "ConEmu", "tmux", "screen"]
            if syntax == "r" or syntax == "rmd" or syntax == "rnw":
                app_list = app_list + ["R GUI", "RStudio Desktop"]
        elif plat == "linux":
            app_list = ["[Reset]", "tmux", "screen", "linux-terminal"]
            if syntax == "r" or syntax == "rmd" or syntax == "rnw":
                app_list = app_list + ["RStudio Desktop"]
        else:
            sublime.error_message("Platform not supported!")

        app_list += ["SublimeREPL", "TerminalView"]

        def on_done(action):
            if action == -1:
                return
            elif action > 0:
                result = app_list[action]
                result = "R" if result == "R GUI" else result
                result = "RStudio" if result == "RStudio Desktop" else result
                result = result.lower()
                settings.set("prog", result)
            elif action == 0:
                settings.erase("prog")

        self.show_quick_panel(app_list, on_done)
