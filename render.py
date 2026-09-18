#!/usr/bin/env python3
"""Render briefs/*.md into a static site under site/.

Standard library only, on purpose: this runs in a fresh cloud container every
morning, and a site build that can't break because a dependency moved is worth
more here than any convenience a markdown library would add.

Usage:  python3 render.py

Environment:
  BRIEF_TITLE   optional  what your brief is called, e.g. "Field notes".
                          Defaults to "Daily morning brief". Set it once in
                          your environment and it names every page, the
                          browser tab, and the phone notification.
"""

import html
import os
import re
from datetime import date

BRIEFS_DIR = "briefs"
SITE_DIR = "site"

# Nothing here is telecom-specific on purpose: one variable names the whole
# site, so a brief about anything reads as its own rather than as someone
# else's template with the words left in.
TITLE = os.environ.get("BRIEF_TITLE", "Daily morning brief")

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

CSS = """
:root {
  color-scheme: light dark;
  --bg: #fbfaf8;
  --surface: #ffffff;
  --text: #1c1b19;
  --muted: #6b6862;
  --rule: #e5e2dc;
  --link: #1a5f4a;
  --accent: #0f4c3a;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #16171a;
    --surface: #1d1f23;
    --text: #e8e6e3;
    --muted: #9a968f;
    --rule: #2e3138;
    --link: #6fcfae;
    --accent: #6fcfae;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 0 20px 64px;
  background: var(--bg);
  color: var(--text);
  font: 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto,
        "Helvetica Neue", Arial, sans-serif;
  -webkit-text-size-adjust: 100%;
}
.wrap { max-width: 44rem; margin: 0 auto; }
header.masthead {
  padding: 40px 0 20px;
  border-bottom: 2px solid var(--rule);
  margin-bottom: 32px;
}
.kicker {
  font-size: 12px;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 6px;
}
h1 { font-size: 1.7rem; line-height: 1.25; margin: 0; letter-spacing: -.01em; }
h2 {
  font-size: 12px;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 40px 0 4px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--rule);
}
p { margin: 18px 0; }
a { color: var(--link); text-decoration-thickness: 1px; text-underline-offset: 2px; }
a:hover { text-decoration-thickness: 2px; }
strong a { text-decoration: none; }
strong a:hover { text-decoration: underline; }
.quiet { color: var(--muted); font-style: italic; }
.archive { margin-top: 64px; padding-top: 24px; border-top: 2px solid var(--rule); }
.archive ul { list-style: none; padding: 0; margin: 16px 0 0; }
.archive li { padding: 7px 0; border-bottom: 1px solid var(--rule); }
.archive a { text-decoration: none; }
.archive a:hover { text-decoration: underline; }
.back { display: inline-block; margin: 0 0 24px; font-size: 14px; text-decoration: none; }
footer { margin-top: 56px; padding-top: 20px; border-top: 1px solid var(--rule);
         color: var(--muted); font-size: 13px; }
@media (max-width: 480px) {
  body { font-size: 16px; padding: 0 16px 48px; }
  h1 { font-size: 1.4rem; }
}
"""


def pretty_date(iso):
    """2026-09-10 -> Thursday, Sep 10, 2026. Falls back to the raw string."""
    try:
        y, m, d = (int(p) for p in iso.split("-"))
        dt = date(y, m, d)
        return f"{dt.strftime('%A')}, {MONTHS[m - 1]} {d}, {y}"
    except (ValueError, IndexError):
        return iso


def inline(text):
    """Convert the inline markdown the briefs actually use, safely.

    Escape first, then build tags, so nothing in a headline or URL pulled off
    the web can inject markup. Only http(s) links survive.
    """
    text = html.escape(text, quote=True)

    def link(m):
        label, href = m.group(1), m.group(2)
        if not re.match(r"https?://", href, re.I):
            return label
        return f'<a href="{href}" rel="noopener noreferrer">{label}</a>'

    # The URL group allows one level of balanced parens so that links like
    # en.wikipedia.org/wiki/Fiber_(optics) survive intact.
    text = re.sub(r"\[([^\]]+)\]\(((?:[^()\s]|\([^()\s]*\))+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", text)
    return text


def parse(md):
    """Split a brief into (title, [(section_or_None, [paragraphs])])."""
    lines = md.replace("\r\n", "\n").split("\n")
    title, blocks, section, buf = "", [], None, []

    def flush():
        if buf:
            blocks.append((section, "\n".join(buf).strip()))
            buf.clear()

    for line in lines:
        if line.startswith("# "):
            flush()
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            section = line[3:].strip()
        elif not line.strip():
            flush()
        else:
            buf.append(line.strip())
    flush()
    return title, blocks


def body_html(md):
    _, blocks = parse(md)
    out, seen = [], None
    for section, para in blocks:
        if section and section != seen:
            out.append(f"<h2>{html.escape(section)}</h2>")
            seen = section
        cls = ' class="quiet"' if para.lower().startswith("nothing new") else ""
        out.append(f"<p{cls}>{inline(para)}</p>")
    return "\n".join(out)


def page(title, body, back=False):
    home = '<a class="back" href="./">&larr; All briefs</a>' if back else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{home}
{body}
<footer>Generated automatically each morning.</footer>
</div>
</body>
</html>
"""


def masthead(title, sub):
    return (f'<header class="masthead"><p class="kicker">{html.escape(sub)}</p>'
            f"<h1>{html.escape(title)}</h1></header>")


def main():
    os.makedirs(SITE_DIR, exist_ok=True)
    briefs = []
    if os.path.isdir(BRIEFS_DIR):
        for name in sorted(os.listdir(BRIEFS_DIR), reverse=True):
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", name):
                with open(os.path.join(BRIEFS_DIR, name), encoding="utf-8") as fh:
                    briefs.append((name[:-3], fh.read()))

    # One page per brief.
    for iso, md in briefs:
        body = masthead(TITLE, pretty_date(iso)) + body_html(md)
        with open(os.path.join(SITE_DIR, f"{iso}.html"), "w", encoding="utf-8") as fh:
            fh.write(page(f"{TITLE} - {iso}", body, back=True))

    # Index: newest brief in full, everything older as a list.
    if briefs:
        iso, md = briefs[0]
        body = masthead(TITLE, pretty_date(iso)) + body_html(md)
        if len(briefs) > 1:
            items = "\n".join(
                f'<li><a href="{o}.html">{pretty_date(o)}</a></li>'
                for o, _ in briefs[1:]
            )
            body += f'<div class="archive"><h2>Earlier briefs</h2><ul>{items}</ul></div>'
    else:
        body = (masthead(TITLE, "Not running yet")
                + "<p class=\"quiet\">No briefs yet. The first one appears here "
                  "after the scheduled run.</p>")

    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page(TITLE, body))

    # wrangler.jsonc sets not_found_handling to "404-page", which expects this.
    nf = (masthead("Not found", "404")
          + '<p class="quiet">No brief at that address.</p>'
          + '<p><a href="./">Go to the latest brief</a></p>')
    with open(os.path.join(SITE_DIR, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(page(f"Not found - {TITLE}", nf))

    print(f"rendered {len(briefs)} brief(s) into {SITE_DIR}/")


if __name__ == "__main__":
    main()
