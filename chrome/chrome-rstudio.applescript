on run argv
    set cmd to item 1 of argv
    tell application "Google Chrome"
        set URL of front window's active tab to "javascript:{" & "
            var input = document.getElementById('rstudio_console_input');
            var textarea = input.getElementsByTagName('textarea')[0];
            textarea.value += \"" & cmd & "\";
            var e = document.createEvent('KeyboardEvent');
            e.initKeyboardEvent('input');
            textarea.dispatchEvent(e);
            var e = document.createEvent('KeyboardEvent');
            e.initKeyboardEvent('keydown');
            Object.defineProperty(e, 'keyCode', {'value' : 13});
            input.dispatchEvent(e);
        " & "}"
    end tell
end run
