import subprocess


def execute_applescript(script_path, *args):
    subprocess.check_call(["osascript", script_path] + list(args))
