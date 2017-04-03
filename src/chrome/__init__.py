import os
from ..applescript import osascript

CJUPYTER = os.path.join(os.path.dirname(__file__), "chrome-jupyter.applescript")
CRSTUDIO = os.path.join(os.path.dirname(__file__), "chrome-rstudio.applescript")


def send_to_chrome_jupyter(cmd):
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("\"", "\\\"")
    cmd = cmd.replace("\n", "\\n")
    osascript(CJUPYTER, cmd)


def send_to_chrome_rstudio(cmd):
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("\"", "\\\"")
    cmd = cmd.replace("\n", "\\n")
    osascript(CRSTUDIO, cmd)
