# Venue Template Reference

## MICCAI (Medical Image Computing and Computer Assisted Intervention)

| Field | Value |
|-------|-------|
| Format | LNCS (Lecture Notes in Computer Science), Springer |
| Columns | Double-column |
| Page Limit | 8 pages main text + up to 2 pages references |
| Anonymous | Yes (double-blind review) |
| Citation Style | `\bibliographystyle{splncs04}` numbered |
| Template | `llncs.cls` (Springer LNCS) |
| Abstract | Max 250 words, unstructured |
| Key Sections | 1 Introduction, 2 Method, 3 Experiments, 4 Discussion, 5 Conclusion |
| LaTeX Command | `\documentclass[llncs]{llncs}` or `\documentclass{llncs}` |
| Common Pitfalls | Overlength → trim Discussion; figure placement in double-column; bib style mismatch |
| Template URL | https://www.springer.com/gp/authors-editors/book-authors-editors/springernature-latex-template |

## MedIA (Medical Image Analysis)

| Field | Value |
|-------|-------|
| Format | Elsevier journal |
| Columns | Double-column |
| Page Limit | No strict limit, typically 12-20 pages |
| Anonymous | Usually yes for initial submission |
| Citation Style | numbered, e.g. `\bibliographystyle{elsarticle-num}` |
| Template | `elsarticle.cls` |
| Abstract | Structured (Background, Methods, Results, Conclusions) |
| Key Sections | 1 Introduction, 2 Related Work, 3 Method, 4 Experiments (4.1 Setup, 4.2 Results, 4.3 Ablation), 5 Discussion, 6 Conclusion |
| LaTeX Command | `\documentclass[3p,times]{elsarticle}` |
| Common Pitfalls | Figure resolution (≥300 DPI); structured abstract compliance |
| Template URL | https://www.elsevier.com/authors/policies-and-guidelines |

## AAAI (Association for the Advancement of Artificial Intelligence)

| Field | Value |
|-------|-------|
| Format | AAAI Press custom |
| Columns | Double-column |
| Page Limit | 8 pages main + 2 pages references |
| Anonymous | Yes (double-blind) |
| Citation Style | AAAI-specific: `aaai.bst` |
| Template | `aaai24.sty` (version-specific) |
| Abstract | Max 200 words, unstructured |
| LaTeX Command | `\documentclass[letterpaper]{article}` + `\usepackage{aaai24}` |
| Common Pitfalls | No page numbers; bibliography must be within 2 extra pages |
| Template URL | https://aaai.org/conference/aaai/aaai25/submission-guidelines/ |

## CVPR (Computer Vision and Pattern Recognition)

| Field | Value |
|-------|-------|
| Format | IEEE/CVF |
| Columns | Double-column |
| Page Limit | 8 pages main |
| Anonymous | Yes |
| Citation Style | `\bibliographystyle{ieeenat}` |
| Template | `cvpr.cls` |
| Abstract | Max 200 words |
| LaTeX Command | `\documentclass[10pt,twocolumn,letterpaper]{article}` + `\usepackage{cvpr}` |
| Common Pitfalls | 8 pages exactly, not including references; supplementary material separate |
| Template URL | https://cvpr.thecvf.com/ |

## IEEE ISBI (International Symposium on Biomedical Imaging)

| Field | Value |
|-------|-------|
| Format | IEEE conference |
| Columns | Single-column |
| Page Limit | 4-6 pages |
| Anonymous | Yes |
| Citation Style | IEEE numbered |
| Template | IEEEtran.cls |
| Abstract | Max 150 words |
| LaTeX Command | `\documentclass[conference]{IEEEtran}` |
| Common Pitfalls | Very tight page limit → maximize figures, minimize prose; single-column is unusual for IEEE |
| Template URL | https://2025.ieee-isbi.org/ |

## Nature Medicine (or Nature Biomedical Engineering)

| Field | Value |
|-------|-------|
| Format | Nature Publishing Group |
| Columns | Double-column (PDF) |
| Page/Word Limit | ~3,000 words main text; 50 references max |
| Anonymous | No (usually not after initial screening) |
| Citation Style | numbered (Nature style: bold number, e.g. `\textbf{1}.`) |
| Template | `sn-jnl.cls` (Springer Nature) |
| Abstract | 150-200 words, highly structured |
| Key Sections | Introduction → Results → Discussion → Methods (at end) |
| Common Pitfalls | Very strict word limits; data availability statement required; competing interests |
| Template URL | https://www.nature.com/natmed/for-authors |

## IEEE Access / IEEE Transactions

| Field | Value |
|-------|-------|
| Format | IEEE |
| Columns | Double-column |
| Page Limit | No strict limit (typically 10-15 pages) |
| Anonymous | No (single-blind) |
| Citation Style | IEEE numbered |
| Template | `IEEEtran.cls` |
| Abstract | 150-250 words, unstructured or structured |
| LaTeX Command | `\documentclass[journal]{IEEEtran}` |
| Common Pitfalls | Figure quality; data/code availability statements increasingly required |
