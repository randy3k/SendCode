import sublime
import sublime_plugin


class SendReplChooseProgramCommand(sublime_plugin.WindowCommand):

    def show_quick_panel(self, options, done):
        sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)

    def run(self):
        plat = sublime.platform()
        if plat == 'osx':
            self.app_list = ["[Reset]", "Terminal", "iTerm",
                             "R", "RStudio", "Chrome-RStudio", "Chrome-Jupyter",
                             "Safari-RStudio", "Safari-Jupyter",
                             "tmux"]
        elif plat == "windows":
            self.app_list = ["[Reset]", "Cmder", "ConEmu",
                             "R", "RStudio"]
        elif plat == "linux":
            self.app_list = ["[Reset]", "tmux", "screen", "RStudio"]
        else:
            sublime.error_message("Platform not supported!")

        self.show_quick_panel(self.app_list, self.on_done)

    def on_done(self, action):
        if action == -1:
            return
        settings = sublime.load_settings('SendREPL.sublime-settings')
        settings.set("prog", self.app_list[action].lower() if action > 0 else None)
        sublime.save_settings('SendREPL.sublime-settings')
