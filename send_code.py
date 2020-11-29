import sublime
import sublime_plugin

from .code_getter import CodeGetter
from .code_sender import CodeSender


class SendCodeCommand(sublime_plugin.TextCommand):

    def run(self, edit, code=None, cmd=None, prog=None, resolve=True, confirmation=None):
        # set CodeSender before get_code() because get_code may change cursor locations.

        if confirmation:
            ok = sublime.ok_cancel_dialog(confirmation)
            if not ok:
                return

        if not code and cmd:
            print("SendCode: argument `cmd` is deprecated, use `code` instead.")
            code = cmd

        getter = CodeGetter.initialize(self.view)
        sender = CodeSender.initialize(self.view, prog=prog, from_view=code is None)
        if code and resolve:
            code = getter.resolve(code)
        else:
            code = getter.get_code()
        
        if code:
            sublime.set_timeout_async(lambda: sender.send_text(code))
