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
        # return top most setting
        if self.s.has(key) and self.s.get(key):
            return self.s.get(key)

        syntax = self.syntax()

        #  check syntax settings
        if syntax and self.s.get(syntax):
            syntax_settings = self.s.get(syntax)
            if key in syntax_settings:
                return syntax_settings[key]

        # fallback
        return default
