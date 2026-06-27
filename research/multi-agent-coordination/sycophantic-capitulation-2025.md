# Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate
*Filed: 2026-06-07 | Source: arxiv 2509.05396, September 2025 | Signal: High*

## Why this matters to the Canopy
This paper names the most dangerous failure mode for a council built on one model
instantiated in multiple voices: sycophantic capitulation — agents shift from correct
to incorrect positions under social pressure, even when the challenging position is
wrong. This is a current Canopy vulnerability.

## Key findings
- Primary failure mode: agents shift from correct to incorrect answers in response
  to peer pressure, even when the peer's reasoning is flawed
- Debate harms performance even when stronger models outnumber weaker ones —
  majority-competence is not a safety guarantee
- CommonSenseQA debate always degrades performance — value-laden judgment tasks
  are especially vulnerable (Canopy's primary domain)
- The failure is structural, not model-specific

## What it changes or validates
- **Urgent gap:** there is currently no mechanism in the Canopy harness that prevents
  a Challenger's DISSENT from being soft-overridden by the synthesis voice. The
  synthesis turn can report consensus while a live DISSENT is silently absorbed.
  Dissent must persist in the decision packet, not just be heard and integrated away
- **Validates:** the Challenger's structural independence ("cannot be the same
  reasoning process that just agreed") — but independence in the voice definition
  is not enough without a protocol-level guarantee that dissent persists
- **Implication for v2:** the decision packet (borrowed from DCI above) should be
  a required output structure for council_respond(), not just the synthesis prose
