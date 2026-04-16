---
title: "Automaton Model"
date: 2026-04-15T12:29:25-05:00
math: mathjax
draft: false
_build:
  list: never
---


We discuss the framework presented in [this paper](https://www.nature.com/articles/s41587-024-02271-7) from 2024. 

## Background

Broadly, there are two classes of chemotherapy treatments, usually differentiated by cell cycle nonspecific agents (CCNSA) and cell cycle specific agents (CCSA). Non-specific treatments kill cancer cells at all phases of the cell cycle, but these are usually significantly more toxic<sup>[1](#ref1)</sup>.  Specific treatments can be further distinguished by whether it is cytotoxic (killing agents that kill the neoplastic/abnormal cells) or cytostastic (blocking agents that prohibit the proliferation of abnormal cells).  

Alternatively, there is also targeted therapy.  Rather than attacking (almost) all rapidly dividing cells, targeted therapies interfere with specific cell molecules required for carcinogenesis. By blocking specific enzymes and modifying functions of proteins regulating gene expression, these therapies, in an ideal world, would be the 'magic bullet' in treating cancer.  However, in practice, while these therapies will prolong patient survival, they often do not lead to a cure.  These drugs target specific sites within the tumor, and consequently, any mild deviation in the tumor landscape will lead to pockets of cells that are not affected by the therapy.  Tumors exhibit a significant degree of heterogeniety - as cells divide, they acquire new mutations, creating distinct subclones with completely different molecular profiles.  Even if cells are susceptible at first, there is no guarantee that things will stay that way.  Moreover, even within the initial batch of cancer cells, there is often a side-population of resiliant cancer stem cells (or tumor-initiating cells) that survive<sup>[2](#ref2)</sup>.  

Rather than a single drug, one could employ a combination of targeted treatments, which has been shown to outpace evolution of resistances. When doing so, it is important to ensure that the mechanisms of resistance are distinct for each drug.  Otherwise, a mutation leading to the resistance of one drug would also impact the efficacy of the other drugs.  However, determining a drug cocktail with completely orthogonal resistance pathways is challenging, and suggests a limited potential<sup>[3](#ref3)</sup>.

One variation of targeted therapy is gene-directed enzyme prodrug therapy (GDEPT).  GDEPT is a three-part system: a delivery carrier, a gene encoding a specific enzyme, and a harmless prodrug (i.e. an inactive drug). After the gene is cloned into a vector and delivered to a tumor cell, the enzyme then expressed converts prodrug to a potent cytotoxic drug.  By passive diffusion, the cytotoxin not only kills the modified cell, but also neighboring cells<sup>[4](#ref4)</sup>.  
<figure>
  <img src="/posts/automata/gdept_diagram.jpg" alt="GDEPT Mechanism" width="500">
  <figcaption style="text-align: center;">Figure 1: Process for GDEPT<sup><a href="#ref4">[4]</a></sup>.</figcaption>
</figure>

While GDEPT significantly reduces the toxicity by limiting the the cytotoxic drug to point-sources within the tumor, it is physically impossible to successfully deliver the suicide gene to 100% of the cells in a dense, solid tumor, or even anywhere near the required percentage. The bystander effect helps, but depending on the composition of the tumor, the engineered cells often cannot manufacture enough toxin to create an effect strong enough to wipe out the entire mass.  

## Pritchard Lab Framework
Rather than iterating through single drugs, with each drug working until the cells evolve to be resistant (a reverse engineering approach), this alternative framework proposes to redesign tumors prior to treatment to be more responsive to intervention in the first place (a forward engineering approach).  This is similar to GDEPT, but in addition to the introduction of suicide genes, these gene drive cells are also modified to have higher fitness, and thus the evolution of the tumor begins by an increase in concentration and quantity of modified cells, before the release of the cytotoxin (hopefully) killing all cancerous cells.  

More concretely, the approach first genetically engineers a circuit composed of two genes ('switches') that are introduced into a small number of cells ('gene drives').  Switch 1 acts as a synthetic resistance gene, granting immunity to frontline targeted therapies like osimertinib, a Tyrosine Kinase Inhibitor (TKI).  Importantly, this resistance is only active in the presence of a dimerizer.   Switch 2 is the therapeutic payload gene - once activated by the 5-Fluorocytosine (5-FC) prodrug, the engineered cells blanket the tumor with the cytotoxin 5-Fluorouracil (5-FU).  During the first phase, both the osimertinib and the dimerizer are administered while Switch 1 is active, causing the susceptible cells to die and the gene drive cells, containing Switch 1 and tethered to Switch 2, to survive and multiply.  Additionally, any TKI resistant cells also survive and multiply, at a rate faster than that of the gene drives due to a lower intrinsic fitness cost.  During the second phase, 5-FC is introduced, activating Switch 2 and locally manufacturing 5-FU, which diffuses through the tumor and kills all neighboring cells, TKI resistant or not.  And during the third phase, the dimerizer is stopped, causing Switch 1 to deactivate and the gene drive to become susceptible to the TKI.  

The duration of Phase 2 is a crucial question - Switch 1 often needs to remain active alongside the generation of 5-FU, giving a survival advantage to the gene drive cells.  This advantage must occur just long enough for the gene drive to endure the beginning of the increasing local toxicity and generate enough 5-FU to target the entire tumor, but not so long that it undergoes a mutation that silences Switch 2 but leaves the cell still resistant to the targeted therapy. 

There are concerns about mutational points of failure, including resistance to the therapeutic action of the Switch 2 gene and loss of Switch 2 activity among gene drive cells, but we omit those details the purposes of this discussion. 

## Automaton Model

To obtain a better understanding of how this framework behaves, we present here a cellular automaton model, with the following spatial considerations: each unit of the grid represents one cell, each cell can influence all surrounding cells (i.e. a Moore neighborhood), and there is no boundary. 

There are two grids to keep track of the cell and toxin states.

**Cell States:** 

`0`: Empty Space

`1`: Sensitive Cell (S)

`2`: Native Resistant Cell (R)

`3`: Gene Drive Cell (G)

**Toxin States:** 

`0`: Empty

`1`: 5-FU Present

The coloring for this state-space is as follows:

| Color | State |
| :--- | :--- |
| White | Empty |
| Light Blue | Susceptible|
| Light Red | Resistant|
| Light Green | Gene Drive|
| Purple | 5-FU |
| Dark Blue | Susceptible + 5-FU |
| Dark Red | Resistant + 5-FU |
| Dark Green | Gene Drive + 5-FU |

The model is initially seeded with a spherical tumor with a given percentage of susceptible, resistant, and gene drive cells.  Outside of the tumor is empty space.

Temporally, there are four phases:

**Phase 0 (Untreated):** No drugs active. (Time spent: `phase_0_length`)

**Phase 1 (Switch 1):** TKI + Dimerizer are active. (Time spent: `phase_1_length`)

**Phase 2 (Switch 1 and 2):** TKI + Dimerizer + 5-FC are active. (Time spent: `phase_2_length`)

**Phase 3 (Switch 2):** TKI + 5-FC are active.

#### Step 1: 5-FC update rules
If the 5-FC is active, the toxin grid updates via the following steps:

**Production:** Every **G** cell evaluates its current coordinate. If the coordinate is completely empty of toxin, it spawns a new particle with a probability of `P_produce_toxin`.

**Decay:** Each toxin particle undergoes a survival check and is deleted from the grid with a probability of `P_toxin_decay`.

**Diffusion:** If a particle survives decay, it attempts to physically move. It randomly selects one of its eight neighbors. It will only move to that target coordinate if it is completely empty of toxin.

#### Step 2: Cell update rules
To prevent bias, the cells are internally shuffled before evaluating the following rules sequentially:

**Switch 1 Death Check:** If the TKI is active:

**S** cells die with a probability of `P_TKI_kill`.

**R** cells remain alive.

**G** cells remain alive if the dimerizer is active, and die with probability `P_TKI_kill` if the dimerizer is inactive.

**Switch 2 Death Check:**

If there exists a 5-FU particle within a radius of `bystander_radius` of a surviving cell, then the cell dies with probability `P_toxin_kill`.  In the event of death, the 5-FU particle triggering death is removed.

**Division and Migration:**
If the cell survives both death checks, it attempts to physically expand.  With a probability `P_divide_S`, `P_divide_R`, or `P_divide_G` (depending on cell type), the cell duplicates itself into a randomly selected empty neighbor.  If the cell does not divide, it makes a secondary check to move into a randomly selected empty neighbor, with probability `P_move`.

(TO DO: Should there be a lower bound on the number of neighboring cells before division or migration?)

### Example

<div style="display: flex; justify-content: space-around;">
  
  <figure style="width: 45%; margin: 0;">
    <img src="/posts/automata/tumor1_v2.gif" alt="tumor shrinking" style="width: 100%;">
    <figcaption style="text-align: center;">Figure 2: Case of tumor shrinking</figcaption>
  </figure>

  <figure style="width: 45%; margin: 0;">
    <img src="/posts/automata/tumor3_v2.gif" alt="tumor grwoth" style="width: 100%;">
    <figcaption style="text-align: center;">Figure 3: Case of tumor growth</figcaption>
  </figure>

</div>

#### Parameters for the above simulations:

| Parameter | Value | Description |
| :--- | :--- | :--- |
| `grid_size` | 100 | Size of the grid |
| `frames` | 200 | Number of frames |
| `P_move` | 0.2 | Cell migration prob |
| `P_TKI_kill` | 0.5 | Prob TKI kills susceptible cells per step |
| `P_produce_toxin` | 1 | Prob a G cell spawns a 5-FU particle (Switch 2) |
| `P_toxin_kill` | 0.2 | Prob a 5-FU particle kills a cell on contact |
| `P_toxin_decay` | 0.05 | Prob a toxin particle naturally degrades |
| `bystander_radius` | 2 | Kill zone radius for cell given presence of 5-FU |
| `tumor_radius` | 8 | Initial radius of tumor |
| `init_susceptible` | 0.85 | Initial percentage of susceptible cells |
| `init_resistant` | 0.02 | Initial percentage of resistant cells |
| `P_divide_S` | 0.15 | Susceptible cell growth |
| `P_divide_R` | 0.15 | Resistant cell growth |
| `P_divide_G` | 0.14 | Gene Drive cell growth |
| `phase_0_length` | 30 | Length of Phase 0 |
| `phase_1_length` | 30 | Length of Phase 1 |
| `phase_2_length` | 50 | Length of Phase 2 |


### Next Steps
Possibly consider a hybrid cellular automaton model, similar to [this](https://pmc.ncbi.nlm.nih.gov/articles/PMC2652069/).





## References:

<p id="ref1">[1] Sun Y, Liu Y, Ma X, Hu H. The Influence of Cell Cycle Regulation on Chemotherapy. Int J Mol Sci. 2021 Jun 28;22(13):6923. doi: 10.3390/ijms22136923. PMID: 34203270; PMCID: PMC8267727.</p>


<p id="ref2">[2] Joo WD, Visintin I, Mor G. Targeted cancer therapy--are the days of systemic chemotherapy numbered? Maturitas. 2013 Dec;76(4):308-14. doi: 10.1016/j.maturitas.2013.09.008. Epub 2013 Sep 20. PMID: 24128673; PMCID: PMC4610026.</p>

<p id="ref3">[3] Leighow SM, Reynolds JA, Sokirniy I, Yao S, Yang Z, Inam H, Wodarz D, Archetti M, Pritchard JR. Programming tumor evolution with selection gene drives to proactively combat drug resistance. Nat Biotechnol. 2025 May;43(5):737-751. doi: 10.1038/s41587-024-02271-7. Epub 2024 Jul 4. PMID: 38965430; PMCID: PMC12285669.</p>

<p id="ref4">[4] Zhang J, Kale V, Chen M. Gene-directed enzyme prodrug therapy. AAPS J. 2015 Jan;17(1):102-10. doi: 10.1208/s12248-014-9675-7. Epub 2014 Oct 23. PMID: 25338741; PMCID: PMC4287286.</p>