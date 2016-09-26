import sublime
import sublime_plugin
from .settings import Settings


class SendReplChooseProgramCommand(sublime_plugin.TextCommand):

    def show_quick_panel(self, options, done):
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(options, done), 10)

    def run(self, edit):
        plat = sublime.platform()
        syntax = Settings(self.view).syntax()
        if plat == 'osx':
            app_list = [
                "[Reset]", "Terminal", "iTerm", "tmux", "screen"]
            if syntax == "r":
                app_list = app_list + ["R", "RStudio", "Chrome-RStudio", "Safari-RStudio"]
            if syntax in ["r", "python", "julia"]:
                app_list = app_list + ["Chrome-Jupyter", "Safari-Jupyter"]

        elif plat == "windows":
            app_list = ["[Reset]", "Cmder", "ConEmu", "tmux", "screen"]
            if syntax == "r":
                app_list = app_list + ["R", "RStudio"]
        elif plat == "linux":
            app_list = ["[Reset]", "tmux", "screen"]
            if syntax == "r":
                app_list = app_list + ["RStudio"]
        else:
            sublime.error_message("Platform not supported!")

        app_list.append("SublimeREPL")

        def on_done(action):
            if action == -1:
                return
            s = sublime.load_settings('SendREPL.sublime-settings')
            if action > 0:
                s.set("prog", app_list[action].lower())
            elif action == 0:
                s.erase("prog")
            sublime.save_settings('SendREPL.sublime-settings')

        self.show_quick_panel(app_list, on_done)
