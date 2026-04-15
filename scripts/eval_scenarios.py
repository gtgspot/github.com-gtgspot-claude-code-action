#!/usr/bin/env python3
"""Evaluate architecture scenario JSON files with a simple sustainability model."""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

REQUIRED_FIELDS = {
    "name",
    "maintainability",
    "scalability",
    "performance_risk",
    "technical_debt_risk",
    "paradigm_tension",
}


def _validate_component(component: dict) -> None:
    missing = REQUIRED_FIELDS - component.keys()
    if missing:
        raise ValueError(f"Component missing fields: {sorted(missing)}")

    for key in REQUIRED_FIELDS - {"name"}:
        value = component[key]
        if not isinstance(value, (int, float)):
            raise ValueError(f"Field '{key}' must be numeric")
        if not 0 <= float(value) <= 1:
            raise ValueError(f"Field '{key}' must be between 0 and 1")


def evaluate_scenario(path: Path) -> dict:
    data = json.loads(path.read_text())
    components = data.get("components")
    if not isinstance(components, list) or not components:
        raise ValueError("Scenario must include a non-empty 'components' list")

    for component in components:
        _validate_component(component)

    maintainability = statistics.mean(c["maintainability"] for c in components)
    scalability = statistics.mean(c["scalability"] for c in components)
    performance_risk = statistics.mean(c["performance_risk"] for c in components)
    debt_risk = statistics.mean(c["technical_debt_risk"] for c in components)
    paradigm_tension = statistics.mean(c["paradigm_tension"] for c in components)

    maintainability_pressure = 1 - maintainability
    scalability_pressure = 1 - scalability

    sustainability = max(
        0.0,
        min(
            1.0,
            1 - (
                0.30 * maintainability_pressure
                + 0.25 * scalability_pressure
                + 0.20 * performance_risk
                + 0.15 * debt_risk
                + 0.10 * paradigm_tension
            ),
        ),
    )

    return {
        "scenario": data.get("scenario", path.stem),
        "component_count": len(components),
        "maintainability_pressure": round(maintainability_pressure, 4),
        "scalability_pressure": round(scalability_pressure, 4),
        "performance_risk": round(performance_risk, 4),
        "technical_debt_risk": round(debt_risk, 4),
        "paradigm_tension": round(paradigm_tension, 4),
        "sustainability_score": round(sustainability, 4),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 scripts/eval_scenarios.py <scenario.json>")
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"Error: file not found: {path}")
        return 2

    try:
        result = evaluate_scenario(path)
    except ValueError as exc:
        print(f"Validation failed: {exc}")
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
