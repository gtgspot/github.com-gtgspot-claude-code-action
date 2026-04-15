# Repository Additions Exploration

This repository currently contains a single GitHub Actions workflow that invokes `anthropics/claude-code-action` when someone comments on an issue or pull request review.

Below are practical additions you can adopt incrementally. Each section includes:

- **What it looks like** (representative configuration)
- **What it achieves** (architectural/operational impact)

---

## 1) Trigger Guardrails + Manual Dispatch

### What it looks like
- Keep comment-based triggers, but only run when the body contains `@claude`.
- Add `workflow_dispatch` for manual execution.

### What it achieves
- Reduces accidental runs and API spend.
- Makes testing/debugging easier through manual runs.
- Increases control without changing contributor behavior.

---

## 2) Explicit Token Permissions (Principle of Least Privilege)

### What it looks like
```yaml
permissions:
  contents: read
  issues: write
  pull-requests: write
```

### What it achieves
- Improves security posture by avoiding broad default permissions.
- Documents exactly what the automation needs.
- Makes future security audits simpler and faster.

---

## 3) Concurrency Control

### What it looks like
```yaml
concurrency:
  group: claude-code-${{ github.event_name }}-${{ github.event.issue.number || github.event.pull_request.number || github.run_id }}
  cancel-in-progress: false
```

### What it achieves
- Prevents race conditions on high-comment threads.
- Keeps discussion context coherent by serializing related runs.
- Improves determinism (fewer overlapping bot responses).

---

## 4) Time Budgeting and Failure Predictability

### What it looks like
```yaml
jobs:
  claude:
    timeout-minutes: 30
```

### What it achieves
- Prevents long-running/blocked jobs from consuming runner minutes indefinitely.
- Makes operational behavior more predictable.
- Gives maintainers a clear upper bound for incident debugging.

---

## 5) Add a CI Validation Workflow (Recommended Next)

### What it looks like
Create `.github/workflows/ci.yml` with checks such as:
- YAML linting (`actionlint`)
- Markdown linting
- Optional shell linting if scripts are added later

### What it achieves
- Detects invalid workflow syntax before production events.
- Protects maintainability as the repository grows.
- Lowers change risk when adding more automation.

---

## 6) Add an Evaluation Harness for Prompt/Policy Changes (Future)

### What it looks like
- Add a lightweight `eval/` folder with representative issue comments.
- Add a script that replays scenarios and checks expected outputs.

### What it achieves
- Converts subjective behavior changes into measurable regressions.
- Improves confidence in prompt/policy iteration.
- Supports the long-term sustainability of automation logic.

---

## Change Implemented in This Branch

The `main.yml` workflow in this branch now includes:

1. `workflow_dispatch` trigger
2. Explicit `permissions`
3. `concurrency` grouping
4. Job-level trigger guard (`@claude` mention or manual dispatch)
5. A `timeout-minutes` cap

This gives a more deterministic, secure baseline while preserving the original repository goal.
