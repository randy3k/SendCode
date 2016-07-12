import sublime
import subprocess
import os


XDOTOOL = os.path.join(os.path.dirname(__file__), sublime.arch(), "xdotool")


def xdotool(*args, path=None):
    if not path:
        path = XDOTOOL
    return subprocess.check_output([path] + list(args))
