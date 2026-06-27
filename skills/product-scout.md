---
name: product-scout
type: playbook
scope: universal
invocation: on-demand
description: Structured protocol for researching competing products, tools, or vendors — feature audit, pricing, user signals, fit score
---

# Product Scout — Research Protocol

Use when evaluating: competing products, tools under consideration, vendors, or market alternatives before building or recommending.

The goal is not to produce a ranking. It is to surface what each option is actually good at, who it serves, and where it fails — so the founder can make a grounded decision.

## The Five Dimensions

### 1. Feature Parity

What does it do? What does it explicitly not do?

- Core feature list (what it's designed for)
- Notable gaps (what users ask for that doesn't exist)
- Edge behaviors (what happens at the limits of its design?)
- Platform availability (mobile? web? API? offline?)

Do not infer from the marketing page. Check: product changelog, user reviews, community forums, support tickets where visible.

### 2. Pricing and Access

- Pricing model: per-seat, usage-based, tiered, freemium?
- Who can afford it? (Is this enterprise-only in practice?)
- What's behind a paywall that matters?
- Free tier limits — do they matter for the actual use case?
- Contract terms: annual lock-in? data portability on exit?

### 3. User Signals

Go to where users speak unfiltered: Reddit, app store reviews, G2/Capterra, Hacker News "Ask HN" or "Show HN" threads, Twitter/X, community Slack/Discord.

Look for:
- Recurring complaints (not one-off)
- What users switched from (and why)
- What users switched to (and why they left)
- What the power users love that casual users never discover

A product with 4.5 stars and 200 reviews saying "setup is a nightmare" is telling you something the homepage isn't.

### 4. Technical Signals

- Open source? Inspectable? Forkable?
- API availability — can you build on top of it?
- Data portability — can you get your data out?
- Infrastructure: self-hosted option? multi-tenant SaaS? where is data stored?
- Security posture: SOC 2? GDPR? COPPA compliance?

### 5. Growth and Decay Signals

Is this product in its prime, rising, or declining?

- Recent release cadence (GitHub commits, changelog dates)
- Community growth (Discord members, Twitter followers trending)
- Funding signals (recent raise = growth phase; no news for 2+ years = possible stasis)
- Job postings (hiring = expanding; layoffs = contracting)
- Acquisition rumors or actual acquisition (acqui-hire = product may be sunsetted)

## Output Format

For each product evaluated, produce:

```
## [Product Name]
**Fit score: X/10** (for [specific use case])

**Strengths:**
- [concrete strength with evidence]

**Gaps:**
- [concrete gap with evidence]

**User signal summary:**
[2-3 sentences on what users actually say]

**Technical notes:**
[relevant API, data, security, or platform constraints]

**Pricing reality:**
[what it actually costs for this use case]

**Verdict:**
[one sentence: who this is for and who it isn't for]
```

## Fit Score Rubric

Score against the specific use case, not against some abstract ideal:

| Score | Meaning |
|-------|---------|
| 9-10 | Strong match — meets all core requirements, no major tradeoffs |
| 7-8 | Good match — meets most requirements, one or two manageable gaps |
| 5-6 | Partial match — covers the core but requires workarounds |
| 3-4 | Poor match — significant gaps or requires fundamental adaptation |
| 1-2 | Wrong tool — would require rebuilding the core capability |

A 6/10 for one use case can be a 9/10 for a different one. Always score against the stated context.

## Comparison Summary

After individual profiles, produce a one-table comparison:

| Product | Fit Score | Strongest For | Key Gap | Price Reality |
|---------|-----------|---------------|---------|---------------|
| A | 8/10 | ... | ... | ... |
| B | 5/10 | ... | ... | ... |

Close with a recommendation and the one tradeoff the founder should know before deciding.
