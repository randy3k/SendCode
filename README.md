# SendCode for Sublime Text

---
## Imporatant notice

Starting from release 0.3.1, SendCode will no longer define the keybind for change working directory. 
User should define their own keybinds in the user settings. Somethings like

```json
    {
        "keys": ["ctrl+shift+h"], "command": "send_code",
        "args": {"cmd": "setwd(\"$file_path\")"},
        "context": [
            { "key": "selector", "operator": "equal", "operand": "source.r" }
        ]
    },
    {
        "keys": ["ctrl+shift+h"], "command": "send_code",
        "args": {"cmd": "%cd \"$file_path\""},
        "context": [
            { "key": "selector", "operator": "equal", "operand": "source.python" }
        ]
    },
    {
        "keys": ["ctrl+shift+h"], "command": "send_code",
        "args": {"cmd": "cd(\"$file_path\")"},
        "context": [
            { "key": "selector", "operator": "equal", "operand": "source.julia" }
        ]
    }
```

---


Send code and text to Terminal, ITerm, ConEmu, Cmder, Tmux; R (RStudio), Julia, IPython/ptpython REPL.

![](https://user-images.githubusercontent.com/1690993/28198891-4ebe5eaa-682f-11e7-8173-10b64faef9b4.png)


Following Programs are supported

- Mac: Terminal, iTerm (>=2.9), R GUI, RStudio Desktop, RStudio and Jupyter running on Chrome and Safari
- Windows: Cmder, ConEmu, R GUI, RStudio Desktop
- Linux: Tmux, Screen, RStudio Desktop
- Others: TerminalView (required [devel](https://github.com/Wramberg/TerminalView/tree/devel) branch), SublimeREPL (deprecating)

### Installation

You could install SendCode via Package Control. If you are using Linux or
Windows, the respective platform dependency
[xdotool](https://github.com/randy3k/sublime-xdotool) and
[pywin32](https://github.com/randy3k/sublime-pywin32) will also be installed
automatically.


### Usage

Select a program using the command `SendCode: Choose Program` in command palette. The default program on macOS, windows and linux are Terminal, Cmder and tmux respectively.

- <kbd>cmd</kbd>+<kbd>enter</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>enter</kbd> (Windows/Linux)

    If text is selected, it sends the text to the program selected. If no text is selected, then it sends the current block (if found). Finally, it moves the cursor to the next line.


- <kbd>cmd</kbd>+<kbd>b</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>b</kbd> (Windows/Linux): source current file (R, Julia and Python (IPython) only)

    SendCode uses Sublime build system to source files, you might have to choose the `Source File` option in a pop up window.


### Troubleshooting

1. RStudio on Windows

   If the code is pasted on the console but it is not being executed, you will need to open an empty RScript file by `File -> New File -> R Script`. This is a quick fix to the RStudio issue: https://support.rstudio.com/hc/en-us/community/posts/208160308-ctrl-enter-doesn-t-work-in-R-console-without-a-source-file-opened

2. Sending code to Python console

   [IPython 5.0](https://ipython.org) or [ptpython](https://github.com/jonathanslenders/ptpython) (or any repls which support bracketed paste mode) are assumed to be used. IPython 4.0 is still supported, but users need to disable `bracketed_paste_mode` in the settings.

3. Safari-Jupyter send does not work
   
   Most likely you haven't enabled JavaScript for AppleScript. Check the option "Allow JavaScript from Apple Events" in the Develop menu (the develope menu needs to be enabled in the preferences).

4. Nothing happens
   
   Make sure the corresponding program is opened when you are sending the text.

### Custom Keybind

It is fairly easy to create your own keybinds for commands which you frequently use. For example, the following keybind run the `R` command `source("<the current file>")` in the active program.

```json
{
    "keys": ["ctrl+shift+h"], "command": "send_code",
    "args": {"cmd": "source(\"$file\")"},
    "context": [
        { "key": "selector", "operator": "equal", "operand": "source.r" }
    ]
}
```

SendCode understands the following variables in the `cmd` field:

- `$file`, the full path to the file
- `$file_path`, the directory contains the file
- `$file_name`, the file name
- `$file_basename`, the file name without extension
- `$file_extension`, the file extension
- `$project_path`, the active folder, if not found, use the directory of current file
- `$selection`, the text selected, or the word under cursor
- `$line`, the current line number


### User settings

A couple of settings can be found `Preferences: SendCode Settings`

### Some details about block expansion

SendCode uses the following logic to expand cursor when sending text.

- R blocks are detected by `{`,`}` pairs or knitr-spin `#+` decorators.
- Julia blocks are detected by `begin`, `end` pairs and indentations.
- Python blocks are detected by indentations or by `# %%`/`# In[]` decorators.
- Markdown fenced code blocks of [Markdown Extended](https://github.com/jonschlinkert/sublime-markdown-extended) and [R Markdown](https://github.com/randy3k/R-Box) are also supported.
