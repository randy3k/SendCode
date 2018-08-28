import sublime
import subprocess


def _send_to_screen(cmd, screen):
    n = 200
    chunks = [cmd[i:i+n] for i in range(0, len(cmd), n)]
    for chunk in chunks:
        if sublime.platform() == "linux":
            chunk = chunk.replace("\\", r"\\")
            chunk = chunk.replace("$", r"\$")
        subprocess.check_call([screen, '-X', 'stuff', chunk])


def send_to_screen(cmd, screen="screen", bracketed=False, commit=True):
    if bracketed:
        subprocess.check_call([screen, '-X', 'stuff', "\x1b[200~"])
        _send_to_screen(cmd, screen)
        subprocess.check_call([screen, '-X', 'stuff', "\x1b[201~"])
        if commit:
            _send_to_screen("\n", screen)
    else:
        if commit:
            cmd = cmd + "\n"
        _send_to_screen(cmd, screen)
