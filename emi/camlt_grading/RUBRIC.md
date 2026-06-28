# CAMLT Final Exam Rubric (100 points)

**Course:** Current Approaches and Methods in Language Teaching  
**Sources:** Printed exam on scan + `manuscript/build_camlt_final_exam.py` answer key

## Printed exam structure (what students sat)

| Part | Points | Notes |
|------|--------|-------|
| **1. EMI** | **50** | front + back |
| 1.a Macaro & McKinley definitions + difference | 10 | open; reward accurate definitions and clear contrast |
| 1.b Five EMI model names | 10 | 2 each |
| 1.c Hard/Soft EMI (6 subjects) | 12 | 2 each |
| 1.d EMI vs CLIL (≥2 differences) | 18 | 9 per clear, explained difference |
| **2. TBLT** | **20** | five design features |
| 2 Five features + brief explanation | 20 | 4 each (≈1 name + 3 explanation) |
| **3. CBI** | **30** | three models |
| 3a Theme-based | 10 | how it works, who teaches, primary goal |
| 3b Sheltered | 10 | same |
| 3c Adjunct | 10 | same |

**Total: 100**

## Answer key — objective items

### 1.b EMI models (2 pts each)
1. Selection Model  
2. Preparatory Year Model  
3. Concurrent Support Model  
4. Multilingual Model (accept Partial EMI Model)  
5. Ostrich Model  

Accept reasonable spelling; must be recognisable model name.

### 1.c Hard / Soft (2 pts each)
1. Medicine → **H**  
2. Applied Linguistics → **S**  
3. Engineering → **H**  
4. TESOL → **S**  
5. History of Art → **H**  
6. Second Language Acquisition → **S**  

Accept H/S only; wrong = 0.

## Open-ended grading principles

- **Empty / no attempt:** 0 for that item (unless stray irrelevant words).
- **Partial:** proportional credit; do not be harsh on minor spelling if meaning is clear.
- **Detail matters:** for 1.a, 1.d, TBLT, CBI — reward accurate course terminology and explanations; brief vague phrases get low partial credit.
- **1.a (10):** ~3 pts per accurate definition (Macaro 2018; McKinley/Rose & McKinley 2018); ~4 pts for at least one clear difference. Confusing authors with models = heavy deduction.
- **1.d (18):** 9 pts per well-explained difference (focus, setting, language goal, learner profile, etc.). One weak difference max ~4–6.
- **TBLT (4 each):** Expected features (any order): Goal, Input, Conditions, Procedures, Predicted outcomes. ~1 pt correct name, ~3 pts accurate brief explanation. Wrong feature name with plausible description → up to 2.
- **CBI (10 each):** Theme-based = language class, themes/topics, language goal primary. Sheltered = content specialist, modified language, content goal primary. Adjunct = parallel language + content courses, coordinated topics, language support for content. Award 3–4 / 1–3 / 0–2 for strong / partial / weak-missing elements.

## JSON output per paper

```json
{
  "folder": "001_cam1",
  "idnumber": "200907063",
  "q1a": 0,
  "q1b": 0,
  "q1c": 12,
  "q1d": 0,
  "q2": 3,
  "q3a": 0,
  "q3b": 0,
  "q3c": 0,
  "section1": 12,
  "section2": 3,
  "section3": 0,
  "total": 15,
  "notes": "Brief English note on quality/gaps."
}
```

Round all subscores to nearest 0.5 where needed; **total = integer** (round final sum).
