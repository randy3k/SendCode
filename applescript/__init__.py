import subprocess


def osascript(script_path, *args):
    subprocess.check_call(["osascript", script_path] + list(args))
