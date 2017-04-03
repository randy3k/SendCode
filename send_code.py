import sublime
import os
from .src.choose_repl import SendCodeChooseReplCommand
from .src.send_repl import SendReplCommand, SendReplBuild


__all__ = [
    "SendCodeChooseReplCommand",
    "SendReplCommand",
    "SendReplBuild"
]


def plugin_loaded():

    old_file = os.path.join(sublime.packages_path(), 'User', 'SendREPL.sublime-settings')
    new_file = os.path.join(sublime.packages_path(), 'User', 'SendCode.sublime-settings')

    if not os.path.exists(new_file) and os.path.exists(old_file):
        os.rename(old_file, new_file)
