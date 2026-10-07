# Proposed research questions

These are Week 1 draft research questions and may be refined after the literature review, data audit, and mentor feedback.

## RQ1 - Recurring-topic coverage

What proportion of eligible, de-identified HR email threads can be assigned to coherent recurring semantic topics suitable for FAQ discovery?

**Initial dependent outcome:** recurring-topic assignment / topic coverage.  
**Initial predictors or grouping inputs:** redacted semantic representation, operational topic/subtopic where available.

## RQ2 - PII redaction and semantic preservation

To what extent does the proposed PII-redaction process preserve the semantic meaning required for downstream similarity and clustering?

**Proposed redaction approach:** English and German spaCy NER plus regex rules for structured identifiers.  
**Initial dependent outcome:** semantic similarity or paired representation difference before versus after redaction.  
**Initial independent condition:** pre-redaction versus post-redaction text.

## RQ3 - Cohesion, grounding, and review quality

What relationship exists between semantic cluster cohesion, grounding similarity, and human review quality for proposed FAQ candidates?

**Initial outcomes:** reviewer quality/approval measure and grounding quality.  
**Initial predictors:** cluster cohesion and grounding similarity.

## RQ4 - Conflict screening

Can semantically similar FAQ questions with dissimilar answer embeddings be used to identify candidate answer conflicts for human review?

**Initial outcome:** human-reviewed conflict/non-conflict label.  
**Initial predictors:** question similarity, answer similarity/distance, and the derived conflict-screening score.

The conflict score is not treated as proof of contradiction. It is a ranking/screening signal that requires expert review.
