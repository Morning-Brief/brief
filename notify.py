#!/usr/bin/env python3
"""Send the day's brief to Pushover as a phone notification.

Standard library only. Reads the brief that was just written, builds a short
teaser, and links to the published page.

Usage:  python3 notify.py 2026-09-10 [--dry-run]

Environment:
  PUSHOVER_TOKEN   optional  application API token from pushover.net/apps/build
  PUSHOVER_USER    optional  your user key from the Pushover dashboard
  SITE_BASE_URL    optional  e.g. https://your-project.workers.dev
  BRIEF_TITLE      optional  what your brief is called. Defaults to
                             "Daily morning brief". Use the same value here
                             as render.py sees, so the notification and the
                             page it links to agree.

Pushover is an upgrade, not a requirement. With neither Pushover variable set
this exits quietly without sending, because the routine's own push and email
notification already covers delivery. Setting only one of the pair is treated
as a mistake and reported.
"""

import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://api.pushover.net/1/messages.json"

TITLE = os.environ.get("BRIEF_TITLE", "Daily morning brief")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

# Long section names cost characters that are better spent on the headline.
SHORT = {
    "OSP news": "OSP",
    "Market forces": "Market",
    "Professional development": "ProDev",
    "Quality practice": "Quality",
}


def summarize(md):
    """Return (headline, [(section, count)], quiet) for a brief."""
    sections, headlines, current = [], [], None
    for line in md.replace("\r\n", "\n").split("\n"):
        line = line.strip()
        if line.startswith("## "):
            current = line[3:].strip()
            sections.append([current, 0])
        elif line.startswith("**"):
            m = re.match(r"\*\*\[([^\]]+)\]", line) or re.match(r"\*\*([^*]+)\*\*", line)
            if m:
                headlines.append(m.group(1).strip())
                if sections:
                    sections[-1][1] += 1
    counts = [(s, n) for s, n in sections if n]
    total = sum(n for _, n in counts)
    return (headlines[0] if headlines else None, counts, total == 0)


def build(iso, md):
    headline, counts, quiet = summarize(md)
    try:
        y, m, d = (int(p) for p in iso.split("-"))
        stamp = f"{MONTHS[m - 1]} {d}"
    except (ValueError, IndexError):
        stamp = iso

    if quiet:
        # Still worth sending: it confirms the run happened. Priority -1 makes
        # it arrive silently so a quiet day never wakes anyone up.
        return f"{TITLE} - {stamp}", "Nothing new across any beat.", -1

    total = sum(n for _, n in counts)
    tally = " / ".join(f"{SHORT.get(s, s)} {n}" for s, n in counts)
    body = headline or "New items today."
    if total > 1:
        body += f"\n\n+{total - 1} more - {tally}"
    else:
        body += f"\n\n{tally}"
    return f"{TITLE} - {stamp} ({total})", body, 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit("usage: notify.py YYYY-MM-DD [--dry-run]")
    iso = args[0]

    path = os.path.join("briefs", f"{iso}.md")
    if not os.path.exists(path):
        sys.exit(f"no brief at {path} - nothing to notify about")
    with open(path, encoding="utf-8") as fh:
        md = fh.read()

    title, message, priority = build(iso, md)
    payload = {"title": title, "message": message, "priority": str(priority)}

    base = os.environ.get("SITE_BASE_URL", "").rstrip("/")
    if base:
        payload["url"] = f"{base}/{iso}.html"
        payload["url_title"] = "Read the brief"

    if dry:
        print("DRY RUN - would send:")
        for k, v in payload.items():
            print(f"  {k}: {v}")
        return

    token, user = os.environ.get("PUSHOVER_TOKEN"), os.environ.get("PUSHOVER_USER")
    if not token and not user:
        # Neither variable set means Pushover was never configured, so there is
        # nothing to fail about - the brief is already written and published,
        # and the routine's own notification carries it. Exit 0 so the run is
        # not reported as a partial failure every morning.
        print("pushover: not configured - skipping (routine notification covers this)")
        return
    if not token or not user:
        # One without the other is a real misconfiguration and worth surfacing.
        missing = "PUSHOVER_TOKEN" if not token else "PUSHOVER_USER"
        sys.exit(f"{missing} is not set - set both Pushover variables, or neither")
    payload.update(token=token, user=user)

    data = urllib.parse.urlencode(payload).encode()
    try:
        with urllib.request.urlopen(API, data=data, timeout=20) as resp:
            print(f"pushover: {resp.status} {resp.read().decode()[:200]}")
    except Exception as exc:  # noqa: BLE001 - the reason matters more than the type
        sys.exit(f"pushover send failed: {exc}")


if __name__ == "__main__":
    main()
