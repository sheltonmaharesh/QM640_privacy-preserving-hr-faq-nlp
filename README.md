# QM 640 - Privacy-Preserving HR FAQ NLP

This repository supports the **QM 640 – Data Analytics Capstone** draft synopsis.

**Student:** Shelton Maharesh Sundersingh  
**Mentor:** Dr. Dr. Sanghitaa Karmakar

## Working topic

**Privacy-Preserving Discovery and Validation of Employee HR FAQs from Enterprise HR Email Using PII Redaction, Semantic Clustering, and Grounded Large Language Models**

The study is based on an HR mailbox at **a leading European bank in Austria**. This public repository contains only course-safe material. It does **not** contain raw HR emails, real employee data, proprietary bank identifiers, internal URLs, credentials, or production secrets.

## Current stage

This repository represents the **starting / synopsis stage** of the capstone. Research questions, statistical assumptions, thresholds, and validation criteria are preliminary and will be refined in later course weeks.

## Proposed research questions

- **RQ1 – Recurring-topic coverage:** What proportion of eligible, de-identified HR email threads can be assigned to coherent recurring semantic topics suitable for FAQ discovery?
- **RQ2 – PII redaction and semantic preservation:** To what extent does PII redaction preserve the semantic meaning required for downstream similarity and clustering?
- **RQ3 – Cohesion, grounding, and review quality:** What relationship exists between semantic cluster cohesion, grounding similarity, and human review quality for proposed FAQ candidates?
- **RQ4 – Conflict screening:** Can semantically similar FAQ questions with dissimilar answer embeddings be used to identify candidate answer conflicts for human review?

## Preliminary pipeline

1. Read approved HR-mailbox records.
2. Detect and redact PII using German/English spaCy NER plus regex rules.
3. Create multilingual semantic embeddings from redacted questions.
4. Group recurring questions using UMAP + HDBSCAN.
5. Generate reviewable FAQ candidates from recurring clusters.
6. Ground proposed answers against source HR responses.
7. Calculate quality signals such as cluster cohesion and grounding similarity.
8. Flag possible answer conflicts when similar questions have dissimilar answers.
9. Send generated FAQs and conflict flags to human review before any operational use.

The conflict score is a **screening signal**, not proof that two answers logically contradict each other.

## Repository structure

```
.
├── analysis/
│   └── sample_size_check.py
├── data/
│   └── synthetic_hr_mailbox.csv
├── docs/
│   ├── data_dictionary.csv
│   ├── proposed_research_questions.md
│   └── sample_size_notes.md
├── tests/
│   └── test_sample_size_check.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Reproduce the preliminary sample-size calculations

Create a virtual environment and install the small analysis dependency set:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -r requirements.txt
python analysis/sample_size_check.py
pytest -q
```

Expected planning minima:

| Research question | Planning method | Minimum |
|---|---|---:|
| RQ1 | 95% CI for a proportion, p=.50, margin ±.03 | 1,068 eligible threads |
| RQ2 | 95% CI for PII precision/recall, p=.50, margin ±.05 | 385 relevant PII decisions per denominator |
| RQ3 | Fisher-z correlation approximation, r=.25, alpha=.05, power=.80 | 124 cluster/FAQ observations |
| RQ4 | 95% CI for a proportion, p=.50, margin ±.07 | 196 reviewed FAQ pairs |

For rubric alignment, the preliminary maximum is:

```
max(1068, 385, 124, 196) = 1068
```

Because the four research questions use **different units of analysis**, 1,068 should be interpreted as the source-corpus planning target rather than as a substitute for each RQ-specific validation requirement.

## Privacy and data-access statement

The real HR-mailbox dataset is confidential and cannot be published. The public `data/` file is entirely synthetic and exists only to make the repository structure reproducible. Any real-data analysis will remain inside the approved secure environment and will use the organization's privacy and access controls.

## Week 1 limitation statement

This repository does not claim completed EDA, final hypotheses, calibrated thresholds, model-performance results, final expert-validation results, or conclusions. Those belong to later capstone phases.
