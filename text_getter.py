import sublime
import re
from .settings import Settings


class TextGetter:

    def __init__(self, view):
        self.view = view
        settings = Settings(view)
        self.auto_expand_line = settings.get("auto_expand_line", True)
        self.auto_advance = settings.get("auto_advance", True)
        self.auto_advance_non_empty = settings.get("auto_advance_non_empty", False)

    @classmethod
    def initialize(cls, view):
        syntax = Settings(view).syntax()
        if syntax == "r":
            return RTextGetter(view)
        elif syntax == "python":
            return PythonTextGetter(view)
        elif syntax == "julia":
            return JuliaTextGetter(view)
        else:
            return TextGetter(view)

    def expand_cursor(self, s):
        s = self.view.line(s)
        if self.auto_expand_line:
            s = self.expand_line(s)
        return s

    def expand_line(self, s):
        return s

    def advance(self, s):
        view = self.view
        view.sel().subtract(s)
        pt = view.text_point(view.rowcol(s.end())[0]+1, 0)
        if self.auto_advance_non_empty:
            nextpt = view.find(r"\S", pt)
            if nextpt.begin() != -1:
                pt = view.text_point(view.rowcol(nextpt.begin())[0], 0)
        view.sel().add(sublime.Region(pt, pt))

    def get_text(self):
        view = self.view
        cmd = ''
        moved = False
        sels = [s for s in view.sel()]
        for s in sels:
            if s.empty():
                s = self.expand_cursor(s)
                if self.auto_advance:
                    self.advance(s)
                    moved = True

            cmd += view.substr(s) + '\n'

        if moved:
            view.show(view.sel())

        return cmd


class RTextGetter(TextGetter):

    def expand_line(self, s):
        view = self.view
        thiscmd = view.substr(s)
        if re.match(r".*\{\s*$", thiscmd):
            es = view.find(
                r"""^(?:.*(\{(?:(["\'])(?:[^\\]|\\.)*?\2|#.*$|[^\{\}]|(?1))*\})[^\{\}\n]*)+""",
                view.line(s).begin()
            )
            if s.begin() == es.begin():
                s = es
        return s


class PythonTextGetter(TextGetter):

    def expand_line(self, s):
        view = self.view
        thiscmd = view.substr(s)
        row = view.rowcol(s.begin())[0]
        prevline = view.line(s.begin())
        lastrow = view.rowcol(view.size())[0]
        if re.match(r"^(#\s%%|#%%|# In\[)", thiscmd):
            while row < lastrow:
                row = row + 1
                line = view.line(view.text_point(row, 0))
                m = re.match(r"^(#\s%%|#%%|# In\[)", view.substr(line))
                if m:
                    s = sublime.Region(s.begin(), prevline.end())
                    break
                else:
                    prevline = line

        elif re.match(r"^[ \t]*\S", thiscmd):
            indentation = re.match(r"^([ \t]*)", thiscmd).group(1)
            while row < lastrow:
                row = row + 1
                line = view.line(view.text_point(row, 0))
                m = re.match(r"^([ \t]*)([^\n\s]+)", view.substr(line))
                if m and len(m.group(1)) <= len(indentation) and \
                        (len(m.group(1)) < len(indentation) or
                            not re.match(r"else|elif|except|finally", m.group(2))):
                    s = sublime.Region(s.begin(), prevline.end())
                    break
                elif re.match(r"^[ \t]*\S", view.substr(line)):
                    prevline = line

        if row == lastrow:
            s = sublime.Region(s.begin(), prevline.end())
        return s


class JuliaTextGetter(TextGetter):

    def expand_line(self, s):
        view = self.view
        thiscmd = view.substr(s)
        if (re.match(r"^\s*(?:function|if|for|while|let|quote|try)", thiscmd) and
                not re.match(r".*end\s*$", thiscmd)) or \
                (re.match(r".*begin\s*$", thiscmd)):
            indentation = re.match("^(\s*)", thiscmd).group(1)
            end = view.find("^"+indentation+"end", s.begin())
            s = sublime.Region(s.begin(), view.line(end.end()).end())

        return s


class MarkDownTextGetter(TextGetter):

    def advance(self, s):
        view = self.view
        view.sel().subtract(view.line(s.begin()-1))
        pt = view.text_point(view.rowcol(s.end())[0]+2, 0)
        if self.auto_advance_non_empty:
            nextpt = view.find(r"\S", pt)
            if nextpt.begin() != -1:
                pt = view.text_point(view.rowcol(nextpt.begin())[0], 0)
        view.sel().add(sublime.Region(pt, pt))

    def expand_line(self, s):
        view = self.view
        thisline = view.substr(s)
        if re.match(r"^```", thisline):
            end = view.find("^```$", s.end())
            s = sublime.Region(s.end()+1, end.begin()-1)
        return s
