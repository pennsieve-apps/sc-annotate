# knee-human.csv — provenance

Human knee joint tissues. No gene is listed for two types in this file. Chondrocyte markers come from cartilage-only data (Ji 2019); each chosen chondrocyte gene was checked against the synovium DE tables of Chou 2020 (Tables S1A/S1B) and is absent there. Ji's RegC, ProC, FC and HomC markers were left out because they overlap with synovial fibroblast or SMC markers in Chou (e.g. CHI3L1/CHI3L2, GLIS3, AKR1C2 in SSF; CRLF1, SEMA3C, AMTN in SIF; FRZB in SMC; FC = COL1A1/THY1/PDGFRB) or, for HomC, are immediate-early stress genes (JUN, FOS, NR4A1, ...), which are likely dissociation artefacts.

Left out (no verified human source found or not separable): osteoblasts, osteoclasts, meniscus-specific cells (Swahn 2023 has healthy cartilage and meniscus 10x scRNA-seq but its supplementary marker tables are NIH-manuscript files not retrievable here), TREM2+ synovial lining macrophages (TREM2 only 0.39 of the Chou macrophage cluster; the TREM2+ lining-macrophage paper was not verified), NK cells (Chou: NK/NKT markers "were not detected"), lymphatic endothelium, inflammatory IL1B+ macrophages (activation-state genes, not specific).

Caveats: Ji 2019 = 1,464 whole cells (STRT-seq) from OA cartilage of 10 patients; the prehypertrophic markers are weak (power 0.40–0.53). Ji Table S5 compares EC with RegC only, not with all clusters. Chou 2020 and Zhang 2019 are whole-cell scRNA-seq (Chou: 10x, OA synovium, 3 donors; Zhang: CEL-seq2 on sorted cells, RA+OA synovium, so Zhang markers are relative to cells of the same lineage). Lining markers PRG4/CD55 are also present in most sublining fibroblasts (Chou pct_other 0.92/0.74), and PRG4 is expressed by superficial-zone chondrocytes (Swahn 2023 FC-2 "highly expressed PRG4"). Chou's "B cell" cluster is plasma-cell-like (MZB1, IGJ, DERL3), so it supports Plasma cell, not B cell. Adipocytes: Emont 2022 human white adipose (subcutaneous/visceral, not infrapatellar fat pad) sNuc-seq.

## Sources

**ji-2019** — Single-cell RNA-seq analysis reveals the progression of human osteoarthritis. Ji Q, Zheng Y, Zhang G, Hu Y, Fan X, Hou Y, Wen L, Li L, Xu Y, Wang Y, Tang F. Ann Rheum Dis 2019;78(1):100-110. DOI 10.1136/annrheumdis-2017-212863; PMID 30026257; PMCID PMC6317448. Licence: CC BY-NC 4.0. Verified: Crossref + PubMed; full text via PMC efetch; supplementary files 4–6 from PMC OA S3 (Table S3 = supp004, Table S4 = supp005 cluster markers, Table S5 = supp006 EC vs RegC).

**chou-2020** — Synovial cell cross-talk with cartilage plays a major role in the pathogenesis of osteoarthritis. Chou CH, Jain V, Gibson J, Attarian DE, Haraden CA, Yohn CB, Laberge RM, Gregory S, Kraus VB. Sci Rep 2020;10(1):10868. DOI 10.1038/s41598-020-67730-y; PMID 32616761; PMCID PMC7331607. Licence: CC BY 4.0. Verified: Crossref + PubMed; full text via PMC efetch; Supplementary file 1 (PDF, 230 pages) from PMC OA S3, Tables S1A (all synoviocyte clusters) and S1B (HLA-DRA+ subclusters) parsed to CSV (markers-research/chou-supp/chou_s1.csv; pct and logFC as printed; old symbols e.g. IGJ, WISP2, SEPP1 as printed).

**zhang-2019** — Defining inflammatory cell states in rheumatoid arthritis joint synovial tissues by integrating single-cell transcriptomics and mass cytometry. Zhang F, Wei K, Slowikowski K, Fonseka CY, Rao DA, Kelly S, Goodman SM, Tabechian D, Hughes LB, Salomon-Escoto K, Watts GFM, Jonsson AH, Rangel-Moreno J, Meednu N, Rozo C, Apruzzese W, Eisenhaure TM, Lieb DJ, Boyle DL, Mandelin AM 2nd, Accelerating Medicines Partnership Rheumatoid Arthritis and Systemic Lupus Erythematosus (AMP RA/SLE) Consortium, Boyce BF, DiCarlo E, Gravallese EM, Gregersen PK, Moreland L, Firestein GS, Hacohen N, Nusbaum C, Lederer JA, Perlman H, Pitzalis C, Filer A, Holers VM, Bykerk VP, Donlin LT, Anolik JH, Brenner MB, Raychaudhuri S (PubMed order; Crossref lists the consortium first). Nat Immunol 2019;20(7):928-942. DOI 10.1038/s41590-019-0378-1; PMID 31061532; PMCID PMC6602051 (NIH author manuscript). Licence: Springer TDM only (no open licence). Verified: Crossref + PubMed; full text via PMC efetch; Supplementary Table 4 ("Top 20 marker genes for each single-cell RNA-seq cluster") from static-content.springer.com MOESM4.

**emont-2022** — A single-cell atlas of human and mouse white adipose tissue. Emont MP, Jacobs C, Essene AL, Pant D, Tenen D, Colleluori G, Di Vincenzo A, Jørgensen AM, Dashti H, Stefek A, McGonagle E, Strobel S, Laber S, Agrawal S, Westcott GP, Kar A, Veregge ML, Gulko A, Srinivasan H, Kramer Z, De Filippis E, Merkel E, Ducie J, Boyd CG, Gourash W, Courcoulas A, Lin SJ, Lee BT, Morris D, Tobias A, Khera AV, Claussnitzer M, Pers TH, Giordano A, Ashenberg O, Regev A, Tsai LT, Rosen ED. Nature 2022;603(7903):926-933. DOI 10.1038/s41586-022-04518-2; PMID 35296864; PMCID PMC9504827 (NIH author manuscript). Licence: Springer TDM only. Verified: Crossref + PubMed; full text via PMC efetch; Supplementary Table 1 ("Markers for human clusters and subclusters", sheet "all markers") from static-content.springer.com MOESM4. Text: "adipocytes were found only in the sNuc-seq dataset".

## Chondrocyte (effector)

- **SNORC** (source: ji-2019)
  - note: symbol in source is C2orf82 (previous HGNC symbol); current HGNC SNORC
  - Ji Results: "ECs can be distinguished by the signature which includes ... C2orf82 , CLEC3A and CYTL1"
  - Ji Table S5 (supplementary file 6, EC vs RegC DEGs) EC-marker row: gene=C2orf82 ave_diff=1.976 power=0.85 myAUC=0.925

- **CLEC3A** (source: ji-2019)
  - Ji Results: "ECs can be distinguished by the signature which includes ... C2orf82 , CLEC3A and CYTL1"

- **CYTL1** (source: ji-2019)
  - Ji Results: "ECs can be distinguished by the signature which includes ... C2orf82 , CLEC3A and CYTL1"
  - Ji Table S5 (supplementary file 6, EC vs RegC DEGs) EC-marker row: gene=CYTL1 ave_diff=1.974 power=0.644 myAUC=0.822

- **CHAD** (source: ji-2019)
  - Ji Table S5 (supplementary file 6, EC vs RegC DEGs) EC-marker row: gene=CHAD ave_diff=1.284 power=0.652 myAUC=0.826

- **CNMD** (source: ji-2019)
  - note: symbol in source is LECT1 (previous HGNC symbol); current HGNC CNMD
  - Ji Table S5 (supplementary file 6, EC vs RegC DEGs) EC-marker row: gene=LECT1 ave_diff=1.810 power=0.558 myAUC=0.779

- **SERPINA5** (source: ji-2019)
  - Ji Table S5 (supplementary file 6, EC vs RegC DEGs) EC-marker row: gene=SERPINA5 ave_diff=1.655 power=0.758 myAUC=0.879

## Chondrocyte (prehypertrophic)

- **SRPX2** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=SRPX2 cluster=preHTC ave_diff=1.138 power=0.53 myAUC=0.765


- **AOC2** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=AOC2 cluster=preHTC ave_diff=1.357 power=0.48 myAUC=0.74


- **SOX11** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=SOX11 cluster=preHTC ave_diff=1.701 power=0.456 myAUC=0.728


- **GALNT16** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=GALNT16 cluster=preHTC ave_diff=1.377 power=0.452 myAUC=0.726


- **GOLGA7B** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=GOLGA7B cluster=preHTC ave_diff=1.349 power=0.422 myAUC=0.711


- **PART1** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=PART1 cluster=preHTC ave_diff=1.017 power=0.404 myAUC=0.702


## Chondrocyte (hypertrophic)

- **COL10A1** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=COL10A1 cluster=HTC ave_diff=4.769 power=0.534 myAUC=0.767


- **IBSP** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=IBSP cluster=HTC ave_diff=2.323 power=0.492 myAUC=0.746


- **BHLHE41** (source: ji-2019)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=BHLHE41 cluster=HTC ave_diff=2.965 power=0.516 myAUC=0.758


## Synovial fibroblast (lining PRG4+)

- **PRG4** (source: chou-2020)
  - Chou Results: "SIF expresses genes producing essential constituents of synovial fluid including lubricin ( PRG4 ) and hyaluronan ( HAS1 )"; Zhang Results: "CD55 + fibroblasts (SC-F4) ... including the highest expression of lubricin ( PRG4 ), suggesting that these cells represent synovial lining fibroblasts"
  - TARGET Chou Table S1A cluster=SIF gene=PRG4 pct_in=0.997 pct_other=0.924 logFC=2.0 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=PRG4 pct_in=0.979 pct_other=0.766 logFC=2.41 padj=2.53e-32
  - Zhang Supplementary Table 4 row: Fibroblast / Lining (SC-F4) gene=PRG4 auc=0.958 pct_nonzero=1.00 log2FC=3.33

- **CD55** (source: chou-2020)
  - Zhang Results: "CD55 + lining fibroblasts (SC-F4)"
  - TARGET Chou Table S1A cluster=SIF gene=CD55 pct_in=0.946 pct_other=0.739 logFC=1.39 padj=0.0
  - other Chou Table S1B cluster=DC gene=CD55 pct_in=0.922 pct_other=0.753 logFC=0.62 padj=2.85e-35
  - Zhang Supplementary Table 4 row: Fibroblast / Lining (SC-F4) gene=CD55 auc=0.890 pct_nonzero=0.96 log2FC=4.69
  - Zhang Supplementary Table 4 row: B cell / Naive B cells (SC-B1) gene=CD55 auc=0.771 pct_nonzero=0.89 log2FC=3.62

- **HBEGF** (source: chou-2020)
  - Zhang Results: "Genes associated with CD55 + fibroblasts (SC-F4) ... ( HBEGF , CLIC5 , HTRA4 , and DNASE1L3 )"
  - TARGET Chou Table S1A cluster=SIF gene=HBEGF pct_in=0.854 pct_other=0.422 logFC=1.11 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=HBEGF pct_in=0.691 pct_other=0.287 logFC=0.63 padj=5.35e-12
  - Zhang Supplementary Table 4 row: Fibroblast / Lining (SC-F4) gene=HBEGF auc=0.906 pct_nonzero=0.90 log2FC=7.14

- **HAS1** (source: chou-2020)
  - Chou Results: "SIF expresses ... lubricin ( PRG4 ) and hyaluronan ( HAS1 )"
  - TARGET Chou Table S1A cluster=SIF gene=HAS1 pct_in=0.870 pct_other=0.544 logFC=0.78 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=HAS1 pct_in=0.763 pct_other=0.125 logFC=1.17 padj=1.55e-55

- **DEFB1** (source: chou-2020)
  - TARGET Chou Table S1A cluster=SIF gene=DEFB1 pct_in=0.829 pct_other=0.203 logFC=1.55 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=DEFB1 pct_in=0.505 pct_other=0.075 logFC=0.83 padj=8.95e-37

- **CLIC5** (source: zhang-2019)
  - Zhang Results: "Genes associated with CD55 + fibroblasts (SC-F4) ... ( HBEGF , CLIC5 , HTRA4 , and DNASE1L3 )"
  - Zhang Supplementary Table 4 row: Fibroblast / Lining (SC-F4) gene=CLIC5 auc=0.888 pct_nonzero=0.81 log2FC=6.26

- **ITGB8** (source: zhang-2019)
  - TARGET Chou Table S1A cluster=SIF gene=ITGB8 pct_in=0.645 pct_other=0.197 logFC=0.66 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=ITGB8 pct_in=0.454 pct_other=0.062 logFC=0.42 padj=1.34e-32
  - Zhang Supplementary Table 4 row: Fibroblast / Lining (SC-F4) gene=ITGB8 auc=0.942 pct_nonzero=0.98 log2FC=5.17

## Synovial fibroblast (sublining)

- **CXCL12** (source: chou-2020)
  - Chou Results: "SSF expresses collagen genes and stromal cell-derived factor 1 ( CXCL12 )"
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=CXCL12 cluster=FC ave_diff=5.243 power=0.556 myAUC=0.778

  - TARGET Chou Table S1A cluster=SSF gene=CXCL12 pct_in=0.718 pct_other=0.251 logFC=1.74 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=CXCL12 pct_in=0.608 pct_other=0.112 logFC=1.26 padj=2.68e-38
  - Zhang Supplementary Table 4 row: Fibroblast / HLA-DRAhi sublining (SC-F2) gene=CXCL12 auc=0.774 pct_nonzero=0.99 log2FC=3.72

- **IGF1** (source: chou-2020)
  - TARGET Chou Table S1A cluster=SSF gene=IGF1 pct_in=0.723 pct_other=0.157 logFC=1.88 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=IGF1 pct_in=0.557 pct_other=0.159 logFC=1.19 padj=3.88e-20
  - other Chou Table S1B cluster=B cell gene=IGF1 pct_in=0.615 pct_other=0.184 logFC=0.68 padj=0.552
  - Zhang Supplementary Table 4 row: Fibroblast / CD34+ sublining (SC-F1) gene=IGF1 auc=0.722 pct_nonzero=0.82 log2FC=3.73

- **MFAP5** (source: chou-2020)
  - TARGET Chou Table S1A cluster=SSF gene=MFAP5 pct_in=0.541 pct_other=0.107 logFC=1.53 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=MFAP5 pct_in=0.371 pct_other=0.038 logFC=1.16 padj=1.34e-35
  - Zhang Supplementary Table 4 row: Fibroblast / CD34+ sublining (SC-F1) gene=MFAP5 auc=0.639 pct_nonzero=0.43 log2FC=2.43

- **COL14A1** (source: chou-2020)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=COL14A1 cluster=FC ave_diff=5.951 power=0.578 myAUC=0.789

  - TARGET Chou Table S1A cluster=SSF gene=COL14A1 pct_in=0.869 pct_other=0.233 logFC=1.36 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=COL14A1 pct_in=0.629 pct_other=0.031 logFC=1.25 padj=3.76e-105

- **CCN5** (source: chou-2020)
  - note: symbol in source is WISP2 (previous HGNC symbol); current HGNC CCN5
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=WISP2 cluster=FC ave_diff=5.010 power=0.452 myAUC=0.726

  - TARGET Chou Table S1A cluster=SSF gene=WISP2 pct_in=0.842 pct_other=0.375 logFC=1.88 padj=0.0
  - other Chou Table S1B cluster=iFIB gene=WISP2 pct_in=0.742 pct_other=0.129 logFC=1.64 padj=2.01e-57

## Macrophage (synovial)

- **C1QA** (source: chou-2020)
  - TARGET Chou Table S1A cluster=HLA-DR+-1 gene=C1QA pct_in=0.988 pct_other=0.141 logFC=3.21 padj=0.0
  - TARGET Chou Table S1B cluster=IR-M! gene=C1QA pct_in=0.988 pct_other=0.723 logFC=0.97 padj=1.4e-89
  - Zhang Supplementary Table 4 row: Monocyte / C1QA+ (SC-M3) gene=C1QA auc=0.774 pct_nonzero=0.99 log2FC=1.99

- **C1QB** (source: chou-2020)
  - TARGET Chou Table S1A cluster=HLA-DR+-1 gene=C1QB pct_in=0.974 pct_other=0.124 logFC=2.99 padj=0.0
  - TARGET Chou Table S1B cluster=IR-M! gene=C1QB pct_in=0.964 pct_other=0.683 logFC=0.81 padj=5.7e-58
  - Zhang Supplementary Table 4 row: Monocyte / C1QA+ (SC-M3) gene=C1QB auc=0.777 pct_nonzero=0.98 log2FC=2.17

- **FOLR2** (source: chou-2020)
  - Chou Fig. 2c legend: "The top highly expressed genes in IR-MΦ were SEPP1 and FLOR2 [sic]"
  - TARGET Chou Table S1A cluster=HLA-DR+-1 gene=FOLR2 pct_in=0.909 pct_other=0.057 logFC=2.35 padj=0.0
  - TARGET Chou Table S1B cluster=IR-M! gene=FOLR2 pct_in=0.956 pct_other=0.570 logFC=1.08 padj=6.66e-101
  - Zhang Supplementary Table 4 row: Monocyte / NUPR1+ (SC-M2) gene=FOLR2 auc=0.734 pct_nonzero=0.93 log2FC=3.78

- **MARCO** (source: chou-2020)
  - TARGET Chou Table S1A cluster=HLA-DR+-1 gene=MARCO pct_in=0.908 pct_other=0.080 logFC=2.65 padj=0.0
  - TARGET Chou Table S1B cluster=IR-M! gene=MARCO pct_in=0.912 pct_other=0.573 logFC=0.98 padj=1.27e-70
  - Zhang Supplementary Table 4 row: Monocyte / C1QA+ (SC-M3) gene=MARCO auc=0.697 pct_nonzero=0.87 log2FC=2.85

- **LYVE1** (source: chou-2020)
  - TARGET Chou Table S1A cluster=HLA-DR+-1 gene=LYVE1 pct_in=0.668 pct_other=0.050 logFC=1.84 padj=0.0
  - TARGET Chou Table S1B cluster=IR-M! gene=LYVE1 pct_in=0.744 pct_other=0.312 logFC=1.1 padj=2.68e-64

- **CD163** (source: chou-2020)
  - Chou Results: "Classic macrophage marker genes ( CD14 , CD163 and FCGR3A ) were highly expressed in IR-MΦ, I-MΦ and iFIB"
  - TARGET Chou Table S1A cluster=HLA-DR+-1 gene=CD163 pct_in=0.773 pct_other=0.033 logFC=1.41 padj=0.0
  - TARGET Chou Table S1B cluster=IR-M! gene=CD163 pct_in=0.791 pct_other=0.503 logFC=0.51 padj=5.77e-34

- **VSIG4** (source: chou-2020)
  - TARGET Chou Table S1A cluster=HLA-DR+-1 gene=VSIG4 pct_in=0.859 pct_other=0.058 logFC=1.76 padj=0.0
  - other Chou Table S1A cluster=HLA-DR+-2 gene=VSIG4 pct_in=0.715 pct_other=0.109 logFC=0.89 padj=8.37e-169
  - TARGET Chou Table S1B cluster=IR-M! gene=VSIG4 pct_in=0.903 pct_other=0.754 logFC=0.63 padj=5.03e-42
  - Zhang Supplementary Table 4 row: Monocyte / NUPR1+ (SC-M2) gene=VSIG4 auc=0.801 pct_nonzero=0.97 log2FC=3.01

## Dendritic cell (CD1C+)

- **CD1C** (source: chou-2020)
  - Chou Results: "DC marker genes, FCER1A and CD1C were exclusively expressed in DC"
  - TARGET Chou Table S1A cluster=HLA-DR+-2 gene=CD1C pct_in=0.464 pct_other=0.002 logFC=1.32 padj=3.6e-256
  - TARGET Chou Table S1B cluster=DC gene=CD1C pct_in=0.531 pct_other=0.015 logFC=1.41 padj=1.38e-119

- **CLEC10A** (source: chou-2020)
  - TARGET Chou Table S1A cluster=HLA-DR+-2 gene=CLEC10A pct_in=0.769 pct_other=0.016 logFC=1.65 padj=0.0
  - TARGET Chou Table S1B cluster=DC gene=CLEC10A pct_in=0.803 pct_other=0.169 logFC=1.36 padj=1.52e-114

- **PKIB** (source: chou-2020)
  - TARGET Chou Table S1A cluster=HLA-DR+-2 gene=PKIB pct_in=0.311 pct_other=0.010 logFC=0.55 padj=3.72e-128
  - TARGET Chou Table S1B cluster=DC gene=PKIB pct_in=0.334 pct_other=0.063 logFC=0.5 padj=7.84e-35

- **CD1E** (source: chou-2020)
  - TARGET Chou Table S1A cluster=HLA-DR+-2 gene=CD1E pct_in=0.223 pct_other=0.001 logFC=0.43 padj=5e-116
  - TARGET Chou Table S1B cluster=DC gene=CD1E pct_in=0.259 pct_other=0.004 logFC=0.49 padj=5.78e-56

## T cell

- **CD2** (source: chou-2020)
  - TARGET Chou Table S1A cluster=T cell gene=CD2 pct_in=0.764 pct_other=0.008 logFC=1.81 padj=4.37e-200

- **CD3D** (source: chou-2020)
  - TARGET Chou Table S1A cluster=T cell gene=CD3D pct_in=0.764 pct_other=0.007 logFC=1.63 padj=1.55e-195

- **CD3E** (source: chou-2020)
  - TARGET Chou Table S1A cluster=T cell gene=CD3E pct_in=0.708 pct_other=0.003 logFC=1.41 padj=4.59e-187

- **CD3G** (source: chou-2020)
  - TARGET Chou Table S1A cluster=T cell gene=CD3G pct_in=0.521 pct_other=0.003 logFC=1.1 padj=1.16e-131

- **LCK** (source: chou-2020)
  - TARGET Chou Table S1A cluster=T cell gene=LCK pct_in=0.479 pct_other=0.005 logFC=0.85 padj=1.41e-107

## B cell

- **MS4A1** (source: zhang-2019)
  - Zhang Supplementary Table 4: Memory B cells (SC-B2) top marker
  - Zhang Supplementary Table 4 row: B cell / Memory B cells (SC-B2) gene=MS4A1 auc=0.760 pct_nonzero=0.97 log2FC=4.46

- **CD19** (source: zhang-2019)
  - Zhang Supplementary Table 4: ABCs (SC-B3) top marker; B cells were sorted as CD45+CD3−CD19+
  - Zhang Supplementary Table 4 row: B cell / ABCs (SC-B3) gene=CD19 auc=0.803 pct_nonzero=0.91 log2FC=4.15

- **CXCR5** (source: zhang-2019)
  - Zhang Supplementary Table 4: Naive B cells (SC-B1) top marker
  - Zhang Supplementary Table 4 row: B cell / Naive B cells (SC-B1) gene=CXCR5 auc=0.758 pct_nonzero=0.71 log2FC=4.41

- **RALGPS2** (source: zhang-2019)
  - Zhang Methods: "We used 2 marker genes expected to be exclusively expressed in each of the 4 cell types: ... CD79A and RALGPS2 for B cells"
  - other Chou Table S1B cluster=B cell gene=RALGPS2 pct_in=0.615 pct_other=0.013 logFC=0.53 padj=6.07e-54

## Plasma cell

- **MZB1** (source: chou-2020)
  - Chou Fig. 2c legend: "Consistent with identification as B cells were cells with high expression of MZB1 , TNFRSF17 and CD79A" (this cluster is plasma-cell-like)
  - TARGET Chou Table S1B cluster=B cell gene=MZB1 pct_in=1.000 pct_other=0.005 logFC=4.09 padj=3.83e-191
  - Zhang Supplementary Table 4 row: B cell / plasmablasts (SC-B4) gene=MZB1 auc=0.995 pct_nonzero=1.00 log2FC=10.09

- **JCHAIN** (source: chou-2020)
  - note: symbol in source is IGJ (previous HGNC symbol); current HGNC JCHAIN
  - TARGET Chou Table S1B cluster=B cell gene=IGJ pct_in=0.846 pct_other=0.007 logFC=4.56 padj=6.69e-129

- **DERL3** (source: chou-2020)
  - TARGET Chou Table S1B cluster=B cell gene=DERL3 pct_in=1.000 pct_other=0.009 logFC=3.37 padj=7.43e-153
  - Zhang Supplementary Table 4 row: B cell / plasmablasts (SC-B4) gene=DERL3 auc=0.976 pct_nonzero=0.97 log2FC=9.09

- **TNFRSF17** (source: chou-2020)
  - Chou Fig. 2c legend: "high expression of MZB1 , TNFRSF17 and CD79A"
  - TARGET Chou Table S1B cluster=B cell gene=TNFRSF17 pct_in=0.692 pct_other=0.001 logFC=0.86 padj=8.22e-182

- **FKBP11** (source: chou-2020)
  - TARGET Chou Table S1B cluster=B cell gene=FKBP11 pct_in=1.000 pct_other=0.061 logFC=2.58 padj=3.44e-40
  - Zhang Supplementary Table 4 row: B cell / plasmablasts (SC-B4) gene=FKBP11 auc=0.988 pct_nonzero=0.98 log2FC=9.66

## Mast cell

- **TPSAB1** (source: chou-2020)
  - TARGET Chou Table S1A cluster=Mast cell gene=TPSAB1 pct_in=1.000 pct_other=0.107 logFC=5.34 padj=0.0

- **CPA3** (source: chou-2020)
  - TARGET Chou Table S1A cluster=Mast cell gene=CPA3 pct_in=0.975 pct_other=0.010 logFC=2.52 padj=1e-270

- **HDC** (source: chou-2020)
  - TARGET Chou Table S1A cluster=Mast cell gene=HDC pct_in=0.600 pct_other=0.004 logFC=1.23 padj=1.25e-133

- **KIT** (source: chou-2020)
  - TARGET Chou Table S1A cluster=Mast cell gene=KIT pct_in=0.617 pct_other=0.006 logFC=1.12 padj=4.35e-133

- **RGS13** (source: chou-2020)
  - TARGET Chou Table S1A cluster=Mast cell gene=RGS13 pct_in=0.850 pct_other=0.014 logFC=1.94 padj=3.27e-207

- **SLC18A2** (source: chou-2020)
  - TARGET Chou Table S1A cluster=Mast cell gene=SLC18A2 pct_in=0.775 pct_other=0.003 logFC=1.49 padj=1.31e-182

## Endothelial

- **PLVAP** (source: chou-2020)
  - TARGET Chou Table S1A cluster=EC gene=PLVAP pct_in=0.870 pct_other=0.021 logFC=2.31 padj=0.0

- **EMCN** (source: chou-2020)
  - TARGET Chou Table S1A cluster=EC gene=EMCN pct_in=0.925 pct_other=0.010 logFC=1.78 padj=0.0

- **VWF** (source: chou-2020)
  - TARGET Chou Table S1A cluster=EC gene=VWF pct_in=0.751 pct_other=0.014 logFC=1.42 padj=0.0

- **CLEC14A** (source: chou-2020)
  - TARGET Chou Table S1A cluster=EC gene=CLEC14A pct_in=0.847 pct_other=0.014 logFC=1.52 padj=0.0

- **ECSCR** (source: chou-2020)
  - TARGET Chou Table S1A cluster=EC gene=ECSCR pct_in=0.904 pct_other=0.010 logFC=1.62 padj=0.0

- **CDH5** (source: chou-2020)
  - TARGET Chou Table S1A cluster=EC gene=CDH5 pct_in=0.601 pct_other=0.006 logFC=0.8 padj=0.0

## Pericyte / smooth muscle

- **RGS5** (source: chou-2020)
  - TARGET Chou Table S1A cluster=SMC gene=RGS5 pct_in=0.951 pct_other=0.049 logFC=3.44 padj=0.0
  - other Chou Table S1A cluster=ProIC gene=RGS5 pct_in=0.250 pct_other=0.077 logFC=0.68 padj=1.0

- **ACTA2** (source: chou-2020)
  - TARGET Chou Table S1A cluster=SMC gene=ACTA2 pct_in=0.931 pct_other=0.164 logFC=3.19 padj=0.0
  - other Chou Table S1A cluster=ProIC gene=ACTA2 pct_in=0.462 pct_other=0.187 logFC=0.28 padj=1.0

- **NOTCH3** (source: chou-2020)
  - Ji Table S4 (online supplementary file 5, cluster markers vs all other clusters) row: gene=NOTCH3 cluster=FC ave_diff=3.823 power=0.42 myAUC=0.71

  - TARGET Chou Table S1A cluster=SMC gene=NOTCH3 pct_in=0.840 pct_other=0.054 logFC=1.47 padj=0.0
  - other Chou Table S1A cluster=ProIC gene=NOTCH3 pct_in=0.250 pct_other=0.079 logFC=0.3 padj=1.0

- **MYH11** (source: chou-2020)
  - TARGET Chou Table S1A cluster=SMC gene=MYH11 pct_in=0.496 pct_other=0.019 logFC=1.7 padj=7.74e-220

- **PPP1R14A** (source: chou-2020)
  - TARGET Chou Table S1A cluster=SMC gene=PPP1R14A pct_in=0.734 pct_other=0.008 logFC=1.58 padj=0.0

## Adipocyte

- **ADIPOQ** (source: emont-2022)
  - Emont Fig. 3b legend: "Expression of adipocyte marker ADIPOQ"
  - Emont Supplementary Table 1 ('all markers', human) row: cluster=adipocyte pct.1=0.872 pct.2=0.105 avg_log2FC=2.54 p_val_adj=0.0e+00

- **PLIN1** (source: emont-2022)
  - Emont Supplementary Table 1 ('all markers', human) row: cluster=adipocyte pct.1=0.957 pct.2=0.093 avg_log2FC=3.10 p_val_adj=0.0e+00

- **GPAM** (source: emont-2022)
  - Emont Supplementary Table 1 ('all markers', human) row: cluster=adipocyte pct.1=0.942 pct.2=0.141 avg_log2FC=3.62 p_val_adj=0.0e+00

- **AQP7** (source: emont-2022)
  - Emont Supplementary Table 1 ('all markers', human) row: cluster=adipocyte pct.1=0.894 pct.2=0.05 avg_log2FC=2.61 p_val_adj=0.0e+00

- **PLIN4** (source: emont-2022)
  - Emont Supplementary Table 1 ('all markers', human) row: cluster=adipocyte pct.1=0.802 pct.2=0.07 avg_log2FC=2.34 p_val_adj=0.0e+00

- **SLC19A3** (source: emont-2022)
  - Emont Supplementary Table 1 ('all markers', human) row: cluster=adipocyte pct.1=0.875 pct.2=0.071 avg_log2FC=2.81 p_val_adj=0.0e+00

- **GPD1** (source: emont-2022)
  - Emont Supplementary Table 1 ('all markers', human) row: cluster=adipocyte pct.1=0.701 pct.2=0.024 avg_log2FC=1.90 p_val_adj=0.0e+00
