from os import system
from shlex import quote

def send_to_kitty(cmd, path, socket):
    template = "{path} @ --to {socket} send-text --match state:focused {cmd}\r"
    command = template.format(path=path, socket=socket, cmd=quote(cmd))
    system(command)
