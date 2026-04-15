# Claude Code Action Playground

This repository provides a practical foundation for experimenting with **AI-assisted automation** and **architecture-aware expansion planning**.

## Infrastructure-first expansion model

To match a city-scale analogy (room → house → suburb → city), each software component node is now modeled with explicit dependency on shared utility infrastructure.

- **Room**: feature-level component
- **House**: bounded context (application area)
- **Suburb**: domain/platform slice
- **City**: organizational architecture
- **Underground utilities**: identity, event transport, config/secrets, telemetry, governance

This lets us measure not only component quality but also hidden infrastructure fragility that can destabilize larger systems.

## What this repository now includes

1. **Pedagogical architecture guide** in `docs/component_model.md`.
2. **Scenario evaluator** in `scripts/eval_scenarios.py` with utility-network aware scoring.
3. **Scenario datasets** in `eval/scenarios/*.json` (baseline + city-scale).
4. **CI checks** in `.github/workflows/foundation-checks.yml` for scenario validation and actionlint.
5. **Expansion issue template** in `.github/ISSUE_TEMPLATE/expansion-opportunity.yml`.

## Quick start

Run the baseline scenario:

```bash
python3 scripts/eval_scenarios.py eval/scenarios/component-architecture-baseline.json
```

Run the city-scale scenario:

```bash
python3 scripts/eval_scenarios.py eval/scenarios/city-scale-utility-network.json
```

Output includes:
- component pressures (maintainability/scalability),
- risk signals (performance/debt/paradigm tension),
- infrastructure signals (utility fragility/resilience/observability),
- an aggregate `sustainability_score`.
