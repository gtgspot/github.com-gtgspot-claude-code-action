#!/usr/bin/env python3
"""Evaluate architecture scenarios with component and utility-network signals."""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

COMPONENT_FIELDS = {
    "name",
    "maintainability",
    "scalability",
    "performance_risk",
    "technical_debt_risk",
    "paradigm_tension",
    "service_criticality",
    "utility_dependencies",
}

UTILITY_FIELDS = {
    "name",
    "resilience",
    "capacity_headroom",
    "observability",
}


def _is_unit_interval(value: object) -> bool:
    return isinstance(value, (int, float)) and 0 <= float(value) <= 1


def _validate_component(component: dict) -> None:
    missing = COMPONENT_FIELDS - component.keys()
    if missing:
        raise ValueError(f"Component missing fields: {sorted(missing)}")

    numeric_fields = COMPONENT_FIELDS - {"name", "utility_dependencies"}
    for key in numeric_fields:
        value = component[key]
        if not _is_unit_interval(value):
            raise ValueError(f"Field '{key}' must be numeric between 0 and 1")

    dependencies = component["utility_dependencies"]
    if not isinstance(dependencies, list) or not dependencies:
        raise ValueError("Component field 'utility_dependencies' must be a non-empty list")
    if not all(isinstance(dep, str) and dep for dep in dependencies):
        raise ValueError("Each utility dependency must be a non-empty string")


def _validate_utility(utility: dict) -> None:
    missing = UTILITY_FIELDS - utility.keys()
    if missing:
        raise ValueError(f"Utility missing fields: {sorted(missing)}")

    for key in UTILITY_FIELDS - {"name"}:
        value = utility[key]
        if not _is_unit_interval(value):
            raise ValueError(f"Utility field '{key}' must be numeric between 0 and 1")


def evaluate_scenario(path: Path) -> dict:
    data = json.loads(path.read_text())
    components = data.get("components")
    utilities = data.get("utility_systems")

    if not isinstance(components, list) or not components:
        raise ValueError("Scenario must include a non-empty 'components' list")
    if not isinstance(utilities, list) or not utilities:
        raise ValueError("Scenario must include a non-empty 'utility_systems' list")

    for component in components:
        _validate_component(component)
    for utility in utilities:
        _validate_utility(utility)

    utility_names = {utility["name"] for utility in utilities}
    for component in components:
        unknown = [d for d in component["utility_dependencies"] if d not in utility_names]
        if unknown:
            raise ValueError(
                f"Component '{component['name']}' references unknown utilities: {sorted(unknown)}"
            )

    maintainability = statistics.mean(c["maintainability"] for c in components)
    scalability = statistics.mean(c["scalability"] for c in components)
    performance_risk = statistics.mean(c["performance_risk"] for c in components)
    debt_risk = statistics.mean(c["technical_debt_risk"] for c in components)
    paradigm_tension = statistics.mean(c["paradigm_tension"] for c in components)
    criticality = statistics.mean(c["service_criticality"] for c in components)

    utility_resilience = statistics.mean(u["resilience"] for u in utilities)
    utility_capacity = statistics.mean(u["capacity_headroom"] for u in utilities)
    utility_observability = statistics.mean(u["observability"] for u in utilities)

    maintainability_pressure = 1 - maintainability
    scalability_pressure = 1 - scalability
    utility_fragility = 1 - ((utility_resilience + utility_capacity + utility_observability) / 3)

    sustainability = max(
        0.0,
        min(
            1.0,
            1
            - (
                0.23 * maintainability_pressure
                + 0.19 * scalability_pressure
                + 0.17 * performance_risk
                + 0.14 * debt_risk
                + 0.09 * paradigm_tension
                + 0.12 * utility_fragility
                + 0.06 * criticality
            ),
        ),
    )

    return {
        "scenario": data.get("scenario", path.stem),
        "component_count": len(components),
        "utility_count": len(utilities),
        "maintainability_pressure": round(maintainability_pressure, 4),
        "scalability_pressure": round(scalability_pressure, 4),
        "performance_risk": round(performance_risk, 4),
        "technical_debt_risk": round(debt_risk, 4),
        "paradigm_tension": round(paradigm_tension, 4),
        "service_criticality": round(criticality, 4),
        "utility_fragility": round(utility_fragility, 4),
        "utility_resilience": round(utility_resilience, 4),
        "utility_capacity_headroom": round(utility_capacity, 4),
        "utility_observability": round(utility_observability, 4),
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
