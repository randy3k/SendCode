import sublime
import subprocess
import os
import shutil


prompt_installing_xdotool = False


def xdotool(*args):
    xdotool_path = shutil.which("xdotool")
    if not xdotool_path:
        xdotool_install_path = os.path.join(sublime.packages_path(), "User", "SendCode", "xdotool")
        if os.path.isfile(xdotool_install_path):
            xdotool_path = xdotool_install_path
        else:
            global prompt_installing_xdotool
            if not prompt_installing_xdotool:
                sublime.active_window().run_command(
                    "send_code_install_xdotool", {"path": xdotool_path})
                prompt_installing_xdotool = True

    if not xdotool_path:
        raise FileNotFoundError("xdotool cannot be found")

    return subprocess.check_output([xdotool_path] + list(args))
