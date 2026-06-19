# Datasets

This directory contains all StellarDataLab datasets organized into three categories:

## Structure

- **`raw/`** - Original, unmodified data from sources (CSV, JSON)
- **`curated/`** - Processed, validated, and labeled datasets ready for research
- **`metadata/`** - YAML metadata files documenting each dataset

## Dataset Organization

Each dataset follows a naming convention:

- `datasets/raw/{dataset_name}_raw.{format}` - Raw data
- `datasets/curated/{dataset_name}_curated.{format}` or `{dataset_name}_labeled.{format}` - Processed data
- `datasets/metadata/{dataset_name}.metadata.yml` - Metadata documentation

## Catalog

See `CATALOG.md` for a complete searchable catalog of all datasets.

## Adding a New Dataset

1. Create metadata file: `datasets/metadata/my_dataset.metadata.yml`
2. Define schema: `schemas/my_dataset.schema.json`
3. Write collection script: `scripts/collect_my_dataset.py`
4. Run collection and processing through the pipeline
5. Export curated data to `datasets/curated/`

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed instructions.

## Data Quality

All curated datasets have been:

- ✓ Validated against JSON Schema
- ✓ Checked for integrity (duplicates, nulls)
- ✓ Tested for semantic correctness
- ✓ Analyzed for quality metrics

See individual metadata files for quality reports.

## Access

Download datasets from:
- This repository (via Git)
- [GitHub Releases](https://github.com/stellar/stellar-data-lab/releases) (versioned downloads)
