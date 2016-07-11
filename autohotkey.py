import os
import subprocess


def execute_autohotkey_script(script_path, *args):
    ahk_path = os.path.join(os.path.dirname(__file__), os.sep, 'autohotkey', 'AutoHotkeyU32.exe')
    subprocess.check_call([ahk_path, script_path] + list(args))
