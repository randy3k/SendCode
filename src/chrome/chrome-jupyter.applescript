on run argv
    tell application "Google Chrome"
        set URL of front window's active tab to "javascript:{" & "
            var mycell = IPython.notebook.get_selected_cell();
            mycell.set_text(\"" & item 1 of argv & "\");
            mycell.execute();
            var nextcell = IPython.notebook.insert_cell_below();
            IPython.notebook.select_next();
            IPython.notebook.scroll_to_cell(IPython.notebook.find_cell_index(nextcell));
        " & "}"
    end tell
end run
