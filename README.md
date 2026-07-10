# StellarDataLab

**Open-source research and data repository for the Stellar ecosystem.**

StellarDataLab collects, curates, labels, validates, and publishes datasets for blockchain research, ecosystem analytics, fraud detection, network monitoring, and machine-learning applications.

## Project Vision

The Stellar ecosystem generates rich, complex data across transactions, accounts, operations, and network activity. StellarDataLab makes this data accessible, reproducible, and research-grade by:

- **Collecting** data from Stellar Horizon API and other sources
- **Curating** raw data through normalization and deduplication
- **Validating** datasets against schemas and semantic rules
- **Labeling** transactions and accounts for ML training
- **Publishing** immutable, versioned datasets on GitHub

All data flows through a Python pipeline, stored in Git as CSV/JSON, and validated by GitHub Actions. No databases, no cloud infrastructure—just simple, reproducible data workflows.

## Quick Start

### Prerequisites
- Python 3.10+
- Git

### Setup (5 minutes)

```bash
# Clone the repository
git clone https://github.com/johnsaviour56-ship-it/StellarDataLab.git
cd StellarDataLab

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pytest tests/ -q
```

### Run the Pipeline

```bash
# Validate all datasets
python -m pipeline.orchestrator validate

# Process datasets (collect → transform → validate → export)
python -m pipeline.orchestrator process

# Generate dataset registry
python -m pipeline.exporters generate_registry
```

## Dataset Catalog

### Phase 1 (MVP) Datasets

| Dataset | Description | Rows | Format | Version |
|---------|-------------|------|--------|---------|
| **Stellar Transactions 2024** | All transactions from Stellar mainnet | 1M+ | CSV | 1.0 |
| **Wallet Snapshot** | Active accounts with metadata | 500K+ | CSV | 1.0 |
| **Operation Types** | Stellar operation reference data | 13 | JSON | 1.0 |

### Roadmap

- **Phase 2**: Expanded dataset coverage (swaps, anchors, liquidity pools)
- **Phase 3**: Wallet classification research (exchange, dapp, bot, personal)
- **Phase 4**: Wash-trading detection research
- **Phase 5**: Sybil detection datasets
- **Phase 6**: ML benchmark datasets

See [ROADMAP.md](#) for detailed roadmap.

## Core Components

### Data Pipeline

```
Raw Data → Collection → Transformation → Validation → Curation → Export
```

- **Collections** (`scripts/`): Fetch data from APIs and files
- **Pipeline** (`pipeline/`): Orchestrate collection, transformation, validation
- **Schemas** (`schemas/`): JSON Schema definitions for all datasets
- **Metadata** (`datasets/metadata/`): YAML documentation of datasets
- **Validation**: Schema, integrity, semantic, and quality checks
- **Labeling**: YAML-based classification rules

### GitHub Actions CI/CD

- **Validate on Push**: Run schema and integrity checks on every push
- **Publish Release**: Generate dataset registry and tag releases
- **Code Quality**: Lint, format, and test all code

## Documentation

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to add a new dataset (30-minute guide)
- **[RESEARCH.md](RESEARCH.md)** - Reproducibility and research standards
- **[docs/pipeline-guide.md](docs/pipeline-guide.md)** - Pipeline architecture
- **[docs/schema-guide.md](docs/schema-guide.md)** - JSON Schema basics
- **[docs/validation-guide.md](docs/validation-guide.md)** - Validation layers
- **[docs/labeling-guide.md](docs/labeling-guide.md)** - Labeling framework

## Project Structure

```
StellarDataLab/
├── pipeline/              # Core Python pipeline
│   ├── __init__.py
│   ├── orchestrator.py    # Main orchestration
│   ├── collectors.py      # Data collection interface
│   ├── transformers.py    # Data transformations
│   ├── validators.py      # Schema & validation
│   └── exporters.py       # Export to CSV/JSON
├── schemas/               # JSON Schema definitions
│   ├── transaction.schema.json
│   ├── wallet.schema.json
│   └── operation_types.schema.json
├── datasets/
│   ├── raw/               # Original unmodified data
│   ├── curated/           # Processed, validated data
│   ├── metadata/          # Dataset metadata (YAML)
│   └── CATALOG.md         # Dataset registry
├── scripts/               # Collection scripts
│   ├── collect_transactions.py
│   ├── collect_wallets.py
│   └── ...
├── tests/                 # Unit & integration tests
│   ├── test_validators.py
│   ├── test_transformers.py
│   ├── test_collectors.py
│   └── fixtures/          # Test data
├── docs/                  # Documentation
│   ├── pipeline-guide.md
│   ├── schema-guide.md
│   ├── validation-guide.md
│   └── labeling-guide.md
└── .github/workflows/     # GitHub Actions CI/CD
    ├── validate-datasets.yml
    ├── publish-release.yml
    └── check-quality.yml
```

## For Contributors

Want to add a new dataset? See [CONTRIBUTING.md](CONTRIBUTING.md) for a step-by-step guide.

Key files to understand:

1. **How data flows**: [docs/pipeline-guide.md](docs/pipeline-guide.md)
2. **Dataset schemas**: [docs/schema-guide.md](docs/schema-guide.md)
3. **Validation rules**: [docs/validation-guide.md](docs/validation-guide.md)
4. **Labeling**: [docs/labeling-guide.md](docs/labeling-guide.md)

## Research & Reproducibility

All datasets include:

- **JSON Schema** for machine-readable validation
- **YAML Metadata** documenting source, methodology, and lineage
- **Version tags** for immutable dataset versions
- **Collection scripts** for reproducibility

See [RESEARCH.md](RESEARCH.md) for research standards and reproducibility principles.

## Data Access

### GitHub Releases

Datasets are published on [GitHub Releases](https://github.com/johnsaviour56-ship-it/StellarDataLab/releases) with version tags:

```bash
# Download a specific version
wget https://github.com/johnsaviour56-ship-it/StellarDataLab/releases/download/v1.0.0/datasets.tar.gz
tar -xzf datasets.tar.gz
```

### From Git

Datasets are committed to this repository:

```bash
# Clone and access curated datasets
git clone https://github.com/johnsaviour56-ship-it/StellarDataLab.git
cd StellarDataLab/datasets/curated/
```

## Dependencies

**Core**:
- pandas >= 2.0
- pydantic >= 2.0
- jsonschema >= 4.20
- pyyaml >= 6.0
- requests >= 2.31

**Development**:
- pytest >= 7.4
- pytest-cov >= 4.1
- black >= 23.11
- flake8 >= 6.1

See [pyproject.toml](pyproject.toml) for complete list.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

All datasets are released under [CC0 1.0 Universal (Public Domain)](https://creativecommons.org/publicdomain/zero/1.0/), unless otherwise specified.

## Citation

If you use StellarDataLab datasets in your research, please cite:

```bibtex
@software{stellardatalab2024,
  title={StellarDataLab: Open-source Research and Data Repository for the Stellar Ecosystem},
  author={StellarDataLab Contributors},
  year={2024},
  url={https://github.com/stellar/stellar-data-lab}
}
```

## Community

- **Questions?** Open an [Issue](https://github.com/johnsaviour56-ship-it/StellarDataLab/issues)
- **Ideas?** Start a [Discussion](https://github.com/johnsaviour56-ship-it/StellarDataLab/discussions)
- **Contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

For issues, questions, or contributions:

1. Check [existing issues](https://github.com/johnsaviour56-ship-it/StellarDataLab/issues)
2. Read the [documentation](docs/)
3. Open a new [issue](https://github.com/johnsaviour56-ship-it/StellarDataLab/issues/new)

---

**Made by the Stellar community, for the Stellar community.** 🌟
