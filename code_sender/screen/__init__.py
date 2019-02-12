import sublime
import subprocess


def _send_to_screen(cmd, screen):
    n = 200
    chunks = [cmd[i:i+n] for i in range(0, len(cmd), n)]
    for chunk in chunks:
        subprocess.check_call([screen, '-X', 'register', 'z', chunk])
        subprocess.check_call([screen, '-X', 'paste', 'z'])


def send_to_screen(cmd, screen="screen", bracketed=False, commit=True):
    if bracketed:
        subprocess.check_call([screen, '-X', 'stuff', "\x1b[200~"])
        _send_to_screen(cmd, screen)
        subprocess.check_call([screen, '-X', 'stuff', "\x1b[201~"])
        if commit:
            _send_to_screen("\r", screen)
    else:
        if commit:
            cmd = cmd + "\r"
        _send_to_screen(cmd, screen)
