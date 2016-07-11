import os
from ..applescript import execute_applescript

TERMINAL = os.path.join(os.path.dirname(__file__), "terminal.applescript")
TERMINAL_BRACKETED = os.path.join(os.path.dirname(__file__), "terminal_bracketed.applescript")


def send_to_terminal(cmd, bracketed=False):
    if bracketed:
        execute_applescript(TERMINAL_BRACKETED, cmd)
    else:
        execute_applescript(TERMINAL, cmd)
