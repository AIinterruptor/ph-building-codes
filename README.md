# Philippine Building Codes — Machine-Readable

Machine-readable YAML/JSON encoding of Philippine building regulations for automated compliance checking.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Covered Codes

| Code | Reference | Scope | Status |
|------|-----------|-------|--------|
| **National Building Code** | PD 1096 (2004 Revised IRR) | Setbacks, FAR, PSO, ceiling heights, ventilation, occupancy | ✅ Seeded |
| **Accessibility Law** | BP 344 (2024 Revised IRR) | Ramps, PWD parking, doors, toilets, corridors | ✅ Seeded |
| **Fire Code** | RA 9514 (2019 RIRR) | Occupant loads, travel distance, exit widths, fire ratings | ✅ Seeded |

## Repository Structure

```
ph-building-codes/
├── nbcp/                    # PD 1096 — National Building Code
│   ├── setbacks.yaml        # Minimum setbacks by zoning type
│   ├── building_bulk.yaml   # FAR, PSO, height limits
│   ├── light_ventilation.yaml  # Ceiling heights, window ratios, courts
│   └── occupancy.yaml       # Occupancy classifications
├── bp344/                   # BP 344 — Accessibility Law
│   ├── ramps.yaml           # Ramp slopes, widths, landings
│   ├── parking.yaml         # PWD parking dimensions
│   ├── doors_corridors.yaml # Door widths, corridor widths
│   └── toilets.yaml         # Accessible toilet requirements
├── ra9514/                  # RA 9514 — Fire Code
│   ├── occupant_loads.yaml  # Load factors by occupancy type
│   ├── means_of_egress.yaml # Travel distance, exit widths, dead ends
│   └── fire_resistance.yaml # Fire ratings, firewalls, suppression
├── schemas/                 # JSON Schema for rule validation
│   └── rule_schema.json
├── scripts/                 # Build tools
│   └── build_json.py        # YAML → JSON converter
└── dist/                    # Auto-generated JSON (do not edit)
```

## Data Format

Each YAML file contains rules organized by section, with every rule carrying:

```yaml
- id: "NBCP-VIII-S001"          # Unique rule identifier
  section: "Rule VIII, Sec. 5"   # Official section reference
  description: "Minimum court width for 1-2 storey buildings"
  value: 2.0
  unit: "m"
  applies_to: ["R-1", "R-2", "R-3"]
  conditions:
    storeys_max: 2
  source: "2004 Revised IRR of PD 1096"
```

## Usage

### Python
```python
import yaml

with open("nbcp/setbacks.yaml") as f:
    rules = yaml.safe_load(f)

# Find R-1 front setback
for rule in rules["rules"]:
    if "R-1" in rule.get("applies_to", []) and "front" in rule.get("description", "").lower():
        print(f"{rule['description']}: {rule['value']}{rule['unit']}")
```

### Build JSON
```bash
python scripts/build_json.py          # Generates dist/*.json
python scripts/build_json.py --validate  # Validate against schema
```

## Contributing

This is a community effort to digitize Philippine building codes. Contributions welcome:

1. **Verify existing rules** — Cross-check values against official IRR documents
2. **Add missing provisions** — Many sections are not yet encoded
3. **Add LGU-specific overrides** — Local zoning ordinances may differ
4. **Improve metadata** — Add cross-references, exceptions, notes

### Rule ID Convention

Format: `{CODE}-{RULE}-{TYPE}{NUMBER}`

- Code: `NBCP`, `BP344`, `FC` (Fire Code)
- Rule: Roman numeral or section (e.g., `VIII`, `IRR`)
- Type: `S` (setback), `H` (height), `A` (area), `R` (ratio), `D` (dimension), `L` (load), `T` (time/distance)
- Number: Sequential 3-digit (e.g., `001`)

## Disclaimer

This repository is an **unofficial digitization** of Philippine building codes for educational and tooling purposes. It is NOT a substitute for the official legal texts published by DPWH and BFP. Always verify against the current official IRR before making compliance decisions.

**Official sources:**
- [DPWH — PD 1096 IRR](https://www.dpwh.gov.ph/dpwh/references/laws_codes_orders/PD1096)
- [DPWH — BP 344 IRR](https://www.dpwh.gov.ph/dpwh/references/laws_codes_orders/bpb344)
- [BFP — RA 9514 RIRR 2019](https://bfp.gov.ph/wp-content/uploads/2019/10/RA9514-RIRR-rev-2019.pdf)

## License

MIT — see [LICENSE](LICENSE).
