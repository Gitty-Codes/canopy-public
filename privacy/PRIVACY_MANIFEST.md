# The Canopy — Privacy Manifest
*For organizations using The Canopy to process their data*

---

## What this document is

This is a plain-language explanation of how The Canopy handles your organization's data —
what classification your data receives, what that means for how it is processed, and
what you can control.

You should be able to read this without a technical background and understand
exactly what happens to information you share with The Canopy.

---

## The four data tiers

Every request processed by The Canopy is classified into one of four tiers
before any AI model sees it.

### Public
**What it is:** Information your organization has already made public or would freely share —
program descriptions, concert dates, mission statements, published impact numbers.

**How it is processed:** Cloud AI models (Anthropic API). Standard protections apply.

**Memory:** May be written to session memory to improve future responses.

---

### Operational
**What it is:** Internal working information that is not sensitive but is not public —
grant deadlines, meeting notes, campaign timelines, board agendas, draft documents.

**How it is processed:** Cloud AI models (Anthropic API). Standard protections apply.
Anthropic's API does not use your data for model training. Data is retained for 7 days
on Anthropic's servers, then deleted.

**Memory:** May be written to session memory.

**Note:** This is the default classification for unrecognized content. If your
content is misclassified as Operational when it should be Sensitive, pass
`privacy_class="sensitive"` explicitly when calling run_task().

---

### Sensitive
**What it is:** Information about identifiable individuals, or confidential organizational matters.

Examples:
- Donor names, gift amounts, and giving history
- Staff salaries and employment information
- Unpublished grant applications
- Financial statements and budget details
- Board member personal contact information
- Organizational strategy not intended for public disclosure

**How it is processed:** Cloud AI models are allowed, but only with your awareness.
When The Canopy auto-detects Sensitive data, it prints a notice so you can
make an informed decision. You can confirm by passing `privacy_class="sensitive"`.

**Memory:** Session memory writes are suppressed automatically. Sensitive data
is not written to The Canopy's local memory store.

**Audit:** Every Sensitive request generates a local audit record in
`memory/privacy_audit/`. The audit records processing metadata only —
not the content of your request.

---

### Protected
**What it is:** Information with legal protections or the highest sensitivity.

Examples:
- Student records and participation data (FERPA)
- Information about minors (COPPA applies to anyone under 13)
- Health-adjacent information: mental health, diagnoses, IEPs, treatment plans (HIPAA adjacent)
- Social Security numbers, bank account numbers, routing numbers

**How it is processed:** Cloud processing is blocked. The Canopy will raise a
PrivacyError and refuse to send this data to any external model.

**Memory:** Memory writes are blocked.

**Audit:** An audit record is created locally.

**What to do:** If you need AI assistance with Protected data, you must use a
local model (Ollama or similar). The Canopy's harness will support this path
in a future release. For now, remove or anonymize Protected data before
using cloud-assisted task runs.

---

## What Anthropic's API does with your data

When The Canopy uses the Anthropic API (claude.ai/api):

- **No training:** Anthropic does not use API data to train its models.
  This is their published policy as of 2025 and applies to all API users.
- **Retention:** Data sent via the API is retained for **7 days** by Anthropic,
  then deleted. This is shorter than the consumer claude.ai interface.
- **You must be on the API path.** If you are using The Canopy through its
  command-line interface with an ANTHROPIC_API_KEY, you are on the API path.
  The consumer claude.ai website has different terms and is not appropriate
  for organizational data.

---

## What The Canopy stores locally

The Canopy maintains a local memory store on the machine where it runs.
This is separate from Anthropic's servers — it is a set of files on your
own computer or server.

**Session memory** may be written after task runs (for Operational/Public data).
These records contain: the task name, a summary of the inputs, and the artifact produced.
They do not contain full request text.

**Sensitive data is never written to memory** — this is enforced automatically.

**Protected data is never written to memory** — this is enforced automatically.

**Audit records** are written for all Sensitive and Protected requests.
They contain: timestamp, classification, task name, engine used, model used,
whether memory was written, and a brief (≤200 character) inputs summary.
They do not contain request content.

---

## Your controls

### Explicit classification
If you know what tier your data belongs in, tell The Canopy explicitly:

```python
result = run_task(
    "nonprofit-comms",
    {"request": "..."},
    privacy_class="sensitive",   # explicit classification
)
```

This overrides auto-classification and suppresses the auto-detect warning.

### Suppress memory writes
Pass `save_to_memory=False` to any run_task() call to prevent session memory
from being written, regardless of classification:

```python
result = run_task(
    "nonprofit-comms",
    {"request": "..."},
    save_to_memory=False,
)
```

### View the audit log
```python
from privacy.audit import read_audit_log, audit_summary

# Summary counts
print(audit_summary())

# Last 20 records
for record in read_audit_log():
    print(record["timestamp"], record["classification"], record["task"])
```

---

## Known gaps (as of May 2026)

**Classification is pattern-based.** The auto-classifier uses keyword and
pattern matching. It may miss sensitive data that does not match its patterns,
and it may over-classify benign content. Explicit `privacy_class` overrides are
available when the classifier makes the wrong call.

**Org-memory skill files are not yet classified.** When The Canopy loads
org-specific context files (e.g., `projects/clients/my-org/org-memory-intake.md`)
into a cloud prompt, the contents of those files are not independently classified.
Do not put Protected-tier data into org-memory context files until this is resolved.

**No local-model path in the harness.** Protected data currently raises a hard error
rather than routing to a local model. A local-model fallback will be added in a
future release.

**Anonymization is not yet implemented.** The spec describes a pattern of stripping
sensitive details before sending to a cloud model, then rehydrating the response.
This is not yet built. Until it is, Sensitive data goes to cloud models in full
(with audit trail) or is processed locally.

---

## Who to talk to

Questions about The Canopy's privacy architecture: the system was designed
by The Canopy team. This document is the authoritative public description.

Questions about what your organization should classify as Protected vs. Sensitive:
that is a conversation for your organization's leadership and, for regulated categories
(student records, health data, financial identity), your legal counsel.

The Canopy team does not make those classifications for you — we build the mechanism.
Your organization holds the judgment about your own data.

---

*This document is versioned. We do not rewrite the past.*
*May 2026 — v1.0*
