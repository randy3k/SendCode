import sublime
import sublime_plugin
import re

from .text_getter import TextGetter
from .text_sender import TextSender


def escape_dquote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace('"', '\\"')
    return cmd


def escape_squote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace("\'", "\'")
    return cmd


PATTERN = re.compile(r"""
    (?P<quote>["'])
    (?P<quoted_var>
        \$ (?: [_a-z][_a-z0-9]*  | \{[^}]*\} )
    )
    (?P=quote)
    |
    (?P<var>
        \$ (?: [_a-z][_a-z0-9]*  | \{[^}]*\} )
    )
""", re.VERBOSE)


class SendCodeCommand(sublime_plugin.TextCommand):

    def resolve(self, cmd):
        view = self.view
        window = view.window()
        extracted_variables = window.extract_variables()
        if len(view.sel()) == 1:
            row, _ = view.rowcol(view.sel()[0].begin())
            extracted_variables["line"] = str(row + 1)

            word = view.substr(view.sel()[0])
            if not word:
                word = view.substr(view.word(view.sel()[0].begin()))
            extracted_variables["selection"] = word

        def convert(m):
            quote = m.group("quote")
            if quote:
                var = sublime.expand_variables(m.group("quoted_var"), extracted_variables)
                if quote == "'":
                    return "'" + escape_squote(var) + "'"
                else:
                    return '"' + escape_dquote(var) + '"'
            else:
                return sublime.expand_variables(m.group("var"), extracted_variables)

        cmd = PATTERN.sub(convert, cmd)

        return cmd

    def run(self, edit, cmd=None, prog=None, confirmation=None):
        # set TextGetter before get_text() because get_text may change cursor locations.

        if confirmation:
            ok = sublime.ok_cancel_dialog(confirmation)
            if not ok:
                return

        sender = TextSender.initialize(self.view, prog=prog, from_view=cmd is None)
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
