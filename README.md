# SendREPL for Sublime Text

Send Text to Terminal, ITerm, ConEmu, Cmder, Tmux; R (RStudio), Julia, IPython REPL.
This is a rewrite of [SendTextPlus](https://github.com/randy3k/SendTextPlus) which aims for higher extensibility and higher self-containedness.

*Note*: IPython console is assumed for Python syntax.

Following Programs are supported

- Mac: Terminal, iTerm (>=2.9), RStudio Desktop, R GUI, RStudio and Jupyter running on Chrome and Safari
- Linux: Tmux, Screen, RStudio Desktop
- Windows: Cmder, ConEmu, R GUI, RStudio Desktop


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
