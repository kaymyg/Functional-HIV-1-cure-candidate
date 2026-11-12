# Open problems

The unresolved questions in this program, written so that someone can pick one up and
work on it. Each entry says what is unknown, why it matters, what would settle it, and
what counts as done.

They are split by what kind of resource they need, because that is the real constraint.
Tier 1 problems can be worked on by anyone with a laptop and public data. Tier 2 problems
cannot be solved on GitHub at all and need a laboratory with primary cells from
ART-suppressed donors.

The main document is
[`LNP-BT01-preclinical-development-package.md`](LNP-BT01-preclinical-development-package.md).
Section references below point into it.

---

## Tier 1: computational, open to anyone now

These use public data. No wet lab, no institutional access, no funding required.

### OP-1. Is the LTR target site conserved outside subtype B?

**Status:** open. Highest value problem in Tier 1.

**The question.** Brec1 was directed-evolved against a specific asymmetric target sequence
in the HIV-1 LTR. The dBrec1 construct in this program inherits that recognition site, and
the proposed CRISPR guides target the LTR as well. How conserved is that site across the
subtypes that actually dominate the global epidemic?

**Why it matters.** Subtype B is a minority of global HIV-1 infections. The burden sits in
subtype C across southern Africa, A1 and D across East Africa, and CRF01_AE across
Southeast Asia. A construct that only recognises subtype B LTR sequences is a therapy for
high-income countries, which would make most of the rest of this document moot. Nobody in
this program has checked.

**Data.** Los Alamos HIV Sequence Database, which is public and free. LTR alignments by
subtype and by circulating recombinant form.

**Method.** Pull the LTR alignments, locate the recognition site in each sequence, score
per-position conservation, and report coverage by subtype, by CRF, and by geography.
Report the fraction of sequences with a perfect match, and the fraction within one and two
mismatches.

**Done when:** a table of recognition site conservation by subtype and CRF, with sequence
counts and the date of the database snapshot, plus a short note on which populations would
and would not be covered. A reproducible script in `analysis/`.

**Skills:** sequence alignment, basic bioinformatics. Good first problem.

---

### OP-2. Pick the two excision guides, and show their off-target profile

**Status:** open. Depends on OP-1.

**The question.** Section 7 argues the guide array should drop from seven sites to two,
because excision needs only two cuts and seven concurrent breaks give 21 pairings that can
mis-join rather than one. Which two guides?

**Why it matters.** This is the difference between a design with one translocation pairing
and a design with 21, and it is decidable from sequence alone before anyone touches a cell.

**Data.** Los Alamos HIV Sequence Database for on-target conservation. Human reference
genome for off-target search.

**Method.** Candidate guides in the LTR regions flanking the provirus. Score each for
conservation across subtypes, then run off-target prediction with Cas-OFFinder or CRISPOR
against the human genome. Prefer guide pairs where every predicted off-target carries at
least four mismatches, and where no off-target sits in or near a tumour suppressor or an
essential gene.

**Done when:** a ranked shortlist of guide pairs with per-subtype on-target conservation
and full predicted off-target tables, plus the exclusion reasoning for rejected candidates.

**Skills:** CRISPR guide design, genomics.

---

### OP-3. Implement the corrected PK/PD model

**Status:** open. Specification already written.

**The question.** Section 6 specifies four structural changes to the model: connect
delivery to effect per compartment, make the lock reversible with a dilution-by-division
term, count cells rather than fractions, and output a rebound hazard rather than a locked
fraction. Nobody has implemented it.

**Why it matters.** The current model's outputs are artifacts of its structure, documented
in section 3 and reproducible with `analysis/verify_model.py`. A correctly structured model
would at least tell us which parameters the answer is sensitive to, which tells the wet lab
what to measure first.

**Hard constraint on this contribution.** Every parameter that has not been measured must
be explicitly marked as unmeasured, carry a plausible range rather than a point value, and
the model must report its output as a range across those ranges. A new model that emits a
single confident number would reproduce exactly the failure this repository documents. Pull
requests that hardcode invented point estimates will not be merged.

**Done when:** a model implementing the section 6 structure, with a parameter file
separating measured from assumed values, and a sensitivity analysis that shows which
unknowns actually move the rebound hazard.

**Skills:** ODE modelling, Python, scientific computing.

---

### OP-4. Literature priors for the four parameters that matter

**Status:** open. Incremental, many small contributions welcome.

**The question.** Section 6 names four parameters that dominate the outcome. None has a
sourced value in this repository:

| Parameter | What it is |
| --- | --- |
| `β · ε` | Methylation mark loss per cell division in memory CD4+ T cells |
| `f_lymph` | Endosomal escape fraction for LNP cargo in lymphoid tissue |
| `a` | Successful reactivation rate per residual intact provirus |
| `k_lock` | Locking rate as a function of achievable intracellular construct concentration |

**Why it matters.** `β · ε` decides whether block-and-lock is durable, and durability is the
product. Right now it is a guess.

**Method.** Find published measurements or defensible proxies, with full citations, and
record a range rather than a point value. Proxies are acceptable if the substitution is
argued explicitly, for example using CpG island methylation maintenance fidelity as a proxy
for `ε`.

**Done when:** `analysis/parameters.yaml` with a range, a source, and a confidence note for
each parameter. Partial contributions are fine, one parameter per pull request.

**Skills:** literature search, HIV virology or epigenetics reading knowledge. Good first
problem for someone with library access and no coding background.

---

### OP-5. Model the reservoir as heterogeneous, because it is

**Status:** open. Harder than OP-3.

**The question.** Every model in this program treats the reservoir as one uniform pool.
Most integrated proviruses are defective and irrelevant. Among intact proviruses, those in
closed chromatin are already quiet, and those in actively transcribed regions are the ones
that drive rebound and the hardest to silence.

**Why it matters.** The therapy has to work hardest exactly where it works least well, and
no current model can represent that. This is the difference between a model that flatters
the approach and one that tests it.

**Data.** Published HIV integration site datasets, and published intact versus defective
proviral ratios from IPDA studies.

**Done when:** a reservoir model stratified by integration site chromatin context, showing
how the rebound hazard changes when silencing efficiency is allowed to depend on that
context.

**Skills:** computational biology, integration site data handling.

---

## Tier 2: needs a wet lab

These cannot be done through pull requests. They need primary CD4+ T cells from
ART-suppressed donors, which needs a laboratory, ethics approval and donor consent. They
are listed so a lab that is interested can see exactly what would help.

### OP-6. The durability experiment (highest priority in the whole program)

Serial LTR methylation in dividing primary CD4+ T cells over 90 days, to measure how much
of the mark survives proliferation. This is Gate 1 in section 8.

It is the cheapest experiment that can end the program. If the mark does not survive cell
division, block-and-lock fails and no amount of delivery optimisation rescues it. Everything
else in this repository is downstream of an answer nobody has.

### OP-7. Does catalytically dead Brec1 actually bind?

Electrophoretic mobility shift or ChIP, testing the dead recombinase and the full
four-domain fusion against LTR sequences from a panel of clinical isolates. Recombinase
binding and catalysis are coupled, and dead variants do not automatically make good
DNA-binding domains. Section 9 treats this as the foundational unknown.

If the answer is no, a dCas9 or zinc finger targeting module does the same job with
established behaviour.

### OP-8. Endosomal escape in lymphoid tissue

Reporter mRNA in humanized mice with single-cell resolution in lymph node. This is the
parameter the original model omitted entirely and the usual reason LNP programs fail in vivo.

### OP-9. Translocation panel

CAST-Seq or UDiTaS across the chosen guide pairings in primary CD4+ T cells from at least
six donors. The source material correctly identified translocation as a risk and then
included no study that would detect one.

---

## How a lab can get involved

The Tier 2 work needs a partner, not a contributor. If you run or work in a relevant lab,
open an issue or make contact directly.

For anyone looking for the groups already working in this space, the NIH Martin Delaney
Collaboratories are the flagship HIV cure research program, currently ten consortia
including BEAT-HIV at the Wistar Institute, CARE, REACH and the pediatric PAVE
collaboratory. The program explicitly encourages international partnerships, which matters
for OP-1, since the subtype coverage question is most pressing in exactly the regions least
represented in existing cure research.

---

## What is not an open problem

To save people time, these parts of the document are not looking for contributions:

- **The toxicology plan.** It follows ICH guidance and is conventional. It will be rewritten
  by whoever runs the studies.
- **The regulatory strategy.** Needs a regulatory affairs professional and a real sponsor.
- **CMC.** Needs a formulation group and a GMP facility.
- **Alternative cure strategies in general.** This repository is a design review of one
  specific architecture. Proposals for unrelated approaches are better as their own project.
