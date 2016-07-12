import os
from ..applescript import execute_applescript

SJUPYTER = os.path.join(os.path.dirname(__file__), "safari-jupyter.applescript")
SRSTUDIO = os.path.join(os.path.dirname(__file__), "safari-rstudio.applescript")


def send_to_safari_jupyter(cmd):
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("\"", "\\\"")
    cmd = cmd.replace("\n", "\\n")
    execute_applescript(SJUPYTER, cmd)


def send_to_safari_rstudio(cmd):
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("\"", "\\\"")
    cmd = cmd.replace("\n", "\\n")
    execute_applescript(SRSTUDIO, cmd)
