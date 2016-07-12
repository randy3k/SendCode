import os
from ..applescript import execute_applescript
from ..autohotkey import execute_autohotkey_script
from ..clipboard import Clipboard

RAPPLESCRIPT = os.path.join(os.path.dirname(__file__), "r.applescript")
RAHK = os.path.join(os.path.dirname(__file__), "r.ahk")


def send_to_r(cmd):
    execute_applescript(RAPPLESCRIPT, cmd)


def send_to_r32(cmd, r32=None):
    Clipboard.set_clipboard(cmd)
    if not r32:
        r32 = 0
    execute_autohotkey_script(RAHK, cmd, r32)
    Clipboard.reset_clipboard()


def send_to_r64(cmd, r64=None):
    Clipboard.set_clipboard(cmd)
    if not r64:
        r64 = 0
    execute_autohotkey_script(RAHK, cmd, r64)
    Clipboard.reset_clipboard()
