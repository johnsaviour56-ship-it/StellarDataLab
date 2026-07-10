# Quick Start Guide

Get StellarDataLab running in 5 minutes.

## Prerequisites

- Python 3.10 or later
- Git
- 500 MB disk space

## Installation

```bash
# 1. Clone repository
git clone https://github.com/johnsaviour56-ship-it/StellarDataLab.git
cd StellarDataLab

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run tests to verify setup
pytest tests/ -v
```

**Done!** ✓ You're ready to use StellarDataLab.

---

## Basic Usage

### Use the Pipeline

```python
from pipeline import (
    validate_schema,
    normalize_addresses,
    deduplicate,
    export_to_csv,
)
import pandas as pd
import json

# Load data
data = pd.read_csv("datasets/raw/transactions.csv")

# Normalize addresses
data = normalize_addresses(data, ["sender", "receiver"])

# Remove duplicates
data = deduplicate(data, key=["tx_id"])

# Validate against schema
with open("schemas/transaction.schema.json") as f:
    schema = json.load(f)

from pipeline.validators import validate_dataframe_schema
result = validate_dataframe_schema(data, schema)

if result.is_valid:
    # Export to curated
    export_to_csv(data, "datasets/curated/transactions_curated.csv")
    print(f"✓ Exported {len(data)} rows")
else:
    print(f"✗ Validation failed: {result.errors}")
```

### Run the Orchestrator

```python
from pipeline import orchestrate_pipeline

# Process all configured datasets
results = orchestrate_pipeline("config.yml")
print(f"Success: {results['succeeded']}/{results['total']}")
```

---

## Next Steps

1. **Learn the Architecture**: Read [docs/pipeline-guide.md](docs/pipeline-guide.md)
2. **Add a Dataset**: Follow [CONTRIBUTING.md](CONTRIBUTING.md)
3. **Understand Methodology**: Read [RESEARCH.md](RESEARCH.md)
4. **Explore Code**: Start with `pipeline/__init__.py`

---

## Key Files

| File | Purpose |
|------|---------|
| `pipeline/` | Core pipeline modules |
| `datasets/` | Data storage (raw, curated, metadata) |
| `schemas/` | JSON Schema definitions |
| `tests/` | Unit and integration tests |
| `docs/` | Detailed documentation |
| `scripts/` | Data collection scripts |
| `README.md` | Project overview |
| `CONTRIBUTING.md` | How to contribute |

---

## Troubleshooting

**Import errors?**
```bash
# Ensure venv is activated
# Then reinstall
pip install -r requirements.txt
```

**Tests failing?**
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run tests
pytest tests/ -v
```

**Want to add a dataset?**
See [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step guide.

---

## Get Help

- **Read the docs**: [docs/](docs/)
- **Open an issue**: https://github.com/johnsaviour56-ship-it/StellarDataLab/issues
- **Start a discussion**: https://github.com/johnsaviour56-ship-it/StellarDataLab/discussions

---

**Ready to dive deeper?** Read the full [README.md](README.md).
