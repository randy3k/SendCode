import sublime


class Settings:
    scope_mapping = {
        "source.r": "r",
        "text.tex.latex.rsweave": "rnw",
        "text.html.markdown.rmarkdown": "rmd",
        "text.html.markdown": "md",
        "source.python": "python",
        "source.julia": "julia"
    }

    def __init__(self, view):
        self.s = sublime.load_settings("SendCode.sublime-settings")
        self.view = view

    def syntax(self):
        """
        SendCode.settings.Settings(view).syntax()
        """
        pt = self.view.sel()[0].begin() if len(self.view.sel()) > 0 else 0
        # to go beginning of the line
        pt = self.view.line(pt).begin()
        scores = [self.view.score_selector(pt, s) for s, lang in self.scope_mapping.items()]
        max_score = max(scores)
        if max_score > 0:
            return list(self.scope_mapping.values())[scores.index(max_score)]
        else:
            return None

    def get(self, key, default=None):
        syntax = self.syntax()

        settings_list = [self.s]

        window = sublime.active_window()
        if window:
            project_data = window.project_data() or {}
            project_settings = project_data.get("settings", {}).get("SendCode", {})
            if project_settings:
                settings_list.insert(0, project_settings)

        for settings in settings_list:
            #  check syntax settings
            if syntax:
                syntax_settings = settings.get(syntax, {})
                if key in syntax_settings:
                    return syntax_settings[key]

            # check global settings
            if settings.get(key, None) is not None:
                return settings.get(key)

        # fallback
        return default

    def set(self, key, value):
        syntax = self.syntax()

        window = sublime.active_window()
        if window:
            project_data = window.project_data() or {}
            project_settings = project_data.get("settings", {}).get("SendCode", {})

            if key == "prog" and key in project_settings:
                project_settings[key] = value

            if syntax:
                syntax_settings = project_settings.get(syntax, {})
                if key in syntax_settings:
                    syntax_settings[key] = value
                    window.set_project_data(project_data)
                    return
            if key in project_settings:
                project_settings[key] = value
                window.set_project_data(project_data)
                return

        #  check syntax settings
        if key == "prog":
            self.s.set(key, value)

        if syntax:
            syntax_settings = self.s.get(syntax, {})
            syntax_settings[key] = value
            self.s.set(syntax, syntax_settings)
        else:
            self.s.set(key, value)

        sublime.save_settings('SendCode.sublime-settings')
