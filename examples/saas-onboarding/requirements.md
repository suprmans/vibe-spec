# Requirements — SaaS Self-Serve Onboarding

Version: 0.1
Run ID: ex-saas-onboarding-001
Date: 2026-04-15
Traceability root: ex-saas-onboarding-001 (context.json)

---

## User stories

### REQ-001: Guided data source connection

**Story:** As a trial user, I want to connect my first data source without needing IT credentials or admin access, so that I can reach my first aha moment within 3 days of starting a trial.

**Acceptance criteria:**
- [ ] AC1: A trial user with viewer-level permissions can connect at least one data source type without requiring admin OAuth approval.
- [ ] AC2: The connection wizard completes in ≤ 5 steps with no steps requiring IT intervention.
- [ ] AC3: Time-to-first-successful-connection is ≤ 10 minutes for first-time users (measured by product analytics).

**Traceability:** OBJ-001, OBJ-002, PAIN-002
**Priority:** Must Have (confidence: 0.93)
**Scorecard:**
- invest_score: 0.88
- ambiguity_flag: 0
- ac_coverage: 3
- priority_confidence: 0.93

---

### REQ-002: Onboarding progress indicator

**Story:** As a trial user, I want to see my onboarding progress and the next step to complete, so that I know what to do next and don't abandon the product out of confusion.

**Acceptance criteria:**
- [ ] AC1: A progress bar showing onboarding completion percentage is visible on every page of the trial experience.
- [ ] AC2: The next recommended action is displayed on the dashboard with a single click-to-action.
- [ ] AC3: Users who return to the product after ≥ 24 hours are shown a resume prompt.

**Traceability:** OBJ-001, PAIN-001
**Priority:** Must Have (confidence: 0.88)
**Scorecard:**
- invest_score: 0.85
- ambiguity_flag: 0
- ac_coverage: 3
- priority_confidence: 0.88

---

### REQ-003: Trial expiry and conversion nudge

**Story:** As a trial user approaching day 7 without completing onboarding, I want to receive a targeted re-engagement notification, so that I have a specific reason and path to continue.

**Acceptance criteria:**
- [ ] AC1: An in-product notification is sent at day 5 if the user has not connected a data source.
- [ ] AC2: The notification includes a direct deep-link to the connection wizard step the user last reached.
- [ ] AC3: Email re-engagement is triggered at day 7 with a 1-click "resume setup" link.

**Traceability:** OBJ-003, PAIN-001
**Priority:** Should Have (confidence: 0.80)
**Scorecard:**
- invest_score: 0.83
- ambiguity_flag: 0
- ac_coverage: 3
- priority_confidence: 0.80

---

## Functional requirements

### FR-001: OAuth delegated connection

**Category:** integration
**Description:** The system shall support data source connections using delegated OAuth tokens with read-only scope, without requiring the connecting user to hold admin-level permissions on the source system.
**Rationale:** Removes the IT dependency that blocks 35% of trial drop-offs (PAIN-002).
**Traceability:** OBJ-002, PAIN-002
**Priority:** Must Have
**Measurable criterion:** At least 3 of the top 5 data source integrations support delegated read-only OAuth by launch.
**Confidence:** 0.87

---

### FR-002: Onboarding state persistence

**Category:** data
**Description:** The system shall persist each user's onboarding state — current step, completed actions, and skipped steps — across sessions, devices, and browser restarts.
**Rationale:** Users interrupted during onboarding must be able to resume without restarting (PAIN-001).
**Traceability:** OBJ-001, PAIN-001
**Priority:** Must Have
**Measurable criterion:** A user who closes and reopens the product resumes at their last onboarding step with zero data loss in 100% of cases.
**Confidence:** 0.91

---

### FR-003: Onboarding analytics events

**Category:** reporting
**Description:** The system shall emit a structured analytics event for each onboarding step completion, step skip, and drop-off, with a timestamp and user ID, to a product analytics pipeline.
**Rationale:** Required to measure improvement in time-to-first-value and identify new drop-off points (OBJ-001).
**Traceability:** OBJ-001, OBJ-003
**Priority:** Must Have
**Measurable criterion:** 100% of onboarding interactions are captured with ≤ 1% event loss rate at 99th-percentile load.
**Confidence:** 0.85

---

## Scorecard summary

| Metric | Value | Target | Status |
|---|---|---|---|
| Total user stories | 3 | — | — |
| invest_score avg | 0.85 | ≥ 0.75 | PASS |
| ambiguity_flag total | 0 | 0 | PASS |
| ac_coverage avg | 3.0 | ≥ 2 | PASS |
| priority_confidence avg | 0.87 | ≥ 0.70 | PASS |
| Total functional requirements | 3 | — | — |
| fr_measurability avg | 0.88 | ≥ 0.80 | PASS |
| requirements_completeness | 0.87 | ≥ 0.80 | PASS |
