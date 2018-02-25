import sublime_plugin
import sublime
import subprocess
import sys
import os

from .utils.progress_bar import ProgressBar


class SendCodeInstallXdotoolCommand(sublime_plugin.WindowCommand):
    def run(self, path=None):
        if not sublime.ok_cancel_dialog(
                "xdotool was not installed. " +
                "Do you want to download xdotool binary now?"):
            return
        self.progress_bar = ProgressBar("installing xdotool")
        self.progress_bar.start()
        if not path:
            path = os.path.join(sublime.packages_path(), "User", "SendCode", "xdotool")
        sublime.set_timeout_async(lambda: self.install_xdotool(path))

    def install_xdotool(self, path):
        url = "https://github.com/randy3k/sublime-xdotool/raw/master/st3_linux_{}/xdotool/xdotool"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            p = subprocess.Popen(
                [
                    "curl", "-L", "-o", path,
                    url.format("x64" if sys.maxsize > 2**32 else "x32")
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        finally:
            self.progress_bar.stop()

        stdout, stderr = p.communicate()
        if p.returncode == 0:
            os.chmod(path, 0o700)
        else:
            if stdout:
                print(stdout.decode("utf-8"))
            if stderr:
                print(stderr.decode("utf-8"))
