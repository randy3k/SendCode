import sublime


def send_to_sublimerepl(cmd):
    window = sublime.active_window()
    view = window.active_view()
    external_id = view.scope_name(0).split(" ")[0].split(".", 1)[1]
    window.run_command(
        "repl_send", {"external_id": external_id, "text": cmd})
