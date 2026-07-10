# Dataset Catalog

Welcome to the StellarDataLab dataset catalog! This page lists all available datasets.

## Status: Phase 1 - Foundation (MVP)

The following datasets are available:

### 📊 Stellar Transactions 2024

**Status**: Planned (Phase 3)

- **Description**: Complete set of transactions on Stellar mainnet during 2024
- **Source**: Stellar Horizon API
- **Format**: CSV
- **Rows**: ~1,000,000 (estimated)
- **Columns**: tx_id, timestamp, sender, receiver, amount, operation_type
- **Schema**: [transaction.schema.json](schemas/transaction.schema.json)
- **Use Cases**: Network monitoring, activity analysis, fraud detection

### 👥 Wallet Snapshot

**Status**: Planned (Phase 4)

- **Description**: Snapshot of active Stellar accounts with metadata
- **Source**: Stellar Horizon API
- **Format**: CSV
- **Rows**: ~500,000 (estimated)
- **Columns**: account, created_date, balance, signer_count, updated_date
- **Schema**: [wallet.schema.json](schemas/wallet.schema.json)
- **Use Cases**: Network statistics, account profiling, ecosystem health

### 🔧 Operation Types Reference

**Status**: Available (Phase 5)

- **Description**: Reference data for Stellar operation types
- **Format**: JSON
- **Rows**: 13 (all Stellar operations)
- **Columns**: operation_type, code, description, example
- **Schema**: [operation_types.schema.json](schemas/operation_types.schema.json)
- **Use Cases**: Classification, labeling, documentation

---

## Accessing Datasets

### From This Repository

Clone and browse datasets:

```bash
git clone https://github.com/johnsaviour56-ship-it/StellarDataLab.git
cd stellar-data-lab
ls datasets/curated/
```

### From GitHub Releases

Download versioned datasets:

```bash
# Get v1.0.0
wget https://github.com/johnsaviour56-ship-it/StellarDataLab/releases/download/v1.0.0/datasets.tar.gz
tar -xzf datasets.tar.gz
```

### Using Python

```python
import pandas as pd

# Load transaction dataset
transactions = pd.read_csv("datasets/curated/transactions_2024_labeled.csv")

# Load wallet dataset
wallets = pd.read_csv("datasets/curated/wallets_snapshot_curated.csv")

# Load reference data
import json
with open("datasets/curated/operation_types.json") as f:
    operations = json.load(f)
```

---

## Phase Roadmap

### Phase 1: Foundation (Current)
- ✓ Repository structure
- ✓ Pipeline infrastructure
- ⏳ Transaction dataset
- ⏳ Wallet snapshot
- ⏳ Reference data

### Phase 2: Expanded Coverage
- Swap activities (DEX volumes)
- Anchor/token issuance data
- Network peer connectivity
- Liquidity pool analytics

### Phase 3: Wallet Classification
- Labeled training dataset
- Labels: exchange, dapp, personal, bot, unknown
- Baseline model performance

### Phase 4: Fraud Detection
- Suspicious transactions
- Labels: wash_trading, normal, unknown

### Phase 5: Sybil Detection
- Account clusters
- Community-labeled annotations

### Phase 6: ML Benchmarks
- Standardized train/val/test splits
- Baseline model results
- Evaluation metrics

---

## Data Quality

All curated datasets have been:

- ✓ Validated against JSON Schema
- ✓ Checked for integrity (duplicates, nulls)
- ✓ Tested for semantic correctness
- ✓ Analyzed for quality metrics
- ✓ Documented with complete metadata

See individual metadata files in `datasets/metadata/` for quality reports.

---

## Contributing

Want to add a dataset? See [CONTRIBUTING.md](CONTRIBUTING.md) for a step-by-step guide.

---

## Citation

If you use StellarDataLab datasets in your research, please cite:

```bibtex
@software{stellardatalab2024,
  title={StellarDataLab: Open-source Research and Data Repository for the Stellar Ecosystem},
  author={StellarDataLab Contributors},
  year={2024},
  url={https://github.com/johnsaviour56-ship-it/StellarDataLab}
}
```

For specific datasets, cite the dataset version and date:

```bibtex
@dataset{stellardatalab_transactions_2024_v1,
  title={Stellar Transactions 2024},
  author={StellarDataLab Contributors},
  year={2024},
  version={1.0},
  url={https://github.com/johnsaviour56-ship-it/StellarDataLab/releases}
}
```

---

**Last updated**: January 2024

**Questions?** Open an [issue](https://github.com/johnsaviour56-ship-it/StellarDataLab/issues) or [discussion](https://github.com/johnsaviour56-ship-it/StellarDataLab/discussions).
