# EMI proficiency study (explanatory mixed methods)

**Design.** QUANT → QUAL (explanatory sequential).  
**Quantitative (now):** RQ1 — paired Pre (PYP exit) vs Post (graduation) proficiency.  
**Qualitative (next):** RQ2–RQ3 — lecturer and student accounts of translanguaging / EMI language practice explaining oral–aural attrition.

See `RESEARCH_QUESTIONS.md`.

## Quantitative files

| File | Role |
| --- | --- |
| `EMI_quantitative_prepost_N120.xlsx` | Slim primary quant workbook (Pre/Post + paired tests) |
| `EMI_PYP_pre_post_synthetic_N120.xlsx` | Same slim panel (compatibility path for scripts) |
| `EMI_PYP_pre_post_FULL_ARCHIVE_with_mechanism.xlsx` | Archived fuller synthetic panel (not used in RQ1) |
| `EMI_Methodology_and_Quantitative_Results.docx` / `.md` | Methods + RQ1 results |
| `outputs/rstudio/fig1_skill_prepost_ggplot.png` | Figure 1 (preferred) |

## Rebuild quant

```bash
python reform_quantitative.py
Rscript rstudio/fig1_and_fig2_styled.R
python write_methods_results_docx.py
```

## Scale

0–100 institutional scores; PYP pass threshold = 60 (≈ CEFR B1).
