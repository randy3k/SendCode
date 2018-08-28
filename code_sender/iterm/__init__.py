import os
from ..applescript import osascript

ITERM = os.path.join(os.path.dirname(__file__), "iterm.applescript")
ITERM_BRACKETED = os.path.join(os.path.dirname(__file__), "iterm_bracketed.applescript")


def send_to_iterm(cmd, bracketed=False, commit=True):
    if bracketed:
        osascript(ITERM_BRACKETED, cmd, str(commit))
    else:
        osascript(ITERM, cmd, str(commit))
