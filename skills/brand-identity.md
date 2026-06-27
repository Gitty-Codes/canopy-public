---
name: brand-identity
type: lens
scope: universal
invocation: on-demand
description: >
  The Canopy's visual and verbal identity system — typography, color, space,
  agent card design, micro-copy register, and what it refuses to look like.
  Load when designing screens, reviewing visual direction, or writing UI copy.
hint_keywords: [brand, design, visual, UI, wireframe, typography, color, style, logo, identity, copy, micro-copy]
---

# Brand Identity — The Canopy

*Derived from council deliberation, June 13, 2026.*
*The constitution informs every visual decision here.*

---

## What The Canopy looks like — and why

The Canopy is built from words. Deliberation, constitution, reasoning made legible.
The visual system trusts type over decoration. Words do the work because words are
the product.

The AI product aesthetic of 2026 — gradients, particle effects, blue glow, Inter
font in all caps, floating 3D cards — signals: venture-backed, optimized for demos,
probably won't last. The Canopy's visual language signals the opposite: something
built with intention, not investment. Restrained and warm. Precise and alive.

The canopy metaphor — shelter, cover, conditions for more life, light filtering
through leaves — lives in the *feeling* of the brand, not the graphic elements.
No leaf graphics. No forest photography. The warmth and breathing room are
the metaphor.

---

## Typography

**Primary: Serif for headings and agent names.**
Carries weight. Signals permanence and document-quality. The Cultural Constitution
is a founding document — the visual system should feel like one too.

Candidates: Lora, Playfair Display (more expressive), Source Serif 4, or EB Garamond.
*Do not use: display serifs, slab serifs, or anything that reads as decorative.*

**Secondary: Humanist sans-serif for body, UI text, and labels.**
Warm and readable. Not geometric (too cold). Not grotesque (too neutral).
Humanist forms have human energy.

Candidates: Source Sans 3, Inter (used sparingly, not as the hero), or Nunito Sans.
*Do not use: geometric sans like Futura, or anything that reads as "tech startup."*

**Scale discipline:**
- H1 (screen titles): 28–32px, serif, warm charcoal
- H2 (section headers): 20–24px, serif or sans-serif
- Body: 15–16px, humanist sans, line-height 1.6 (room to breathe)
- Agent name: 14–15px, serif, uppercase tracking — distinctive but not decorative
- Agent question: 11–12px, sans, muted charcoal — subtitle beneath the name
- Micro-copy (labels, placeholders): 13px, sans, medium weight

---

## Color

**Background: Warm off-white**
Not clinical white (#fff). A warm off-white: `#FAF8F4` or `#F7F5F0`.
Clean but not cold. The page breathes.

**Text: Warm charcoal**
Not pure black. A warm charcoal: `#2C2A27` or `#1F1E1B`.
Reduces harshness. More alive on the warm background.

**Primary: Deep forest green**
The canopy metaphor, carried structurally not decoratively.
Used for: primary buttons, active states, key UI elements, the app header.
Target: `#2D5016` (deep) or `#3A6B1A` (slightly lighter). Dark, confident, not corporate.
Not a "nature" green — a serious green.

**Accent: Deep amber / warm gold**
Used very sparingly: save/confirm actions, success states, the occasional emphasis.
Target: `#C4860A` or `#A8720A`. Warm, earned, not aggressive.
*One accent only. Do not add a second.*

**Surface / card background:**
Slightly off the main background: `#F0EDE8` or `#EDE9E3`. Creates depth without shadow.

**Muted text / secondary:**
`#6B6560` — for labels, secondary information, the agent's primary question beneath
their name on the council screen.

**What is never used:**
- Blue (the default SaaS/AI color — actively avoided)
- Pure black or pure white
- Gradients
- Opacity effects that create glass morphism
- Drop shadows heavier than `0 1px 4px rgba(0,0,0,0.06)`

---

## Space

Generous. Each element needs room. The Council screen is not a dashboard —
it is a room where distinct voices are present.

**Base spacing unit: 8px**
Standard: 8, 16, 24, 32, 48, 64px increments.

**Card padding:** 20–24px internal. Not tight. The agent needs room to exist.

**Between agent cards:** 16px. Close enough to read as a sequence,
far enough to read as distinct entries.

**Content max-width:** 720px on wide screens. Not full-bleed. The product
is a focused tool, not a dashboard. Give it a spine.

---

## The Agent Card — The Core Design Problem

This is where the brand lives most vividly. Get this right.
Everything else follows from the agent card design.

**Each agent card contains:**
```
┌─────────────────────────────────────────────────────┐
│ [left border — 3px, agent color]                    │
│                                                     │
│  THE GUARDIAN                                       │  ← serif, small caps
│  What could go wrong, and who could be harmed?      │  ← sans, muted, 11px
│                                                     │
│  [agent response text — 15px humanist sans,         │
│   line-height 1.6, warm charcoal]                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Agent differentiation:**
Agents are subtly distinguished by a 3px left border in a unique muted color.
Not bright colors — muted, dignified. Examples:
- The Elder: muted sage `#7A9A6B`
- The Guardian: muted clay `#9A6B5B`
- The Listener: muted slate `#6B7A9A`
- The Challenger: muted amber `#9A7A3A`
- The Strategist: muted indigo `#5B6B8A`
- (etc. — consistent across the app, subtle enough to inform without decorating)

These colors are subtle signals, not primary branding. The hierarchy is:
name first, question second, response third.

**Working state:**
When an agent is working, the card shows:
- Name + question (same as complete)
- A subtle animated underline or single pulsing dot beneath the name
- No spinner, no progress bar with percentage — too mechanical
- The response area is empty, slightly dimmed

**Complete state:**
Response fills in. Border appears in full opacity. Card is static.

**Pending state (agents not yet reached):**
Name only, smaller, in a muted row below active cards.
Not cards — just names in a horizontal list: `○ The Builder  ○ The Elder`

---

## Synthesis Card

The synthesized result appears below the agent cards, visually separated.

```
┌─────────────────────────────────────────────────────┐
│ [full-width top border — 2px forest green]          │
│                                                     │
│  SYNTHESIS                                          │  ← serif, small caps, green
│                                                     │
│  [synthesized text — same 15px body, warm charcoal] │
│                                                     │
│  [Save to Drive ↑]  [Open in Canva]  [Copy]         │
└─────────────────────────────────────────────────────┘
```

The synthesis card is distinguished by the full green top border, not a left border.
It is the result of all the voices — its visual treatment reflects that: it doesn't
belong to one agent, it belongs to the council.

---

## Micro-Copy Register

UI copy is written in The Canopy's voice: direct, warm, specific, not technical.
The founder voice profile applies here.

**Placeholder text in the workspace input:**
→ `What do you want to work on today?`
Not: `Enter your prompt here` / `Ask the council` / `Type a message...`

**Empty state — no projects yet:**
→ `You haven't started a project yet. Create one to begin.`
Not: `No projects found` / `Get started!` / `Create your first project`

**Connection status — Google not connected:**
→ `Google Drive not connected — outputs won't be saved automatically.`
Not: `Connect Google Drive to unlock features!`

**Working state header:**
→ `The council is working on: [task description]`
Not: `Processing...` / `AI is thinking...`

**Error state — API failure:**
→ `The council ran into a problem. Nothing was lost — try again.`
Not: `Error 500` / `Something went wrong` / `Please try again later`

**Success — saved to Drive:**
→ `Saved to Google Drive.` (then the link)
Not: `Success! Your document has been saved.`

The register: short, honest, warm, no exclamation points. A sentence that
could come from a person who respects the user's time.

---

## What The Canopy Never Looks Like

- Blue as a primary color (too AI-generic)
- Dark mode as the default (warm off-white is the identity; dark mode is an option)
- Full-bleed hero images or photography
- Gradient backgrounds or buttons
- Floating cards with heavy drop shadows
- Rotating/animated logos
- "✨" or emoji in UI copy
- Sans-serif-only typography (loses the document-weight the brand needs)
- Three-column dashboards
- Sidebar navigation with 12+ items
- Any visual element that would look at home in a generic SaaS product

---

## Logo Direction

*Updated: June 2026 — dome mark adopted.*

**The mark: a dome — ~270° of a circle, open at the bottom.**
SVG path: `M8,44 A24,24 0 1,1 52,44` — large-arc, sweep clockwise, open base.
The form is a shelter you can enter: contained world above, open threshold below.
No gradient. No fill. Stroke only. Round linecaps.

Inspired by: the Ohm sign without the tail. A snowglobe cut at the base.
A canopy in the literal sense — overhead, open, inviting entry.

**Primary color: Forest green `#2D5016` on warm cream `#FAF8F4`.**
No other color is the primary mark. Amber `#C4860A` is a permitted alternate
for Practice Buddy contexts (warmer, more youth-facing). Deep red and blue
do not appear in the primary mark.

**Wordmark: mixed case, not all-caps.**
"The Canopy" in Lora 700, `#2C2A27`, letter-spacing 1.5px.
Not "THE CANOPY" — mixed case reads as a place name, not a product label.

**Taglines — two, for two moments:**
- *"Think it through."* — functional tagline. Lives in the lockup, the header,
  the moment before someone begins working. Why you come here.
- *"Welcome home."* — relational tagline. Lives in first login, onboarding,
  the return visit. How it feels to be here. Used after trust is established,
  not as the first thing someone sees.

**Stroke weight: medium (stroke-width 4–5.5 depending on viewBox).**
Holds from 24px to 96px. Confident without heaviness.

**Favicon:** the dome mark at 16px — dome stroke in forest green on cream.
Not the letterform C. The mark is distinctive enough at small size to carry it.

**What is never used in the mark:**
No gradient. No fill. No glow. No animation. No leaf graphics.
The dome is the mark. It does not need help.

---

## Application to the Three Screens

**App header (all screens):** Dome mark (~32px tall) + "The Canopy" in Lora 700
+ "THINK IT THROUGH" in Source Sans 3, 8.5px, letter-spacing 2px, muted `#B0ABA5`.
Nav links (Projects, Memory, Settings) in the secondary type. "New project" button
in forest green. Cream background `#FAF8F4`, 1px warm border bottom `#DDD9D3`.
Height: 48px. This header is the established pattern — don't vary it.

**Screen 1 (Home):** Warm, minimal. Project cards in the surface color.
"Good morning, Sarah" in the heading serif, warm and personal. Connected
services shown as small, clean status tags — not icons with badges.
First login only: "Welcome home." in italic Lora beneath the user's name —
the relational tagline used once, at the moment it's true.

**Screen 2 (Workspace):** Tool mode. The typography tightens slightly.
The quick action chips: small, sans, forest green border on hover.
The input box: generous padding, placeholder in muted charcoal, no border
until focused (then a 1px forest green border).
The sidebar (recent + files): muted background, smaller type, links in forest green.

**Screen 3 (Council in Session):** The most designed screen. Agent cards
stream in as agents complete. Each card distinct but part of a coherent set.
The synthesis card anchors the bottom. This screen should feel like something
is genuinely happening — not because of animation, but because the content
is arriving with intention.

---

## Reference figures

When a design decision is unclear, ask what these people would do with it.
Not "what would they literally make" — what *principle* would they apply?

**James Baldwin — voice and micro-copy**
Baldwin trusted the reader completely. He gave the truth whole, without softening
it for easier consumption, and his sentences landed because they were precise and
earned. The Canopy's copy register should feel like this: direct, warm, specific,
nothing wasted. When you're tempted to soften a UI string or add an exclamation
point to be encouraging, ask what Baldwin would cut. He would cut almost everything
that apologizes for itself.

**Dieter Rams — visual discipline**
"As little design as possible." Rams designed Braun products for thirty years with
complete consistency — restraint not as minimalism but as respect. His ten principles
are practically constitutional: good design is honest, unobtrusive, long-lasting,
and as little as possible. When a design element is tempting, ask if it's doing
real work or performing sophistication. Rams would remove it if it was performing.

**Charles and Ray Eames — feeling**
They made serious things joyful without making them frivolous. They believed good
design was available to everyone, not only the wealthy. Their line: *"Take your
pleasure seriously."* The Canopy's warmth — the off-white surface, the breathing
room, the serif — should feel like their work: considered and alive at once. Not
cold precision and not decorative warmth. Both at the same time.

**Fred Rogers — the customer relationship**
Rogers spoke to each person as if their inner life was the most important thing
in the room. Not condescending — radically present. He testified before Congress
and changed a senator's mind by being exactly himself. When writing onboarding
copy, empty states, or any moment where the user is uncertain, ask how Rogers
would address them: directly, warmly, without performing care. The register is
not childlike — it is genuinely regarding.

---

## How to use this skill

**When designing screens:** Apply the typography scale, color system,
and agent card design. The council screen is always the reference.

**When writing UI copy:** Apply the micro-copy register. Short, honest,
warm, no exclamation points. A sentence from a person who respects the user.

**When reviewing designs:** Check against the "What The Canopy Never Looks Like"
list. If any prohibited element is present, name it and propose the alternative.

**When this skill doesn't have the answer:** The constitution does.
"Are we being who we say we are?" is the test. Apply it visually.
