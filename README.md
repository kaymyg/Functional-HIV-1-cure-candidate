# Functional HIV-1 Cure Candidate

Preclinical design and development package for a sequenced, epigenetic-plus-immune
approach to functional HIV-1 cure.

## Contents

| Path | What it is |
| --- | --- |
| [`docs/LNP-BT01-preclinical-development-package.md`](docs/LNP-BT01-preclinical-development-package.md) | The main package: design review, model audit, corrected architecture, Target Product Profile, PK/PD model spec, IND-enabling plan, risk register and gates |
| [`analysis/verify_model.py`](analysis/verify_model.py) | Verification script that re-runs the original PK/PD models and demonstrates the structural defects documented in the model audit |
| [`docs/OPEN-PROBLEMS.md`](docs/OPEN-PROBLEMS.md) | The unresolved questions, split into what needs a laptop and what needs a laboratory, each with acceptance criteria |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute, and the one rule about unmeasured numbers |

## Summary of findings

The originally proposed single-particle co-delivery design, one lipid nanoparticle
carrying both a BrecOFF epigenetic silencer and the EZH2 inhibitor tazemetostat,
does not work as specified. Three blocking problems:

1. **The two payloads oppose each other.** EZH2 inhibition is a documented
   latency-reversing mechanism. Tazemetostat actively dismantles the heterochromatin
   that BrecOFF is there to build.
2. **The CRISPR sweep is scheduled behind a barrier it cannot cross.** Heterochromatin
   impedes Cas9, worst of all under the brief, low-level RNP exposure the protocol
   specifies.
3. **Every optimization result in the original scripts is an artifact.** The targeting
   parameters and the efficacy endpoint are not connected in the model, so the
   objective function is flat and the optimizer returns its starting guess.

The proposed resolution is a sequenced three-stage regimen of separate products,
with the excision step moved ahead of the silencing step rather than after it.

## Status

Concept stage. There is no experimental data in this program yet. Everything here
is design work and model verification. See the Gaps section of the main document for
what has to be generated next, and the Gates section for the order to generate it in.

Separately: tazemetostat was withdrawn worldwide on 9 March 2026 following a secondary
haematologic malignancy signal. The Stage A agent requires a decision before any
downstream work is commissioned.

## Running the verification

```bash
pip install numpy scipy
python3 analysis/verify_model.py
```

## Contributing

Scrutiny is more useful here than volume. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and
pick something from [`docs/OPEN-PROBLEMS.md`](docs/OPEN-PROBLEMS.md).

Two worth singling out:

- **OP-1, LTR target site conservation outside subtype B.** Needs only public Los Alamos
  sequence data and a laptop. If the recognition site is not conserved across subtypes C,
  A1 and D, this is a therapy for a minority of the global epidemic, and most of the rest
  of the document stops mattering. Nobody has checked.
- **OP-6, the 90-day methylation durability experiment.** Needs a wet lab. It is the
  cheapest experiment that could end this program, and everything here is downstream of
  an answer nobody has.

This repository has no licence yet, so default copyright applies and reuse rights are not
granted. That should be settled before outside contributions.

## Disclaimer

Concept-stage design work. Not a clinical protocol, not medical advice, and not tested in
any biological system.
