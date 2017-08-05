import os
from ..applescript import osascript

TERMINAL = os.path.join(os.path.dirname(__file__), "terminal.applescript")
TERMINAL_BRACKETED = os.path.join(os.path.dirname(__file__), "terminal_bracketed.applescript")


def send_to_terminal(cmd, bracketed=False):
    if bracketed:
        osascript(TERMINAL_BRACKETED, cmd)
    else:
        osascript(TERMINAL, cmd)
