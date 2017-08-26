import sublime
import sublime_plugin
import os
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


def replace_variable(cmd, var, value):
    cmd = cmd.replace("\"" + var + "\"", "\"" + escape_dquote(value) + "\"")
    cmd = cmd.replace("'" + var + "'", "'" + escape_squote(value) + "'")
    return cmd.replace(var, value)


class SendCodeCommand(sublime_plugin.TextCommand):

    def resolve(self, cmd):
        view = self.view
        file = view.file_name()
        if file:
            file_name = os.path.basename(file)
            file_path = os.path.dirname(file)
            file_base_name, file_ext = os.path.splitext(file_name)
            cmd = replace_variable(cmd, "$file_path", file_path)
            cmd = replace_variable(cmd, "$file_name", file_name)
            cmd = replace_variable(cmd, "$file_base_name", file_base_name)
            cmd = replace_variable(cmd, "$file_extension", file_ext)
            cmd = replace_variable(cmd, "$file", file)

        if len(view.sel()) == 1:
            row, _ = view.rowcol(view.sel()[0].begin())
            cmd = replace_variable(cmd, "$line", str(row+1))

        pd = view.window().project_data()
        if pd and "folders" in pd and len(pd["folders"]) > 0:
            project_path = pd["folders"][0].get("path")
            if project_path:
                cmd = replace_variable(cmd, "$project_path", project_path)

        # resolve $project_path again
        if file and file_path:
            cmd = replace_variable(cmd, "$project_path", file_path)

        if len(view.sel()) == 1:
            word = view.substr(view.sel()[0])
            if not word:
                word = view.substr(view.word(view.sel()[0].begin()))

            cmd = replace_variable(cmd, "$selection", word)

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
