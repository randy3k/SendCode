import os
from ..applescript import execute_applescript

CJUPYTER = os.path.join(os.path.dirname(__file__), "chrome-jupyter.applescript")
CRSTUDIO = os.path.join(os.path.dirname(__file__), "chrome-rstudio.applescript")


def send_to_chrome_jupyter(cmd):
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("\"", "\\\"")
    cmd = cmd.replace("\n", "\\n")
    execute_applescript(CJUPYTER, cmd)


def send_to_chrome_rstudio(cmd):
    cmd = cmd.replace("\\", "\\\\")
    cmd = cmd.replace("\"", "\\\"")
    cmd = cmd.replace("\n", "\\n")
    execute_applescript(CRSTUDIO, cmd)
