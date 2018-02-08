import sublime
import re
from ..settings import Settings


class CodeGetter:

    def __init__(self, view):
        self.view = view
        self.settings = Settings(view)
        self.auto_expand_line = self.settings.get("auto_expand_line", True)
        self.auto_advance = self.settings.get("auto_advance", True)
        self.auto_advance_non_empty = self.settings.get("auto_advance_non_empty", False)

    @classmethod
    def initialize(cls, view):
        syntax = Settings(view).syntax()
        if syntax == "r":
            return RCodeGetter(view)
        elif syntax == "md" or syntax == "rmd":
            return MarkDownCodeGetter(view)
        elif syntax == "python":
            return PythonCodeGetter(view)
        elif syntax == "julia":
            return JuliaCodeGetter(view)
        else:
            return CodeGetter(view)

    def expand_cursor(self, s):
        s = self.view.line(s)
        if self.auto_expand_line:
            s = self.expand_line(s)
        return s

    def expand_line(self, s):
        return s

    def advance(self, s):
        view = self.view
        pt = view.text_point(view.rowcol(s.end())[0] + 1, 0)
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
                original_s = s
                s = self.expand_cursor(s)
                if self.auto_advance:
                    view.sel().subtract(original_s)
                    self.advance(s)
                    moved = True

            cmd += view.substr(s) + '\n'

        if moved:
            view.show(view.sel())

        return cmd

    def find_inline(self, pattern, pt):
        while True:
            result = self.view.find(pattern, pt)
            if result.begin() == -1 or \
                    self.view.rowcol(result.begin())[0] != self.view.rowcol(pt)[0]:
                return sublime.Region(-1, -1)
            else:
                if not self.view.score_selector(result.begin(), "string, comment"):
                    return result
                else:
                    pt = result.end()

    def forward_expand(self, s, pattern=r"\S(?=\s*$)", scope="keyword.operator", paren=True):
        level = 0
        row = self.view.rowcol(s.begin())[0]
        lastrow = self.view.rowcol(self.view.size())[0]
        while row <= lastrow:
            line = self.view.line(self.view.text_point(row, 0))
            pt = line.begin()
            while paren:
                res = self.find_inline(r"[{}\[\]()]", pt)
                if res.begin() == -1:
                    break
                if self.view.substr(res) in ["{", "[", "("]:
                    level += 1
                elif self.view.substr(res) in ["}", "]", ")"]:
                    level -= 1
                pt = res.end()

            if level > 0:
                row = row + 1
            else:
                res = self.find_inline(pattern, pt)
                if res.begin() != -1 and \
                        self.view.score_selector(res.begin(), scope):
                    row = row + 1
                else:
                    s = sublime.Region(s.begin(), line.end())
                    break
        if row == lastrow:
            s = sublime.Region(s.begin(), line.end())

        return s

    def backward_expand(self, s, pattern=r"[+\-*/](?=\s*$)", scope="keyword.operator"):
        # backward_expand previous lines ending with operators

        view = self.view
        row = view.rowcol(s.begin())[0]
        while row > 0:
            row = row - 1
            line = view.line(view.text_point(row, 0))
            if re.search(pattern, view.substr(line)):
                endpt = self.find_inline(r"\S(?=\s*$)", line.begin()).begin()
                if self.view.score_selector(endpt, scope):
                    s = line
                    continue
            break

        return s


class RCodeGetter(CodeGetter):

    def expand_line(self, s):
        view = self.view
        if view.score_selector(s.begin(), "string"):
            return s

        s = self.backward_expand(s, r"([+\-*/]|%[+<>$:a-zA-Z]+%)(?=\s*$)")

        thiscmd = view.substr(s)
        row = view.rowcol(s.begin())[0]
        lastrow = view.rowcol(view.size())[0]
        if re.match(r"#\+", thiscmd):
            prevline = view.line(s.begin())
            while row < lastrow:
                row = row + 1
                line = view.line(view.text_point(row, 0))
                m = re.match(r"#'|#\+", view.substr(line))
                if m:
                    s = sublime.Region(s.begin(), prevline.end())
                    break
                elif len(view.substr(line).strip()) > 0:
                    prevline = line

            if row == lastrow:
                s = sublime.Region(s.begin(), prevline.end())

        else:
            s = self.forward_expand(s, pattern=r"([+\-*/]|%[+<>$:a-zA-Z]+%)(?=\s*$)")

        return s


class PythonCodeGetter(CodeGetter):

    def expand_line(self, s):
        view = self.view
        if view.score_selector(s.begin(), "string"):
            return s
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
                elif len(view.substr(line).strip()) > 0:
                    prevline = line

            if row == lastrow:
                s = sublime.Region(s.begin(), prevline.end())

        elif re.match(r"[ \t]*\S", thiscmd):
            indentation = re.match(r"[ \t]*", thiscmd).group(0)
            while row < lastrow:
                row = row + 1
                line = view.line(view.text_point(row, 0))
                m = re.match(r"([ \t]*)([^\n\s]+)", view.substr(line))
                if m and len(m.group(1)) <= len(indentation) and \
                        (len(m.group(1)) < len(indentation) or
                            not re.match(r"else|elif|except|finally", m.group(2))):
                    s = sublime.Region(s.begin(), prevline.end())
                    break
                elif re.match(r"[ \t]*\S", view.substr(line)):
                    prevline = line

            if row == lastrow:
                s = sublime.Region(s.begin(), prevline.end())

        return s


class JuliaCodeGetter(CodeGetter):

    def expand_line(self, s):
        view = self.view
        if view.score_selector(s.begin(), "string"):
            return s
        thiscmd = view.substr(s)
        keywords = [
            "function", "macro", "if", "for", "while", "let", "quote",
            "try", "module", "abstruct", "type", "struct", "immutable", "mutable"
        ]
        if (re.match(r"\s*(?:{})".format("|".join(keywords)), thiscmd) and
                not re.match(r".*end\s*$", thiscmd)) or \
                (re.match(r".*begin\s*$", thiscmd)):
            indentation = re.match(r"^(\s*)", thiscmd).group(1)
            endline = view.find("^" + indentation + "end", s.begin())
            s = sublime.Region(s.begin(), view.line(endline.end()).end())

        elif re.match(r"\s*(using|import|export)", thiscmd):
            row = view.rowcol(s.begin())[0]
            lastrow = view.rowcol(view.size())[0]
            while row <= lastrow:
                line = view.line(view.text_point(row, 0))
                if re.match(r".*[:,]\s*$", view.substr(line)):
                    row = row + 1
                else:
                    s = sublime.Region(s.begin(), line.end())
                    break

        else:
            s = self.forward_expand(s, pattern=r"[+\-*/](?=\s*$)")

        return s


class MarkDownCodeGetter(CodeGetter):

    def advance(self, s):
        view = self.view
        nextline = view.substr(view.line(s.end() + 1))
        if re.match(r"^```", nextline):
            pt = view.text_point(view.rowcol(s.end())[0] + 2, 0)
            if self.auto_advance_non_empty:
                nextpt = view.find(r"\S", pt)
                if nextpt.begin() != -1:
                    pt = view.text_point(view.rowcol(nextpt.begin())[0], 0)
            view.sel().add(sublime.Region(pt, pt))
        else:
            super().advance(s)

    def expand_line(self, s):
        view = self.view
        thisline = view.substr(s)
        if re.match(r"^```", thisline):
            end = view.find("^```$", s.end())
            s = sublime.Region(s.end() + 1, end.begin() - 1)
        return s
