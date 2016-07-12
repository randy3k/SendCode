import os
import subprocess


def autohotkey(*args):
    ahk_path = os.path.join(os.path.dirname(__file__), 'AutoHotkeyU32.exe')
    subprocess.check_call([ahk_path] + list(args))
