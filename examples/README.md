# Example beats

The beats in `.claude/agents/` are tuned for outside plant fiber design and QC,
because that is what the person who built this kit does. That makes the shipped
example coherent - you can run `/brief` before changing anything and get a real
brief rather than a demo - but it also makes the repository *look* like a
telecom tool, which it is not.

These files exist to show that. They are the same structure as the beats that
ship, for fields with nothing to do with telecom:

| File | Field |
|---|---|
| `beats/real-estate-market-drivers.md` | Commercial real estate underwriting |
| `beats/data-center-market-drivers.md` | Data center siting and delivery |

Read either one next to `.claude/agents/market-forces.md` and the only thing
that changed is the subject. The scaffolding - reading `covered.json` first,
opening every source before reporting it, the output format, the item cap, the
`nothing new` rule - is identical, because that scaffolding is what makes the
brief trustworthy regardless of what it is about.

## These are not running

Nothing in `examples/` is loaded. Beats only run from `.claude/agents/`, and
they only run if `.claude/commands/brief.md` names them in its spawn list.

## They have no source lists, on purpose

Both files stop short of listing URLs. The beats that ship list sources that
were opened and checked first; nobody has done that for these two, and a list of
plausible-looking links that nobody verified would teach exactly the habit the
rest of the file argues against.

Instead each one carries a research brief: where to look, in what priority
order, and how to judge a candidate before relying on it.

**`/setup` does that work for you.** It interviews you, searches for candidates
in your field, opens each one to confirm it is live and readable without a
subscription, drops what fails, and writes finished beat files with real
sources. That is the intended path, and it is why these two were left
deliberately incomplete rather than filled in with guesses.

## Using one anyway

If your field is close to one of these and you would rather start here than run
the interview:

1. Copy the file into `.claude/agents/`.
2. Rewrite **Who you are reporting for** to describe you, in the second person,
   concretely. Every "why it matters" line gets judged against it.
3. Fill in **Starting sources**, opening each one before you list it.
4. Add the beat name to the spawn list in `.claude/commands/brief.md` step 2,
   and update the item-count arithmetic in step 3.
5. Add every new domain to your environment's network allowlist, or the beat
   will find things it cannot open.

Step 5 is the one people forget, and its symptom is a beat that quietly returns
almost nothing.
