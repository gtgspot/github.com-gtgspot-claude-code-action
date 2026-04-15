# Claude Code Action Playground

This repository is a lightweight foundation for experimenting with **AI-assisted repository automation** and **architecture-aware expansion planning**.

## What exists now

- A comment-driven Claude Code workflow (`@claude`) with manual dispatch support.
- Security and reliability guardrails (permissions, concurrency, timeout).
- A starter architecture exploration document.

## New foundation for expansion opportunities

This repository now includes:

1. **Component model primer** (`docs/component_model.md`) for a pedagogical architecture framework.
2. **Scenario-based evaluation harness** (`eval/scenarios/*.json` + `scripts/eval_scenarios.py`) to score maintainability/scalability/sustainability assumptions.
3. **Continuous checks workflow** (`.github/workflows/foundation-checks.yml`) to validate scenario files and workflow syntax.
4. **Issue template** (`.github/ISSUE_TEMPLATE/expansion-opportunity.yml`) to standardize future proposals.

## Quick start

Run the scenario evaluator locally:

```bash
python3 scripts/eval_scenarios.py eval/scenarios/component-architecture-baseline.json
```

This prints derived metrics such as maintainability pressure, paradigm tension, and a baseline sustainability score.
