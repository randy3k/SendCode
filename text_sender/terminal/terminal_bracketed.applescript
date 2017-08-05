on run argv
    tell application "Terminal" to do script ¬
        (ASCII character 27) & "[200~" &  item 1 of argv & (ASCII character 27) & "[201~" ¬
        in front window
end run
