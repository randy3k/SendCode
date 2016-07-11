import sublime


class Settings:
    scope_mapping = {
        "source.r": "r",
        "source.python": "python",
        "source.julia": "julia"
    }

    def __init__(self, view):
        self.s = sublime.load_settings("SendREPL.sublime-settings")
        self.view = view

    def syntax(self):
        """
        SendREPL.settings.Settings(view).syntax()
        """
        pt = self.view.sel()[0].begin() if len(self.view.sel()) > 0 else 0
        scores = [self.view.score_selector(pt, s) for s, lang in self.scope_mapping.items()]
        max_score = max(scores)
        if max_score > 0:
            return list(self.scope_mapping.values())[scores.index(max_score)]
        else:
            return None

    def get(self, key, default=None):
        # return top most setting
        if self.s.has(key):
            return self.s.get(key, default)

        syntax = self.syntax()

        # check user settings
        usettings = self.s.get("user", {})
        #  check user syntax settings
        if syntax and syntax in usettings and usettings[syntax]:
            syntax_settings = usettings[syntax]
            if key in syntax_settings:
                return syntax_settings[key]
        # check user default settings
        if key in usettings and usettings[key]:
            return usettings[key]

        # check default settings
        dsettings = self.s.get("default", {})
        #  check default syntax settings
        if syntax and syntax in dsettings and dsettings[syntax]:
            syntax_settings = dsettings[syntax]
            if key in syntax_settings:
                return syntax_settings[key]
        # check default default settings
        if key in dsettings and dsettings[key]:
            return dsettings[key]

        # fallback
        return default
