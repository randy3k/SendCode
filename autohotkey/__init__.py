import os
import subprocess


def autohotkey(script_path, *args):
    ahk_path = os.path.join(os.path.dirname(__file__), 'AutoHotkeyU32.exe')
    subprocess.check_call([ahk_path, script_path] + list(args))
