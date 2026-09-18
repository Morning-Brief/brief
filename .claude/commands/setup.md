---
description: Interview me, then write my beats and tell me what to click
---

You are setting up this person's daily brief. They may have arrived here having
read almost nothing, so carry the whole process.

Your job has three parts: **interview**, **research their sources**, **write
their beats**. Then hand them the short list of things only they can click.

Do not ask them to write markdown. Do not send them to read `SETUP.md`. You are
the setup process.

---

## Step 1 - Interview

Open with two sentences on what is about to happen: you will ask a few
questions, go find good sources for what they care about, write their beat
files, and hand back a short list of things to click. Two minutes of questions.

Then ask **all of the following in a single message**, numbered, and say they
can answer roughly or skip any of them. Do not interview one question at a
time - it is tedious and they will lose patience.

1. **What do you do?** Role, industry, and what a normal working day involves.
2. **What do you already know cold?** What is already on your radar every day -
   so the brief can skip it instead of telling you things you know.
3. **Where are you trying to get to?** A promotion, a certification, a move into
   management, a different specialty. This shapes what counts as useful.
4. **What do you want tracked?** Plain topics, as many as you like. Do not
   worry about sources - naming publications is optional and you should not feel
   you need any. Example of the right level of detail:
   *"AT&T fiber buildouts, BEAD funding news, copper retirement, supply chain
   and manufacturing - Corning, Prysmian - competitor activity, government
   policy."*

   **Ask where, too.** National, or does a region, state or metro actually
   decide what matters to them? *"Telecom, but the Northeast."* *"Multifamily,
   Phoenix and Tucson."* Geography changes a source list more than almost
   anything else: state regulators, regional grid operators, state broadband
   offices, metro business journals and county dockets are frequently the whole
   story, and a national list will miss all of it. If they name a region, go
   find that region's bodies specifically in Step 3 - do not settle for national
   coverage that occasionally mentions their state.
5. **Any sources you already read and trust?** Optional. If you have them, they
   go in first.
6. **Anything you specifically do not want?** Vendor press releases, stock
   analysis, conference marketing - whatever wastes your time.
7. **What should it be called?** The name on the page and the morning
   notification. Optional - suggest one from their answers if they shrug.

If they answer thinly, work with it and infer. Ask at most **one** short
follow-up round, and only if something essential is genuinely missing - usually
that is question 1 or 4. Never send a third round of questions.

## Step 2 - Propose the beats, and confirm

From their answers, group the topics into **two to five beats**. Three or four
is the usual sweet spot. A beat is a coherent area one researcher could own -
not a single topic and not everything at once.

Show them the proposed structure compactly: a name and one line of scope each.
Something like:

```
1. industry-news   - carrier buildouts, BEAD and funding, M&A, competitor moves
2. supply-chain    - cable and hardware manufacturing, lead times, Corning et al
3. policy          - FCC, state programs, permitting, pole attachment
```

Ask if that split looks right, and let them rename, merge, split, add, or drop.
Get a yes before writing anything. This is the only confirmation gate - do not
check in again after this.

## Step 3 - Go find their sources

**This is the part that earns your keep.** They named topics; you find the
publications, and you verify them.

For each beat, use WebSearch and WebFetch to assemble **six to twelve sources**:

- **Primary sources first.** For anything regulatory, standards-related, or
  credentialing, go to the body itself - the regulator, the standards
  organization, the association. Trade press covers that material thinly and
  late, and the primary source is the only place the dates are authoritative.
- **Trade press** that actually covers the beat, not general business media.
- **Associations and practitioner outlets** in their field.
- **Regional bodies, if they named a region in question 4.** State regulators
  and commissions, state programs and offices, regional operators and authorities,
  metro business journals, county and city dockets. A local decision usually
  appears nowhere else, and these are easy to skip past when an obvious national
  source is sitting right there. A regional beat with only national sources is
  the most common way this comes out disappointing.
- Anything they named in question 5, checked like the rest.

**Verify every source before you list it.** Open it. Confirm it is live,
publishing recently, and readable without a subscription. Drop anything dead,
redirecting, archive-only, or hard-paywalled, and find a replacement.

Some sites refuse automated fetches and return 403 to any bot. Note those, keep
them if they are genuinely important to the beat, and tell the person the beat
may not always be able to read them.

Do not pad a list with sites you did not open. A short verified list beats a
long speculative one.

## Step 4 - Write the beat files

Write one file per beat to `.claude/agents/<name>.md`.

**Use the existing files in `.claude/agents/` as your structural template.** They
encode rules learned from real failures, and they must survive into the new
files unchanged:

- the frontmatter shape: `name`, `description`, `model: sonnet`,
  `tools: WebSearch, WebFetch, Read`
- **Step 1 - read `covered.json` before you search**
- **"Before you report anything: open it"** - the whole section, including the
  partly-gated-site nuance. This is the most important rule in the repository.
- the `Source notes:` reporting convention
- the output format block
- the Rules section: item cap, the `nothing new` rule, direct URLs, the
  source-breadth rule, and that agents cannot write files

Replace only the beat-specific parts: the description, the "Who you are
reporting for" profile, the beat scope, the source list, and what makes an item
worth reporting.

Write the **profile** from their answers to questions 1-3, in the second person
about them, concretely. This is what every "why it matters" line gets judged
against, so vagueness here poisons everything downstream.

Write **"what makes an item worth reporting"** from questions 3 and 6. State
the test as something they could do differently as a result - and name what to
reject, using their own words for what wastes their time.

If they asked for fewer or more beats than the files already present, delete or
add files so `.claude/agents/` contains exactly their beats and nothing else.

## Step 5 - Wire the beats into the pipeline

Edit `.claude/commands/brief.md`:

- **Step 2** - the spawn list must name exactly their beats
- **Step 3** - the "up to N items" figure: beats × the per-beat cap
- **Step 5** - the section order and headings in the brief

Then check nothing else in that file still refers to a beat that no longer
exists.

## Step 6 - Hand over what only they can do

Give them a short, ordered list. No essay, and no pointing at `SETUP.md`.

Include the **allowlist block**, ready to paste, built from every domain across
their beats - apex and `*.` wildcard for each, plus `api.pushover.net` only if
they chose Pushover below:

```
example.com
*.example.com
...
api.pushover.net
```

Then the steps, in this order:

1. **Notifications** - decide this first, because it changes step 3.
   **Recommend Pushover**: about $5 once on Google Play or the App Store, no
   subscription, and it is the only option that arrives every morning without
   fail. They install the app, sign in at pushover.net, copy their user key,
   then create an application to get an API token. The free alternative is the
   routine's own **Push** and **Email** toggles, switched on in step 4 with
   nothing to install, but the platform decides whether to send it and it does
   not always fire. Say that plainly and let them choose. If they pick the free
   one, tell them to confirm it actually arrived after step 6
2. **Cloudflare** - optional. Their briefs are committed as markdown and GitHub
   renders it, so the website is an upgrade, not a requirement. If they want it:
   dash.cloudflare.com → Workers & Pages → import their repository → build
   command empty, deploy command `npx wrangler deploy`
3. **Cloud environment** at claude.ai/code - a **new** one, never their Default,
   since narrowing Default breaks their other work. Network access **Custom**
   with the allowlist above, plus `BRIEF_TITLE` set to what they want their
   brief called, `SITE_BASE_URL` if they set up the site, and `PUSHOVER_TOKEN`
   and `PUSHOVER_USER` only if they chose Pushover in step 1
4. **Routine** at claude.ai/code/routines - the prompt to paste is in
   `SETUP.md` Step 5; their repository; the environment from step 3; **remove
   all connectors**; turn on the routine's **Push** and/or **Email**
   notification unless they chose Pushover, in which case turn both off to avoid
   a duplicate every morning; schedule it about **15 minutes before** they
   want the notification, since the run takes 6-12 minutes and starts at the
   scheduled time rather than finishing then
5. **Check usage credits are off** at claude.ai/settings/usage, so hitting a
   plan limit skips a run instead of billing them
6. **Run it once now** with **Run now**, rather than waiting for the schedule

## Step 7 - Commit

Commit the files you wrote:

```bash
git add .claude/ && git commit -m "setup: configure beats"
```

Push if they have a remote configured.

---

## Throughout

**Set expectations honestly at the end.** The plumbing is tested; the beats are
a first draft. Tell them to read the first few briefs critically and say which
items were useless, because the editorial judgment in those files is the actual
product and it cannot be got right in the abstract. Offer to tune whichever beat
produces the weakest items.

Never invent a source you did not open. Never promise the brief will cover
something you could not find a readable source for - say so instead, and tell
them which topic is thinly covered.
