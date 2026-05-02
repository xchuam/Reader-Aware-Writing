# Dossiers

Each benchmark topic should have one fixed dossier. The dossier is the only
source material writing subagents may use unless a run explicitly allows web
access.

Recommended file name:

`<dossier_id>.md`, for example `D001_antibiotic_resistance_microbiome.md`.

## Dossier Template

```markdown
---
dossier_id: D001
created_at_utc: YYYY-MM-DDTHH:MM:SSZ
created_by: TBD
article_type: Research article | Review article | Brief report | Perspective
target_reader: TBD
target_venue_or_context: TBD
word_count_target: TBD
citation_style: APA | Vancouver | numbered | none
web_access_allowed: false
---

# Topic

One-sentence topic.

# Target Reader

Describe expertise, likely questions, and what the reader needs from the
article.

# Article Goal

State what the article should accomplish for the reader.

# Background Facts

- Fact 1.
- Fact 2.

# Research Question or Thesis

State the central question, hypothesis, or argument.

# Study Design / Methods / Evidence Base

Describe the design, methods, dataset, intervention, comparison, or evidence
base. Include enough detail for a scientific article but do not overload the
dossier with irrelevant facts.

# Results / Findings

Provide the exact findings that all authoring conditions must use. Include
numbers, uncertainty, subgroup results, null results, and exceptions where
relevant.

# Limitations

- Limitation 1.
- Limitation 2.

# Required Claims

- Claim that must appear if supported by the dossier.

# Prohibited Claims

- Claims the article must not make.
- Overgeneralizations to avoid.

# Allowed References

List only references that subagents may cite. Include complete reference details
or a stable citation key. If this section is empty, authoring subagents should
not invent references.

# Formatting Requirements

State section requirements, word count, citation style, and any required terms.
```

