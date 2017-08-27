import sublime
import os


def plugin_loaded():

    # update SendCode.sublime-settings

    fpath = os.path.join(sublime.packages_path(), 'User', 'SendCode.sublime-settings')
    s = sublime.load_settings("SendCode.sublime-settings")

    try:
        with open(fpath, mode='r', encoding="utf-8") as f:
            content = f.read()
            data = sublime.decode_value(content)
            if "user" in data and data["user"]:
                for k, v in data["user"].items():
                    if k not in data:
                        s.set(k, v)

                s.erase("user")
                sublime.save_settings('SendCode.sublime-settings')

            if s.has("prog"):
                prog = s.get("prog")
                if prog:
                    if s.has("julia") and "prog" not in s.get("julia"):
                        d = s.get("julia")
                        d["prog"] = prog
                        s.set("julia", d)

                    if s.has("python") and "prog" not in s.get("python"):
                        d = s.get("python")
                        d["prog"] = prog
                        s.set("python", d)

                    if s.has("r") and "prog" not in s.get("r"):
                        d = s.get("r")
                        d["prog"] = prog
                        s.set("r", d)

                sublime.save_settings('SendCode.sublime-settings')
    except:
        pass


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

        #  check syntax settings
        if syntax:
            syntax_settings = self.s.get(syntax, {})
            if key in syntax_settings:
                return syntax_settings[key]

        # check global settings
        if self.s.has(key) and self.s.get(key):
            return self.s.get(key)

        # fallback
        return default

    def set(self, key, value):
        syntax = self.syntax()

        #  check syntax settings
        if syntax:
            syntax_settings = self.s.get(syntax, {})
            syntax_settings[key] = value
            self.s.set(syntax, syntax_settings)
        else:
            self.s.set(key, value)

        if key == "prog":
            self.s.set(key, value)

        sublime.save_settings('SendCode.sublime-settings')

    def erase(self, key):
        syntax = self.syntax()

        #  check syntax settings
        if syntax and self.s.get(syntax):
            syntax_settings = self.s.get(syntax)
            syntax_settings.pop(key, None)
            self.s.set(syntax, syntax_settings)
        else:
            self.s.erase(key)

        sublime.save_settings('SendCode.sublime-settings')
