import sublime


def send_to_terminalview(cmd, bracketed=False):
    window = sublime.active_window()
    if bracketed:
        cmd = "\x1b[200~" + cmd + "\x1b[201~"

    cmd = cmd + "\r"
    window.run_command("terminal_view_send_string", args={"string": cmd})
