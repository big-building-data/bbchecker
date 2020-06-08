_html_escape_table = {
    "&": "&amp;",
    ">": "&gt;",
    "<": "&lt;",
}


def html_escape(s: str) -> str:
    return "".join(_html_escape_table.get(c, c) for c in s)


def pre(s: str) -> str:
    return "<pre>%s</pre>" % html_escape(s)


def bold(s: str) -> str:
    return "<b>%s</b>" % html_escape(s)
