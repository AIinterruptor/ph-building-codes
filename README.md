# Philippine Building Codes + Feng Shui — Machine-Readable

Machine-readable YAML/JSON encoding of Philippine building regulations and classical Feng Shui principles for automated architectural compliance and design analysis.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Covered Codes

| Code | Reference | Scope | Rules | Status |
|------|-----------|-------|-------|--------|
| **National Building Code** | PD 1096 (2004 Revised IRR) | Setbacks, FAR, PSO, ceiling heights, ventilation, occupancy | 90 | ✅ Seeded |
| **Accessibility Law** | BP 344 (2024 Revised IRR) | Ramps, PWD parking, doors, toilets, corridors | 44 | ✅ Seeded |
| **Fire Code** | RA 9514 (2019 RIRR) | Occupant loads, travel distance, exit widths, fire ratings | 70 | ✅ Seeded |
| **Feng Shui** | Classical Form & Compass Schools | Orientation, doors, room layout, five elements, water, landscaping | 150 | ✅ Seeded |

**Total: 354 machine-readable rules across 20 files.**

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
├── fengshui/                # Feng Shui — Classical Design Principles
│   ├── orientation_siting.yaml  # Four Animals, lot shape, elevation
│   ├── main_door_entry.yaml     # Qi mouth, Lu Ban ruler, door alignment
│   ├── room_layout.yaml         # Ba Gua sectors, bedroom, kitchen, living
│   ├── five_elements.yaml       # Wu Xing cycles, materials, colors
│   ├── water_wealth.yaml        # Water placement, pools, drains, wealth
│   ├── stairs_corridors.yaml    # Circulation, stair design, corridors
│   ├── building_shape.yaml      # Plan shape, roof form, proportion
│   ├── commercial_office.yaml   # Office, retail, restaurant design
│   └── landscaping_exterior.yaml # Trees, paths, fences, lighting
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

- Code: `NBCP`, `BP344`, `FC` (Fire Code), `FS` (Feng Shui)
- Rule: Roman numeral or section (e.g., `VIII`, `IRR`, `SITE`, `DOOR`, `ROOM`, `ELEM`, `WATER`, `STAIR`, `SHAPE`, `COMM`, `LAND`)
- Type: `S` (setback/siting), `H` (height), `A` (area), `R` (ratio/room), `D` (dimension/door), `L` (load/landscape), `T` (time/distance), `W` (water), `E` (element), `C` (circulation), `F` (form), `B` (business)
- Number: Sequential 3-digit (e.g., `001`)

### Feng Shui as Architectural Data

The Feng Shui rules are encoded using the same schema as legal building codes, making them queryable alongside compliance data. They are clearly marked as traditional design philosophy — not legal requirements. This allows architects and AI tools to run a single query that returns both code compliance results and Feng Shui design recommendations.

**Example:** "Is my south-facing door compliant?" returns:
- `NBCP-VIII-S001`: Front setback 4.5m — PASS (legal)
- `FS-SITE-S010`: South facing preferred for prosperity — PASS (Feng Shui)
- `FS-DOOR-D010`: Check front-to-back door alignment — CHECK (Feng Shui)

## Disclaimer

This repository is an **unofficial digitization** of Philippine building codes for educational and tooling purposes. It is NOT a substitute for the official legal texts published by DPWH and BFP. Always verify against the current official IRR before making compliance decisions.

**Official sources:**
- [DPWH — PD 1096 IRR](https://www.dpwh.gov.ph/dpwh/references/laws_codes_orders/PD1096)
- [DPWH — BP 344 IRR](https://www.dpwh.gov.ph/dpwh/references/laws_codes_orders/bpb344)
- [BFP — RA 9514 RIRR 2019](https://bfp.gov.ph/wp-content/uploads/2019/10/RA9514-RIRR-rev-2019.pdf)

## License

MIT — see [LICENSE](LICENSE).
