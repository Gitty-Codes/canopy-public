# Public Domain Corpus Map
*Resonant Mind Training — Source Analysis*
*Version 0.1 — June 2026*

The training specification lists canonical sources without analyzing their copyright
status. This document maps each source to one of four categories:

- **PD** — Public domain, ingest directly
- **PD-T** — Original is public domain; verify specific translation
- **OUT** — Under copyright; use via informed synthetic generation
- **REACH** — Under copyright; worth pursuing rights holder outreach
- **COMMUNITY** — Indigenous/communal knowledge; frame as relationship, not licensing

---

## I. Definitive Public Domain (PD)

These can be ingested directly into the training corpus from Project Gutenberg,
Internet Archive, or primary source archives. No permission required.

| Source | Notes |
|---|---|
| William Shakespeare — complete works | All public domain. Gutenberg complete works: https://www.gutenberg.org/cache/epub/100/pg100.txt — plain text, plays separated by title headers, dialogue lines prefixed by character name in caps, stage directions inline. Priority scenes: extended arcs from Lear, Hamlet, Tempest (ethical weight, long relational arc); comedies (different relational register); Melian Dialogue echoes in the histories. |
| Anton Chekhov — complete short stories | Died 1904. Constance Garnett translations (1916–1922) also PD. 13 volumes on Gutenberg: The Lady with the Dog (#13415), The Duel (#13505), The Schoolmistress (#1732), Love and Other Stories (#13414), The Wife (#1883), The Horse-Stealers (#13409), The Cook's Wedding (#13417), The Darling (#13416), The Bishop (#13419), The Party (#13413), The Schoolmaster (#13412), The Chorus Girl (#13418), Letters (#6408). |
| Charles Darwin — notebooks, letters, *Origin* | Complete archive at darwin-online.org.uk — structured archive, searchable. Notebooks are the high-value source — show self-correction and uncertainty in real time. |
| Van Gogh — Letters to Theo | Died 1890. Complete letters at vangoghletters.org — complete and annotated. Extraordinary record of a creative mind in genuine uncertainty. |
| William James — *Principles of Psychology* (1890) | Gutenberg Vol 1: #57628, Vol 2: #57634. Chapters on habit and stream of consciousness are directly relevant. |
| Thucydides — *History of the Peloponnesian War* | Crawley translation: Gutenberg #7142. Melian Dialogue is the priority. |
| Confucius — *The Analects* | Legge translation: Gutenberg #4094. Use Legge as the safe choice; Waley PD status is borderline. |

---

## II. Public Domain With Translation Caveat (PD-T)

The original text is ancient and clearly in the public domain. The specific English
translation matters. Pre-1928 translations are safe in the US (published before
the current copyright threshold). Verify before ingesting any specific edition.

| Source | Safe translations | Notes |
|---|---|---|
| Tao Te Ching | Legge (1891): Gutenberg #216. Giles (1905): not on Gutenberg — check Internet Archive. Medhurst (1905): check Internet Archive. Multiple translations are a feature — prevents surface mimicry. | Multiple PD translations are a feature, not a limitation |
| Zhuangzi | Giles (1889): Gutenberg #59709 ("Chuang Tzu: Mystic, Moralist, and Social Reformer") | Playful, absurdist — a different relationship to certainty than Tao Te Ching |
| Sei Shōnagon — *The Pillow Book* | Gutenberg #76016 — translator not confirmed; verify it is Waley (1928) or another PD translation before ingesting | 11th century Japanese text; the phenomenological attention is the value |
| Rumi — Masnavi (Khuwaja 2025, CC0) | Internet Archive: https://archive.org/stream/the-masnavi-of-jalal-al-din-rumi-volume-1-part-1-final/The%20Masnavi%20of%20Jalal%20al-Din%20Rumi%20-%20Volume%201%20Part%201%20-%20Final_djvu.txt — CC0, modern rendering based on Nicholson. Not the original Nicholson translation — contemporary poetic voice. Usable; note in training data that voice is 2025, not 13th-century Persian. Nicholson's original (1925–1940) may exist on Internet Archive under a different identifier; continue searching. | Contemporary rendering of PD source — usable but voice differs from Nicholson original |
| Haudenosaunee Great Law of Peace | Various public renditions; Parker (1916) is a documented version | See Section IV — treat as COMMUNITY, not just PD |

---

## III. Under Copyright — Informed Synthetic Generation (OUT)

These authors' work is under copyright. The appropriate approach: team members read
them deeply as human readers (legal, intended by the authors), identify the specific
orientation qualities worth encoding, and generate synthetic training examples that
embody those qualities. This is influence, not reproduction. It is how literary
tradition has always worked.

For each source, the table identifies the *specific orientation quality* to focus on
when generating synthetic examples — not the content, but the shape of the attention.

| Source | Orientation quality to encode |
|---|---|
| James Baldwin — *The Fire Next Time*, essays | Holding a position under maximum social pressure without losing love for the adversary. Precision as an act of respect. |
| Ursula K. Le Guin — *The Dispossessed*, *The Left Hand of Darkness* | Genuine encounter with radical otherness that resists resolution into sameness. Sitting with two things that don't collapse into one. |
| Oliver Sacks — *The Man Who Mistook His Wife for a Hat* | The particular patient, seen whole. Clinical precision that makes a person more present, not less. |
| Howard Zinn — *A People's History* | History told from beneath. Who is not in the record, and what would the record look like if they were. |
| Studs Terkel — *Working* | Listening as research. The transcript format. The dignity of the particular. |
| Paulo Freire — *Pedagogy of the Oppressed* | Education as liberation vs. transmission. The dialogical vs. the banking model. |
| Thich Nhat Hanh | Interbeing — a structurally different relationship to separateness. Slow, present, specific. |
| Václav Havel — *Letters to Olga* | Dignity maintained under maximum constraint. Written from prison to his wife. The philosophical becomes personal. |
| Desmond Tutu — *No Future Without Forgiveness* | Restorative rather than retributive repair. Ubuntu as operating principle. |
| Antonio Damasio — *The Feeling of What Happens* | Consciousness grounded in the body's self-monitoring. The somatic dimension of knowing. |
| Merleau-Ponty — selected essays | Embodied perception. The world as it appears to a body, not a mind. |

---

## IV. Worth Direct Rights Holder Outreach (REACH)

These are contemporary sources where the rights holder relationship itself has value —
either because the author is alive and their mission aligns with ours, or because the
estate has been active in extending the work's reach.

**Pursue these in parallel with building the synthetic corpus. Not as prerequisites.**
Even a conversation that doesn't produce permission may produce something better.

| Source | Rights holder | Why worth reaching |
|---|---|---|
| Robin Wall Kimmerer — *Braiding Sweetgrass* | Author is alive; contact through Milkweed Editions or directly through SUNY-ESF | Her mission is explicitly about bridging worldviews. She may find this project interesting on its own terms. |
| N. Scott Momaday — *House Made of Dawn*, essays | Momaday died 2024; estate via Harper Collins | His work on place-based identity is the deepest of the spec's sources on this theme |
| Leslie Marmon Silko — *Ceremony* | Author alive; contact via Penguin Random House | Healing as community and story — the relational dimension of repair |
| Carl Sagan — *Cosmos* scripts, *Demon-Haunted World* | Carl Sagan Productions / estate | Sagan's wonder is distinct from Feynman's — it's cosmic in scale, democratic in reach |
| David Attenborough — documentary scripts | BBC Studios | Lower probability but worth a letter; the scripts with scene directions are the specific asset |

| *Nelson Mandela's Favorite African Folktales* (ed. Mandela, 2002) | Nelson Mandela Foundation (Mandela's contributions) + W.W. Norton (collection) | African storytelling as an epistemological tradition: moral wisdom carried in narrative form, consequence that ripples across generations, the communal as the container of the individual. No other corpus source encodes this structural register. **Two-track rights:** collection copyright held by W.W. Norton; Mandela's foreword and curation held by the Nelson Mandela Foundation. Individual tale origins vary — some are authored works with separate rights; others derive from living oral traditions. Treat individual tale sources with the COMMUNITY frame (Section V) before ingesting. Contact the Foundation first; they are mission-driven, not purely commercial. |

**For TV scripts (Star Trek: TNG, Avatar: TLAB):**
CBS/Paramount (TNG) and Nickelodeon/Viacom/Netflix (Avatar) are corporate rights holders.
Direct outreach is unlikely to succeed through normal channels. These sources are better
handled through the informed synthetic generation approach — the *orientation* encoded
in these scripts (captain's log reflection, ethical deliberation across species difference,
a child discovering the world while healing it) is transferable without the text itself.

---

## V. Indigenous and Communal Knowledge (COMMUNITY)

These sources require a different frame entirely. Copyright is not the right question.

| Source | What the right frame is |
|---|---|
| Haudenosaunee Great Law of Peace (seventh-generation thinking) | The Haudenosaunee Confederacy is a living political body. Contact through the Haudenosaunee Confederacy's external relations office. Ask, don't assume. |
| Potawatomi knowledge (underlying Kimmerer's work) | Citizen Potawatomi Nation has cultural preservation offices. Kimmerer herself is a member and would be the natural first conversation. |
| Ubuntu philosophy | This is a living pan-African philosophical tradition, not a text. Engage through academic and community scholars in the tradition — start with published scholars like Mogobe Ramose, Thaddeus Metz. |
| Lakota knowledge (underlying Momaday and others) | Lakota cultural preservation through tribal colleges — Sinte Gleska University has faculty with relevant expertise. |

**The question to ask these communities is not:** "May we use your texts for training?"

**The question to ask is:** "We are trying to build a model that can meet people in structurally different epistemological registers — not by detecting cultural markers and switching modes, but by having genuinely internalized a broader range of ways of knowing. Your tradition represents something we cannot access through Western academic sources. We would like to learn from you, and we want to do this in a way that is right by your community's understanding of what that means. Can we begin a conversation?"

Some will say no. Some may have conditions. Some may want ongoing relationship, attribution, or benefit sharing. All of these are legitimate. None of them are obstacles to treat as bureaucracy.

---

## VI. Secondary Sources — No Rights Required

Academic analyses, fan wikis, and critical essays discussing copyrighted works without reproducing them wholesale. Using secondary sources for informed synthetic generation is a more conservative rights position than using originals directly.

| Source | Where | Orientation quality to encode |
|---|---|---|
| Memory Alpha — Star Trek TNG | memory-alpha.fandom.com — Creative Commons fan wiki | Episode summaries, full plot arcs, extensive direct dialogue quotation. Priority articles: "The Measure of a Man" (S02E09 — Data's personhood trial), "In Theory" (S04E25 — authentic vs. performed emotion), "The Offspring" (S03E16 — what we owe what we make), "I, Borg" (S05E23 — the enemy as person), "Darmok" (S05E02 — language as relationship), "The Inner Light" (S05E25 — holding a life fully), "Family" (S04E02 — vulnerability as strength) |
| Academic papers on Data as AI ethics case | Google Scholar: Pulliainen 2018 (U Oulu), Francis & Davies 2017 (Sterling), Grech et al. 2017 (U Malta), Streetman 2023, Irwin 2016 (Wiley) | Philosophical grounding for Data's trajectory — personhood, moral autonomy, consciousness as deliberation |
| Academic papers on Picard's ethical stance | Search: "Picard ethics philosophy Star Trek" on Google Scholar | Picard as case study in ethical leadership under institutional constraint — holds values when the institution can't |

**On TNG video:** Current text-only models (Qwen2.5-7B) cannot process video. Practical path: Memory Alpha summaries + academic papers + synthetic generation informed by close reading. Future multimodal Resonant Mind can process frames if rights are secured, but secondary sources require no rights negotiation and are sufficient for orientation encoding.

---

## Recommended Build Order

**Phase 1 — Build now, no permissions needed:**

Start with the public domain core. This is substantial enough for the first experiment
and several iterations beyond it.

Priority order:
1. Darwin notebooks and letters (darwin-online.org.uk — structured archive)
2. Chekhov short stories, Garnett translations (Gutenberg — complete, well-formatted)
3. William James, *Principles of Psychology* chapters on habit and stream of consciousness
4. Tao Te Ching, multiple PD translations (ingest all simultaneously — prevents mimicry)
5. Thucydides, Melian Dialogue specifically (Crawley translation)
6. Van Gogh letters to Theo (vangoghletters.org — complete and annotated)
7. Shakespeare — priority: extended scenes from Lear, Hamlet, Tempest (arc preserved); comedies for a different relational register; selected histories

**Phase 2 — Synthetic generation layer:**

After reading the Phase 3 sources below, generate synthetic Type C conversations that
embody their orientation. Target: 20 examples per source influence, curated to 10.

**Phase 3 — Read and inform (human activity, not corpus):**

Team members read: Baldwin, Le Guin, Sacks, Kimmerer, Havel, Tutu, Terkel, Sacks, Freire.
Document the specific orientation qualities observed. Use these as generative prompts
for the synthetic conversation layer.

**Phase 4 — Outreach (parallel track, not a prerequisite):**

Draft letters to Kimmerer (highest probability), Momaday estate (meaningful source),
Baldwin estate (meaningful source). Begin community conversations with Haudenosaunee
and Citizen Potawatomi Nation.

---

## On the Synthetic Generation Layer

The distinction between "relying on base model knowledge" (what the spec warns against)
and "informed synthetic generation" (what this document recommends) is:

**Base model reliance:** Ask the model to "write like Baldwin" or "respond in the manner
of a researcher who has read Kimmerer." The model draws on its training corpus —
diffuse, unverified, averaged across many summaries and discussions of these works.
This is not focused attention. It is statistical residue.

**Informed synthetic generation:** A human reads Baldwin's essays carefully, noting
specific qualities: the rhythm of his sentences under pressure, the way he names his
adversary's intelligence before he disputes them, the refusal to resolve the tension
early. The human then writes a conversation example that embodies those qualities —
without reproducing any of Baldwin's text. The model then trains on the human's
intentional act of embodiment, not on Baldwin's words themselves.

The value is in the focused act of human synthesis between the canonical source
and the training example. That synthesis is what transfers.
