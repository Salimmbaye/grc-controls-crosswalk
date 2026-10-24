# Security Controls Crosswalk — NIST CSF ⇄ 800-53 ⇄ ISO 27001 ⇄ CIS

A multi-framework **security controls crosswalk** with a Python query tool. It maps
31 control areas across four of the most common frameworks, so a single control —
"enforce MFA," say — can be translated between them instantly.

> Part of a three-project GRC portfolio. Companion to the
> [fintech risk assessment](../grc-risk-assessment-fintech) (that project's report
> references this crosswalk for its control mappings).

---

## Why this exists

Organizations rarely answer to just one framework — a company might run **NIST CSF**
internally, need **SOC 2** (NIST 800-53-style controls) to close enterprise deals,
hold **ISO/IEC 27001** for international partners, and follow **CIS Controls** on the
engineering side. A crosswalk lets you **assess once and comply many**: collect
evidence a single time and apply it across every audit, surface coverage gaps, and
scope a new framework as a delta instead of a fresh start.

Full rationale and the "mappings are many-to-many" caveat:
[`docs/why-crosswalks-matter.md`](docs/why-crosswalks-matter.md).

## Frameworks covered

| Framework | ID style | Column |
|-----------|----------|--------|
| NIST CSF 2.0 | `PR.AA-03` | `NIST_CSF_2_0` |
| NIST SP 800-53 Rev 5 | `IA-2(1)` | `NIST_800_53_r5` |
| ISO/IEC 27001:2022 (Annex A) | `A.8.5` | `ISO_27001_2022` |
| CIS Controls v8 | `6.3` | `CIS_v8` |

## The query tool

```bash
# list every control area, grouped by NIST CSF function
python3 scripts/crosswalk.py list

# search all fields for a term
python3 scripts/crosswalk.py search mfa

# translate a control from one framework to the others
python3 scripts/crosswalk.py map iso A.8.5        # ISO -> all frameworks
python3 scripts/crosswalk.py map csf PR.AA-03     # CSF -> all frameworks
python3 scripts/crosswalk.py map 800-53 IA-2      # 800-53 -> all frameworks

# coverage statistics
python3 scripts/crosswalk.py stats
```

**Example** — `map iso A.8.5`:

```
ISO 27001:2022 'A.8.5' maps to:

  ■ Multi-factor authentication  [Protect]
    Authenticate users; enforce MFA for remote and privileged access.
      NIST CSF 2.0    : PR.AA-03
      NIST 800-53r5   : IA-2(1), IA-2(2)
      ISO 27001:2022  : A.8.5
      CIS v8          : 6.3, 6.4, 6.5
```

## Deliverables

- [`Controls-Crosswalk-Report.docx`](Controls-Crosswalk-Report.docx): crosswalk report (Word)
- [`Controls-Crosswalk.xlsx`](Controls-Crosswalk.xlsx): crosswalk workbook (Excel)

## Repository structure

```
grc-controls-crosswalk/
├── README.md
├── docs/
│   └── why-crosswalks-matter.md     ← the concept, the caveats, framework reference
├── data/
│   └── control-crosswalk.csv        ← 31 control areas × 4 frameworks (source of truth)
└── scripts/
    └── crosswalk.py                 ← CLI: list / search / map / stats (standard library only)
```

No third-party dependencies — the tool uses only the Python standard library.

## What this project demonstrates

- **Framework fluency** across the four frameworks GRC programs use most.
- Understanding that control mappings are **many-to-many professional judgments**,
  not exact equivalences.
- The **"assess once, comply many"** efficiency principle behind real compliance programs.
- Practical **Python tooling** (argparse CLI, CSV parsing) to make the mapping usable.

## Provenance & accuracy

Mappings are **curated for education**, aligned to the published NIST CSF 2.0
Informative References / NIST OLIR, CIS Controls v8 mappings, and ISO/IEC 27001:2022
Annex A. They are representative, not exhaustive — validate against current official
sources before relying on them in an audit. See
[`docs/why-crosswalks-matter.md`](docs/why-crosswalks-matter.md).
