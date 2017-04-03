on run argv
    tell application "Safari"
        tell front window's current tab to do JavaScript "
            var mycell = IPython.notebook.get_selected_cell();
            mycell.set_text(\"" & item 1 of argv & "\");
            mycell.execute();
            var nextcell = IPython.notebook.insert_cell_below();
            IPython.notebook.select_next();
            IPython.notebook.scroll_to_cell(IPython.notebook.find_cell_index(nextcell));
        "
    end tell
end run
