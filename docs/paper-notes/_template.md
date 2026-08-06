# <Paper Title>

> Copy this file to `docs/paper-notes/<year>-<firstauthor>-<keyword>.md` and fill
> it in. Do not add a paper to the literature review as "read" until this note is
> complete. Analyse, don't just summarise.

**First, decide which shape fits the paper — don't force one onto the other.**
Not every worth-reading paper is built around solving a hard technical problem;
some establish a concept, synthesise a field, or define a standard, and forcing
those into an "empirical" shape produces empty or strained sections. Use:

- **Empirical / experimental / model-building papers** (proposes a method,
  mechanism, or model and tests or derives it) — the full template below,
  sections 1–13. Example: Ostrom (1990), Fehr & Gächter (2002), OWG (1992),
  Piatti et al./GovSim (2024) — each is explaining or demonstrating something
  genuinely non-obvious, so "why is this hard" has real content (e.g. Ostrom:
  three influential models all predict collapse — why do real commons often
  not collapse?).
- **Conceptual / definitional / review / standards papers** (introduces
  vocabulary, synthesises a field, or specifies a protocol, without a
  hard-problem-and-test structure) — replace sections 3–9 (`Why the Problem Is
  Difficult` through `Future Work`) with **`Key Concepts`** (the definitions/
  distinctions that matter, quoted precisely) and **`Main Contribution`** (what
  organizing move the paper makes). Keep sections 1–2 and 10–13 as-is. Example:
  Folke (2006, resilience review), Walker et al. (2004, definitional), Grimm et
  al. (2020, the ODD protocol — used "The Seven Elements" / "What changed"
  instead of Key Concepts/Main Contribution; adapt the two substitute sections'
  *names* to whatever best carries the paper's actual content, the point is
  dropping the hard-problem/method/results shape, not matching new section
  titles exactly).

If a paper sits awkwardly between the two, pick the closer fit and say so in a
one-line note under the title (as several existing notes do).

---

## 1. Citation
<!-- Full, verified reference: authors, year, title, venue, pages, DOI/URL. -->

## 2. Research Problem
<!-- What problem/question does the paper actually address? State it precisely. -->

### For empirical/experimental/model-building papers, continue with 3–9:

## 3. Why the Problem Is Difficult
<!-- What makes it hard / non-trivial? Why don't naive approaches work? -->

## 4. Proposed Method
<!-- The core idea/mechanism/model. Enough that you could re-implement the gist. -->

## 5. Experimental Setup
<!-- Environment, agents, parameters, conditions compared, baselines. -->

## 6. Metrics
<!-- How is success measured? Definitions and assumptions. -->

## 7. Main Results
<!-- Key quantitative/qualitative findings. Numbers where possible. -->

## 8. Limitations
<!-- Stated and unstated. Where might the results not hold? -->

## 9. Future Work
<!-- Explicit future work the authors name. -->

### For conceptual/definitional/review/standards papers, use 3'–4' instead of 3–9:

## 3'. Key Concepts
<!-- The definitions/distinctions that matter, quoted precisely where it matters. -->

## 4'. Main Contribution
<!-- What organizing move does the paper make? What's the single reusable artefact
     (a taxonomy, a distinction, a protocol) a reader takes away? -->

## 8'. Limitations
<!-- Stated and unstated. What does the framework/review not cover or resolve? -->

### Both paths continue with 10–13:

## 10. Relevance to This Project
<!-- How does this affect our direction, design, metrics, or baselines? -->

## 11. Possible Follow-Up Contribution
<!-- Is a smaller, bachelor-feasible follow-up realistic? Sketch it. (Optional for
     conceptual/review papers if nothing concrete applies — say so rather than
     stretching for one.) -->

## 12. Important Terms
<!-- Terms to add/clarify in docs/terminology.md. -->

## 13. Questions
<!-- What is unclear? What to check or read next? -->
