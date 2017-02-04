# SendREPL for Sublime Text

Send Text to Terminal, ITerm, ConEmu, Cmder, Tmux; R (RStudio), Julia, IPython REPL.
This is a rewrite of [SendTextPlus](https://github.com/randy3k/SendTextPlus) which aims for higher extensibility and higher self-containedness.

*Note*: IPython console is assumed for Python syntax.

Following Programs are supported

- Mac: Terminal, iTerm (>=2.9), Tmux, Screen, RStudio Desktop, R GUI, RStudio and Jupyter running on Chrome and Safari
- Windows: Cmder, ConEmu, R GUI, RStudio Desktop
- Linux: Tmux, Screen, RStudio Desktop
- Others: SublimeREPL

### Installation

You could install SendREPL via Package Control. If you are using Linux
(Windows), the corresponding platform dependency
[xdotool](https://github.com/randy3k/sublime-xdotool)
([pywin32](https://github.com/randy3k/sublime-pywin32)) will also be installed
automatically.


### Usage

Select a program using the command `SendREPL: Choose REPL Program` in command palette. The default program is Terminal for Mac, Cmder for Windows and tmux for Linux.

- <kbd>cmd</kbd>+<kbd>enter</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>enter</kbd> (Windows/Linux)

    If text is selected, it sends the text to the program selected. If no text is selected, then it sends the current block (if found). Finally, it moves the cursor to the next line.


- <kbd>cmd</kbd>+<kbd>\\</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>\\</kbd> (Windows/Linux): change working directory (R, Julia and Python (IPython) only)


- <kbd>cmd</kbd>+<kbd>b</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>b</kbd> (Windows/Linux): source current file (R, Julia and Python (IPython) only)

    SendREPL uses Sublime build system to source files, you might have to choose the `Source File` option in a pop up window.


### Custom Keybind

It is fairly easy to create your own keybinds for commands which you frequently use. For example, the following keybind run the `R` command `source("<the current file>")` in the active program.

```json
{
    "keys": ["super+shift+e"], "command": "send_repl",
    "args": {"cmd": "source(\"$file\")"},
    "context": [
        { "key": "selector", "operator": "equal", "operand": "source.r" }
    ]
}
```

SendREPL understands the following variables in the `cmd` field:

- `$file`, the full path to the file
- `$file_path`, the directory contains the file
- `$file_name`, the file name
- `$file_basename`, the file name without extension
- `$file_extension`, the file extension
- `$project_path`, the active folder, if not found, use the directory of current file
- `$selection`, the text selected, or the word under cursor
- `$line`, the current line number


### User settings

User setttings should go into the `user` key in the `SendREPL.sublime-settings`. For example

```json
{
    "user":{
        "python" : {
            "prog": "terminal",
            "bracketed_paste_mode": true
        }
    }
}

```

### Some details about block detection

SendREPL uses the following logic to expand cursor when sending text.

- R blocks are detected by `{`,`}` pairs or knitr-spin `#+` decorators.
- Julia blocks are detected by `begin`, `end` pairs and indentations.
- Python blocks are detected by indentations or by `# %%`/`# In[]` decorators.
- Markdown fenced code of [Markdown Extended](https://github.com/jonschlinkert/sublime-markdown-extended) and [R Markdown](https://github.com/randy3k/R-Box) is also supported.
