---
description: Run all four research beats in parallel and write today's brief
---

Produce today's research brief. Work through these steps in order.

## 1. Set up

Get today's date once and use it everywhere:

```bash
date +%F
```

Call that `TODAY` (format `YYYY-MM-DD`). Make sure `briefs/` exists
(`mkdir -p briefs`) and that `covered.json` exists and parses as a JSON array.
If `covered.json` is missing or corrupt, stop and tell me - do not silently
recreate it, because that would erase the dedupe history and the next brief
would repeat everything.

If `briefs/$TODAY.md` already exists, you are doing a **second run for the
same day**. Do not overwrite it: you will add new items to the existing file
in step 5.

## 2. Run all four beats in parallel

Spawn all four subagents **in a single message** so they run concurrently,
and wait for all four to return:

- `osp-news` - outside plant and fiber industry news
- `market-forces` - supply chain, trade policy, capital, labor, demand drivers
- `prodev` - professional development and credentialing
- `quality-practice` - the QA/QC craft itself

Give each the same instruction: read `covered.json` first, skip anything
already covered, return exactly `nothing new` if there is nothing worth
reporting, and respect the item cap in its own file - 6 for most beats,
5 for `market-forces`.

Each agent reads `covered.json` on its own, so they may independently pick the
same story. That is expected - step 3 handles it.

If an agent errors out or returns nothing usable, treat that beat as
`nothing new` for this run, and say so in your reply to me. Do not retry more
than once, and do not write items for a beat that did not report.

## 3. Merge and drop redundancy

You now have up to 23 items. Cut them down:

- **Same URL in two beats** - keep it once, in whichever beat it fits best.
  Prefer the more specific beat: a BICSI manual revision is `prodev`, not
  `osp-news`, even if both found it. `osp-news` and `market-forces` will
  collide most often - funding and supply stories look like both. Put it in
  `market-forces` when the point is the money, the materials, or the timeline;
  put it in `osp-news` when the point is what was built, ruled, or standardised.
- **Same story, different URLs** - keep the better source (primary document
  over coverage of it; full text over a summary) and drop the rest.
- **Same substance, different framing** - if two items would leave me with the
  same takeaway, keep one.
- **Already covered** - re-check every surviving URL against `covered.json`
  yourself. The agents are told to filter, but this is the last gate before an
  item gets written, and a repeat is the most annoying failure mode this
  system has.

Then rank what is left by how much it actually matters to me - an OSP designer
and QC specialist heading toward team lead / PM. Something with a deadline or
a direct effect on how I design, review, or estimate outranks background news.

**Spread the sources.** If three items in a section come from the same outlet,
and a comparable item from a different one is sitting just below the cut, take
the different one. The point of a wide source list is range; a brief that is
three-quarters one publication has quietly narrowed back down. This breaks ties
between items of similar value - it never promotes a weak item over a strong
one.

## 4. Check the length

Budget **60 to 90 words per item** - what happened, plus a "why it matters"
that names an actual consequence rather than gesturing at significance. Three
sentences is the usual shape.

The file has an **1800-word ceiling**. At twenty-three items that is roughly
78 words each, which is the point: the room exists to carry **more items from
more sources**, not to make each item longer. Resist padding.

Let a busy day run long and a quiet day run short. Only if you genuinely exceed
1800 words, **cut the weakest items entirely** - never truncate an item
mid-thought or shave every item into fragments. Ten well-explained items beat
twenty-three stubs.

Items you cut are *not* reported, so they do **not** go into `covered.json`.
They stay eligible and can resurface tomorrow.

## 5. Write the brief

Write to `briefs/$TODAY.md`.

Structure: a date header, then one `##` section per beat that reported
anything, in this order - OSP news, Market forces, Professional development,
Quality practice. Under each section, one **short paragraph per item**.

Paragraphs, not bullet fragments. Each item is three or four sentences of
flowing prose: open with the headline as a markdown link, say what happened in
plain language, then say why it matters to me specifically. The agents hand
you labeled fields (`Summary`, `Why it matters`) - that is an intake format,
not the output format. Rewrite them into prose. Do not emit `- URL:` lines or
carry the field labels into the brief.

```markdown
# Brief - 2026-09-09

## OSP news

**[Headline of the item](https://example.com/article)** - What happened, in
one or two plain sentences. Then why it lands on my desk: the design, QC,
cost, schedule, or deadline consequence, concretely.

**[Second item](https://example.com/other)** - Same shape. Vary the sentence
structure between items; do not write the same template five times.

## Market forces

...

## Professional development

...

## Quality practice

...
```

A beat that returned nothing gets its heading and a single line -
`Nothing new this run.` - so I can see it was checked and came up empty. A
beat that errored gets `_Beat did not run this time._` instead, so a coverage
gap never looks like a quiet day.

**If all four beats returned nothing**, skip all of the above and write a
one-line file, nothing else:

```markdown
# Brief - 2026-09-09 - nothing new across all four beats.
```

On a second run for a day, add the new items into the existing sections of
today's file rather than replacing it, keep the whole file under 1800 words,
and if the file was the one-line "nothing new" version, replace that line with
the real structure.

Then verify: `wc -w briefs/$TODAY.md`. If it is 1800 or over, cut the weakest
item and check again.

## 6. Append to covered.json

Every item that **appears in the written brief** gets exactly one entry:

```json
{ "url": "...", "headline": "...", "date": "YYYY-MM-DD" }
```

`date` is `TODAY` - the date the item went into a brief, not the article's
publication date. That is what makes pruning by age straightforward.

Append to the end of the array, keep the file valid JSON with 2-space indent,
and do not reorder or rewrite existing entries. Use a script rather than
hand-editing, so a malformed file cannot break every future run:

```bash
python3 - <<'PY'
import json
new = [
    {"url": "https://example.com/article", "headline": "Headline of the item", "date": "2026-09-09"},
]
covered = json.load(open("covered.json"))
seen = {e["url"] for e in covered}
covered += [e for e in new if e["url"] not in seen]
json.dump(covered, open("covered.json", "w"), indent=2, ensure_ascii=False)
open("covered.json", "a").write("\n")
PY
```

The `seen` guard makes a re-run harmless. Confirm the result still parses
before moving on.

## 7. Render the website

```bash
python3 render.py
```

This regenerates everything under `site/` from `briefs/*.md` - today's page, every
past page, and the index. It is deterministic and safe to re-run; never hand-edit
anything in `site/`, because the next run overwrites it.

If it errors, fix the cause rather than skipping it. A brief that never reaches
the website is a brief I never read.

## 8. Commit and push

```bash
git add briefs/$TODAY.md covered.json site/
git commit -m "brief: $TODAY"
git push origin HEAD
```

The push matters: Cloudflare redeploys the site on every push, so nothing
reaches me until this succeeds. If the push is rejected, say so loudly in your
reply - do not carry on to step 9 as though it worked.

## 9. Send the notification

```bash
python3 notify.py $TODAY
```

Reads today's brief, builds a short teaser, and sends it to my phone with a link
to the published page. Quiet days go out at low priority so they arrive without a
sound.

**Pushover is optional.** If `PUSHOVER_TOKEN` and `PUSHOVER_USER` are both
absent, the script prints that it is skipping and exits 0. That is the expected,
supported path for anyone relying on the routine's own push or email notification
instead. **Do not report a skipped send as a failure** - say it was skipped, or
say nothing about it.

If only one of the pair is set, that is a real misconfiguration: the script exits
non-zero and you should tell me plainly which one is missing. `SITE_BASE_URL` is
what puts the link in the message. Add `--dry-run` to see what would be sent
without sending it.

## 10. Report back

**Open your reply with the link to today's brief, on its own line** - the
`SITE_BASE_URL` value followed by `/$TODAY.html`. If `SITE_BASE_URL` is not set,
say that instead of inventing a URL.

This matters more than it looks. When this runs as a scheduled routine, Claude's
own push and email notification carries a summary of your reply, so leading with
the URL is what makes that notification tappable. Without it, anyone not using
Pushover is told the brief is ready and then has to go find it.

Then keep it short: how many items ran in each beat, anything you dropped as
redundant or over budget, and whether the push succeeded. If any agent returned
`Source notes:` lines about a dead, moved, or paywalled source, surface them here
so I can update the agent file - those belong in your reply, never in the brief.

State any failure plainly rather than rounding it up to success. A run where the
brief was written but the push failed is a partial run and I need to know. A
skipped Pushover send is **not** a failure: Pushover is optional, and skipping it
when it was never configured is the designed behavior.

Do not paste the brief back at me. It is in the file.
