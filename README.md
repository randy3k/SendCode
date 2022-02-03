# SendCode for Sublime Text

<a href="https://packagecontrol.io/packages/SendCode"><img src="https://packagecontrol.herokuapp.com/downloads/SendCode.svg"></a>
<a href="https://www.paypal.me/randy3k/5usd" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-blue.svg" /></a>

Send code and text to macOS and Linux Terminals, iTerm, ConEmu, Cmder, Tmux, Terminus; R (RStudio), Julia, IPython.

![](https://user-images.githubusercontent.com/1690993/28198891-4ebe5eaa-682f-11e7-8173-10b64faef9b4.png)


Following Programs are supported

- Mac: Terminal, iTerm (>=2.9), R GUI, RStudio Desktop, RStudio and Jupyter running on Chrome and Safari
- Windows: Cmder, ConEmu, R GUI, RStudio Desktop
- Linux: Tmux, Screen, Gnome-Terminal, Pantheon-Terminal, Mate-Terminal, Konsole, RStudio Desktop
- Sublime Plugin: [Terminus](https://github.com/randy3k/Terminus)

### Installation

You could install SendCode via Package Control.

- If you don't have Package Control installed, follow the [installation instructions on the Package Control website](https://packagecontrol.io/installation).
- In Sublime Text, type <kbd>cmd</kbd>+<kbd>shift</kbd>+<kbd>p</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>p</kbd> (Windows/Linux)  to bring up the command palette.
- Into the command palette start typing `Package Control: Install Package` and select the option when in pops up.
- In the Install Package window start typing `SendCode` and select the option when it pops up.
- SendCode should then be installed.

If you are using Linux, we might need to install
[xdotool](http://www.semicomplete.com/projects/xdotool/) to use some features. Ubuntu users can use
```
sudo apt-get install xdotool
```
If it cannot be found, you will be prompted
to download a [binary distribution](https://github.com/randy3k/sublime-xdotool).

### Usage

Select a program using the command `SendCode: Choose Program` in command palette. The default program on macOS, windows and linux are Terminal, Cmder and tmux respectively. Each syntax binds to its own program. For instance, you could bind `R` to r files and `tmux` to python files.

There are two main keybindings:

- <kbd>cmd</kbd>+<kbd>enter</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>enter</kbd> (Windows/Linux)

    If text is selected, it sends the text to the program selected. If no text is selected, then it sends the current block (if found). Finally, it moves the cursor to the next line.


- <kbd>cmd</kbd>+<kbd>b</kbd> (Mac) or <kbd>ctrl</kbd>+<kbd>b</kbd> (Windows/Linux): source current file (R, Julia and Python (IPython) only)

    SendCode uses Sublime build system to source files, you might have to choose the `Source File` option in a pop up window.


### Troubleshooting


1. Python console

   [IPython](https://ipython.org) (5.0 or above, or any repls which support bracketed paste mode) are assumed to be used.

1. [radian](https://github.com/randy3k/radian) console

   You might want to turn on `bracketed_paste_mode` if [radian](https://github.com/randy3k/radian) is used.

1. RStudio on Windows
    
   Make sure [RStudio v1.1.383](https://www.rstudio.com/products/rstudio/download/) or above is used.

1. R Gui on Windows

   Make sure the corresponding R program is opened when you are sending the text.

1. Cmder/ Conemu on Windows

   You might need to set the path to `ConEmuC.exe` in SendCode settings. For Cmder, the file is located at
   `<path to cmder folder>\\vendor\\conemu-maximus5\\ConEmu\\ConEmuC.exe`.

1. Safari-Jupyter on macOS

   Most likely you haven't enabled JavaScript for AppleScript. Check the option "Allow JavaScript from Apple Events" in the `Develop` menu (the `Develope` menu needs to be enabled in the preferences).


### Custom Keybindings

It is fairly easy to create your own keybinds for commands which you frequently use. For example, the following keybinds execute changing working directory commands for R, Python and Julia.

```json
[
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
]
```

SendCode expands following variables in the `cmd` field:

- `$file`, the full path to the file
- `$file_path`, the directory contains the file
- `$file_name`, the file name
- `$file_base_name`, the file name without extension
- `$file_extension`, the file extension
- `$folder`, the first folder of current window
- `$project_path`, the directory where sublime-project is stored
- `$current_folder`, the folder of the window which contains the current view
- `$selection`, the text selected, or the word under cursor
- `$line`, the current line number

It also supports placeholders for variables, details can be found in the [unofficial documentation](http://docs.sublimetext.info/en/latest/reference/build_systems/configuration.html#placeholders-for-variables).

```
${file_path:$folder}
```
This will emit the directory of current file if there is one, otherwise the first folder of the current window.

You also don't have to worry about escaping quotes and backslashes between quotes, SendCode will
handle them for you.

The `prog` argument determines which program to use

```json
[
    {
        "keys": ["ctrl+shift+enter"], "command": "send_code",
        "args": {"cmd": "\n", "prog": "tmux"}
    }
]
```

### User settings

A couple of settings can be found `Preferences: SendCode Settings`.
Project-wise settings could also be specified in `sublime-project` as

```js
{
    "settings": {
        "SendCode": {
            "prog": "terminus",
            "r" : {
                "bracketed_paste_mode": true
            }
        }
    }
}
```

#### Enabling selection by window name/title (WM_NAME) for linux-terminal

If you have multiple instances of the same terminal emulator running (e.g. one `alacritty` window for R, one for IPython, etc.), you may want to want to send code to a terminal with a specific name/title (e.g. so `python` code is sent to the window named `My Special IPython` but 'julia' code is sent to `My Julia`). If you force a permanent window name when running your terminal emulator (e.g. `$ alacritty -t "My Special IPython"`), you can place this name in a `linux_window_name` SendCode setting. SendCode will then first try to find a window with the corresponding `WM_NAME` *before* using the `WM_CLASS` specified by the `linux_terminal` global setting. A minimal example is:

```js
{
    "linux_terminal": "alacritty",
    "prog": "linux-terminal",

    // First try to send Python & Julia code to the named windows, respectively
    "python" : {
        "linux_window_name": "My Special IPython",
        "bracketed_paste_mode": true,
    }, 
    "julia" : {
        "linux_window_name": "My Julia",
        "bracketed_paste_mode": true,
    }
    // Other code behaves as usual (e.g. R gets sent to the last alacritty window)
}
```

It is not recommended to use the `linux_window_name` setting unless you specify a permanent window name when running your terminal emulator; by default, window names may change frequently, which makes this setting unreliable (although you can use a regular expression in `linux_window_name` to try to catch these windows). Note that `linux_window_name` is only meaningful when in a settings block where `prog` is set to `linux-terminal`.

### Block expansion

SendCode uses the following logics to expand cursor when sending code.

- Expand current line to match `()`, `[]` and `{}`.
- R: 
  - backward expand if the previous line ends with a pipe opeartor `%>%`
  - `# %%` decorators
  - `#+` spin decorators
  - `#'` roxygen decorators
- Julia
  - `begin`, `end` indented pairs.
  - `# %%` decorators
- Python: 
  - indentations
  - `# %%` decorators.
- (See the settings `block_start_pattern` and `block_end_pattern`)
- Markdown fenced code blocks 
  - put the cursor at the line of <kbd>\`\`\`</kbd> to send the whole block.
