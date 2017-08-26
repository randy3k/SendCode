import sublime
import sublime_plugin
from .text_getter import TextGetter
from .text_sender import TextSender


class SendCodeCommand(sublime_plugin.TextCommand):

    def resolve(self, cmd):
        view = self.view
        extracted_variables = view.window().extract_variables()

        if len(view.sel()) == 1:
            row, _ = view.rowcol(view.sel()[0].begin())
            extracted_variables["line"] = str(row+1)

            word = view.substr(view.sel()[0])
            if not word:
                word = view.substr(view.word(view.sel()[0].begin()))

            extracted_variables["$selection"] = word

        cmd = sublime.expand_variables(cmd, extracted_variables)

        return cmd

    def run(self, edit, cmd=None, prog=None, confirmation=None):
        # set TextGetter before get_text() because get_text may change cursor locations.

        if confirmation:
            ok = sublime.ok_cancel_dialog(confirmation)
            if not ok:
                return

        sender = TextSender.initialize(self.view, prog=prog)
        if cmd:
            cmd = self.resolve(cmd)
        else:
            getter = TextGetter.initialize(self.view)
            cmd = getter.get_text()

        sublime.set_timeout_async(lambda: sender.send_text(cmd))


# historial reason
class SendReplCommand(SendCodeCommand):
    def run(self, *args, **kargs):
        # print("The `send_repl` command has been deprecated, please use `send_code` command.")
        super(SendReplCommand, self).run(*args, **kargs)


class SendCodeBuildCommand(sublime_plugin.WindowCommand):

    def run(self, cmd=None, prog=None):
        self.window.active_view().run_command(
            "send_code",
            {"cmd": cmd, "prog": prog}
        )
