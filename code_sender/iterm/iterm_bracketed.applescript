on run argv
    tell application "iTerm"
        tell the current window to tell current session
            set cmd to (item 1 of argv) as string
            set start_pos to 1
            set len to length of cmd
            if len is greater than 1000 then
                set end_pos to 1000
            else
                set end_pos to len
            end if
            write text (ASCII character 27) & "[200~" without newline
            if len is greater than 0 then
                repeat
                    write text (text start_pos thru end_pos of cmd) without newline
                    -- write text is not synchronized?
                    delay 0.2
                    if end_pos is len then
                        exit repeat
                    else
                        set start_pos to end_pos + 1
                        if len is greater than end_pos + 1000 then
                            set end_pos to end_pos + 1000
                        else
                            set end_pos to len
                        end if
                    end if
                end repeat
            end
            write text (ASCII character 27) & "[201~"
        end tell
    end
end run
