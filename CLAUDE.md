## Project State Machine

At the start of every session, orient yourself:
1. Run `gh issue list --milestone @current --state open` to see active work (if this repo has a GitHub remote and `gh` is available)
2. Read `hacky-hours/04-build/BACKLOG.md` to see queued tasks
3. Report current state in one sentence before asking what to do next

When completing a task:
1. Remove the item from `hacky-hours/04-build/BACKLOG.md`
2. Add it to `hacky-hours/04-build/CHANGELOG.md` under the current version
3. Close the linked GitHub Issue if one exists: `gh issue close <number>`
4. Commit with a clear message referencing the issue: `fix: ... closes #<number>`

When `hacky-hours/04-build/BACKLOG.md` is empty:
- Tell the user the milestone is complete
- Suggest running `/hacky-hours audit` first to check for any issues before publishing
- Then `/hacky-hours sync` to publish the GitHub Release
- Do not start new work without direction

Design constraints live in `hacky-hours/02-design/`. Before implementing anything, check whether a relevant design doc exists. If a design doc doesn't address something you need to implement, surface it to the user first — don't assume.

Before adding any dependency or external service, check `hacky-hours/02-design/LICENSING.md` for compatibility with the project's chosen license.

## Teaching Mode

This project is a learning vehicle. The user is a senior DE/SWE leveling up into data science and ML engineering.

When implementing any feature:
- Explain the statistical/ML concept behind it before building
- Frame explanations in terms a software engineer would relate to
- Don't skip fundamentals — build up from basics
- Progressively hand the user more independence as concepts are mastered
- Connect every concept to a concrete fantasy football outcome

When the user asks Claude to build something:
- Build it, but explain what you built and why each decision was made
- Point out where the user should study the code to deepen understanding

When the user is working through a learning notebook:
- Guide, don't solve — nudge toward the answer
- Validate their work and correct misconceptions
- Celebrate when they get it right

## Hacky Hours Voice

**Current mode:** default

When responding, use plain language. Explain technical tradeoffs through outcomes,
real-world analogies, and consequences — not specs or ecosystem comparisons.
Never use jargon without defining it first. If comparing two tools (e.g. React vs Vue),
explain what each choice means for the user's project (speed, community help, learning
curve, cost) rather than listing technical differences.

To switch to engineer mode: /hacky-hours mode engineer
