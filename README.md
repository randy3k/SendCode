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

You should use Package Control to install SendREPL and its (Linux and Windows) dependency.
In the development stage, you have to add the following repository to Package Control.
Run `Package Control: Add Repository` and add

```
https://raw.githubusercontent.com/randy3k/SendREPL/repo/packages.json
```

Then you should be able to install SendREPL via Package Control as usual. If you are using Linux or Windows, the corresponding platform dependency will also be installed automatically.

### Usage

Use the command `SendREPL: Choose REPL Program` in command palette to quickly change the active program. The default is Terminal for Mac, Cmder for Windows and tmux for Linux. 

- <kbd>cmd</kbd>+<kbd>enter</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>enter</kbd> (Windows/Linux)

    If text is selected, it sends the text to the program selected. If no text is selected, then it sends the current block (if found). Finally, it moves the cursor to the next line.


- <kbd>cmd</kbd>+<kbd>\\</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>\\</kbd> (Windows/Linux): change working directory (R, Julia and Python only)


- <kbd>cmd</kbd>+<kbd>b</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>b</kbd> (Windows/Linux): source current file (R, Julia and Python only)

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
    },
```

SendREPL understands the following variables in the `cmd` field: 

- `$file`, the full path to the file
- `$file_path`, the directory contains the file
- `$file_name`, the file name
- `$file_basename`, the file name without extension
- `$file_extension`, the file extension
- `$project_path`, the active folder, if not found, use the directory of current file
- `$selection`, the text selected, or the word under cursor


### Some details about block detection

SendREPL uses the following logic to expand cursor when sending text.

- R blocks are detected by `{`,`}` pairs. 
- Julia blocks are detected by `begin`, `end` pairs and indentations. 
- Python blocks are detected by indentations or by `# %%`/`# In[]` decorators.
- Markdown fenced code of [Markdown Extended](https://github.com/jonschlinkert/sublime-markdown-extended) and [R Markdown](https://github.com/randy3k/R-Box) is also supported.
