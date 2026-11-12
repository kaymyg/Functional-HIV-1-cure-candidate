# Contributing

Thanks for looking. This project is at concept stage and it benefits from scrutiny more
than from volume.

Start with [`docs/OPEN-PROBLEMS.md`](docs/OPEN-PROBLEMS.md). It lists the unresolved
questions, split by whether they need a laptop or a laboratory, each with what would settle
it and what counts as done.

## What this project is

A design review and development package for one proposed functional HIV-1 cure
architecture. There is no experimental data in it. Everything here is design work,
literature synthesis and model verification.

It is not a clinical trial, not a protocol anyone should act on, and not medical advice.
Nothing in this repository has been tested in a cell, let alone a person.

## The one rule that matters

**Do not contribute confident numbers that nothing measured.**

This repository exists partly because the original analysis generated a great deal of
precise-looking output from a model whose structure determined its own answers. The
headline figures were artifacts, documented in section 3 of the main document and
reproducible by running `analysis/verify_model.py`.

So, concretely:

- Every parameter that has not been measured is marked as unmeasured, carries a range
  rather than a point value, and the range is justified.
- Every claim taken from the literature carries a citation to a paper that was actually
  read, not a search snippet.
- Model outputs are reported as ranges across the input ranges, not as single values.
- If a result turns out to be insensitive to an input, say so. That is a finding, and in
  this project it has already been the most useful kind.

Pull requests that add invented point estimates, or that report a single confident number
from unmeasured inputs, will be asked to change before merge.

Disagreement with the conclusions in the main document is welcome, including the central
one. If the sequencing argument in section 4 is wrong, the useful thing is a pull request
or an issue that says why, with sources.

## How to contribute

1. Open an issue first for anything substantial, so two people do not do the same work.
2. For a Tier 1 problem, say which one in the issue.
3. Keep pull requests to one problem each.
4. Put analysis code in `analysis/`, written so someone else can rerun it. Pin what you
   need in a comment at the top rather than adding a dependency file for one script.
5. Document changes go in `docs/`. If a change alters a conclusion in the main package,
   update the main package too, and say so in the pull request.

### Writing style in the documents

Lead with the finding. Specifics rather than adjectives. Units on every number. Mark
uncertainty where it exists instead of smoothing it over.

## If you run a lab

Tier 2 in the open problems document lists four experiments that cannot be done through
GitHub. OP-6, the 90-day methylation durability experiment in dividing primary CD4+ T
cells, is the one that matters most. It is the cheapest experiment that could end this
program, and until someone runs it everything else here is downstream of a guess.

If that is something your group could do, or you can point at published data that already
answers it, please open an issue.

## Licence

**This repository currently has no licence, which means default copyright applies and
nobody has the legal right to reuse or redistribute the contents.** That needs fixing
before outside contributions make sense. Until a licence is added, treat anything you
contribute as subject to whatever licence the owner later chooses, and raise it in your
issue if that is a problem for you.

## Conduct

Assume good faith, argue with the work rather than the person, and cite your sources.
