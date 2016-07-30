import subprocess


def send_to_tmux(cmd, tmux="tmux", bracketed_paste_mode=False):
    if bracketed_paste_mode:
        subprocess.check_call([tmux, 'set-buffer', "\x1b[200~"])
        subprocess.check_call([tmux, 'paste-buffer', '-d'])
        send_to_tmux(cmd, tmux, False)
        subprocess.check_call([tmux, 'set-buffer', "\x1b[201~"])
        subprocess.check_call([tmux, 'paste-buffer', '-d'])
    else:
        n = 200
        if cmd != "\x04":
            cmd = cmd + "\n"
        chunks = [cmd[i:i+n] for i in range(0, len(cmd), n)]
        for chunk in chunks:
            subprocess.check_call([tmux, 'set-buffer', '--', chunk])
            subprocess.check_call([tmux, 'paste-buffer', '-d'])
