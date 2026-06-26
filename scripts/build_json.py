#!/usr/bin/env python3
"""
Build script: convert YAML rule files to JSON for programmatic consumption.

Usage:
    python scripts/build_json.py              # Convert all YAML to JSON in dist/
    python scripts/build_json.py --validate   # Also validate against schema
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SCHEMA_PATH = ROOT / "schemas" / "rule_schema.json"
SOURCE_DIRS = ["nbcp", "bp344", "ra9514"]


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_rule(rule: dict, schema: dict) -> list[str]:
    errors = []
    if "id" not in rule:
        errors.append(f"Missing 'id' in rule: {rule.get('description', '?')}")
    if "section" not in rule:
        errors.append(f"Missing 'section' in rule {rule.get('id', '?')}")
    if "description" not in rule:
        errors.append(f"Missing 'description' in rule {rule.get('id', '?')}")
    if "value" not in rule and "value_min" not in rule:
        errors.append(f"Missing 'value' or 'value_min' in rule {rule.get('id', '?')}")
    return errors


def build(validate: bool = False) -> int:
    DIST.mkdir(exist_ok=True)

    schema = None
    if validate and SCHEMA_PATH.exists():
        with open(SCHEMA_PATH) as f:
            schema = json.load(f)

    total_rules = 0
    total_files = 0
    all_errors = []
    all_ids = set()

    for src_dir in SOURCE_DIRS:
        src_path = ROOT / src_dir
        if not src_path.exists():
            continue

        for yaml_file in sorted(src_path.glob("*.yaml")):
            data = load_yaml(yaml_file)
            if data is None:
                continue

            out_name = f"{src_dir}_{yaml_file.stem}.json"
            out_path = DIST / out_name

            if validate and "rules" in data:
                for rule in data["rules"]:
                    errors = validate_rule(rule, schema)
                    all_errors.extend(errors)

                    rid = rule.get("id")
                    if rid:
                        if rid in all_ids:
                            all_errors.append(f"Duplicate rule ID: {rid}")
                        all_ids.add(rid)

                total_rules += len(data.get("rules", []))

            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            total_files += 1
            print(f"  {yaml_file.relative_to(ROOT)} -> {out_path.relative_to(ROOT)}")

    # Build combined index
    index = {
        "codes": [],
        "total_rules": 0,
        "total_files": total_files,
    }

    for src_dir in SOURCE_DIRS:
        src_path = ROOT / src_dir
        if not src_path.exists():
            continue

        code_entry = {"directory": src_dir, "files": []}
        for yaml_file in sorted(src_path.glob("*.yaml")):
            data = load_yaml(yaml_file)
            if data is None:
                continue
            n_rules = len(data.get("rules", [])) + len(data.get("classifications", []))
            code_entry["files"].append({
                "name": yaml_file.stem,
                "code": data.get("code", ""),
                "section": data.get("section", ""),
                "rule_count": n_rules,
            })
            index["total_rules"] += n_rules
        index["codes"].append(code_entry)

    with open(DIST / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*50}")
    print(f"Built {total_files} files -> dist/")
    print(f"Total rules indexed: {index['total_rules']}")

    if validate:
        print(f"Unique rule IDs: {len(all_ids)}")
        if all_errors:
            print(f"\nValidation errors ({len(all_errors)}):")
            for e in all_errors:
                print(f"  ✗ {e}")
            return 1
        else:
            print("Validation: PASS")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build JSON from YAML rule files")
    parser.add_argument("--validate", action="store_true", help="Validate rules against schema")
    args = parser.parse_args()

    sys.exit(build(validate=args.validate))
