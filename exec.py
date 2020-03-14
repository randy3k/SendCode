import sublime_plugin


class SendCodeExecCommand(sublime_plugin.WindowCommand):

    def run(self, code=None, prog=None):
        self.window.active_view().run_command(
            "send_code",
            {"code": code, "prog": prog}
        )


# backward compatibility
class SendCodeBuildCommand(SendCodeExecCommand):
    pass
