# drg-human.csv — provenance

Human dorsal root ganglion. Gene choice rule: support in a human dataset of the cited source; no listed gene used for two types in this file. For Bhuiyan-sourced neuronal genes, the Table S6 row in the TARGET cluster is the evidence (padj<0.05, avg_log2FC >= 0.5 unless noted), and "other" rows show any other cluster where the gene is also up (log2FC>0.25) so specificity can be judged.

Types left out: Calca+Adra2a and Calca+Dcn (PEP subtypes) — too few specific human markers (89 and 33 rows in S6, most padj=1 or shared); separate A-beta RA vs A-beta SA/field LTMR — merged because the two human clusters share their markers; NPPB-only or GFRA2-based pruritogen/C-LTMR markers — NPPB, IL31RA and OSMR are also up in the human NP cluster, GFRA2 in NP and C-LTMR; perineurial vs endoneurial fibroblasts — not resolved in these sources (Bhuiyan: fibroblast clusters "likely a mixture of meningeal fibroblasts and those derived from epineurium, perineurium, and endoneurium"); B cells, neutrophils and macrophage subtypes — human immune subclusters in Bhuiyan are cross-species and partly single-donor.

Caveats: names like "CALCA+SMR2" and "MRGPRD-type" are the harmonized-atlas names (SMR2 has no human orthologue; human NP neurons do not list MRGPRD as a marker). Tavares-Ferreira says peptidergic and nonpeptidergic subsets may not be separable in humans (CALCA/TAC1 are broadly expressed). C-LTMR (Th cluster) is small in human (pct values come in steps of ~1/15). Non-myelinating Schwann markers are weak: SCN7A is an annotation marker in Bhuiyan Table S2, but its S6 row is not specific (pct 0.78/0.78).

## Changes after review (2026-10-31)

- Added **Neuron** (SNAP25, RBFOX3; source bhuiyan-2024): Table S2 sheet "Neurons" lists Rbfox3 and Snap25 as "General Neuronal Marker"; sheet WashU (a human dataset) lists SNAP25 and RBFOX3 for "Neurons". It names neuronal clusters whose subtype the sets cannot separate.
- Removed RELN, CDH1, MSR1, CCND2, POU6F2, MCTP2 and SPON1 from the neuron sets: their Table S6 neuronal rows are specific among neurons, but sheet DRG_nonneuronal_human shows them in at least 60 % of a non-neuronal cluster with avg_log2FC >= 0.3 (RELN Schwann-M 0.92; CDH1 satellite glia 0.92; MSR1 immune 0.72; CCND2 Schwann-N 0.84; POU6F2 fibroblast 0.73; MCTP2 Schwann-M 0.66; SPON1 satellite glia 0.61), and the app z-scores every set over all nuclei. ATF3 (pericytes 0.96) is kept as the defining gene of the injured-neuron set; it is a stress gene, so this set should be read with that in mind.
- ABCC9 is attributed to avraham-2022 (Table 1, human smooth-muscle column), its stronger source; its Bhuiyan DRG pericyte row is weak (pct 0.38 vs 0.31).
- ZNF385B is kept: Table S6 sheet DRG_human_FindAllMarker_markers, cluster Pvalb, gene Zfp385b (the mouse-ortholog symbol Table S6 uses for every species), avg_log2FC 1.773, pct.1 0.535, pct.2 0.077, p_val_adj 0.
- SCN7A (non-myelinating Schwann) traces only to Table S2 (annotation markers, the cross-species sheet and the WashU and UTD human sheets); its Table S6 row is not specific.

## Sources

**tavares-ferreira-2022** — Spatial transcriptomics of dorsal root ganglia identifies molecular signatures of human nociceptors. Tavares-Ferreira D, Shiers S, Ray PR, Wangzhou A, Jeevakumar V, Sankaranarayanan I, Cervantes AM, Reese JC, Chamessian A, Copits BA, Dougherty PM, Gereau RW 4th, Burton MD, Dussor G, Price TJ. Sci Transl Med 2022;14(632):eabj8186. DOI 10.1126/scitranslmed.abj8186; PMID 35171654; PMCID PMC9272153 (NIH author manuscript). Licence: none stated by Crossref; PMC: "available for text mining ... consistent with fair use". Verified: Crossref + PubMed esummary; text read from PMC efetch XML. Human DRG Visium (55-µm spots; neuronal barcodes include signal from surrounding cells), 12 clusters H1–H12. Data file S1 (per-cluster rankings) was NOT downloadable (author-manuscript supplement not in PMC OA bucket); only main-text statements are used.

**bhuiyan-2024** — Harmonized cross-species cell atlases of trigeminal and dorsal root ganglia. Bhuiyan SA, Xu M, Yang L, Semizoglou E, Bhatia P, Pantaleo KI, Tochitsky I, Jain A, Erdogan B, Blair S, Cat V, Mwirigi JM, Sankaranarayanan I, Tavares-Ferreira D, Green U, McIlvried LA, Copits BA, Bertels Z, Del Rosario JS, Widman AJ, Slivicki RA, Yi J, Sharif-Naeini R, Woolf CJ, Lennerz JK, Whited JL, Price TJ, Gereau RW IV, Renthal W. Sci Adv 2024;10(25):eadj9173. DOI 10.1126/sciadv.adj9173; PMID 38905344; PMCID PMC11804847. Licence: CC BY-NC 4.0 (PMC XML licence statement); erratum published 6 Dec 2024 (corrections to text/figures/SM; incorporated in PMC version). Verified: Crossref + PubMed; full text via Europe PMC XML; Tables S1–S14 zip from PMC OA S3 (pmc-oa-opendata/PMC11804847.1/sciadv.adj9173_tables_s1_to_s14.zip). Used: Table S6 sheet "DRG_human_FindAllMarker_markers" (human DRG nuclei, neuronal types; Seurat FindAllMarkers vs all other neuronal types) and sheet "DRG_nonneuronal_human"; Table S2 annotation markers (sheets HMS/WashU/UTD = the three human snRNA-seq datasets). NOTE: genes in Table S6 are written as mouse orthologs (paper: "genes from all species were converted to their mouse ortholog"); human symbols here are the HGNC equivalents. Cluster names follow the harmonized (mouse-derived) nomenclature; human data had no Mrgpra3+Mrgprb4, Mrgpra3+Trpv1, Rxfp1 or Calca+Oprk1 rows.

**avraham-2022** — Profiling the molecular signature of satellite glial cells at the single cell level reveals high similarities between rodents and humans. Avraham O, Chamessian A, Feng R, Yang L, Halevi AE, Moore AM, Gereau RW 4th, Cavalli V. Pain 2022;163(12):2348-2364. DOI 10.1097/j.pain.0000000000002628; PMID 35503034; PMCID PMC9522926 (NIH author manuscript). Licence: none in Crossref; PMC: text-mining/fair use. Verified: Crossref + PubMed; text via PMC efetch XML. Human L4/L5 DRG snRNA-seq, 10x Chromium 3' v3, 5 donors, 18,648 nuclei. Used: Table 1 (top 10 DE genes per population, human columns; fold change >1.5 vs all other DRG cell types) and Results text on human marker genes.

## Neuron
Bhuiyan 2024 Table S2: sheet "Neurons": General Neuronal Marker -> Rbfox3, Snap25; sheet WashU (human): Neurons -> SNAP25, RBFOX3.

- **SNAP25** (source: bhuiyan-2024)
- **RBFOX3** (source: bhuiyan-2024)

## Proprioceptor (PVALB+)
Bhuiyan 2024 cluster(s): Pvalb

- **PVALB** (source: tavares-ferreira-2022)
  - Tavares-Ferreira 2022 Results: "The first cluster was classified as proprioceptors (cluster 1) based on the expression of parvalbumin ( PVALB ), neurotrophic receptor tyrosine kinase 3 ( NTRK3 ), and acid-sensing ion channel subunit 1 ( ASIC1 )..."
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Pvalb gene=Pvalb pct.1=0.742 pct.2=0.199 avg_log2FC=2.369 p_val_adj=3.47e-89
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Pvalb pct.1=0.5 pct.2=0.226 avg_log2FC=0.462 p_val_adj=7.13e-10

- **NXPH1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Pvalb gene=Nxph1 pct.1=0.455 pct.2=0.027 avg_log2FC=1.792 p_val_adj=1.16e-138

- **ZNF385B** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Pvalb gene=Zfp385b pct.1=0.535 pct.2=0.077 avg_log2FC=1.773 p_val_adj=2.18e-96
  - note: Table S6 uses mouse-ortholog symbol Zfp385b; human HGNC symbol ZNF385B

- **RUNX3** (source: tavares-ferreira-2022)
  - Tavares-Ferreira 2022 Results: "...displayed enriched expression of Runt-related transcription factor (RUNX) family transcription factor 3 ( RUNX3 )... in A-fiber proprioceptors ( Fig. 2A )"
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Pvalb gene=Runx3 pct.1=0.423 pct.2=0.008 avg_log2FC=0.622 p_val_adj=5.82e-189
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Immune gene=Runx3 pct.1=0.439 pct.2=0.21 avg_log2FC=0.291 p_val_adj=1.01e-01

- **KCNS1** (source: tavares-ferreira-2022)
  - Tavares-Ferreira 2022 Results: proprioceptor "cluster was also enriched for potassium voltage-gated channel modifier subfamily S member 1 ( KCNS1 )"
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Pvalb gene=Kcns1 pct.1=0.399 pct.2=0.061 avg_log2FC=0.787 p_val_adj=1.36e-62
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+S100a16 gene=Kcns1 pct.1=0.412 pct.2=0.083 avg_log2FC=0.330 p_val_adj=3.06e-06

- **WLS** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=Wls pct.1=0.377 pct.2=0.183 avg_log2FC=0.268 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Pvalb gene=Wls pct.1=0.7 pct.2=0.143 avg_log2FC=1.345 p_val_adj=1.16e-102

## A-beta LTMR (NTRK3-high)
Bhuiyan 2024 cluster(s): Ntrk3high+Ntrk2, Ntrk3high+S100a16

- **PTGFR** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Ptgfr pct.1=0.443 pct.2=0.08 avg_log2FC=0.800 p_val_adj=3.71e-48
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3high+S100a16 gene=Ptgfr pct.1=0.559 pct.2=0.095 avg_log2FC=1.170 p_val_adj=2.97e-15

- **HSPB7** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Hspb7 pct.1=0.375 pct.2=0.072 avg_log2FC=0.284 p_val_adj=2.45e-11
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Pvalb gene=Hspb7 pct.1=0.268 pct.2=0.062 avg_log2FC=0.310 p_val_adj=8.40e-22
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Hspb7 pct.1=0.38 pct.2=0.06 avg_log2FC=0.643 p_val_adj=1.84e-43
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3high+S100a16 gene=Hspb7 pct.1=0.471 pct.2=0.073 avg_log2FC=0.887 p_val_adj=3.99e-13

- **NRGN** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=Nrgn pct.1=0.311 pct.2=0.085 avg_log2FC=0.305 p_val_adj=8.07e-05
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Nrgn pct.1=0.247 pct.2=0.081 avg_log2FC=0.392 p_val_adj=4.60e-08
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3high+S100a16 gene=Nrgn pct.1=0.5 pct.2=0.085 avg_log2FC=0.660 p_val_adj=2.08e-12

- **KCNN1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Kcnn1 pct.1=0.321 pct.2=0.123 avg_log2FC=0.303 p_val_adj=6.56e-01
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Kcnn1 pct.1=0.209 pct.2=0.122 avg_log2FC=0.101 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3high+S100a16 gene=Kcnn1 pct.1=0.471 pct.2=0.122 avg_log2FC=0.782 p_val_adj=3.98e-05

## A-delta LTMR (NTRK2+)
Bhuiyan 2024 cluster(s): Ntrk3low+Ntrk2

- **KCNV1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Kcnv1 pct.1=0.857 pct.2=0.122 avg_log2FC=2.064 p_val_adj=7.05e-62
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Smr2 gene=Kcnv1 pct.1=0.367 pct.2=0.124 avg_log2FC=0.381 p_val_adj=4.13e-12

- **CBLN2** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Cbln2 pct.1=0.661 pct.2=0.06 avg_log2FC=1.063 p_val_adj=5.90e-65
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Pvalb gene=Cbln2 pct.1=0.254 pct.2=0.057 avg_log2FC=0.260 p_val_adj=3.86e-21

- **DCHS2** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Dchs2 pct.1=0.607 pct.2=0.031 avg_log2FC=0.860 p_val_adj=1.38e-95

- **KCNJ4** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Kcnj4 pct.1=0.554 pct.2=0.016 avg_log2FC=0.853 p_val_adj=2.45e-129
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Kcnj4 pct.1=0.127 pct.2=0.021 avg_log2FC=0.316 p_val_adj=9.27e-11

- **CACNA1H** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Cacna1h pct.1=0.536 pct.2=0.035 avg_log2FC=0.702 p_val_adj=5.57e-67
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Trpm8 gene=Cacna1h pct.1=0.339 pct.2=0.039 avg_log2FC=0.400 p_val_adj=2.36e-21

## A-delta HTMR (CALCA+BMPR1B)
Bhuiyan 2024 cluster(s): Calca+Bmpr1b

- **SCGN** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Bmpr1b gene=Scgn pct.1=0.437 pct.2=0.051 avg_log2FC=0.897 p_val_adj=1.30e-133

- **TSPAN18** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Bmpr1b gene=Tspan18 pct.1=0.455 pct.2=0.123 avg_log2FC=0.637 p_val_adj=1.90e-84

- **SERTM1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Bmpr1b gene=Sertm1 pct.1=0.597 pct.2=0.255 avg_log2FC=0.771 p_val_adj=9.44e-74

- **PTGIR** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Bmpr1b gene=Ptgir pct.1=0.523 pct.2=0.213 avg_log2FC=0.557 p_val_adj=3.71e-54
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Sstr2 gene=Ptgir pct.1=0.389 pct.2=0.276 avg_log2FC=0.390 p_val_adj=2.52e-05

## A-delta HTMR (CALCA+SMR2)
Bhuiyan 2024 cluster(s): Calca+Smr2

- **CHRNA7** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Smr2 gene=Chrna7 pct.1=0.599 pct.2=0.067 avg_log2FC=2.195 p_val_adj=4.12e-105

- **SAMSN1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Smr2 gene=Samsn1 pct.1=0.51 pct.2=0.123 avg_log2FC=0.837 p_val_adj=6.30e-38
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Immune gene=Samsn1 pct.1=0.525 pct.2=0.3 avg_log2FC=0.501 p_val_adj=1.77e-31

- **LRRTM3** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Smr2 gene=Lrrtm3 pct.1=0.381 pct.2=0.116 avg_log2FC=0.598 p_val_adj=3.98e-17

## Nociceptor (PEP CALCA+SSTR2)
Bhuiyan 2024 cluster(s): Calca+Sstr2

- **PTPRT** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Sstr2 gene=Ptprt pct.1=0.764 pct.2=0.242 avg_log2FC=2.349 p_val_adj=1.53e-163
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Adra2a gene=Ptprt pct.1=0.59 pct.2=0.354 avg_log2FC=0.305 p_val_adj=1.00e+00

- **CNBD1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Sstr2 gene=Cnbd1 pct.1=0.331 pct.2=0.07 avg_log2FC=1.720 p_val_adj=5.71e-68

- **PCDH15** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Sstr2 gene=Pcdh15 pct.1=0.399 pct.2=0.152 avg_log2FC=0.910 p_val_adj=5.42e-43

- **CACNG3** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Calca+Sstr2 gene=Cacng3 pct.1=0.366 pct.2=0.155 avg_log2FC=0.783 p_val_adj=1.19e-32

## Nociceptor (NP MRGPRD-type)
Bhuiyan 2024 cluster(s): Mrgprd

- **COL6A6** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Mrgprd gene=Col6a6 pct.1=0.691 pct.2=0.133 avg_log2FC=1.460 p_val_adj=1.52e-143
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Smr2 gene=Col6a6 pct.1=0.476 pct.2=0.189 avg_log2FC=0.295 p_val_adj=7.32e-10

- **PRDM8** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Mrgprd gene=Prdm8 pct.1=0.751 pct.2=0.229 avg_log2FC=1.256 p_val_adj=1.33e-116

- **LYPD6B** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Mrgprd gene=Lypd6b pct.1=0.601 pct.2=0.059 avg_log2FC=1.183 p_val_adj=5.26e-179

- **TMEM45B** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Mrgprd gene=Tmem45b pct.1=0.52 pct.2=0.04 avg_log2FC=0.790 p_val_adj=2.84e-168

- **RASSF6** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Mrgprd gene=Rassf6 pct.1=0.598 pct.2=0.105 avg_log2FC=1.056 p_val_adj=1.35e-121

## Pruritogen receptor (SST+)
Bhuiyan 2024 cluster(s): Sst

- **SST** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Sst gene=Sst pct.1=0.944 pct.2=0.14 avg_log2FC=5.088 p_val_adj=8.65e-175

- **CCK** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Sst gene=Cck pct.1=0.416 pct.2=0.019 avg_log2FC=1.706 p_val_adj=8.95e-129

- **CACNG2** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Sst gene=Cacng2 pct.1=0.652 pct.2=0.121 avg_log2FC=1.223 p_val_adj=1.88e-78
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Smr2 gene=Cacng2 pct.1=0.435 pct.2=0.137 avg_log2FC=0.362 p_val_adj=5.65e-16

- **PTPN5** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Sst gene=Ptpn5 pct.1=0.59 pct.2=0.121 avg_log2FC=0.875 p_val_adj=4.95e-64

- **PRKCG** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Sst gene=Prkcg pct.1=0.447 pct.2=0.073 avg_log2FC=0.720 p_val_adj=3.95e-54

- **GRIK4** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Sst gene=Grik4 pct.1=0.683 pct.2=0.291 avg_log2FC=1.253 p_val_adj=7.73e-30

## Cold thermoreceptor (TRPM8+)
Bhuiyan 2024 cluster(s): Trpm8

- **TRPM8** (source: tavares-ferreira-2022)
  - Tavares-Ferreira 2022 Results: "( TRPM8 ), a known menthol and cold-sensitive channel, labeled the cold nociceptors (cluster 6)"
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Trpm8 gene=Trpm8 pct.1=0.732 pct.2=0.135 avg_log2FC=2.065 p_val_adj=4.92e-40

- **ADCY2** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Trpm8 gene=Adcy2 pct.1=0.714 pct.2=0.185 avg_log2FC=1.352 p_val_adj=3.62e-24
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Fibroblast gene=Adcy2 pct.1=0.548 pct.2=0.364 avg_log2FC=0.502 p_val_adj=3.20e-88

- **STUM** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Trpm8 gene=Stum pct.1=0.446 pct.2=0.033 avg_log2FC=0.977 p_val_adj=5.36e-50

- **GPR26** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Trpm8 gene=Gpr26 pct.1=0.375 pct.2=0.011 avg_log2FC=0.870 p_val_adj=5.15e-84

## C-LTMR (TAFA4+)
Bhuiyan 2024 cluster(s): Th

- **GREM1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Th gene=Grem1 pct.1=0.667 pct.2=0.036 avg_log2FC=1.475 p_val_adj=1.23e-32

- **KCNJ6** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Th gene=Kcnj6 pct.1=0.6 pct.2=0.076 avg_log2FC=1.111 p_val_adj=5.56e-10

- **SAMD5** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Th gene=Samd5 pct.1=0.667 pct.2=0.091 avg_log2FC=1.045 p_val_adj=1.84e-10

- **CDH9** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Mrgprd gene=Cdh9 pct.1=0.197 pct.2=0.028 avg_log2FC=0.258 p_val_adj=5.36e-37
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Th gene=Cdh9 pct.1=0.533 pct.2=0.047 avg_log2FC=1.027 p_val_adj=5.66e-14

- **TAFA4** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Trpm8 gene=Tafa4 pct.1=0.232 pct.2=0.051 avg_log2FC=0.309 p_val_adj=2.71e-04
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Th gene=Tafa4 pct.1=0.467 pct.2=0.053 avg_log2FC=0.531 p_val_adj=1.43e-07

## Injured neuron (ATF3+)
Bhuiyan 2024 cluster(s): Atf3

- **ATF3** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Atf3 gene=Atf3 pct.1=1.0 pct.2=0.212 avg_log2FC=2.310 p_val_adj=1.59e-59
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Pvalb gene=Atf3 pct.1=0.31 pct.2=0.222 avg_log2FC=0.470 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Atf3 pct.1=0.411 pct.2=0.218 avg_log2FC=0.452 p_val_adj=1.07e-03
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Pericyte gene=Atf3 pct.1=0.959 pct.2=0.38 avg_log2FC=0.526 p_val_adj=0.00e+00

- **UCN** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Atf3 gene=Ucn pct.1=0.869 pct.2=0.087 avg_log2FC=2.297 p_val_adj=2.72e-92

- **FLRT3** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Atf3 gene=Flrt3 pct.1=0.82 pct.2=0.185 avg_log2FC=1.146 p_val_adj=4.76e-37

- **STAR** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Atf3 gene=Star pct.1=0.607 pct.2=0.067 avg_log2FC=0.990 p_val_adj=1.88e-52

- **SDC1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Atf3 gene=Sdc1 pct.1=0.639 pct.2=0.035 avg_log2FC=0.844 p_val_adj=1.13e-101

- **CARTPT** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_human_FindAllMarker_markers cluster=Atf3 gene=Cartpt pct.1=0.508 pct.2=0.08 avg_log2FC=1.087 p_val_adj=6.58e-28

## Satellite glia
Bhuiyan 2024 cluster(s): Satellite glia
Avraham 2022 Table 1 (Human, top 10 DE genes per population): SGC: GPR98 HMGCS1 TTC6 CTNND2 TRDN QRFPR RIMS1 HEY2 SHANK2 MMD2

- **FABP7** (source: avraham-2022)
  - Avraham 2022 text: "Human specific marker genes were used to classify cell populations; ... SGC (FABP7,CDH19)"; "Fabp7 is expressed at high levels in a majority of SGC (mouse 92%, rat 88% and human 96%"
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=Fabp7 pct.1=0.656 pct.2=0.355 avg_log2FC=0.437 p_val_adj=3.74e-01

- **CDH19** (source: avraham-2022)
  - Avraham 2022 text: "SGC (FABP7,CDH19)" (human markers); "Cdh19 was expressed in most human SGC (98%)"
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=Cdh19 pct.1=0.525 pct.2=0.286 avg_log2FC=0.316 p_val_adj=1.00e+00

- **KCNJ3** (source: avraham-2022)
  - Avraham 2022 text: "Kcnj3 is widely expressed in human (82%) but not in rodents SGC (Fig. 3D)"; Table 2 lists KCNJ3 among top ion channels in human SGC
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Kcnj3 pct.1=0.714 pct.2=0.275 avg_log2FC=0.636 p_val_adj=8.39e-10
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Kcnj3 pct.1=0.456 pct.2=0.274 avg_log2FC=0.454 p_val_adj=1.13e-02
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+S100a16 gene=Kcnj3 pct.1=0.588 pct.2=0.281 avg_log2FC=0.725 p_val_adj=1.00e+00

- **QRFPR** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists QRFPR

- **MMD2** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists MMD2
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Satellite glia gene=Mmd2 pct.1=0.961 pct.2=0.919 avg_log2FC=1.473 p_val_adj=0.00e+00
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Schwann-N gene=Mmd2 pct.1=0.933 pct.2=0.935 avg_log2FC=0.298 p_val_adj=1.00e+00

## Myelinating Schwann cell
Bhuiyan 2024 cluster(s): Schwann-M
Avraham 2022 Table 1 (Human, top 10 DE genes per population): mySC: FMN2 CTNNA3 FUT8 DRP2 MAG NCMAP CDH7 ANKRD30B LRRC7 PMP22

- **PRX** (source: avraham-2022)
  - Avraham 2022 text: "Myelinating Schwann cells ( PRX,MAG,PMP22 )" (human markers)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=Prx pct.1=0.377 pct.2=0.138 avg_log2FC=0.479 p_val_adj=6.87e-03
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Schwann-M gene=Prx pct.1=0.984 pct.2=0.393 avg_log2FC=1.718 p_val_adj=0.00e+00

- **MPZ** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S2 sheets HMS/WashU/UTD: Schwann_M -> MPZ; text: "Myelinating Schwann cells (Schwann_M) express Mpz"
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=Mpz pct.1=0.607 pct.2=0.269 avg_log2FC=0.762 p_val_adj=6.52e-04
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Schwann-M gene=Mpz pct.1=0.941 pct.2=0.278 avg_log2FC=1.342 p_val_adj=0.00e+00

- **NCMAP** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists NCMAP
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Schwann-M gene=Ncmap pct.1=0.927 pct.2=0.266 avg_log2FC=1.091 p_val_adj=0.00e+00

- **DRP2** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists DRP2
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Schwann-M gene=Drp2 pct.1=0.856 pct.2=0.193 avg_log2FC=1.332 p_val_adj=0.00e+00

- **CDH7** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists CDH7
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Pvalb gene=Cdh7 pct.1=0.235 pct.2=0.053 avg_log2FC=0.269 p_val_adj=8.09e-20
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Cdh7 pct.1=0.228 pct.2=0.057 avg_log2FC=0.358 p_val_adj=1.70e-12
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Schwann-M gene=Cdh7 pct.1=0.729 pct.2=0.217 avg_log2FC=0.911 p_val_adj=1.25e-209

- **MAG** (source: avraham-2022)
  - Avraham 2022 text: "Myelinating Schwann cells ( PRX,MAG,PMP22 )"
  - Avraham 2022 Table 1, human column for this population lists MAG

## Non-myelinating Schwann cell
Bhuiyan 2024 cluster(s): Schwann-N
Avraham 2022 Table 1 (Human, top 10 DE genes per population): nmSC: NRXN1 ANK3 GPM6B CNKSR3 LRRC8B MYO1E IL34 CADM2 KCNMB4 ST6GALNAC5

- **SCN7A** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S2 (annotation markers) sheets WashU and UTD: Schwan_n / Scwhann_N -> SCN7A; main text: "non-myelinating Schwann cells (Schwann_N) express Scn7a"
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Bmpr1b gene=Scn7a pct.1=0.896 pct.2=0.784 avg_log2FC=0.394 p_val_adj=6.43e-11
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Schwann-N gene=Scn7a pct.1=0.778 pct.2=0.783 avg_log2FC=0.303 p_val_adj=1.00e+00

- **IL34** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists IL34
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Satellite glia gene=Il34 pct.1=0.63 pct.2=0.703 avg_log2FC=0.377 p_val_adj=7.10e-267
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Schwann-M gene=Il34 pct.1=0.835 pct.2=0.667 avg_log2FC=0.611 p_val_adj=1.65e-154
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Schwann-N gene=Il34 pct.1=0.889 pct.2=0.675 avg_log2FC=1.044 p_val_adj=4.32e-13

- **MYO1E** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists MYO1E
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3low+Ntrk2 gene=Myo1e pct.1=0.536 pct.2=0.175 avg_log2FC=0.666 p_val_adj=1.13e-08
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Trpm8 gene=Myo1e pct.1=0.339 pct.2=0.179 avg_log2FC=0.509 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Th gene=Myo1e pct.1=0.533 pct.2=0.181 avg_log2FC=0.608 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Pvalb gene=Myo1e pct.1=0.376 pct.2=0.166 avg_log2FC=0.516 p_val_adj=9.54e-11
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Endothelial gene=Myo1e pct.1=0.718 pct.2=0.552 avg_log2FC=0.367 p_val_adj=1.36e-74
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Pericyte gene=Myo1e pct.1=0.677 pct.2=0.565 avg_log2FC=0.387 p_val_adj=3.73e-13
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Schwann-N gene=Myo1e pct.1=0.778 pct.2=0.567 avg_log2FC=0.663 p_val_adj=2.29e-05

- **CNKSR3** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists CNKSR3
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Sstr2 gene=Cnksr3 pct.1=0.52 pct.2=0.42 avg_log2FC=0.734 p_val_adj=2.02e-09

- **LRRC8B** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists LRRC8B
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Sst gene=Lrrc8b pct.1=0.64 pct.2=0.466 avg_log2FC=0.410 p_val_adj=7.30e-04
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Smr2 gene=Lrrc8b pct.1=0.694 pct.2=0.464 avg_log2FC=0.354 p_val_adj=1.68e-03
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Adra2a gene=Lrrc8b pct.1=0.59 pct.2=0.474 avg_log2FC=0.456 p_val_adj=1.00e+00

## Fibroblast
Bhuiyan 2024 cluster(s): Fibroblast

- **DCN** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S2 HMS/WashU/UTD: Fibroblast -> DCN
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=Dcn pct.1=0.656 pct.2=0.258 avg_log2FC=0.831 p_val_adj=3.40e-08
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Fibroblast gene=Dcn pct.1=0.825 pct.2=0.255 avg_log2FC=0.986 p_val_adj=0.00e+00

- **PDGFRA** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Fibroblast gene=Pdgfra pct.1=0.726 pct.2=0.317 avg_log2FC=0.835 p_val_adj=0.00e+00

- **SNED1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Sst gene=Sned1 pct.1=0.36 pct.2=0.271 avg_log2FC=0.252 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Sstr2 gene=Sned1 pct.1=0.417 pct.2=0.235 avg_log2FC=0.784 p_val_adj=8.50e-23
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Fibroblast gene=Sned1 pct.1=0.966 pct.2=0.348 avg_log2FC=1.585 p_val_adj=0.00e+00

- **EBF2** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Bmpr1b gene=Ebf2 pct.1=0.287 pct.2=0.109 avg_log2FC=0.522 p_val_adj=1.13e-28
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Fibroblast gene=Ebf2 pct.1=0.884 pct.2=0.317 avg_log2FC=1.465 p_val_adj=0.00e+00
  - Bhuiyan 2024 Table S6 row: other DRG_nonneuronal_human cluster=Pericyte gene=Ebf2 pct.1=0.847 pct.2=0.511 avg_log2FC=0.364 p_val_adj=5.09e-31

- **BICC1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Bmpr1b gene=Bicc1 pct.1=0.298 pct.2=0.144 avg_log2FC=0.309 p_val_adj=5.34e-17
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Smr2 gene=Bicc1 pct.1=0.435 pct.2=0.174 avg_log2FC=0.351 p_val_adj=9.37e-10
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Fibroblast gene=Bicc1 pct.1=0.911 pct.2=0.317 avg_log2FC=1.396 p_val_adj=0.00e+00

- **COL1A1** (source: avraham-2022)
  - Avraham 2022 text: "connective tissue/mesenchymal ( COL1A1,DCN )" (human markers)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Fibroblast gene=Col1a1 pct.1=0.654 pct.2=0.371 avg_log2FC=0.579 p_val_adj=0.00e+00

## Endothelial
Bhuiyan 2024 cluster(s): Endothelial
Avraham 2022 Table 1 (Human, top 10 DE genes per population): Endothelial: LIFR PTPRM EMCN ANO2 VWF EGFL7 TCF4 MKL2 FLT1 CLDN5

- **VWF** (source: bhuiyan-2024)
  - Avraham 2022 Table 1, human column for this population lists VWF
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Endothelial gene=Vwf pct.1=0.941 pct.2=0.251 avg_log2FC=1.645 p_val_adj=0.00e+00

- **FLT1** (source: bhuiyan-2024)
  - Avraham 2022 Table 1, human column for this population lists FLT1
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Endothelial gene=Flt1 pct.1=0.869 pct.2=0.221 avg_log2FC=1.341 p_val_adj=0.00e+00

- **EGFL7** (source: bhuiyan-2024)
  - Avraham 2022 Table 1, human column for this population lists EGFL7
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Bmpr1b gene=Egfl7 pct.1=0.589 pct.2=0.463 avg_log2FC=0.321 p_val_adj=1.07e-07
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+Ntrk2 gene=Egfl7 pct.1=0.703 pct.2=0.486 avg_log2FC=0.421 p_val_adj=7.58e-05
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Ntrk3high+S100a16 gene=Egfl7 pct.1=0.735 pct.2=0.496 avg_log2FC=0.275 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Endothelial gene=Egfl7 pct.1=0.882 pct.2=0.308 avg_log2FC=1.225 p_val_adj=0.00e+00

- **EMCN** (source: bhuiyan-2024)
  - Avraham 2022 Table 1, human column for this population lists EMCN
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Endothelial gene=Emcn pct.1=0.885 pct.2=0.309 avg_log2FC=1.272 p_val_adj=0.00e+00

- **CLDN5** (source: bhuiyan-2024)
  - Avraham 2022 Table 1, human column for this population lists CLDN5
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Endothelial gene=Cldn5 pct.1=0.74 pct.2=0.223 avg_log2FC=0.491 p_val_adj=0.00e+00

- **ERG** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Endothelial gene=Erg pct.1=0.909 pct.2=0.273 avg_log2FC=1.325 p_val_adj=0.00e+00

## Pericyte / smooth muscle
Bhuiyan 2024 cluster(s): Pericyte
Avraham 2022 Table 1 (Human, top 10 DE genes per population): Smooth Muscle: PRKG1 MYH11 INPP4B PIP5K1B RBPMS DGKG MYO1B FAM13C ABCC9 LDB3

- **NOTCH3** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S2 HMS/WashU/UTD: Pericyte(s) -> NOTCH3
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Calca+Dcn gene=Notch3 pct.1=0.231 pct.2=0.061 avg_log2FC=0.379 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Pericyte gene=Notch3 pct.1=0.995 pct.2=0.381 avg_log2FC=1.652 p_val_adj=0.00e+00

- **RGS5** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Pericyte gene=Rgs5 pct.1=0.721 pct.2=0.246 avg_log2FC=0.710 p_val_adj=8.98e-85

- **MYH11** (source: bhuiyan-2024)
  - Avraham 2022 Table 1, human column for this population lists MYH11
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Pericyte gene=Myh11 pct.1=0.698 pct.2=0.199 avg_log2FC=1.325 p_val_adj=1.07e-80

- **ACTA2** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Pericyte gene=Acta2 pct.1=0.73 pct.2=0.219 avg_log2FC=0.893 p_val_adj=9.45e-94

- **ABCC9** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists ABCC9
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Pericyte gene=Abcc9 pct.1=0.384 pct.2=0.31 avg_log2FC=0.414 p_val_adj=6.33e-09

## Macrophage
Bhuiyan 2024 cluster(s): Immune
Avraham 2022 Table 1 (Human, top 10 DE genes per population): Macrophages: RBPJ SLC1A3 CD163 TCF12 MRC1 SYK SPTLC2 LRRK2 DENND3 SLC9A9

- **CD163** (source: avraham-2022)
  - Avraham 2022 text: "macrophages ( CD163,MRC1 )" (human markers)
  - Avraham 2022 Table 1, human column for this population lists CD163
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Immune gene=Cd163 pct.1=0.768 pct.2=0.291 avg_log2FC=1.173 p_val_adj=0.00e+00

- **MRC1** (source: avraham-2022)
  - Avraham 2022 text: "macrophages ( CD163,MRC1 )" (human markers)
  - Avraham 2022 Table 1, human column for this population lists MRC1
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Immune gene=Mrc1 pct.1=0.49 pct.2=0.259 avg_log2FC=0.546 p_val_adj=1.06e-17

- **CSF1R** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S2 sheets HMS/WashU/UTD: Immune -> CSF1R
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=Csf1r pct.1=0.525 pct.2=0.161 avg_log2FC=0.466 p_val_adj=1.59e-08
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Immune gene=Csf1r pct.1=0.928 pct.2=0.413 avg_log2FC=1.157 p_val_adj=0.00e+00

- **F13A1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: other DRG_human_FindAllMarker_markers cluster=Atf3 gene=F13a1 pct.1=0.311 pct.2=0.132 avg_log2FC=0.265 p_val_adj=1.00e+00
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Immune gene=F13a1 pct.1=0.799 pct.2=0.323 avg_log2FC=1.163 p_val_adj=0.00e+00

- **STAB1** (source: bhuiyan-2024)
  - Bhuiyan 2024 Table S6 row: TARGET DRG_nonneuronal_human cluster=Immune gene=Stab1 pct.1=0.97 pct.2=0.506 avg_log2FC=1.328 p_val_adj=0.00e+00

## T cell
Bhuiyan 2024 cluster(s): Immune
Avraham 2022 Table 1 (Human, top 10 DE genes per population): T-cells: PARP8 THEMIS RASGRP1 CD2 LCK STAT4 SKAP1 IL7R ACAP1 CD96

- **CD2** (source: avraham-2022)
  - Avraham 2022 text: "T-cells ( Cd2,Cd3g,Cd28 )" (human marker list)
  - Avraham 2022 Table 1, human column for this population lists CD2

- **CD3G** (source: avraham-2022)
  - Avraham 2022 text: "T-cells ( Cd2,Cd3g,Cd28 )" (human marker list)

- **LCK** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists LCK

- **THEMIS** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists THEMIS

- **IL7R** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists IL7R

- **CD96** (source: avraham-2022)
  - Avraham 2022 Table 1, human column for this population lists CD96
