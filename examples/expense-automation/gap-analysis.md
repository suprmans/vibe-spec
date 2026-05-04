# Gap Analysis — Expense Approval Automation

Version: 0.1
Run ID: ex-expense-automation-001
Date: 2026-03-20
Traceability root: ex-expense-automation-001 (context.json)

---

## AS-IS state

The current expense approval process is a three-step manual chain:

1. Employee completes a paper form or Excel spreadsheet
2. Line manager reviews and emails to Finance
3. Finance manually reconciles and processes reimbursement

**Key metrics (baseline):**
- Reimbursement cycle time: 3–6 weeks
- Finance reconciliation effort: 40 hours/month
- Audit trail: none (paper/email)
- Employee satisfaction: low (dissatisfaction explicitly noted)

---

## TO-BE state

A digital expense management workflow:

1. Employee submits expense via a web or mobile form with receipt photo
2. System routes for manager approval (auto-approve below policy threshold)
3. Finance receives structured, validated data — no manual re-entry
4. Reimbursement processed within 5 business days

**Target metrics:**
- Reimbursement cycle: ≤ 5 business days
- Finance reconciliation effort: ≤ 20 hours/month (50% reduction)
- Audit trail: complete, searchable, with approval timestamps
- Policy compliance: automated flagging of out-of-policy submissions

---

## Gap inventory

### GAP-001: No digital submission channel

**AS-IS:** Paper forms and Excel spreadsheets — no digital submission capability.
**TO-BE:** Web and mobile expense submission with receipt capture.
**Impact:** 9.0 (blocks entire transformation — no digital process without this)
**Effort:** M
**Trace:** PAIN-001, OBJ-001

**Scorecard:**
- quick_win_flag: false
- priority_tier: 2
- priority_label: Strategic bet

---

### GAP-002: No automated approval routing

**AS-IS:** Managers email Finance manually — no routing rules, no SLA, no status visibility.
**TO-BE:** Rule-based routing with policy thresholds, manager delegation, and status tracking.
**Impact:** 8.5 (directly drives reimbursement cycle time)
**Effort:** M
**Trace:** PAIN-001, OBJ-002

**Scorecard:**
- quick_win_flag: false
- priority_tier: 2
- priority_label: Strategic bet

---

### GAP-003: No audit trail or compliance reporting

**AS-IS:** No searchable record of who approved what or when.
**TO-BE:** Immutable approval log with timestamps, exportable for audit.
**Impact:** 7.0 (compliance and internal audit requirement)
**Effort:** S
**Trace:** PAIN-003, CON-001

**Scorecard:**
- quick_win_flag: true
- priority_tier: 1
- priority_label: Quick win

---

### GAP-004: Finance reconciliation is fully manual

**AS-IS:** Finance re-enters data from emails into accounting system — 40 hrs/month.
**TO-BE:** Structured data export or direct accounting system integration.
**Impact:** 8.0 (40 hrs/month saving)
**Effort:** L
**Trace:** PAIN-002, OBJ-003

**Scorecard:**
- quick_win_flag: false
- priority_tier: 2
- priority_label: Strategic bet

---

### GAP-005: No out-of-policy detection

**AS-IS:** Policy compliance depends on manager memory and manual review.
**TO-BE:** Automated flagging of submissions exceeding per-diem limits or missing receipts.
**Impact:** 5.0 (reduces Finance review burden)
**Effort:** S
**Trace:** PAIN-002, OBJ-003

**Scorecard:**
- quick_win_flag: true
- priority_tier: 1
- priority_label: Quick win

---

## Prioritisation summary

| ID | Gap | Tier | Label | Impact | Effort |
|---|---|---|---|---|---|
| GAP-003 | Audit trail | 1 | Quick win | 7.0 | S |
| GAP-005 | Policy detection | 1 | Quick win | 5.0 | S |
| GAP-001 | Digital submission | 2 | Strategic bet | 9.0 | M |
| GAP-002 | Approval routing | 2 | Strategic bet | 8.5 | M |
| GAP-004 | Finance integration | 2 | Strategic bet | 8.0 | L |

**Quick wins (deliver early):** GAP-003 (audit trail), GAP-005 (policy detection)
**Core platform (Q3 delivery):** GAP-001, GAP-002, GAP-004

---

## Scorecard summary

| Metric | Value | Target | Status |
|---|---|---|---|
| Total gaps | 5 | — | — |
| Quick wins identified | 2 | ≥ 1 | PASS |
| Tier 1 or 2 gaps | 5/5 | — | — |
| Avg impact | 7.5 | ≥ 5.0 | PASS |
| All gaps traced | 5/5 | 100% | PASS |
| gap_coverage | 1.00 | ≥ 0.80 | PASS |
