# broad.csv — provenance

Generic broad types. Every gene is a PanglaoDB marker with human=True for the PanglaoDB cell type(s) named under each type, taken from the OmniPath annotations endpoint exactly as the existing app does: `curl -sSL "https://omnipathdb.org/annotations?resources=PanglaoDB&format=tsv"` (downloaded 2026-10-31; copy in markers-research/panglao/panglao_omnipath.tsv; long-format rows pivoted by genesymbol+record_id). Selection: canonical_marker=True where possible, low ubiquitousness index, preferring genes with non-zero human_sensitivity, and no gene in two types of this file. "also a PanglaoDB marker of" lists other PanglaoDB types that list the same gene (outside this set's choice).

Left out: lymphatic endothelial cells — PanglaoDB has no lymphatic endothelial cell type in this export; dendritic cells and monocytes — not requested as separate types (could be added from PanglaoDB "Dendritic cells"/"Monocytes"). Neutrophils: their PanglaoDB markers have human_sensitivity 0 except CSF3R (0.23), and neutrophils are poorly captured by single-nucleus RNA-seq. Adipocyte markers have human_sensitivity 0 in PanglaoDB (no human adipocyte data behind them), but they are canonical. Erythroid: haemoglobin transcripts are a common ambient contaminant in nuclei data, so a high score is not by itself proof of erythroid cells. Epithelial: KRT8/KRT18/KRT19/CLDN4 are PanglaoDB markers of "Luminal epithelial cells" (KRT19 also ductal/cholangiocytes), not of the generic "Epithelial cells" type; EPCAM and CDH1 are from "Epithelial cells".

## Source

**panglaodb-2019** — PanglaoDB: a web server for exploration of mouse and human single-cell RNA sequencing data. Franzén O, Gan LM, Björkegren JLM. Database (Oxford) 2019;2019:baz046. DOI 10.1093/database/baz046; PMID 30951143; PMCID PMC6450036. Licence of the article: CC BY 4.0 (Crossref). Verified: Crossref + PubMed esummary + PMC ID converter. The marker table was accessed through OmniPath (resource "PanglaoDB"); the PanglaoDB data licence itself was not checked here.

## T cells
PanglaoDB cell type(s) used: T cells

- **CD3D**
  - PanglaoDB (OmniPath record_id 8014): cell_type=T cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.053, human_sensitivity=0.964427, human_specificity=0.0571623
  - also a PanglaoDB marker of: T cells naive, T follicular helper cells, T helper cells, T memory cells

- **CD3E**
  - PanglaoDB (OmniPath record_id 6226): cell_type=T cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.041, human_sensitivity=0.810277, human_specificity=0.0384485
  - also a PanglaoDB marker of: Macrophages, Pyramidal cells, T memory cells

- **TRAC**
  - PanglaoDB (OmniPath record_id 8034): cell_type=T cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.042, human_sensitivity=0.972332, human_specificity=0.0595441
  - also a PanglaoDB marker of: T cytotoxic cells, T memory cells

- **LCK**
  - PanglaoDB (OmniPath record_id 8059): cell_type=T cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.048, human_sensitivity=0.648221, human_specificity=0.0330044
  - also a PanglaoDB marker of: T memory cells

- **CD6**
  - PanglaoDB (OmniPath record_id 8057): cell_type=T cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.007, human_sensitivity=0.126482, human_specificity=0.00544403

- **TRBC2**
  - PanglaoDB (OmniPath record_id 8028): cell_type=T cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.066, human_sensitivity=0.940711, human_specificity=0.0833617
  - also a PanglaoDB marker of: T memory cells

## NK cells
PanglaoDB cell type(s) used: NK cells

- **GNLY**
  - PanglaoDB (OmniPath record_id 5021): cell_type=NK cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.013, human_sensitivity=0.851351, human_specificity=0.0635022
  - also a PanglaoDB marker of: Gamma delta T cells

- **NKG7**
  - PanglaoDB (OmniPath record_id 5032): cell_type=NK cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.056, human_sensitivity=0.945946, human_specificity=0.0878768
  - also a PanglaoDB marker of: Gamma delta T cells, T memory cells

- **KLRD1**
  - PanglaoDB (OmniPath record_id 5041): cell_type=NK cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.02, human_sensitivity=0.594595, human_specificity=0.0256575
  - also a PanglaoDB marker of: Gamma delta T cells, T helper cells

- **KLRF1**
  - PanglaoDB (OmniPath record_id 5039): cell_type=NK cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.003, human_sensitivity=0.256757, human_specificity=0.0150738
  - also a PanglaoDB marker of: Gamma delta T cells

- **PRF1**
  - PanglaoDB (OmniPath record_id 5035): cell_type=NK cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.009, human_sensitivity=0.310811, human_specificity=0.0240539
  - also a PanglaoDB marker of: Gamma delta T cells, Natural killer T cells

## B cells
PanglaoDB cell type(s) used: B cells

- **MS4A1**
  - PanglaoDB (OmniPath record_id 1148): cell_type=B cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.014, human_sensitivity=0.483871, human_specificity=0.0111821
  - also a PanglaoDB marker of: B cells memory, B cells naive, Plasma cells

- **CD79B**
  - PanglaoDB (OmniPath record_id 1179): cell_type=B cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.028, human_sensitivity=0.919355, human_specificity=0.0255591
  - also a PanglaoDB marker of: B cells memory, B cells naive

- **BANK1**
  - PanglaoDB (OmniPath record_id 1307): cell_type=B cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.006, human_sensitivity=0.225806, human_specificity=0.00415335
  - also a PanglaoDB marker of: B cells memory, B cells naive

- **TNFRSF13C**
  - PanglaoDB (OmniPath record_id 1206): cell_type=B cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.008, human_sensitivity=0.451613, human_specificity=0.0105431
  - also a PanglaoDB marker of: B cells naive

- **PAX5**
  - PanglaoDB (OmniPath record_id 1296): cell_type=B cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.003, human_sensitivity=0.0483871, human_specificity=0.000638978
  - also a PanglaoDB marker of: B cells memory

- **CD19**
  - PanglaoDB (OmniPath record_id 1265): cell_type=B cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.007, human_sensitivity=0.129032, human_specificity=0.00543131
  - also a PanglaoDB marker of: B cells memory, B cells naive, Macrophages, Plasma cells

## Plasma cells
PanglaoDB cell type(s) used: Plasma cells

- **MZB1**
  - PanglaoDB (OmniPath record_id 1301): cell_type=Plasma cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.025, human_sensitivity=0.972222, human_specificity=0.0275665
  - also a PanglaoDB marker of: B cells, Plasmacytoid dendritic cells

- **JCHAIN**
  - PanglaoDB (OmniPath record_id 1299): cell_type=Plasma cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.017, human_sensitivity=0.833333, human_specificity=0.0405577
  - also a PanglaoDB marker of: B cells, Plasmacytoid dendritic cells

- **TNFRSF17**
  - PanglaoDB (OmniPath record_id 1327): cell_type=Plasma cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.005, human_sensitivity=0.777778, human_specificity=0.00126743
  - also a PanglaoDB marker of: B cells, B cells memory

- **PRDM1**
  - PanglaoDB (OmniPath record_id 7533): cell_type=Plasma cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.005, human_sensitivity=0.25, human_specificity=0.0174271

- **SDC1**
  - PanglaoDB (OmniPath record_id 1196): cell_type=Plasma cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.046, human_sensitivity=0.555556, human_specificity=0.0405577
  - also a PanglaoDB marker of: B cells, Luteal cells, Pulmonary alveolar type II cells

- **IGHG1**
  - PanglaoDB (OmniPath record_id 1415): cell_type=Plasma cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.006, human_sensitivity=0.638889, human_specificity=0.01109
  - also a PanglaoDB marker of: B cells

## Macrophages
PanglaoDB cell type(s) used: Macrophages

- **CD163**
  - PanglaoDB (OmniPath record_id 3012): cell_type=Macrophages, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.005, human_sensitivity=0.25, human_specificity=0.00628931
  - also a PanglaoDB marker of: Dendritic cells, Kupffer cells, Monocytes

- **VSIG4**
  - PanglaoDB (OmniPath record_id 3018): cell_type=Macrophages, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.005, human_sensitivity=0.666667, human_specificity=0.0110063
  - also a PanglaoDB marker of: Dendritic cells, Kupffer cells

- **MS4A4A**
  - PanglaoDB (OmniPath record_id 6185): cell_type=Macrophages, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.002, human_sensitivity=0.583333, human_specificity=0.00534591
  - also a PanglaoDB marker of: Plasma cells

- **MRC1**
  - PanglaoDB (OmniPath record_id 843): cell_type=Macrophages, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.029, human_sensitivity=0.416667, human_specificity=0.0081761
  - also a PanglaoDB marker of: Alveolar macrophages, Mesangial cells, Monocytes, Myocytes

- **CD68**
  - PanglaoDB (OmniPath record_id 6228): cell_type=Macrophages, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.063, human_sensitivity=0.0, human_specificity=0.0
  - also a PanglaoDB marker of: Monocytes, Osteoclasts

- **MS4A6A**
  - PanglaoDB (OmniPath record_id 6187): cell_type=Macrophages, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.007, human_sensitivity=0.333333, human_specificity=0.0389937
  - also a PanglaoDB marker of: Monocytes

## Mast cells
PanglaoDB cell type(s) used: Mast cells

- **TPSAB1**
  - PanglaoDB (OmniPath record_id 6290): cell_type=Mast cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.002, human_sensitivity=1.0, human_specificity=0.00439698

- **TPSB2**
  - PanglaoDB (OmniPath record_id 6312): cell_type=Mast cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.004, human_sensitivity=1.0, human_specificity=0.00471106

- **CPA3**
  - PanglaoDB (OmniPath record_id 1778): cell_type=Mast cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.009, human_sensitivity=1.0, human_specificity=0.00596734
  - also a PanglaoDB marker of: Basophils, Eosinophils

- **MS4A2**
  - PanglaoDB (OmniPath record_id 1800): cell_type=Mast cells, organ=Immune system, human=True, canonical_marker=False, ubiquitousness=0.003, human_sensitivity=0.75, human_specificity=0.0
  - also a PanglaoDB marker of: Basophils

- **HPGDS**
  - PanglaoDB (OmniPath record_id 6215): cell_type=Mast cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.033, human_sensitivity=1.0, human_specificity=0.0160176
  - also a PanglaoDB marker of: Macrophages, Microglia, T helper cells

- **KIT**
  - PanglaoDB (OmniPath record_id 2272): cell_type=Mast cells, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.015, human_sensitivity=0.625, human_specificity=0.000942211
  - also a PanglaoDB marker of: Cardiac stem and precursor cells, Dendritic cells, Embryonic stem cells, Erythroblasts, Erythroid-like and erythroid precursor cells, Hematopoietic stem cells, Müller cells, NK cells, Stromal cells

## Neutrophils
PanglaoDB cell type(s) used: Neutrophils

- **CSF3R**
  - PanglaoDB (OmniPath record_id 6578): cell_type=Neutrophils, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.012, human_sensitivity=0.230769, human_specificity=0.0204467
  - also a PanglaoDB marker of: Microglia, Monocytes

- **CXCR1**
  - PanglaoDB (OmniPath record_id 6409): cell_type=Neutrophils, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.0, human_sensitivity=0.0, human_specificity=0.0
  - also a PanglaoDB marker of: Megakaryocytes, Myeloid-derived suppressor cells

- **CXCR2**
  - PanglaoDB (OmniPath record_id 6283): cell_type=Neutrophils, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.003, human_sensitivity=0.0, human_specificity=0.0
  - also a PanglaoDB marker of: Mast cells, Megakaryocytes, Pulmonary alveolar type II cells

- **CEACAM8**
  - PanglaoDB (OmniPath record_id 6706): cell_type=Neutrophils, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.0, human_sensitivity=0.0, human_specificity=0.0
  - also a PanglaoDB marker of: Myeloid-derived suppressor cells

- **MMP8**
  - PanglaoDB (OmniPath record_id 7046): cell_type=Neutrophils, organ=Immune system, human=True, canonical_marker=True, ubiquitousness=0.004, human_sensitivity=0.0, human_specificity=0.0

## Endothelial cells
PanglaoDB cell type(s) used: Endothelial cells

- **PECAM1**
  - PanglaoDB (OmniPath record_id 3445): cell_type=Endothelial cells, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.051, human_sensitivity=0.798077, human_specificity=0.0187824
  - also a PanglaoDB marker of: Embryonic stem cells, Megakaryocytes, Monocytes, Neutrophils, Pericytes, Platelets, Stromal cells

- **VWF**
  - PanglaoDB (OmniPath record_id 3549): cell_type=Endothelial cells, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.016, human_sensitivity=0.711538, human_specificity=0.00356218
  - also a PanglaoDB marker of: Hematopoietic stem cells, Megakaryocytes, Platelets

- **CDH5**
  - PanglaoDB (OmniPath record_id 3685): cell_type=Endothelial cells, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.043, human_sensitivity=0.644231, human_specificity=0.00453368

- **CLDN5**
  - PanglaoDB (OmniPath record_id 3674): cell_type=Endothelial cells, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.054, human_sensitivity=0.971154, human_specificity=0.0210492

- **FLT1**
  - PanglaoDB (OmniPath record_id 3709): cell_type=Endothelial cells, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.051, human_sensitivity=0.615385, human_specificity=0.0262306

- **EMCN**
  - PanglaoDB (OmniPath record_id 3667): cell_type=Endothelial cells, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.043, human_sensitivity=0.653846, human_specificity=0.0100389

- **TIE1**
  - PanglaoDB (OmniPath record_id 3571): cell_type=Endothelial cells, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.025, human_sensitivity=0.413462, human_specificity=0.00194301

## Fibroblasts
PanglaoDB cell type(s) used: Fibroblasts

- **DCN**
  - PanglaoDB (OmniPath record_id 4881): cell_type=Fibroblasts, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.084, human_sensitivity=0.936937, human_specificity=0.0772476
  - also a PanglaoDB marker of: Hepatic stellate cells, Meningeal cells

- **LUM**
  - PanglaoDB (OmniPath record_id 2675): cell_type=Fibroblasts, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.051, human_sensitivity=0.873874, human_specificity=0.0587472
  - also a PanglaoDB marker of: Chondrocytes, Meningeal cells, Stromal cells

- **COL1A2**
  - PanglaoDB (OmniPath record_id 4853): cell_type=Fibroblasts, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.097, human_sensitivity=0.711712, human_specificity=0.103213
  - also a PanglaoDB marker of: Hepatic stellate cells, Pancreatic stellate cells

- **COL3A1**
  - PanglaoDB (OmniPath record_id 4858): cell_type=Fibroblasts, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.086, human_sensitivity=0.666667, human_specificity=0.0788705
  - also a PanglaoDB marker of: Hepatic stellate cells, Müller cells, Pancreatic stellate cells

- **PDGFRA**
  - PanglaoDB (OmniPath record_id 4875): cell_type=Fibroblasts, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.044, human_sensitivity=0.396396, human_specificity=0.0350536
  - also a PanglaoDB marker of: Hepatic stellate cells, Meningeal cells, Oligodendrocyte progenitor cells, Pancreatic stellate cells, Stromal cells

## Smooth muscle cells / pericytes
PanglaoDB cell type(s) used: Smooth muscle cells, Pericytes

- **MYH11**
  - PanglaoDB (OmniPath record_id 5939): cell_type=Smooth muscle cells, organ=Smooth muscle, human=True, canonical_marker=True, ubiquitousness=0.015, human_sensitivity=1.0, human_specificity=0.0097761
  - also a PanglaoDB marker of: Juxtaglomerular cells, Myoepithelial cells, Peritubular myoid cells, Salivary mucous cells, Vascular smooth muscle cells

- **CNN1**
  - PanglaoDB (OmniPath record_id 5943): cell_type=Smooth muscle cells, organ=Smooth muscle, human=True, canonical_marker=True, ubiquitousness=0.012, human_sensitivity=0.571429, human_specificity=0.0249133
  - also a PanglaoDB marker of: Juxtaglomerular cells, Myoepithelial cells, Salivary mucous cells

- **LMOD1**
  - PanglaoDB (OmniPath record_id 7975): cell_type=Smooth muscle cells, organ=Smooth muscle, human=True, canonical_marker=True, ubiquitousness=0.01, human_sensitivity=0.761905, human_specificity=0.0116682

- **ACTA2**
  - PanglaoDB (OmniPath record_id 600): cell_type=Smooth muscle cells, organ=Smooth muscle, human=True, canonical_marker=True, ubiquitousness=0.035, human_sensitivity=0.904762, human_specificity=0.0135604
  - PanglaoDB (OmniPath record_id 602): cell_type=Pericytes, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.035, human_sensitivity=0.0, human_specificity=0.0194662
  - also a PanglaoDB marker of: Airway smooth muscle cells, Hepatic stellate cells, Juxtaglomerular cells, Mesangial cells, Myoepithelial cells, Myofibroblasts, Vascular smooth muscle cells

- **HIGD1B**
  - PanglaoDB (OmniPath record_id 7459): cell_type=Pericytes, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.021, human_sensitivity=1.0, human_specificity=0.00376766

- **NOTCH3**
  - PanglaoDB (OmniPath record_id 5639): cell_type=Pericytes, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.02, human_sensitivity=0.857143, human_specificity=0.0125589
  - PanglaoDB (OmniPath record_id 5640): cell_type=Smooth muscle cells, organ=Smooth muscle, human=True, canonical_marker=True, ubiquitousness=0.02, human_sensitivity=0.571429, human_specificity=0.0107222
  - also a PanglaoDB marker of: Immature neurons, Myocytes, Radial glia cells, Satellite cells, Spermatocytes, T cells

- **KCNJ8**
  - PanglaoDB (OmniPath record_id 3717): cell_type=Pericytes, organ=Vasculature, human=True, canonical_marker=True, ubiquitousness=0.017, human_sensitivity=0.428571, human_specificity=0.000941915
  - also a PanglaoDB marker of: Endothelial cells, Glomus cells

## Epithelial cells
PanglaoDB cell type(s) used: Epithelial cells, Luminal epithelial cells

- **EPCAM**
  - PanglaoDB (OmniPath record_id 2554): cell_type=Epithelial cells, organ=Epithelium, human=True, canonical_marker=True, ubiquitousness=0.117, human_sensitivity=0.911765, human_specificity=0.160861
  - also a PanglaoDB marker of: Cholangiocytes, Embryonic stem cells, Epiblast cells, Langerhans cells

- **CDH1**
  - PanglaoDB (OmniPath record_id 513): cell_type=Luminal epithelial cells, organ=Mammary gland, human=True, canonical_marker=True, ubiquitousness=0.056, human_sensitivity=0.533333, human_specificity=0.0393453
  - PanglaoDB (OmniPath record_id 515): cell_type=Epithelial cells, organ=Epithelium, human=True, canonical_marker=True, ubiquitousness=0.056, human_sensitivity=0.294118, human_specificity=0.0389487
  - also a PanglaoDB marker of: Airway epithelial cells, Basophils, Embryonic stem cells, Epiblast cells, Erythroblasts, Hepatoblasts, Hepatocytes, Mammary epithelial cells, Mesothelial cells, Plasmacytoid dendritic cells, Satellite cells, Satellite glial cells, Sebocytes

- **KRT8**
  - PanglaoDB (OmniPath record_id 4605): cell_type=Luminal epithelial cells, organ=Mammary gland, human=True, canonical_marker=True, ubiquitousness=0.12, human_sensitivity=0.933333, human_specificity=0.207743
  - also a PanglaoDB marker of: Epsilon cells, Hepatoblasts, Mammary epithelial cells, Merkel cells

- **KRT18**
  - PanglaoDB (OmniPath record_id 5492): cell_type=Luminal epithelial cells, organ=Mammary gland, human=True, canonical_marker=True, ubiquitousness=0.126, human_sensitivity=0.8, human_specificity=0.235127
  - also a PanglaoDB marker of: Hepatoblasts, Mammary epithelial cells, Merkel cells

- **KRT19**
  - PanglaoDB (OmniPath record_id 2521): cell_type=Luminal epithelial cells, organ=Mammary gland, human=True, canonical_marker=True, ubiquitousness=0.088, human_sensitivity=0.666667, human_specificity=0.168398
  - also a PanglaoDB marker of: Cholangiocytes, Ductal cells, Mammary epithelial cells

- **CLDN4**
  - PanglaoDB (OmniPath record_id 2559): cell_type=Luminal epithelial cells, organ=Mammary gland, human=True, canonical_marker=True, ubiquitousness=0.047, human_sensitivity=0.8, human_specificity=0.125275
  - also a PanglaoDB marker of: Cholangiocytes, Ductal cells, Mammary epithelial cells, Principal cells

## Neurons
PanglaoDB cell type(s) used: Neurons

- **SNAP25**
  - PanglaoDB (OmniPath record_id 2770): cell_type=Neurons, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.112, human_sensitivity=1.0, human_specificity=0.0194785
  - also a PanglaoDB marker of: Chromaffin cells

- **RBFOX3**
  - PanglaoDB (OmniPath record_id 5647): cell_type=Neurons, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.04, human_sensitivity=0.0, human_specificity=0.0109959
  - also a PanglaoDB marker of: Immature neurons

- **STMN2**
  - PanglaoDB (OmniPath record_id 7026): cell_type=Neurons, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.209, human_sensitivity=0.666667, human_specificity=0.0490104

- **NEFM**
  - PanglaoDB (OmniPath record_id 5846): cell_type=Neurons, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.028, human_sensitivity=0.666667, human_specificity=0.0182218
  - also a PanglaoDB marker of: Interneurons, Purkinje fiber cells, Retinal ganglion cells, Trigeminal neurons

- **NEFH**
  - PanglaoDB (OmniPath record_id 6902): cell_type=Neurons, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.009, human_sensitivity=0.444444, human_specificity=0.00251335
  - also a PanglaoDB marker of: Retinal progenitor cells, Trigeminal neurons

## Schwann cells
PanglaoDB cell type(s) used: Schwann cells

- **MPZ**
  - PanglaoDB (OmniPath record_id 3955): cell_type=Schwann cells, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.002, human_sensitivity=0.0, human_specificity=0.00219298
  - also a PanglaoDB marker of: Enteric glia cells, Peri-islet Schwann cells

- **PRX**
  - PanglaoDB (OmniPath record_id 7919): cell_type=Schwann cells, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.002, human_sensitivity=0.0, human_specificity=0.000313283

- **PMP22**
  - PanglaoDB (OmniPath record_id 7924): cell_type=Schwann cells, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.102, human_sensitivity=0.0, human_specificity=0.0958647

- **CLDN19**
  - PanglaoDB (OmniPath record_id 6077): cell_type=Schwann cells, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.001, human_sensitivity=0.0, human_specificity=0.000626566
  - also a PanglaoDB marker of: Loop of Henle cells

## Oligodendrocytes
PanglaoDB cell type(s) used: Oligodendrocytes

- **MOG**
  - PanglaoDB (OmniPath record_id 7269): cell_type=Oligodendrocytes, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.039, human_sensitivity=0.964286, human_specificity=0.000316056

- **MBP**
  - PanglaoDB (OmniPath record_id 7334): cell_type=Oligodendrocytes, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.12, human_sensitivity=1.0, human_specificity=0.0445638

- **ST18**
  - PanglaoDB (OmniPath record_id 7319): cell_type=Oligodendrocytes, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.006, human_sensitivity=1.0, human_specificity=0.00126422

- **MYRF**
  - PanglaoDB (OmniPath record_id 7290): cell_type=Oligodendrocytes, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.019, human_sensitivity=0.535714, human_specificity=0.000948167

- **KLK6**
  - PanglaoDB (OmniPath record_id 7308): cell_type=Oligodendrocytes, organ=Brain, human=True, canonical_marker=True, ubiquitousness=0.004, human_sensitivity=0.5, human_specificity=0.0

## Adipocytes
PanglaoDB cell type(s) used: Adipocytes

- **ADIPOQ**
  - PanglaoDB (OmniPath record_id 261): cell_type=Adipocytes, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.004, human_sensitivity=0.0, human_specificity=0.0
  - also a PanglaoDB marker of: Cardiomyocytes, Paneth cells

- **PLIN1**
  - PanglaoDB (OmniPath record_id 272): cell_type=Adipocytes, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.0, human_sensitivity=0.0, human_specificity=0.0
  - also a PanglaoDB marker of: Hepatocytes

- **LEP**
  - PanglaoDB (OmniPath record_id 201): cell_type=Adipocytes, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.0, human_sensitivity=0.0, human_specificity=0.0
  - also a PanglaoDB marker of: Gastric chief cells, Leydig cells

- **CIDEC**
  - PanglaoDB (OmniPath record_id 301): cell_type=Adipocytes, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.002, human_sensitivity=0.0, human_specificity=0.0

- **CIDEA**
  - PanglaoDB (OmniPath record_id 203): cell_type=Adipocytes, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.004, human_sensitivity=0.0, human_specificity=0.0
  - also a PanglaoDB marker of: Thymocytes

- **LGALS12**
  - PanglaoDB (OmniPath record_id 451): cell_type=Adipocytes, organ=Connective tissue, human=True, canonical_marker=True, ubiquitousness=0.0, human_sensitivity=0.0, human_specificity=0.0

## Erythroid cells
PanglaoDB cell type(s) used: Erythroid-like and erythroid precursor cells

- **HBB**
  - PanglaoDB (OmniPath record_id 4645): cell_type=Erythroid-like and erythroid precursor cells, organ=Blood, human=True, canonical_marker=True, ubiquitousness=0.03, human_sensitivity=0.959064, human_specificity=0.129096

- **HBA1**
  - PanglaoDB (OmniPath record_id 4646): cell_type=Erythroid-like and erythroid precursor cells, organ=Blood, human=True, canonical_marker=False, ubiquitousness=0.03, human_sensitivity=1.0, human_specificity=0.132406
  - PanglaoDB (OmniPath record_id 4647): cell_type=Erythroid-like and erythroid precursor cells, organ=Blood, human=True, canonical_marker=False, ubiquitousness=0.025, human_sensitivity=0.994152, human_specificity=0.10427

- **HBD**
  - PanglaoDB (OmniPath record_id 4659): cell_type=Erythroid-like and erythroid precursor cells, organ=Blood, human=True, canonical_marker=False, ubiquitousness=0.016, human_sensitivity=0.894737, human_specificity=0.0546177

- **ALAS2**
  - PanglaoDB (OmniPath record_id 4641): cell_type=Erythroid-like and erythroid precursor cells, organ=Blood, human=True, canonical_marker=True, ubiquitousness=0.019, human_sensitivity=0.842105, human_specificity=0.000662032

- **AHSP**
  - PanglaoDB (OmniPath record_id 4655): cell_type=Erythroid-like and erythroid precursor cells, organ=Blood, human=True, canonical_marker=False, ubiquitousness=0.01, human_sensitivity=0.900585, human_specificity=0.0158888

- **GYPA**
  - PanglaoDB (OmniPath record_id 4620): cell_type=Erythroid-like and erythroid precursor cells, organ=Blood, human=True, canonical_marker=True, ubiquitousness=0.011, human_sensitivity=0.497076, human_specificity=0.000662032
  - also a PanglaoDB marker of: Erythroblasts
