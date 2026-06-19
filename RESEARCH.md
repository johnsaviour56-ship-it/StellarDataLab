# Research Methodology & Reproducibility

StellarDataLab is committed to research integrity, reproducibility, and transparency. This guide documents the standards all datasets must meet.

## Core Principles

Every dataset in StellarDataLab must be:

1. **Reproducible**: Collection method is documented and repeatable
2. **Transparent**: Data lineage and transformations are fully documented
3. **Auditable**: Git history shows what changed and why
4. **Versioned**: Each release is immutable and citable
5. **Quality-Assured**: Data passes validation and quality checks
6. **Ethically Sound**: Privacy, security, and ecosystem impact considered

## Documenting Methodology

### Metadata Requirements

Every dataset must have a complete metadata file (`datasets/metadata/{name}.metadata.yml`) documenting:

```yaml
name: "Dataset Name"
version: "1.0"
created_date: "2024-01-15"

description: |
  Clear explanation of what this dataset contains.
  Why is it useful for research?
  What questions does it help answer?

source:
  type: "stellar_api"  # or csv, json, github, other
  endpoint: "https://horizon.stellar.org"
  documentation: "https://developers.stellar.org/api/"
  
collection:
  method: "Describe the collection process"
  script: "scripts/collect_transactions.py"
  frequency: "daily"
  date_range: "2024-01-01 to 2024-12-31"
  
  # How to reproduce collection
  reproduce: |
    1. Run: python scripts/collect_transactions.py
    2. Output written to: datasets/raw/transactions_2024_raw.csv
    3. Expected row count: ~1M rows
    
  # How errors are handled
  error_handling: |
    - API timeouts: Retry 3x with exponential backoff
    - Invalid records: Log and skip
    - Rate limits: Pause and retry
    
transformations:
  - name: "address_normalization"
    description: "Convert addresses to lowercase"
    applied: true
  
  - name: "deduplication"
    description: "Remove duplicate transactions by tx_id"
    rows_removed: 1234
    applied: true

schema:
  file: "schemas/transaction.schema.json"
  version: "1.0"

quality_metrics:
  row_count: 1000000
  null_percentage: 0.01
  duplicate_count: 0
  
  columns:
    tx_id:
      distinct: 1000000
      nulls: 0
    sender:
      distinct: 250000
      nulls: 0
      sample_values: ["GABCD...", "GXYZ..."]

# Data lineage
lineage:
  source: "Stellar Horizon API"
  collection_date: "2024-01-15"
  transformation_date: "2024-01-15"
  parent_dataset: null  # If derived from another dataset
  
# Versioning
versions:
  - "1.0": "Initial release"

# Access
license: "CC0 1.0 Universal (Public Domain)"
citation: |
  @dataset{stellardatalab2024,
    title={Stellar Transactions 2024},
    author={StellarDataLab Contributors},
    year={2024},
    doi={TBD}
  }

# Research
research_tags:
  - "transactions"
  - "network-analytics"
  - "activity-classification"

related_papers: []
related_datasets: []
```

## Statistical Validation

All datasets must report these statistics:

- **Row count**: Total number of records
- **Null percentages**: For each column
- **Value ranges**: Min, max, mean, std dev for numeric columns
- **Distinct values**: Unique count for categorical columns
- **Class distribution**: For labeled datasets
- **Temporal coverage**: Date range and any gaps

Example quality report:

```yaml
quality_report:
  timestamp: "2024-01-15T12:00:00Z"
  
  rows: 1000000
  columns: 6
  memory_mb: 450
  
  nulls:
    tx_id: 0
    timestamp: 0
    sender: 0
    receiver: 0
    amount: 0
    type: 0
  
  numeric_columns:
    amount:
      min: 0.0001
      max: 999999999
      mean: 1000.5
      std: 5000.2
  
  categorical_columns:
    type:
      distinct: 13
      distribution:
        payment: 0.70
        swap: 0.15
        create_account: 0.10
        other: 0.05
  
  temporal:
    start: "2024-01-01T00:00:00Z"
    end: "2024-12-31T23:59:59Z"
    gaps: []
```

## Labeling Methodology

For labeled datasets, document the labeling process:

```yaml
labels:
  - column_name: "transaction_type"
    values: ["payment", "swap", "create_account", "other"]
    
    methodology: |
      Classification based on Stellar operation types.
      Operation types mapped to transaction types.
      See: https://developers.stellar.org/docs/learn/building-blocks/operations
    
    confidence:
      high: "0.95+"
      medium: "0.70-0.94"
      low: "< 0.70"
    
    rules:
      - condition: "operation_type = 1"
        value: "payment"
        confidence: "high"
        reasoning: "Direct operation type mapping"
    
    human_review:
      method: "Random sample of 5% verified by domain expert"
      reviewed_count: 50000
      agreement: 0.98
      disagreements: []
    
    validation:
      precision: 0.98
      recall: 0.97
      f1_score: 0.975
```

## Handling Sensitive Data

### Privacy Guidelines

- **No PII**: Don't include personal identifying information (names, emails, phone numbers)
- **Anonymization**: If data contains potentially sensitive info, aggregate or anonymize
- **Compliance**: Ensure compliance with applicable data protection laws (GDPR, CCPA, etc.)

### Data Subject Rights

If dataset includes user data:
- Document how individuals can request access/deletion
- Provide contact information
- Explain data retention policy

Example:
```yaml
privacy:
  pii_included: false
  aggregation_level: "transaction-level"
  anonymization: "Stellar addresses are pseudonymous identifiers"
  
  data_subject_rights:
    note: "This dataset contains pseudonymous blockchain addresses."
    contact: "research@stellardatalab.org"
```

## Benchmarking (ML Datasets)

For datasets designed for ML training:

```yaml
benchmarks:
  purpose: "Train models for transaction classification"
  
  data_splits:
    train: 0.70
    validation: 0.15
    test: 0.15
    
    method: "Random stratified split"
    seed: 42  # For reproducibility
  
  baseline_model:
    name: "Logistic Regression"
    features: ["amount", "sender_age", "type"]
    
    performance:
      accuracy: 0.92
      precision: 0.89
      recall: 0.91
      f1_score: 0.90
  
  class_imbalance:
    method: "Measured with max_class_ratio"
    max_ratio: 1.5
    distribution:
      class_0: 0.65
      class_1: 0.35
```

## Dataset Versioning

Use semantic versioning for datasets:

- **MAJOR** (1.0): Breaking changes (schema change, major reprocessing)
- **MINOR** (1.1): New features (new columns, new labels)
- **PATCH** (1.1.1): Bug fixes (data corrections, quality improvements)

Example version progression:
```yaml
versions:
  "1.0.0": "Initial release with transactions 2024"
  "1.1.0": "Added classification labels"
  "1.1.1": "Fixed 100 corrupted records in May data"
  "2.0.0": "Changed schema to include new fields"
```

Release each version on GitHub and document changes:

```markdown
# v1.1.0 - Transaction Classification

**Release Date**: 2024-02-15

## Changes

- Added `transaction_classification` column
- Classification based on operation types
- 98% human validation accuracy

## Download

- `transactions_2024_v1.1.0.csv` (450 MB)

## Schema

See `schemas/transaction.schema.json` for updated field definitions.
```

## Reproducibility Checklist

Before publishing a dataset, verify:

- [ ] Collection script is deterministic (same input → same output)
- [ ] Data source and method documented
- [ ] Transformation steps documented
- [ ] Validation rules documented
- [ ] Quality metrics reported
- [ ] Metadata file complete
- [ ] Schema is valid JSON
- [ ] No secrets or credentials in code
- [ ] Tests pass
- [ ] Git history shows clear evolution
- [ ] License is appropriate
- [ ] Citation format provided

## Research Integrity

### Conflict of Interest

Document any conflicts:
```yaml
conflicts_of_interest: |
  Maintainer works for Company X which may be affected by this data.
  This is disclosed for transparency.
```

### Funding & Attribution

```yaml
funding: "Funded by Drips Network"
acknowledgments: |
  Thanks to X for feedback on methodology.
  Thanks to Y for data validation.
```

### Limitations

Document known limitations:
```yaml
limitations: |
  - Data is pseudonymous, not anonymous
  - Does not include off-chain transactions
  - Stellar API has rate limits affecting collection timing
  - See methodology for detailed limitations
```

## Publishing Guidelines

When publishing a dataset:

1. **Validate** - Run full validation suite
2. **Document** - Complete all metadata fields
3. **Review** - Have another contributor review
4. **Tag** - Create Git tag for version
5. **Release** - Package and upload to GitHub Releases
6. **Announce** - Post about release (optional)

## Ethical Considerations

### Impact on Ecosystem

Before publishing, consider:

- Could this data enable ecosystem harm?
- Could this data compromise user privacy?
- Are there sufficient safeguards in place?

Example:
```yaml
ethical_review:
  potential_harms: |
    - Data could be used to track whale transactions
    - Mitigation: Data is public and already available on blockchain
  
  privacy_impact: |
    - Dataset contains pseudonymous addresses
    - No personal information included
  
  ecosystem_impact: |
    - Positive: Enables research and fraud detection
    - Potential negative: Could be misused for surveillance
```

---

**By following these standards, we ensure StellarDataLab datasets are research-grade, reproducible, and trustworthy.**

Questions? Open an issue or discussion!
