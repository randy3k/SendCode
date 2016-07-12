import subprocess


def osascript(*args):
    subprocess.check_call(["osascript"] + list(args))
