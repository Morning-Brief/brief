# Setup

One-time setup to get the brief arriving on your phone each morning and readable
on your PC. Everything here is done in a browser - no terminal, no local install.

> **Most people should not read this file.** Open your repository at
> [claude.ai/code](https://claude.ai/code) and run **`/setup`** instead - it
> interviews you, finds and verifies sources for your topics, writes your beat
> files, and gives you a short list of things to click. This document is the
> manual path, and a reference for anything `/setup` hands back to you.

Work through the steps in order; later steps need values from earlier ones.
**Step 3 is optional** and can be skipped entirely.

| | | |
|---|---|---|
| [1](#step-1---make-your-own-copy) | Make your own copy | 1 min |
| [2](#step-2---choose-how-the-brief-reaches-you) | Choose how the brief reaches you | 1 min, or 5 with Pushover |
| [3](#step-3---deploy-the-site-on-cloudflare-optional) | Deploy the site on Cloudflare | **optional**, 5 min |
| [4](#step-4---create-a-cloud-environment) | Create a cloud environment | 5 min |
| [5](#step-5---create-the-routine) | Create the routine | 3 min |
| [6](#step-6---confirm-you-cant-be-billed) | Confirm you can't be billed | 1 min |
| [7](#step-7---test-it-now) | Test it now | 10 min of watching |

Afterwards: [what each file does](#what-each-file-does) ·
[pruning covered.json](#pruning-coveredjson) · [when something breaks](#step-7---test-it-now)

### What `/setup` would have asked you

If you are here because you would rather do this by hand, these are the seven
questions the interview asks. They are worth answering on paper first even if
you never run `/setup`, because your beat files in `.claude/agents/` get written
from them, and a vague answer here produces a vague brief:

1. **What do you do?** Role, industry, and what a normal working day involves.
2. **What do you already know cold?** Whatever is on your radar every day, so
   the brief can skip it instead of telling you things you know.
3. **Where are you trying to get to?** A promotion, a certification, a move into
   management, a different specialty. This decides what counts as useful.
4. **What do you want tracked, and where?** Plain topics, as many as you like.
   You do not need to name a single website. If a region matters, say so:
   "telecom, but the Northeast", "multifamily, Phoenix and Tucson". Geography
   changes a source list more than almost anything else.
5. **Any sources you already read and trust?** Optional. They go in first.
6. **Anything you specifically do not want?** Vendor press releases, stock
   analysis, conference marketing, whatever wastes your time.
7. **What should it be called?** The name on the page and the notification.
   This becomes `BRIEF_TITLE` in Step 4.

Answers to 1 through 3 become the "Who you are reporting for" profile in each
beat file. Answers to 3 and 6 become the test for whether an item is worth
reporting. Answer 4 decides what the beats are, and answer 7 becomes
`BRIEF_TITLE` in Step 4.

Writing those files by hand is the one part of the manual path that is genuinely
more work than running `/setup`, which also goes and finds your sources. Copy an
existing file from `.claude/agents/` and replace only the beat-specific parts:
the description, the profile, the scope, the source list, and what makes an item
worth reporting. Leave the rest alone, since it encodes rules learned from real
failures.

**Time:** about 20 minutes. **Cost:** $0 - nothing here asks for a credit card.

---

## Step 1 - Make your own copy

On this repository's GitHub page, click **Use this template** → **Create a new
repository**.

Name it whatever you like. **Private is fine** - everything downstream works
with a private repository, and nothing here needs to be public.

If you don't see that button, click **Fork** instead. Either gets you your own
copy to edit.

**Success:** a repository under your own account with these files in it.

---

## Step 2 - Choose how the brief reaches you

Two ways, and you only need one. **Pushover is the one we recommend**, because
it is the only option that reaches you every single morning without fail. It
costs about $5 once on your phone's app store, on Android or iOS, and there is
no subscription.

The free alternative works and costs nothing, but the platform decides whether
to send it, so it can quietly not arrive. Both are written out below.

<details open>
<summary><b>Option A - Pushover (recommended, about 5 minutes, ~$5 once)</b></summary>

You get a purpose-built message rather than a run summary: the top headline as
the notification text, a per-beat tally, and a **Read the brief** button that
opens straight to that morning's page. Quiet days are sent silently at low
priority, so a slow news day never wakes you up.

**On your phone:**

1. Install **Pushover** from Google Play or the App Store
2. Open it and sign in, or create an account. The app gives you a free trial
   and then asks for the one-time purchase

**On any browser:**

3. Sign in at **https://pushover.net**
4. Copy **Your User Key** from the dashboard. This is `PUSHOVER_USER`
5. Scroll down and click **Create an Application/API Token**. Name it anything,
   "Daily brief" is fine, and create it
6. Copy the **API Token/Key** it shows you. This is `PUSHOVER_TOKEN`

Keep both somewhere temporary. They go into the environment in Step 4, and never
into the repository.

**Set both or neither.** Setting only one of the pair is treated as a mistake
and reported, because it almost always means a typo rather than a choice.

</details>

<details>
<summary><b>Option B - The routine's own notification (free, no account, less reliable)</b></summary>

A Claude routine can notify you when a run finishes: **push** to the Claude app
on your phone, **email** to your inbox, or both. There is nothing to install, no
account to create, and no keys to manage.

**How to turn it on:** you do not do anything here in Step 2. When you create the
routine in Step 5, switch on **Push**, **Email**, or both in its notification
settings. Leave `PUSHOVER_TOKEN` and `PUSHOVER_USER` out of Step 4 entirely, and
the notification step will detect they are missing and skip itself cleanly.

The brief command leads its final message with the link to that morning's page,
so what arrives is tappable straight through to the brief.

**The catch, stated plainly.** This notification is a summary the platform
chooses to send when a run finishes. It is not a message this kit controls, and
it is best-effort rather than guaranteed. In testing here, a completed run
produced no email at all. It may work perfectly for you, but you have to check.

**So verify it on day one.** After Step 7's **Run now**, confirm something
actually reached you. If nothing did, go back to Option A. Pushover fires every
time because `notify.py` calls the Pushover API directly, rather than waiting for
someone else to decide the run was interesting.

</details>

---

## Step 3 - Deploy the site on Cloudflare (OPTIONAL)

**You can skip this entire step.** Every brief is committed to your repository
as markdown, and GitHub renders markdown perfectly well on a phone. That is
already a complete working system: the brief gets written, saved and delivered
without Cloudflare existing.

What this step buys you is a nicer place to read: a clean page instead of a
GitHub file view, and an archive of past briefs at their own URLs.

**Skipping it?** Leave `SITE_BASE_URL` out of Step 4. The pipeline notices it is
missing and simply reports the brief without a link instead of failing. Nothing
else changes. Jump to Step 4 now.

**Doing it?** Do it before Step 4, because it produces the URL Step 4 needs.

The repository carries a `wrangler.jsonc` that serves `site/` as static assets.
There is no Worker script and none is needed - requests are handled by
Cloudflare's asset path, with no cold start and no CPU billing.

1. Sign in at **https://dash.cloudflare.com** (no card required)
2. **Compute (Workers & Pages)** → **Create** → **Import a repository**
3. Authorize Cloudflare's GitHub app and grant it access to your repository
4. On the **Set up your application** screen:

   | Field | Value |
   |---|---|
   | Project name | whatever you want - it becomes part of your URL |
   | Build command | *leave empty* |
   | Deploy command | `npx wrangler deploy` (already filled in - keep it) |
   | Builds for non-production branches | uncheck |

   The empty build command is correct, not an oversight. The pipeline commits
   finished HTML, so there is nothing to compile.

5. Click **Deploy**

**Success:** a live `*.workers.dev` URL showing *"No briefs yet."* That is the
right answer - no brief has run.

**Copy that URL.** It is `SITE_BASE_URL` in the next step.

### Optional - put the site behind a login

The site is public by default: anyone with the URL can read it. To lock it down,
turn on **Protect with Cloudflare Access** - it's on the deploy screen, free for
up to 50 users, and gives you a one-time email code when you open the site. You
can also enable it later from the project's settings.

---

## Step 4 - Create a cloud environment

This controls what the daily run can reach on the network, and holds your site
URL - plus your Pushover keys, if you chose Pushover in Step 2.

**Create a new environment - do not edit your Default one.** Default uses
*Trusted* access, which allows package registries and dev domains that your other
work probably needs. Narrowing it would break that.

1. Go to **https://claude.ai/code**
2. Click the **cloud icon** above the message box → **Add cloud environment**
3. **Name:** anything, e.g. `daily-brief`
4. **Network access:** select **Custom** - the *Allowed domains* box only appears
   once you do
5. Paste the domain list below into **Allowed domains**

```
lightwaveonline.com
*.lightwaveonline.com
fierce-network.com
*.fierce-network.com
telecompetitor.com
*.telecompetitor.com
bbcmag.com
*.bbcmag.com
isemag.com
*.isemag.com
fiberbroadband.org
*.fiberbroadband.org
fcc.gov
*.fcc.gov
ntia.gov
*.ntia.gov
tiaonline.org
*.tiaonline.org
itu.int
*.itu.int
ieee.org
*.ieee.org
bicsi.org
*.bicsi.org
thefoa.org
*.thefoa.org
pmi.org
*.pmi.org
asq.org
*.asq.org
iso.org
*.iso.org
nist.gov
*.nist.gov
ansi.org
*.ansi.org
astm.org
*.astm.org
esri.com
*.esri.com
qgis.org
*.qgis.org
autodesk.com
*.autodesk.com
bls.gov
*.bls.gov
lightreading.com
*.lightreading.com
broadbandbreakfast.com
*.broadbandbreakfast.com
benton.org
*.benton.org
statescoop.com
*.statescoop.com
ntca.org
*.ntca.org
ustelecom.org
*.ustelecom.org
nspe.org
*.nspe.org
roberthalf.com
*.roberthalf.com
qualitydigest.com
*.qualitydigest.com
elsmar.com
*.elsmar.com
construction-institute.org
*.construction-institute.org
iaf.nu
*.iaf.nu
sec.gov
*.sec.gov
federalregister.gov
*.federalregister.gov
trade.gov
*.trade.gov
reuters.com
*.reuters.com
corning.com
*.corning.com
prysmian.com
*.prysmian.com
prysmiangroup.com
*.prysmiangroup.com
commscope.com
*.commscope.com
att.com
*.att.com
verizon.com
*.verizon.com
frontier.com
*.frontier.com
lumen.com
*.lumen.com
api.pushover.net
```

   Leave **"Also include default list of common package managers"** unchecked -
   this project has no dependencies.

   `api.pushover.net` matters only if you chose Pushover in Step 2 - it is what
   lets that notification out. Drop the line if you are using the routine's own
   notification, which does not go through the allowlist at all.

   **This list matches the OSP/fiber beats shipped in this repository.** If you
   rewrite the beats for a different field, replace these with your own sources.

> **Or just use Full.** The agents drop any item they can't actually open, so
> unreachable sources are discarded rather than guessed at - the allowlist isn't
> doing quality control. What it does is limit where the beats can look, which
> particularly hurts a beat meant to follow good writing wherever it lives.
> Setting **Network access: Full** removes that ceiling and the maintenance. The
> isolation that matters is unchanged either way: the container is ephemeral and
> has no path to your own machine.
>
> Be aware that some sites refuse automated fetches regardless of your network
> setting - several major industry sites return 403 to any bot. Those items get
> dropped and reported. That is the rule working, not a misconfiguration.

6. In **Environment variables**, add what your brief is called and, if you set
   up a site, its URL:

```
BRIEF_TITLE=Daily morning brief
SITE_BASE_URL=https://your-project.your-subdomain.workers.dev
```

   `BRIEF_TITLE` names every page, the browser tab, and the phone notification.
   Set it to whatever your brief actually is - `Cap Rate Weekly`, `Field
   notes`, `Grid & Power` - and nothing anywhere will say someone else's
   subject back at you. Leave it out and it reads "Daily morning brief".

**Only if you chose Pushover in Step 2**, add these two as well:

```
PUSHOVER_TOKEN=your_application_api_token
PUSHOVER_USER=your_user_key
```

No quotes, no spaces around `=`, no trailing slash on the URL.

If you are not using Pushover, leave both of those out entirely. The
notification step detects that they are absent and skips itself cleanly - it is
not an error and your run is not a partial success. Setting only one of the pair
*is* an error, and it will be reported.

7. **Create environment**

> **On the keys.** Environment variables are visible to anyone using this
> environment - on a personal account, that's you. Pushover keys are low risk:
> worst case someone sends notifications to your phone. If one leaks, regenerate
> it on the Pushover dashboard and update it here.

---

## Step 5 - Create the routine

1. Go to **https://claude.ai/code/routines** → **New routine**

   Use the full form, not the "What do you want automated?" box - that drafts a
   paraphrase, and the exact wording below matters.

2. **Name:** anything, e.g. `Daily brief`
3. **Prompt:** paste exactly:

```
Run the daily research brief for this repository.

Read .claude/commands/brief.md and follow it exactly, start to finish. Every
step, in order, including rendering the site, committing, pushing, and the
notification step.

Work on the main branch and push directly to it. Do not open a pull request.

Do not skip the push. If it fails, say so plainly in your final message instead
of reporting success. If Pushover is not configured the notification step skips
itself, which is expected and is not a failure.

Begin your final message with the link to today's brief.
```

4. **Repositories:** your repository from Step 1
5. **Environment:** the one from Step 4 - **not** Default
6. **Connectors:** remove all of them. They are attached by default, and a
   routine runs unattended with no permission prompts, so anything left attached
   is usable without asking. This one needs none.
7. **Trigger:** Schedule → Daily → pick a time
8. **Create**

After creating it, check the **Runs with** row on the detail page and confirm it
lists only your repository and environment. If a connector is still there, click
**Edit** and remove it.

### Pick a time earlier than you want it

The routine **starts** at the scheduled time; the run takes 6-12 minutes and
there's a deliberate few-minute stagger on top. **Schedule it about 15 minutes
before you want the notification.** The offset is consistent per routine, so
after a few mornings you can tighten it.

### Switch on the notification you picked in Step 2

The routine's own **notification** settings are what deliver the brief if you
skipped Pushover. **Push** goes to the Claude app on your phone, **Email** goes
to your inbox, and you can have both. Because the brief command leads its final
message with the link, what arrives is tappable.

- **Not using Pushover?** Turn on Push, Email, or both. This is your delivery -
  leave them all off and nothing will reach you.
- **Using Pushover?** Turn them off, or you get two notifications every morning:
  Pushover's message and Claude's run summary.

---

## Step 6 - Confirm you can't be billed

Go to **https://claude.ai/settings/usage** and check that **usage credits are
off**.

That is the only path by which this could charge you. Off means a run is rejected
if you hit your plan limit. On means it continues on metered overage.

---

## Step 7 - Test it now

Don't wait until the scheduled time to discover a misconfiguration. Click **Run
now** on the routine and watch it.

- [ ] The beats run and return items (or an honest `nothing new`)
- [ ] `briefs/YYYY-MM-DD.md` is written
- [ ] `render.py` succeeds
- [ ] `git push` succeeds - **most likely to fail**
- [ ] Your phone gets a notification
- [ ] Cloudflare shows a new deployment within a minute or two *(only if you did
      Step 3)*
- [ ] Tapping the notification opens today's brief *(only if you did Step 3;
      otherwise open `briefs/` in your repository)*

**Push fails:** check whether `main` is a protected branch.

**No notification:** if you are using the routine's own notification, check that
**Push** or **Email** is actually switched on for the routine - off by default is
the usual cause. If you are using Pushover, confirm `api.pushover.net` is in the
allowlist and that both Pushover values are set. Either way the run log shows the
exact error, and a run that says it skipped the Pushover step is telling you it
found no keys.

**Site doesn't update:** confirm the Cloudflare project's production branch is
`main` and its build output directory is `site`.

---

## After setup

Nothing, from you. Each morning a cloud session starts on its own, researches,
writes, publishes, pushes, and notifies. You read it.

| You want to | Do this |
|---|---|
| Change the time | Routine detail page → edit the schedule |
| Pause it | Routine detail page → toggle in **Repeats** |
| Change what a beat covers | Edit the file in `.claude/agents/` and commit |
| Add or drop a source | Edit the agent file, and update the allowlist in Step 4 |
| Stop notifications | Turn off the routine's Push/Email, and remove `PUSHOVER_TOKEN` if set |
| See why a run did nothing | Routine detail page → open the run and read the log |

A green run status only means the session started and exited without an
infrastructure error. It does not mean the brief was any good. Open the run and
read it when something looks off.

## What each file does

| Path | What it is |
|---|---|
| `.claude/commands/setup.md` | The `/setup` interview. The easy path, and the one most people should use |
| `.claude/agents/*.md` | Your beats. One file per researcher, and where the quality lives |
| `.claude/commands/brief.md` | The pipeline the daily run follows, step by step |
| `render.py` | Turns `briefs/*.md` into the static site under `site/` |
| `notify.py` | Sends the optional Pushover notification. Skips itself cleanly when unconfigured |
| `covered.json` | The dedupe ledger: `{url, headline, date}` for everything ever reported |
| `briefs/` | Your archive, one markdown file per day, never pruned |
| `site/` | Generated output. Only served if you did Step 3 |
| `examples/beats/` | Beat files for fields outside telecom, to copy or read |
| `wrangler.jsonc` | Cloudflare config. Ignored entirely if you skipped Step 3 |

## Pruning covered.json

`covered.json` is a flat array of `{url, headline, date}`, where `date` is the day
the item **went into a brief**, not the article's publication date - which is
what makes pruning by age straightforward.

It grows by up to 23 entries per run at four beats - beats × the per-beat cap. Every agent reads the whole file before
searching, so once it's long it costs real context each run. Prune past roughly
300-500 entries.

```bash
jq 'length' covered.json                    # check size
jq '.[-400:]' covered.json > t && mv t covered.json   # keep the most recent 400
```

Pruning has one consequence: a pruned URL becomes eligible again, so an old item
can resurface. For news beats that's harmless - old news won't clear the bar
anyway. It matters more for a beat with no recency requirement, where a good
article from years ago is a legitimate item forever.

The files in `briefs/` are the real archive - committed and never pruned - so
nothing is lost by trimming the ledger. Keep it a valid JSON array; if it's
corrupt the pipeline stops rather than recreating it, because recreating would
erase the history and make the next brief repeat everything.
