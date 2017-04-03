on run argv
    tell application "Safari"
        tell front window's current tab to do JavaScript "
            var input = document.getElementById('rstudio_console_input');
            var textarea = input.getElementsByTagName('textarea')[0];
            textarea.value += \"" & item 1 of argv & "\";
            var e = document.createEvent('KeyboardEvent');
            e.initKeyboardEvent('input');
            textarea.dispatchEvent(e);
            var e = document.createEvent('KeyboardEvent');
            e.initKeyboardEvent('keydown');
            Object.defineProperty(e, 'keyCode', {'value' : 13});
            input.dispatchEvent(e);
        "
    end tell
end run
