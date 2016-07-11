import os
from ..applescript import execute_applescript

ITERM = os.path.join(os.path.dirname(__file__), "iterm.applescript")
ITERM_BRACKETED = os.path.join(os.path.dirname(__file__), "iterm_bracketed.applescript")


def send_to_iterm(cmd, bracketed=False):
    if bracketed:
        execute_applescript(ITERM_BRACKETED, cmd)
    else:
        execute_applescript(ITERM, cmd)
