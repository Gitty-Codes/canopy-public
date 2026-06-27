---
type: research
track: activism
layer: 1
topic: surveillance-exposure-mapping
status: IN PROGRESS
date: 2026-06-26
council-decision: Entry 011
---

# Layer 1 Research — Surveillance Exposure Mapping

*Research only. No build decisions until organizational conversations complete (Entry 011).*
*This document is the foundation for Layer 2 design once the founder brings back findings from the field.*

---

## What this research is for

Before designing any tool, the council needs to know: what data actually exists,
what legal options actually exist by jurisdiction, and what organizations are
already doing this work. This document collects that ground truth.

---

## I. Public Surveillance Camera Databases

### City-level (government cameras)

**New York City**
- NYC OpenData: `data.cityofnewyork.us` — intersection camera locations published
  for traffic cameras, school zone cameras, red light cameras
- NYPD surveillance: largely opaque; some locations via FOIA; Legal Aid Society
  and NYCLU have done FOIA-based mapping
- Project LINK (NYPD): aggregates private cameras into a network — not publicly mapped

**San Francisco**
- SFpark (SFMTA) publishes parking sensor and traffic camera locations
- SFPD surveillance policy: Board of Supervisors approved surveillance technology
  ordinance 2019 (one of the strongest in the US) — annual inventory reports public
  at sfbos.com

**Chicago**
- POD camera locations: published at data.cityofchicago.org
  ("Police Observational Devices" — ~30,000 cameras)
- Speed cameras: published at data.cityofchicago.org
- CPD Blue Light cameras: some locations public via Freedom of Information requests

**Los Angeles**
- LAPD camera inventory: partially disclosed via public records requests
  - LA Times and Knock LA have done significant mapping work
- Metro cameras: published at metro.net (transit surveillance is generally more transparent)

**Seattle**
- Seattle IT department publishes annual surveillance technology reports (mandatory
  by city ordinance — one of the strongest transparency requirements in the US)
  at seattle.gov/tech/initiatives/privacy

**London (reference — GDPR applies)**
- Met Police: some locations via Freedom of Information requests
- Transport for London: CCTV locations partially published via FOI
- This is the strongest legal jurisdiction for erasure requests (GDPR Article 17)

### Aggregated mapping efforts

**EFF Atlas of Surveillance** — atlasofsurveillance.org
- The most comprehensive public database of surveillance technologies by US jurisdiction
- Includes: drones, license plate readers, body cameras, gunshot detectors, face recognition
- Does NOT map individual camera locations — maps technologies by agency
- **High value for Layer 2 (rights assessment):** shows which agencies use face recognition
  (triggering BIPA/CCPA implications) vs. standard video only

**Open Street Map** — openstreetmap.org
- Community-tagged surveillance cameras (key: `surveillance=camera`)
- Variable quality; urban areas better than rural; community-maintained
- Coverage of ~500,000+ camera locations globally; US coverage patchy but growing
- API available for programmatic access

**Surveillance under Surveillance** — kamba.de/surveillance/
- European-focused OSM-derived surveillance map
- Less relevant for US but shows what's possible with community tagging

### What doesn't exist yet

- A real-time, comprehensive, city-by-city database of private business cameras
- Any systematic mapping of smart glasses or wearable camera deployment
- Residential doorbell camera coverage (Ring/Nest) — Amazon and Google hold this;
  Amazon has police partnership programs but doesn't publish location data publicly

---

## II. Legal Landscape — US Jurisdictions

### What matters: which states have enforceable private rights

The founder's idea (automated erasure/takedown requests) only works where there
is legal standing. This map shows where legal standing exists.

#### Strong — private right of action

**Illinois — BIPA (Biometric Information Privacy Act)**
- Strongest biometric privacy law in the US; private right of action
- Covers: fingerprints, retina/iris scans, face geometry, voiceprints
- Requires written consent before collecting biometric data
- $1,000/violation (negligent), $5,000/violation (intentional or reckless)
- **Surveillance application:** Any face recognition system without prior written
  consent violates BIPA. Private right of action means individuals can sue directly.
- **Erasure path:** BIPA requires destruction of biometric data within 3 years
  or when purpose fulfilled; written policy required

**Texas — CUBI (Capture or Use of Biometric Identifier)**
- Requires consent before capturing biometric identifiers
- Private right of action: $25,000/violation
- Similar scope to BIPA; less litigation history

**Washington — My Health MY Data Act (2023)**
- Covers health data including biometric data; private right of action
- More limited scope than BIPA but growing

#### Moderate — regulatory enforcement, no private right of action

**California — CCPA/CPRA**
- Right to deletion (erasure) for personal data including biometric data
- Right to know what's collected and to opt out of sale
- Enforcement: California Privacy Protection Agency (CPPA); limited private right
  (only for data breaches, not general violations)
- **Practical implication:** Strong for established companies meeting threshold
  ($25M+ revenue OR 100K+ consumers' data); weak for small businesses
- **Surveillance application:** If a business uses face recognition and retains
  your biometric data, CCPA deletion requests have legal grounding for CA residents

**Virginia, Colorado, Connecticut, Oregon** — have comprehensive privacy laws;
deletion rights exist; enforcement by AG only; no private right of action

#### Weak — no private right, no biometric-specific law

Most US states: Georgia, Missouri, Florida, Texas (before CUBI), etc.
General common law privacy (intrusion upon seclusion, appropriation) exists
but is hard to apply to surveillance in public spaces.

#### Federal landscape

**No federal biometric privacy law** exists in the US as of 2026.
BIPA preemption litigation is ongoing; some industries argue federal law preempts
state biometric laws (financial services most active).

**Copyright angle (founder's original idea):** As assessed in COUNCIL-BRIEF-2026-06-26.md,
copyright is the wrong frame. You do not hold copyright over your likeness recorded
in a public space in the US. The right frame is privacy/biometric, not copyright.

#### EU — GDPR (for context; strong, applicable to EU residents)

**GDPR Article 17 — Right to Erasure ("Right to be Forgotten")**
- Applies to any data processor handling EU residents' personal data
- Includes biometric data (special category under Article 9)
- Organizations must respond within 30 days
- Enforcement: national data protection authorities with significant fine authority
- **This is the strongest legal hook for automated erasure requests globally**
- UK GDPR (post-Brexit) has equivalent provisions

---

## III. What Already Exists — Organizations and Tools

### Surveillance rights organizations

**Electronic Frontier Foundation (EFF)** — eff.org
- Atlas of Surveillance: most comprehensive US surveillance tech database
- Surveillance Self-Defense (ssd.eff.org): practical guides for individuals
- Active in policy and litigation; not primarily a tool-builder
- **Conversation candidate for founder (Entry 011)**

**ACLU** — aclu.org/issues/privacy-technology/surveillance-technologies
- Campaigns and litigation on surveillance; less tool-focused
- State affiliates vary significantly in surveillance work

**Fight for the Future** — fightforthefuture.org
- Campaigns specifically on face recognition bans
- Has organized city-by-city bans (15+ cities, including San Francisco, Boston)
- More campaign-focused than tool-focused

**Big Brother Watch** (UK) — bigbrotherwatch.org.uk
- UK-focused; strong on face recognition; publishes police camera maps via FOI
- Template for what a UK-focused tool would look like

**Surveillance Technology Oversight Project (STOP)** — stopspying.org
- NYC-based; focuses on municipal surveillance policy
- Has done significant mapping and FOIA work on NYPD surveillance

### Existing tools

**Privacy Badger** (EFF) — browser extension, not location-based
**Tor Browser** — anonymization, not surveillance mapping
**Jumbo** — privacy assistant app; handles social media and some data deletion requests
  - Closest existing thing to the founder's idea; handles data broker removal
  - Does NOT handle physical surveillance / camera systems
  - **Worth looking at as a design reference**

**Have I Been Pwned** — breach notification; not surveillance

**Nothing directly does what the founder described** — no tool maps physical
surveillance exposure along a route and generates location-specific legal requests.
This is a genuine gap.

---

## IV. The Collective Action Mechanism — Research Notes

The most strategically interesting insight from the council (Entry 011):
coordinated simultaneous requests create administrative cost even where
individual legal standing is weak.

**Precedents for this approach:**

**GDPR collective complaint model**
- noyb.io (Max Schrems' organization) files coordinated GDPR complaints
  against companies on behalf of thousands of individuals simultaneously
- Administrative cost of processing 10,000 complaints exceeds any individual
  complaint's enforcement risk → creates real pressure
- This is the model to study

**Lumen Database** — lumendatabase.org
- Tracks DMCA takedown notices; shows the volume of copyright requests
  Platforms receive → illustrates the administrative cost argument
- Different legal frame (copyright not privacy) but the volume mechanism is visible

**Data broker opt-out services**
- Privacy.com, DeleteMe, Kanary aggregate and automate opt-out requests to
  data brokers — the closest model for what the tool would do at scale
- These work within clear legal rights (CCPA for CA users); the surveillance
  tool needs equivalent clear legal grounding by jurisdiction

---

## V. What the Layer 2 Design Brief Needs (post-conversation)

After the founder's organizational conversations, the Layer 2 design brief should answer:

1. **Which jurisdiction to design for first?** Illinois (BIPA) and California (CCPA)
   are the strongest legal environments. EU users have GDPR. Start with one.

2. **What does the tool know vs. what does it look up?**
   - Static: public camera database (EFF Atlas, city OpenData, OSM)
   - Dynamic: user's location log (phone-side, local only)
   - Generated: jurisdiction-specific rights assessment per data processor

3. **What does "a data processor on your route" mean technically?**
   - City camera → city agency (FOIA + rights request)
   - Business camera → business entity (CCPA/BIPA if applicable)
   - Individual wearing smart glasses → no clear data processor; different approach
   - Face recognition specifically → strongest legal ground (BIPA/Texas CUBI)

4. **Who maintains the database?**
   Community-maintained (OSM model) vs. FOI-aggregated vs. real-time scraping.
   Community model is most privacy-preserving; FOI-aggregated is more reliable;
   real-time scraping creates its own privacy risks.

---

## Open Questions for Organizational Conversations

**For homelessness services org:**
- What data do you need to help someone navigate benefits?
- What happens when someone's information is in multiple city databases?
- What tools have been tried and failed, and why?
- What would you actually use if you had it tomorrow?

**For surveillance rights org:**
- What's the most effective legal mechanism in your jurisdiction right now?
- Has any tool for individual erasure requests worked at scale?
- What does the collective complaint model look like in the US?
- Who else should we talk to?

---

*Layer 1 research is a living document. Update as new sources are found.*
*Layer 2 begins after organizational conversations. Not before.*
