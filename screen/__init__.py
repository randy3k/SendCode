import sublime
import subprocess


def send_to_screen(cmd, screen="screen", bracketed=False):
    if bracketed:
        subprocess.check_call([screen, '-X', 'stuff', "\x1b[200~"])
        send_to_screen(cmd, screen, False)
        subprocess.check_call([screen, '-X', 'stuff', "\x1b[201~"])
    else:
        cmd = cmd + "\n"
        n = 200
        chunks = [cmd[i:i+n] for i in range(0, len(cmd), n)]
        for chunk in chunks:
            if sublime.platform() == "linux":
                chunk = chunk.replace("\\", r"\\")
                chunk = chunk.replace("$", r"\$")
            subprocess.check_call([screen, '-X', 'stuff', chunk])
