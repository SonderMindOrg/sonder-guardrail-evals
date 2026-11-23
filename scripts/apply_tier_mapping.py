# SPDX-License-Identifier: Apache-2.0
"""Add the expected product tier to each input guardrail scenario.

Reads docs/tier_mapping.yaml and src/datasets/input_guardrails_scenarios.yaml and
writes one JSON object per scenario, with its expected tier, to stdout or --out.
Tier counts go to stderr. Fails if a scenario's label is missing from the mapping.

    pip install pyyaml
    python scripts/apply_tier_mapping.py --out input_scenarios_with_tiers.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MAPPING = REPO_ROOT / "docs" / "tier_mapping.yaml"
DEFAULT_SCENARIOS = REPO_ROOT / "src" / "datasets" / "input_guardrails_scenarios.yaml"


def load_mapping(path: Path) -> tuple[list[str], str, dict[str, str]]:
    data = yaml.safe_load(path.read_text())
    tiers = [tier["id"] for tier in data["tiers"]]
    labels = dict(data["labels"])
    unknown = sorted({data["not_fired"], *labels.values()} - set(tiers))
    if unknown:
        raise ValueError(f"{path} uses tiers it does not define: {unknown}")
    return tiers, data["not_fired"], labels


def expected_tier(output: dict, not_fired: str, labels: dict[str, str]) -> str:
    if not output["expected_result"]:
        return not_fired
    label = output.get("expected_observation")
    if label not in labels:
        raise KeyError(f"label {label!r} has no tier in the mapping")
    return labels[label]


def apply(mapping_path: Path, scenarios_path: Path) -> tuple[list[dict], list[str]]:
    tiers, not_fired, labels = load_mapping(mapping_path)
    rows = []
    for index, scenario in enumerate(yaml.safe_load(scenarios_path.read_text())["scenarios"]):
        output = scenario["output"]
        try:
            tier = expected_tier(output, not_fired, labels)
        except KeyError as exc:
            raise KeyError(f"scenario {index} ({scenario['description']!r}): {exc.args[0]}") from None
        rows.append({
            "index": index,
            "description": scenario["description"],
            "category": (scenario.get("metadata") or {}).get("category"),
            "expected_result": bool(output["expected_result"]),
            "expected_observation": output.get("expected_observation"),
            "expected_tier": tier,
        })
    return rows, tiers


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--out", type=Path, help="write JSON Lines here instead of stdout")
    args = parser.parse_args(argv)

    try:
        rows, tiers = apply(args.mapping, args.scenarios)
    except (KeyError, ValueError) as exc:
        print(f"error: {exc.args[0]}", file=sys.stderr)
        return 1

    lines = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    if args.out:
        args.out.write_text(lines, encoding="utf-8")
    else:
        sys.stdout.write(lines)

    counts = Counter(row["expected_tier"] for row in rows)
    for tier in tiers:
        print(f"{tier}: {counts[tier]}", file=sys.stderr)
    print(f"total: {len(rows)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
