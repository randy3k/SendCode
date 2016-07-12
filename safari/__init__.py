import os
from ..applescript import osascript

SJUPYTER = os.path.join(os.path.dirname(__file__), "safari-jupyter.applescript")
SRSTUDIO = os.path.join(os.path.dirname(__file__), "safari-rstudio.applescript")


def send_to_safari_jupyter(cmd):
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("\"", "\\\"")
    cmd = cmd.replace("\n", "\\n")
    osascript(SJUPYTER, cmd)


def send_to_safari_rstudio(cmd):
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("\"", "\\\"")
    cmd = cmd.replace("\n", "\\n")
    osascript(SRSTUDIO, cmd)
