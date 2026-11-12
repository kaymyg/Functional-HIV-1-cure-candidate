# LNP-BT01 Preclinical Development Package

**Functional HIV-1 cure candidate, epigenetic silencing plus immune reinvigoration**

As of 12 November 2026.

---

## Executive summary

**LNP-BT01 cannot be developed as a single co-formulated particle. Its two payloads act in opposite directions on the same molecular target, and the supplied simulations cannot detect this because their structure makes the efficacy result independent of almost every input.**

**Separately, and more urgently: tazemetostat has been withdrawn worldwide.** Ipsen withdrew Tazverik from every market and both approved indications on 9 March 2026, after the SYMPHONY-1 data monitoring committee found a pattern of secondary hematologic malignancies, reported at 5.7 percent against zero in the control arm, mostly myelodysplastic syndrome and acute myeloid leukemia ([Ipsen withdrawal, March 2026](https://www.pharmacytimes.com/view/ipsen-voluntarily-withdraws-tazemetostat-from-all-markets-following-safety-signal-in-confirmatory-trial); [FDA safety alert](https://www.hmpgloballearningnetwork.com/site/onc/fda-alerts/fda-issues-safety-alert-tazemetostat-following-secondary-malignancy-risk)). All active trials and expanded access programs were discontinued. The intended population here is virally suppressed people with near-normal life expectancy, so the risk tolerance is nothing like that of relapsed lymphoma. Section 7 sets out the three ways forward.

The underlying science is sound and the individual components are well chosen. Tazemetostat has real, published support for HIV reservoir work. Epigenetic silencing of the 5' LTR is a legitimate block-and-lock strategy. CRISPR excision of integrated provirus is an active field. The problem is not the parts, it is the assembly.

Three findings drive this package:

1. **Tazemetostat reverses the silencing that BrecOFF establishes.** EZH2 inhibition is a documented latency-reversing mechanism, not a neutral immune adjuvant. Co-delivering it with a heterochromatin-enforcing construct puts the two payloads in direct opposition inside the same cell.
2. **The Phase 4 CRISPR sweep is scheduled at the worst possible moment.** Deep heterochromatin impedes Cas9 access, and the proposed short-lived RNP format is precisely the exposure regime most sensitive to that barrier.
3. **Every optimization result in the supplied scripts is an artifact.** The targeting parameters and the efficacy endpoint are not connected in the model, so the optimizer reports whatever it was initialized near.

The resolution is to stop treating this as one drug and start treating it as a sequenced regimen of two drug products, with the CRISPR step moved ahead of the silencing step rather than after it. That change preserves nearly all of the existing scientific rationale, removes a formulation requirement that was close to physically impossible, and produces a development path that an IND reviewer can follow.

The IND-enabling toxicology plan already drafted is largely sound and carries over with modifications noted in section 7.

---

## 2. Critical design review

Three conflicts block the current architecture. The first two are biological and cannot be engineered around by reformulating. The third is a modelling defect covered in section 3.

### Conflict 1: the two payloads oppose each other at the LTR

The protocol asks BrecOFF to deposit repressive marks at the 5' LTR, then asks tazemetostat to maintain a sustained intracellular concentration for 14 days. Tazemetostat inhibits EZH2, the catalytic subunit of PRC2, which deposits H3K27me3. PRC2 is one of the principal enforcers of HIV-1 latency at that exact promoter.

The consequence is that tazemetostat is a latency-reversing agent. In Th17 primary cell models of latency and in resting memory CD4+ T cells from ART-suppressed patients, EZH2 inhibition with GSK-343 or EPZ-6438, which is tazemetostat, was on its own enough to reactivate latent provirus ([Nguyen et al., mBio 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5347344/)). The same work places PRC2 as the rate-limiting control on proviral reactivation, and names these inhibitors as candidates for latency reversal in the clinic.

So Phase 3 of the protocol spends two weeks actively dismantling the repression that Phase 2 spent its effort building. Co-formulation makes this worse rather than better, because CD4/CCR5 targeting delivers both payloads to the same cells.

This does not mean tazemetostat is the wrong drug. Its reservoir rationale is strong and recent: it raises surface MHC class I on infected CD4+ T cells, counteracting Nef-mediated downregulation, raises pro-apoptotic BIM, improves CTL-mediated killing, and skews CD8+ T cells away from terminally exhausted phenotypes ([EZH2 inhibition and HIV immune evasion, Cell Reports 2025](https://doi.org/10.1016/j.celrep.2025.115652)). That is a reservoir-reduction and immune-clearance mechanism. It belongs in a clearance phase, not alongside a silencing phase.

### Conflict 2: the CRISPR sweep is scheduled behind the chromatin barrier it cannot cross

Phase 4 fires a multiplexed Cas9 RNP pulse after epigenetic stabilization, to clear outlier proviral copies. This runs into a well-characterized constraint: nucleosomes and heterochromatin impede Cas9 binding and cutting.

The penalty is worst under exactly the conditions this protocol specifies. Allele-resolved work in mouse embryonic stem cells found mutagenesis impeded by up to sevenfold when Cas9 exposure was brief and intracellular Cas9 levels were low, and concluded that therapeutic applications using low-level Cas9 exposure are the ones most affected by chromatin state ([Kallimasioti-Pazi et al., PLoS Biology 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6306241)). The protocol's own mitigation strategy, transient RNP with a cytoplasmic half-life under four hours, is that worst case by design.

The same literature points to the fix. Editing is more efficient in euchromatin than heterochromatin ([Jensen et al., FEBS Letters 2017](https://www.pubmed.gov/28580607/)), so the excision step belongs before silencing, while the target is still accessible, not after.

### Conflict 3: the formulation requirement is close to physically self-contradictory

The single-particle design asks one LNP to hold mRNA on a hydrophilic corona for immediate endosomal release, and simultaneously hold a small molecule in a polymer-lipid core for zero-order release over 14 days. Surface-adsorbed mRNA on a circulating particle is exposed to serum RNases and opsonins and will not survive to a lymphoid sanctuary in useful quantity. Separating the two release profiles into two particles removes the conflict entirely and costs nothing scientifically, because, per Conflict 1, the two agents should not arrive together anyway.

---

## 3. Model audit

**None of the headline numbers in the supplied scripts are predictions. They are properties of the equations, and they hold no matter what dose is entered.** The supplied models were re-run to confirm this before writing the redesign. See [`analysis/verify_model.py`](../analysis/verify_model.py).

### Why the efficacy endpoint is pinned

The locking equation is `dP_off/dt = k_off_eff·(1 - P_off) - k_on·P_off`, which settles at `P_off = k_off_eff / (k_off_eff + k_on)`. With `koff_max = 5.0` against `kon = 0.02`, that ratio is 250 to 1. Any dose producing any appreciable BrecOFF concentration drives P_off above 95 percent. The outcome was fixed when those two constants were chosen.

The mRNA equation compounds this. With `deg_b = 1.2` per day, BrecOFF relaxes to a quasi-steady value within roughly one day and forgets its initial condition entirely.

### Verification results

| Claim in the supplied material | What the model actually produces | Verdict |
| --- | --- | --- |
| Dosing drives proviral locking | Varying `k_rel` tenfold, from 0.5 to 5.0, moves final P_off only from 93.5% to 98.8% | Near-flat |
| BrecOFF payload is a key lever | Varying `Brec0` twentyfold, from 2 to 40 nM, changes final P_off by 0.004 percentage points | No effect |
| Monte Carlo shows robust efficacy | The narrow confidence interval reflects a stiff equation, not a robust therapy | Not evidence |
| Toxicity penalty constrains dosing | Cmax equals `0.5 × dose` exactly, so at the upper bound of 8.0 it reaches 4.0, never crossing the 5.0 threshold | Never fires |
| Pareto frontier maps efficacy against toxicity | The toxicity axis is a linear rescaling of dose and the efficacy axis is near-constant | Artifact |
| Optimal lymphatic-to-peripheral targeting ratio | Score varies by 0.0028 percentage points across the entire search domain | Meaningless |
| Sobol total-order indices in the dashboard | Hardcoded constants in the chart definition, not computed from any run | Fabricated |

### The structural defect behind the targeting optimizer

In the eight-state sanctuary model, `P_off_lym` and `P_off_mac` depend only on `Brec_mRNA`, which depends only on `k_rel`, the pH terms and `deg_b`. The parameters `k_lymph` and `k_macro` touch only `Cp`, `Ct`, `Clymph` and `Cmacro`, which feed only `T_exhausted`.

There is no path in the equations from the targeting parameters to the locking endpoint. The objective function is flat, and the optimizer is descending numerical integration noise. Started from four different points it reported four different optima, at (0.350, 0.350), (0.314, 0.314) and (0.252, 0.350), all scoring 97.8995 percent. The reported optimal ratio of 2.8 is the starting guess returned unchanged.

This matters beyond the arithmetic. A model in which sanctuary penetration cannot affect reservoir silencing is a model that cannot evaluate the central premise of the whole program.

### Other defects

- The pH gating factor is `ph_base + ph_sensitivity · exp(-0.05t)`, a function of time alone. It does not reference pH, compartment or endosomal state, so it models no gating mechanism. It is then multiplied by a second decaying exponential, giving the cargo two unexplained decay terms.
- The first simulation script contains `sol.3[-1]` and `sol.4[-1]`, which raise a SyntaxError. That script has never executed.
- `from SALib.sample import saltelli` is deprecated in current SALib, where the path is `SALib.sample.sobol`. Both sensitivity scripts will fail on a modern install.
- The dashboard reports a weighted reservoir lock of 98.4 percent as a live computed KPI. It is live, but for the reasons above it will read near 98 percent for essentially any slider configuration a user chooses.

---

## 4. Resolved therapeutic architecture

**Split the program into two drug products given in sequence, and move the excision step ahead of the silencing step.** The order is the whole fix. Silencing is terminal by design, so anything that needs an accessible provirus has to happen first.

```
AS DESIGNED, four phases in one regimen

  [LNP infusion] -> [BrecOFF lock] -> [Tazemetostat] -> [CRISPR sweep]
     Phase 1          Phase 2        Phase 3, 14 d       Phase 4
                           ^               |
                           +---------------+
                       Phase 3 undoes the Phase 2 lock

  Phase 4 must then cut through the chromatin Phase 2 built,
  which is where Cas9 is weakest.

CORRECTED, three sequenced stages

  [Stage A, clearance] -> [Stage B, excision]  -> [Stage C, lock]
   Tazemetostat,           CRISPR RNP,             BrecOFF,
   Days 0 to 28            around Day 42           around Day 56
   MHC-I up, CTL killing   chromatin accessible    terminal

  Each agent now meets the chromatin state that suits it,
  and no stage has to undo the one before.
```

Stage A reduces the reservoir while it is still visible to the immune system. Stage B excises what survives, while the chromatin is still open enough for Cas9 to work. Stage C silences the remainder, and nothing after it tries to reopen what it closed.

### The three stages

| | Stage A, clearance | Stage B, excision | Stage C, lock |
| --- | --- | --- | --- |
| Product | TAZ-LNP01 | CRX-LNP02 | BRO-LNP03 |
| Payload | Tazemetostat, polymer-lipid core, sustained release | Cas9 RNP, multiplexed guides, ionizable LNP | BrecOFF mRNA, ionizable LNP |
| Window | Days 0 to 28 | Around Day 42 | Around Day 56 |
| Mechanism | EZH2 inhibition raises MHC-I and BIM, reinvigorates CD8+ T cells | Excision at ultraconserved LTR and *pol* sites | Targeted methylation and KRAB repression at the 5' LTR |
| Primary readout | Intact provirus per million CD4+ cells, CD8+ phenotype | Change in intact proviral DNA, translocation panel | LTR CpG methylation, time to rebound off ART |
| Key risk | Transient viremia from latency reversal | Chromosomal translocation | Off-target host methylation |

### Why the washout between Stage A and Stage B matters

Tazemetostat depletes H3K27me3 genome-wide. Stage B should fire while the LTR is accessible, so a short overlap is acceptable and probably helpful. Stage C must not begin until EZH2 activity has recovered, or the lock is being built against an active inhibitor. The gap between Stage B and Stage C exists for that recovery, and the interval has to be set experimentally from an H3K27me3 recovery curve rather than assumed.

### What this removes

- The impossible dual-release particle. Each product now has one release profile.
- The antagonism between payloads. They no longer occupy the same cell at the same time.
- The chromatin barrier to editing. Cas9 now acts before the heterochromatin exists.
- A regulatory problem. Three single-payload products can each be characterized, released and dose-ranged on their own, where one tri-functional particle cannot.

### What it costs

Three INDs instead of one, or one IND with a staged combination protocol and a strong justification. A longer treatment schedule. A combination rule from FDA, which requires the contribution of each component to be demonstrated. These are real costs and they are worth paying, because the single-particle version does not work.

---

## 5. Target Product Profile

**The commercially and clinically meaningful endpoint is ART-free remission measured in an analytical treatment interruption, not a reservoir log reduction.** A regimen that cuts the reservoir by 90 percent and does not delay rebound has failed, because rebound kinetics are driven by the residual intact reservoir and a tenfold cut buys only weeks.

### Regimen-level profile

| Attribute | Minimum acceptable | Target |
| --- | --- | --- |
| Indication | ART-suppressed HIV-1, plasma RNA under 50 copies per mL for at least 24 months, CD4 above 500 | Same, broadened to include suboptimal immune reconstitution |
| Primary endpoint | Time to plasma rebound above 1,000 copies per mL during monitored ATI | Sustained remission off ART at 52 weeks |
| Efficacy bar | Median time to rebound extended from roughly 2 to 4 weeks to at least 12 weeks | No rebound at 52 weeks in at least 30 percent of participants |
| Reservoir readout | At least 1.0 log reduction in intact provirus by IPDA, confirmed by Q4PCR | At least 2.0 log, with no detectable intact provirus in a subset |
| Safety ceiling | No Grade 4 events attributed to the regimen, no new malignancy signal | No Grade 3 or above beyond transient infusion reactions |
| Genomic safety | No clonal expansion detected, no insertional or translocation event above assay background | Zero detected translocation events at the target loci |
| Route and setting | IV infusion, specialist outpatient centre | Same, three visits total |
| ART handling | ART continues throughout all three stages, interrupted only for the monitored ATI | Same |

### Product-level critical quality attributes

The original CQA set carries over per particle, with the dual-payload specification removed.

| CQA | TAZ-LNP01 | CRX-LNP02 | BRO-LNP03 |
| --- | --- | --- | --- |
| Particle diameter, Z-average | 85 ± 15 nm | 90 ± 15 nm | 85 ± 15 nm |
| Polydispersity index | at or below 0.15 | at or below 0.15 | at or below 0.15 |
| Encapsulation efficiency | at or above 85 percent, tazemetostat | at or above 80 percent, RNP | at or above 90 percent, mRNA |
| Release profile | zero-order over 14 days | single bolus, RNP half-life under 4 hours intracellular | endosomal release within 2 hours |
| Endotoxin | at or below 0.5 EU per mL | at or below 0.5 EU per mL | at or below 0.5 EU per mL |
| Targeting ligand | CD4-directed | CD4-directed | CD4-directed |
| Potency assay | EZH2 inhibition, H3K27me3 loss in primary CD4+ cells | indel frequency at each target locus | LTR CpG methylation, Δβ at defined positions |

### A note on the targeting ligand

The original design specifies CD4 and CCR5 ligands. CCR5 is worth reconsidering. Its natural ligands are chemotactic and trigger receptor internalization and downstream signalling, so a CCR5-ligand corona is a pharmacologically active surface, not a passive address label. A CD4-directed single-domain antibody or an anti-CD4 Fab fragment gives the same tropism without agonism. This should be settled before GLP material is made, because it changes the biodistribution package.

---

## 6. Corrected PK/PD model specification

**The model needs four structural changes before it can inform a single decision.** Re-running the current one with better parameters will not help, because the defects are in the equations, not the constants.

### Change 1: connect delivery to effect

Right now there is one global BrecOFF pool that no compartment feeds. Each compartment needs its own cargo concentration, driven by the transfer rate into that compartment. Until this holds, no targeting question can be asked of the model.

```latex
\frac{dB_j}{dt} = f_j \, k_j \, C_p(t) - \delta_B B_j, \qquad j \in \{\text{lymph}, \text{macro}, \text{periph}\}
```

Here `k_j` is the transfer rate into compartment j and `f_j` is the fraction of particles there that achieve endosomal escape. That second term is where most of the real uncertainty lives, and it is currently absent from the model entirely.

### Change 2: make the lock reversible, because it is

The current locking equation has `kon = 0.02` against `koff_max = 5.0`, a 250-fold ratio that guarantees the answer. The dominant route out of a methylated state in a dividing cell is not spontaneous reactivation, it is dilution across replication. Memory CD4+ T cells proliferate, and maintenance methylation is imperfect.

```latex
\frac{dL_j}{dt} = k_{\text{lock}}(B_j)\,(R_j - L_j) \;-\; \left(k_{\text{rev}} + \beta_j \varepsilon\right) L_j
```

`β_j` is the proliferation rate of the reservoir cells in compartment j and `ε` is the per-division probability that the mark is lost. Durability of a block-and-lock therapy is determined almost entirely by that product. It is the single most important parameter in the program and the current model does not contain it.

### Change 3: count cells, not fractions

A locked fraction is not an endpoint. Track intact, reactivation-competent provirus as a count per compartment, so the model speaks the same language as IPDA and as the clinical protocol.

### Change 4: output rebound, not locking

The decision the model exists to support is whether a participant rebounds during an ATI. That requires a hazard built from the residual unlocked reservoir.

```latex
\lambda(t) = \sum_j a_j \left(R_j(t) - L_j(t)\right), \qquad P(\text{no rebound by } T) = \exp\!\left(-\int_0^T \lambda(t)\,dt\right)
```

`a_j` is the per-provirus successful-reactivation rate, meaning reactivation that goes on to establish spreading infection rather than being aborted. The original material asserts this falls below 10 to the minus 6 per cell per month. That assertion is the central claim of the entire program and nothing in the supplied code computes it.

### On parameters and identifiability

The present model carries twelve or more free constants, all invented, and no data. A global sensitivity analysis over invented parameters tells you about the equations, not about the biology, which is why the Sobol results were uninformative even before they turned out to be hardcoded.

The practical path is to cut the model to the parameters that actually move the rebound hazard, then measure those few:

| Parameter | How to measure it | Why it dominates |
| --- | --- | --- |
| `β·ε`, mark loss per division | Serial methylation tracking in dividing primary CD4+ cells over 60 days | Sets durability, and durability is the product |
| `f_lymph`, endosomal escape in lymphoid tissue | Reporter mRNA in humanized mouse lymph node, single-cell resolution | Usually the largest unknown in LNP delivery |
| `a`, successful reactivation per residual provirus | Quantitative viral outgrowth in cells from treated donors | Converts reservoir size into rebound time |
| `k_lock` at achievable `B` | Dose-response of LTR methylation in primary cells | Says whether the effect saturates at a tolerable dose |

Four measured parameters in a model with the right structure will support a go or no-go decision. Twelve invented ones in a model with the wrong structure will not, however many Monte Carlo trials are run over them.

---

## 7. IND-enabling preclinical plan

The drafted GLP toxicology matrix is sound in structure and most of it carries over. Three things have to change first.

### Gating issue: the Stage A agent no longer exists

Tazemetostat is withdrawn, so Stage A needs a decision before anything else is commissioned. There are three options and they are not equally attractive.

**Option 1, substitute another EZH2 inhibitor.** Valemetostat and others exist. The problem is that the liability is probably mechanism-based rather than molecule-specific. PRC2 is required for normal haematopoiesis, and EZH2 loss-of-function is itself a recognised driver lesion in T-cell acute lymphoblastic leukaemia and in myeloid malignancy. Pharmacological inhibition plausibly phenocopies the driver. A different molecule in the same class should be assumed to carry the same risk until shown otherwise, which is an expensive thing to show.

**Option 2, keep EZH2 inhibition but make targeted delivery the mitigation.** This is the strongest scientific argument for the nanoparticle in the first place. The cells that give rise to MDS and AML are CD34+ haematopoietic stem and progenitor cells. A CD4-directed particle should largely spare them. If lymphoid tissue exposure can be achieved with CD34+ compartment exposure held orders of magnitude lower, there is a real case. The burden of proof is high, and it has to be met with a dedicated study rather than asserted from the targeting ligand.

**Option 3, replace the immune arm entirely.** Broadly neutralising antibody combinations, IL-15 superagonists, TLR7 agonists and PD-1 blockade all have HIV reservoir data and none carries a withdrawn-for-leukaemia history.

Recommendation: Option 3 for the lead program, with Option 2 as a parallel track only if the MHC class I restoration mechanism turns out to be load-bearing in the Stage A pharmacology studies. Option 1 should not be pursued without data separating the molecule from the class.

### The species problem in the drafted plan

TOX-01 as written puts a CD4-directed human-targeted construct into Sprague-Dawley rats. An anti-human CD4 ligand will not engage rat CD4, and rats are not infectable with HIV-1. That study therefore measures the lipid platform and the free payload, which is useful, but it is not a toxicology study of the product and should not be labelled as one.

Under ICH S6(R1), if no pharmacologically relevant species exists you need either a homologous surrogate construct or a transgenic model, and you justify the gap. Three actions follow:

1. Confirm cynomolgus CD4 cross-reactivity by surface plasmon resonance and flow cytometry before TOX-02 is designed. If the ligand does not cross-react, TOX-02 has the same defect as TOX-01.
2. Relabel TOX-01 as a platform and excipient toxicology study, which is a legitimate and necessary study in its own right.
3. Keep humanized BLT mice as the pharmacology and biodistribution species. They are not a GLP toxicology species and should not be presented as one.

### Reduce the guide array from seven sites to two

Excision of a provirus requires two cuts, one at each flanking LTR. Seven simultaneous guides do not excise better, they fragment, and they multiply the translocation surface. With n concurrent double-strand breaks the number of pairs available to mis-join is n(n-1)/2, so seven sites give 21 pairings against one for two sites.

The aggregate formula in the source material computes the probability of at least one off-target cut, which is not the quantity of interest. Translocation needs two concurrent breaks, so the expected count scales with the pairwise product:

```latex
E[\text{translocations}] \;\approx\; \sum_{i<j} p_i\,p_j\,\phi_{ij}
```

`φ_ij` is the joining propensity for that pair, which depends on nuclear proximity and is not uniform. Two guides reduce this term by more than an order of magnitude before any high-fidelity engineering is applied.

### Revised study matrix

| Study | Status | Change |
| --- | --- | --- |
| PK-01 biodistribution | Keep | Add CD34+ bone marrow compartment as a named endpoint, not a tissue in a list. This is now a primary readout, not a secondary one |
| GEN-02 off-target methylation | Keep | Extend sampling to Day 90, since durability is the product. Add imprinted loci and tumour suppressor promoters as a prespecified panel |
| TOX-01 rat | Modify | Relabel as platform and excipient toxicology. Do not claim product-level relevance |
| TOX-02 NHP | Modify | Gate on confirmed CD4 cross-reactivity. Add CD34+ clonality and clonal haematopoiesis panel |
| SP-01 safety pharmacology | Keep | No change |
| IMM-01 cytokine release | Keep | Add complement activation in the same donors, so CARPA and CRS are read together |
| GEN-03 genetic toxicology | Keep | No change |
| **TRANS-01 translocation panel** | **New** | Required. CAST-Seq or UDiTaS across all guide pairings in primary CD4+ cells from at least six donors. There is currently no study covering the risk the source material correctly identifies |
| **DUR-01 durability** | **New** | Required. Serial LTR methylation in dividing primary CD4+ cells to 90 days, to measure mark loss per division. This yields the parameter that determines whether the therapy works at all |
| **HSPC-01 stem cell sparing** | **New** | Required only if Option 2 is taken. Quantify CD34+ exposure against lymphoid exposure, with colony-forming and serial-replating readouts |

### On the IND strategy

Three sequential products is a combination development problem. FDA's combination rule requires the contribution of each component to be demonstrated, which in practice means the clinical plan has to include arms that drop a stage. Build that into the Phase 1b design rather than discovering it at the end-of-Phase-1 meeting. A single IND covering a staged protocol is achievable but the justification has to be written early and agreed at a pre-IND meeting.

---

## 8. Risks and go or no-go gates

**The risk that should set the pace of this program is not toxicity, it is durability.** A block-and-lock therapy that loses its mark across cell division fails quietly, months after dosing, in people who have already interrupted ART. Everything else on this list is detectable earlier and managed more conventionally.

### Risk register

| Risk | Why it is serious here | Mitigation | Stopping rule |
| --- | --- | --- | --- |
| Mark loss across division | Memory CD4+ T cells proliferate and maintenance methylation is imperfect. If the lock dilutes, rebound simply arrives later, and the trial reads as a failure after a long and expensive ATI | Measure it before anything else, in DUR-01. Consider co-targeting a self-reinforcing mark rather than methylation alone | Under 80 percent methylation retained at Day 90 in dividing cells ends the block-and-lock approach |
| Secondary haematologic malignancy | The Stage A class has been withdrawn for exactly this. The population is healthy and long-lived | Replace the agent, or prove CD34+ sparing in HSPC-01 | Any clonal expansion signal in the CD34+ compartment stops Stage A |
| Off-target host methylation | DNMT3A-3L fusions methylate promiscuously. This is the characteristic failure of the construct class, not an edge case | GEN-02 extended to Day 90, with a prespecified panel of tumour suppressor and imprinted loci | Any significant hypermethylation at a tumour suppressor promoter stops the construct |
| Chromosomal translocation | Concurrent double-strand breaks mis-join. Currently unmeasured in the plan | Reduce to two guides, high-fidelity Cas9, transient RNP, and TRANS-01 to actually look | Any translocation above assay background at the target pairings |
| Pre-existing anti-Cas9 immunity | Most adults carry antibodies and memory T cells against *S. pyogenes* Cas9, so a Cas9 RNP can meet an established recall response | Screen participants for anti-Cas9 reactivity at entry. Consider an orthologue with lower seroprevalence | High-titre participants excluded, not dosed and monitored |
| Immunogenicity to dBrec1 | An engineered recombinase domain is foreign protein, and CTL clearance of edited cells defeats the purpose | Anti-dBrec1 IgG and IFN-gamma ELISpot at Days 14, 28 and 56 | Durable methylation must be established before adaptive clearance, or the design fails |
| CARPA | PEGylated and targeted LNPs activate complement, with hemodynamic consequences | Stepped 60-minute infusion, SC5b-9 and C3a monitoring at 15, 30 and 60 minutes | C3a above threefold baseline triggers the premedication protocol |
| Transient viremia in Stage A | Latency reversal releases virus while the participant is on ART | ART continues throughout. Monitor plasma RNA weekly | Sustained viremia above 1,000 copies per mL on ART |
| Endosomal escape failure | The usual reason LNP programs fail in vivo, and the parameter the model omits entirely | Measure `f_lymph` directly with a reporter in humanized mice before committing to GLP | Escape fraction too low to reach the `k_lock` dose-response window |

### Gates, in order

These are sequential. Each one can stop the program, and they are ordered cheapest and most decisive first.

1. **Durability, DUR-01.** At least 80 percent of LTR CpG methylation retained at Day 90 in dividing primary CD4+ cells. *This gate comes first because it is the cheapest experiment that can kill the whole premise.* If the mark does not survive proliferation, no amount of delivery optimisation rescues the program.
2. **Delivery, PK-01.** Lymphoid-to-hepatic AUC ratio at or above 3.5, and a measured endosomal escape fraction sufficient to reach the effective concentration window.
3. **Stage A agent decision.** Either a replacement immune agent is selected, or HSPC-01 shows CD34+ exposure at least two orders of magnitude below lymphoid exposure.
4. **Genomic safety, GEN-02 and TRANS-01.** No significant off-target hypermethylation at the prespecified panel. No translocation above assay background.
5. **NHP tolerability, TOX-02.** A NOAEL that supports a maximum recommended starting dose with a tenfold safety factor, in a species with confirmed CD4 cross-reactivity.
6. **Pre-IND meeting.** Agreement on the combination strategy and on the species justification, before GLP material is committed.

Gate 1 is worth emphasising. The entire program rests on a durability parameter that nobody has measured and that the current model does not contain. It is a 90-day cell culture experiment. It should be running now, ahead of any further modelling, formulation or regulatory work.

---

## 9. Gaps

**There is currently no experimental data in this program.** Everything produced so far is simulation of a model whose structure determines its own output. That is a normal place to be at the concept stage, but it should be named, because the volume of generated analysis can make a program feel further along than it is.

### The foundational gap: dBrec1 is not a validated tool

Brec1 is a real engineered recombinase, evolved to excise integrated provirus by recognising a sequence in the LTR. The construct proposed here uses a catalytically dead version as a DNA-binding module to deliver methyltransferase and KRAB domains.

That is a reasonable idea and it is also entirely unvalidated. Three questions have no answer yet:

- Does catalytically dead Brec1 bind the LTR with useful affinity and residence time when it can no longer complete recombination? Recombinase binding and catalysis are coupled, and dead variants do not automatically make good DNA-binding domains.
- Does the roughly 900 residue four-domain fusion fold and retain both binding and methyltransferase activity?
- Does LTR sequence diversity across clinical isolates preserve the recognition site? Brec1 was selected against particular LTR sequences, and conservation across subtypes is an empirical question, not an assumption.

If dBrec1 does not bind well, a dCas9 or zinc finger targeting module does the same job with established behaviour, at the cost of the construct's distinctiveness. This should be tested early and cheaply, because it determines what the program is.

### Reservoir biology the model ignores

The model treats the reservoir as one uniform pool. It is not, and the heterogeneity runs against the therapy.

Most integrated proviruses are defective and clinically irrelevant, so silencing them achieves nothing while still counting toward any assay that does not distinguish intact from defective. More importantly, proviruses sitting in already-closed chromatin are already quiet. The ones that drive rebound are the ones in actively transcribed regions, which are exactly the hardest to silence and the most likely to lose a methylation mark.

So the therapy has to work hardest precisely where it works least well, and the current model cannot represent that at all. Stratifying by integration site context is not a refinement, it is the difference between a model that flatters the approach and one that tests it.

### Everything else that is missing

- No in vitro proof of concept in primary cells from ART-suppressed donors
- No in vivo pharmacology in humanized mice
- No CMC: no process, no analytical methods, no stability, no GMP path
- No validated potency assay for any of the three products
- No clinical protocol, and in particular no framework for the analytical treatment interruption, which carries its own risks around transmission, rebound and CD4 decline and is increasingly scrutinised by ethics committees
- No measured parameter anywhere in the PK/PD model

### What to do next

Three things, in this order, and the first two are small.

1. **Run the durability experiment.** Serial LTR methylation in dividing primary CD4+ cells over 90 days. This is the cheapest experiment that can end the program, so it should run first.
2. **Test dBrec1 binding.** Electrophoretic mobility shift or ChIP against LTR sequences from a panel of clinical isolates, with the full fusion and with the binding domain alone.
3. **Decide the Stage A agent.** This is a strategic decision, not an experiment, and it blocks all downstream formulation and toxicology work.

Until those three are resolved, further modelling, optimisation and sensitivity analysis will add volume without reducing uncertainty.

---

## Sources

Pages opened for this review, as of 12 November 2026.

| Source | Used for |
| --- | --- |
| [Nguyen, Das, Dobrowolski and Karn, mBio 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5347344/) | EZH2 inhibitors GSK-343 and EPZ-6438 reverse HIV latency in primary cells and in patient resting memory CD4+ T cells |
| [EZH2 inhibition mitigates HIV immune evasion, Cell Reports 2025](https://doi.org/10.1016/j.celrep.2025.115652) | Tazemetostat raises MHC class I and BIM, improves CTL clearance, reduces exhaustion |
| [Kallimasioti-Pazi et al., PLoS Biology 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6306241) | Heterochromatin impedes Cas9 mutagenesis up to sevenfold under brief, low-level exposure |
| [Jensen et al., FEBS Letters 2017](https://www.pubmed.gov/28580607/) | Editing efficiency is higher in euchromatin than heterochromatin |
| [TAZVERIK prescribing information, FDA](https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/211723s004lbl.pdf) | Secondary malignancies warning, added November 2023 |
| [Ipsen withdraws tazemetostat, March 2026](https://www.pharmacytimes.com/view/ipsen-voluntarily-withdraws-tazemetostat-from-all-markets-following-safety-signal-in-confirmatory-trial) | Worldwide withdrawal from all indications, 9 March 2026, and discontinuation of all trials |
| [FDA safety alert on tazemetostat](https://www.hmpgloballearningnetwork.com/site/onc/fda-alerts/fda-issues-safety-alert-tazemetostat-following-secondary-malignancy-risk) | SYMPHONY-1 interim rate of 5.7 percent haematologic second primary malignancies against zero in control |

Model verification figures in section 3 come from re-running the supplied scripts, not from a published source.
