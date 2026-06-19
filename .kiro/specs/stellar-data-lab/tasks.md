# Tasks: StellarDataLab Implementation

## Overview

This document breaks the requirements into concrete, implementable tasks organized by phase. Each task is:
- Assignable to a single developer
- Has clear acceptance criteria
- Estimates effort (Small/Medium/Large = 1-2 hours / 3-6 hours / 1-2 days)
- Lists dependencies

**Total Effort**: ~2-3 weeks for single maintainer

---

## Phase 1: Foundation & Setup

### 1.1 Initialize Repository Structure
**Effort**: Small  
**Dependencies**: None  
**Description**: Create all directories and initial README.

**Acceptance Criteria**:
- [ ] All directories exist: `pipeline/`, `schemas/`, `datasets/{raw,curated,metadata}/`, `scripts/`, `tests/fixtures/`, `docs/`, `.github/workflows/`
- [ ] `.gitignore` created with Python exclusions
- [ ] `LICENSE` file added (MIT)
- [ ] Initial README.md created (template)
- [ ] `pyproject.toml` created with project metadata
- [ ] `requirements.txt` with Python dependencies listed

### 1.2 Set Up Python Project
**Effort**: Small  
**Dependencies**: 1.1  
**Description**: Configure Python package and dependencies.

**Acceptance Criteria**:
- [ ] `python -m venv venv` works
- [ ] `pip install -r requirements.txt` succeeds
- [ ] Python version specified (3.10+)
- [ ] `pipeline/` is importable as package (`__init__.py` created)
- [ ] All core modules can be imported

### 1.3 Configure GitHub
**Effort**: Small  
**Dependencies**: None  
**Description**: Set up repository settings on GitHub.

**Acceptance Criteria**:
- [ ] Branch protection enabled on `main` (require reviews, CI checks)
- [ ] Issues enabled
- [ ] Discussions enabled
- [ ] CODEOWNERS file created
- [ ] Repository description updated

### 1.4 Set Up Testing Infrastructure
**Effort**: Small  
**Dependencies**: 1.2  
**Description**: Configure pytest and create fixture framework.

**Acceptance Criteria**:
- [ ] `pytest.ini` created
- [ ] `conftest.py` created in tests/
- [ ] Test fixtures directory structure: `tests/fixtures/`
- [ ] Sample fixture files created (valid/invalid transaction, wallet JSON examples)
- [ ] `pytest tests/ -v` runs without errors (even if no tests yet)

---

## Phase 1.5: Core Pipeline Modules

### 1.5.1 Implement Schema Validator
**Effort**: Medium  
**Dependencies**: 1.2  
**Description**: Implement `pipeline/validators.py` with schema and integrity checking.

**Acceptance Criteria**:
- [ ] `validators.py` module created
- [ ] `validate_schema(row, schema_obj)` function implemented (uses jsonschema)
- [ ] `check_integrity(data, rules)` function checks duplicates and nulls
- [ ] `validate_semantic_rules(data, rules)` function evaluates custom rules
- [ ] `compute_quality_metrics(data)` returns statistics
- [ ] Unit tests in `test_validators.py` with 80%+ coverage
- [ ] All validator functions have docstrings with examples

### 1.5.2 Implement Transformers
**Effort**: Medium  
**Dependencies**: 1.2  
**Description**: Implement `pipeline/transformers.py` with normalization and transformation.

**Acceptance Criteria**:
- [ ] `transformers.py` module created
- [ ] `normalize_addresses(data)` - lowercase and validate addresses
- [ ] `normalize_timestamps(data)` - ISO 8601 format and temporal components
- [ ] `deduplicate(data, key)` - remove duplicates by key
- [ ] `apply_labels(data, labeling_config)` - apply labeling rules
- [ ] Unit tests in `test_transformers.py` with 80%+ coverage
- [ ] All transformer functions have docstrings

### 1.5.3 Implement Collectors Interface
**Effort**: Small  
**Dependencies**: 1.2  
**Description**: Implement `pipeline/collectors.py` with collection script framework.

**Acceptance Criteria**:
- [ ] `collectors.py` module created
- [ ] `run_collection_script(script_name, config)` function
- [ ] Error handling and retry logic (exponential backoff)
- [ ] Logging of collection progress
- [ ] Unit tests in `test_collectors.py`
- [ ] Docstring documenting expected collection script interface

### 1.5.4 Implement Exporters
**Effort**: Small  
**Dependencies**: 1.2  
**Description**: Implement `pipeline/exporters.py` with export formats.

**Acceptance Criteria**:
- [ ] `exporters.py` module created
- [ ] `export_to_csv(data, filepath)` function
- [ ] `export_to_json(data, filepath)` function (line-delimited JSON)
- [ ] `generate_registry(datasets_dir)` function
- [ ] Unit tests in `test_exporters.py`
- [ ] All exports are deterministic

### 1.5.5 Implement Orchestrator
**Effort**: Medium  
**Dependencies**: 1.5.1, 1.5.2, 1.5.3, 1.5.4  
**Description**: Implement `pipeline/orchestrator.py` to orchestrate full pipeline.

**Acceptance Criteria**:
- [ ] `orchestrator.py` module created
- [ ] `orchestrate_pipeline(config_file)` function (main entry point)
- [ ] Orchestrator loads dataset definitions from YAML config
- [ ] Orchestrator runs all phases: collect → transform → validate → export
- [ ] Orchestrator logs progress and errors
- [ ] Integration tests in `test_integration.py` with test datasets
- [ ] Orchestrator handles errors gracefully (report and continue)

---

## Phase 2: Dataset Infrastructure

### 2.1 Create JSON Schemas
**Effort**: Medium  
**Dependencies**: 1.2  
**Description**: Define schemas for all MVP datasets.

**Acceptance Criteria**:
- [ ] `schemas/transaction.schema.json` - valid JSON Schema Draft 7
  - Required: tx_id (64-char hex), timestamp (ISO 8601), sender/receiver (Stellar address), amount (positive number), operation_type
- [ ] `schemas/wallet.schema.json` - valid JSON Schema Draft 7
  - Required: account (Stellar address), created_date, balance (non-negative), signer_count, updated_date
- [ ] `schemas/operation_types.schema.json` - valid JSON Schema Draft 7
  - Required: operation_type, code (integer), description, example
- [ ] All schemas validate with jsonschema library
- [ ] All schemas include descriptions and examples

### 2.2 Create Metadata Templates
**Effort**: Small  
**Dependencies**: 2.1  
**Description**: Create metadata template file for documentation.

**Acceptance Criteria**:
- [ ] `docs/metadata-template.yml` created
- [ ] Template includes all required sections: name, source, collection, schema, transformations, quality_checks, labels
- [ ] Template includes comments explaining each section
- [ ] Template is copied into CONTRIBUTING guide

### 2.3 Implement Validation Rules Configuration
**Effort**: Small  
**Dependencies**: 1.5.1  
**Description**: Create YAML validation rules structure.

**Acceptance Criteria**:
- [ ] Validation rules can be loaded from YAML (in metadata files)
- [ ] Rules include: schema file, duplicate keys, required fields, semantic rules, quality thresholds
- [ ] Rules are documented with examples
- [ ] Validators load rules from YAML at runtime

### 2.4 Implement Labeling Configuration
**Effort**: Small  
**Dependencies**: 1.5.2  
**Description**: Create YAML labeling rules structure.

**Acceptance Criteria**:
- [ ] Labeling rules can be defined in YAML (in metadata files)
- [ ] Rules include: column name, values, rule conditions, confidence, reasoning
- [ ] Labels are evaluated in order (first match wins)
- [ ] Default label applied to unmatched rows
- [ ] Label distribution is logged (value counts)

---

## Phase 3: Transaction Dataset

### 3.1 Implement Transaction Collection Script
**Effort**: Medium  
**Dependencies**: 1.5.3, 2.1  
**Description**: Implement `scripts/collect_transactions.py` to fetch from Stellar API.

**Acceptance Criteria**:
- [ ] Script accepts date_range parameter
- [ ] Fetches transactions from Stellar Horizon API
- [ ] Handles pagination (100 per page limit)
- [ ] Retry logic: 3 attempts with exponential backoff
- [ ] Logs count of transactions collected
- [ ] Writes to `datasets/raw/transactions_YYYY_raw.csv`
- [ ] CSV has columns: tx_id, timestamp, sender, receiver, amount, operation_type
- [ ] Script runs without errors: `python scripts/collect_transactions.py`
- [ ] Handles API errors gracefully (log and skip failed dates)

### 3.2 Create Transaction Metadata
**Effort**: Small  
**Dependencies**: 3.1, 2.2  
**Description**: Create `datasets/metadata/transactions_2024.metadata.yml`.

**Acceptance Criteria**:
- [ ] Metadata file exists with all required fields
- [ ] Documents source: Stellar Horizon API, date range 2024-01-01 to 2024-12-31
- [ ] Documents collection method: daily pagination
- [ ] Documents schema file reference
- [ ] Documents transformations: address normalization, timestamp normalization, deduplication
- [ ] Documents quality checks: no duplicates by tx_id, no nulls in required fields
- [ ] Documents expected row count, data size

### 3.3 Run Transaction Collection
**Effort**: Medium  
**Dependencies**: 3.1  
**Description**: Execute collection script to download transaction data.

**Acceptance Criteria**:
- [ ] `python scripts/collect_transactions.py` runs to completion
- [ ] `datasets/raw/transactions_2024_raw.csv` created
- [ ] CSV has reasonable row count (>1000 transactions)
- [ ] All rows have required columns
- [ ] Collection logs show progress and completion

### 3.4 Test Transaction Collection Script
**Effort**: Small  
**Dependencies**: 3.3  
**Description**: Write tests for collection script.

**Acceptance Criteria**:
- [ ] `test_collectors.py` has test for `collect_transactions()`
- [ ] Test uses mock API responses
- [ ] Test verifies output CSV format
- [ ] Test verifies error handling (API timeout, malformed response)
- [ ] All tests pass

### 3.5 Process Transaction Dataset
**Effort**: Medium  
**Dependencies**: 3.3, 1.5.1, 1.5.2  
**Description**: Apply transformations and validation to transactions.

**Acceptance Criteria**:
- [ ] Run orchestrator on transaction dataset (or run transformers directly)
- [ ] Transformations applied: address normalization, timestamp normalization, deduplication
- [ ] Validation run against schema
- [ ] Output written to `datasets/curated/transactions_2024_labeled.csv`
- [ ] Validation report generated
- [ ] All rows pass schema validation
- [ ] Row count after dedup logged
- [ ] Metadata updated with row counts and quality metrics

---

## Phase 4: Wallet Dataset

### 4.1 Implement Wallet Collection Script
**Effort**: Medium  
**Dependencies**: 1.5.3, 2.1  
**Description**: Implement `scripts/collect_wallets.py` to fetch wallet snapshot.

**Acceptance Criteria**:
- [ ] Script fetches all active accounts from Stellar API
- [ ] Includes: account, created_date, balance, signer_count, updated_date
- [ ] Handles pagination for large result sets
- [ ] Retry logic for failed requests
- [ ] Logs count of accounts collected
- [ ] Writes to `datasets/raw/wallets_snapshot_raw.csv`
- [ ] CSV columns: account, created_date, balance, signer_count, updated_date
- [ ] Script runs without errors: `python scripts/collect_wallets.py`

### 4.2 Create Wallet Metadata
**Effort**: Small  
**Dependencies**: 4.1, 2.2  
**Description**: Create `datasets/metadata/wallets_snapshot.metadata.yml`.

**Acceptance Criteria**:
- [ ] Metadata file exists with all required fields
- [ ] Documents source: Stellar Horizon API full ledger export
- [ ] Documents collection method: enumeration with pagination
- [ ] Documents schema file reference
- [ ] Documents transformations: address normalization, deduplication
- [ ] Documents quality checks: address validation, date range validation

### 4.3 Run Wallet Collection
**Effort**: Medium  
**Dependencies**: 4.1  
**Description**: Execute collection script to download wallet data.

**Acceptance Criteria**:
- [ ] `python scripts/collect_wallets.py` runs to completion
- [ ] `datasets/raw/wallets_snapshot_raw.csv` created
- [ ] CSV has reasonable row count (>100,000 accounts)
- [ ] All rows have required columns
- [ ] Collection logs show progress and completion

### 4.4 Test Wallet Collection Script
**Effort**: Small  
**Dependencies**: 4.3  
**Description**: Write tests for wallet collection script.

**Acceptance Criteria**:
- [ ] `test_collectors.py` has test for `collect_wallets()`
- [ ] Test uses mock API responses
- [ ] Test verifies output CSV format
- [ ] Test verifies error handling
- [ ] All tests pass

### 4.5 Process Wallet Dataset
**Effort**: Medium  
**Dependencies**: 4.3, 1.5.1, 1.5.2  
**Description**: Apply transformations and validation to wallets.

**Acceptance Criteria**:
- [ ] Run orchestrator on wallet dataset
- [ ] Transformations applied: address normalization, deduplication
- [ ] Validation run against schema
- [ ] Output written to `datasets/curated/wallets_snapshot_curated.csv`
- [ ] All rows pass schema validation
- [ ] Row count after dedup logged
- [ ] Metadata updated with row counts and quality metrics

---

## Phase 5: Reference Data

### 5.1 Create Operation Types Reference
**Effort**: Small  
**Dependencies**: 2.1  
**Description**: Curate operation types reference data.

**Acceptance Criteria**:
- [ ] `datasets/curated/operation_types.json` created
- [ ] All 13 Stellar operation types included (Payment, OfferCreate, etc.)
- [ ] Each entry: operation_type (string), code (integer), description, example
- [ ] Valid JSON format
- [ ] Valid against `schemas/operation_types.schema.json`
- [ ] Formatted for readability

### 5.2 Create Operation Types Metadata
**Effort**: Small  
**Dependencies**: 5.1, 2.2  
**Description**: Create metadata for operation types.

**Acceptance Criteria**:
- [ ] `datasets/metadata/operation_types.metadata.yml` created
- [ ] Documents this is static reference data
- [ ] References source: Stellar documentation
- [ ] Documents last updated date and version

---

## Phase 6: CI/CD Pipelines

### 6.1 Create Validate Workflow
**Effort**: Medium  
**Dependencies**: 1.5.1, 1.5.2, 1.5.5  
**Description**: Implement `.github/workflows/validate-datasets.yml`.

**Acceptance Criteria**:
- [ ] Workflow triggered on push to main/develop, changes to datasets/
- [ ] Installs Python and dependencies
- [ ] Runs schema validation on all datasets
- [ ] Runs integrity checks
- [ ] Runs quality checks
- [ ] Generates validation report (JSON artifact)
- [ ] Fails CI if validation fails
- [ ] Succeeds when all checks pass

### 6.2 Create Publish Workflow
**Effort**: Medium  
**Dependencies**: 1.5.4, 1.5.5  
**Description**: Implement `.github/workflows/publish-release.yml`.

**Acceptance Criteria**:
- [ ] Workflow triggered on push to main with git tag (v*)
- [ ] Runs full validation before publishing
- [ ] Generates dataset registry (DATASETS.json)
- [ ] Packages datasets (tar.gz)
- [ ] Creates GitHub Release with artifacts and changelog
- [ ] Release includes version, date, links to datasets

### 6.3 Create Quality Check Workflow
**Effort**: Medium  
**Dependencies**: 1.4  
**Description**: Implement `.github/workflows/check-quality.yml`.

**Acceptance Criteria**:
- [ ] Workflow triggered on push and PR
- [ ] Runs flake8 linting on Python code
- [ ] Runs black formatting check
- [ ] Runs full test suite with coverage report
- [ ] Fails CI if tests fail or coverage < 80%
- [ ] Checks Markdown syntax in documentation

---

## Phase 7: Documentation

### 7.1 Create CONTRIBUTING Guide
**Effort**: Small  
**Dependencies**: 2.2, 3.5, 4.5  
**Description**: Write `CONTRIBUTING.md` for new contributors.

**Acceptance Criteria**:
- [ ] CONTRIBUTING.md exists
- [ ] Quick start: clone, setup venv, install dependencies
- [ ] Step-by-step guide to add new dataset (in 30 minutes)
- [ ] Metadata template (copy-paste starting point)
- [ ] Schema template
- [ ] Collection script template
- [ ] Submission checklist
- [ ] Python code style guidelines (PEP 8, black, flake8)
- [ ] Test writing guidelines

### 7.2 Create RESEARCH Guide
**Effort**: Small  
**Dependencies**: None  
**Description**: Write `RESEARCH.md` for research methodology.

**Acceptance Criteria**:
- [ ] RESEARCH.md exists
- [ ] Reproducibility principles documented
- [ ] How to include methodology in metadata
- [ ] Statistical validation approach
- [ ] Handling sensitive data / privacy considerations
- [ ] Benchmarking guidelines for ML datasets
- [ ] Versioning approach for datasets
- [ ] Examples of well-documented datasets

### 7.3 Create Pipeline Guide
**Effort**: Small  
**Dependencies**: 1.5.5  
**Description**: Write `docs/pipeline-guide.md`.

**Acceptance Criteria**:
- [ ] docs/pipeline-guide.md exists
- [ ] Explains orchestrator, collectors, transformers, validators, exporters
- [ ] Code examples for each component
- [ ] How to add new collection script
- [ ] How to add new transformation
- [ ] Troubleshooting common issues

### 7.4 Create Schema Guide
**Effort**: Small  
**Dependencies**: 2.1  
**Description**: Write `docs/schema-guide.md`.

**Acceptance Criteria**:
- [ ] docs/schema-guide.md exists
- [ ] JSON Schema basics explained
- [ ] How to define fields and validation rules
- [ ] Examples from actual schemas
- [ ] Links to JSON Schema spec

### 7.5 Create Validation Guide
**Effort**: Small  
**Dependencies**: 1.5.1, 2.3  
**Description**: Write `docs/validation-guide.md`.

**Acceptance Criteria**:
- [ ] docs/validation-guide.md exists
- [ ] Validation layers explained (schema, integrity, semantic, quality)
- [ ] How to write validation rules in YAML
- [ ] How to extend validators with new rules
- [ ] Examples

### 7.6 Create Labeling Guide
**Effort**: Small  
**Dependencies**: 1.5.2, 2.4  
**Description**: Write `docs/labeling-guide.md`.

**Acceptance Criteria**:
- [ ] docs/labeling-guide.md exists
- [ ] Labeling framework explained
- [ ] How to write labeling rules in YAML
- [ ] Confidence levels and reasoning
- [ ] Examples from actual labels

### 7.7 Update README
**Effort**: Small  
**Dependencies**: 7.1, 7.2, 3.5, 4.5, 5.1  
**Description**: Complete and finalize README.md.

**Acceptance Criteria**:
- [ ] README.md includes project vision
- [ ] Includes quick start (clone, setup, run)
- [ ] Includes dataset catalog (list of 3 MVP datasets)
- [ ] Includes links to CONTRIBUTING, RESEARCH, docs/
- [ ] Includes license and citation information
- [ ] Includes roadmap (Phase 1-6)
- [ ] Includes links to Stellar documentation

---

## Phase 8: Dataset Catalog

### 8.1 Create Dataset Registry
**Effort**: Small  
**Dependencies**: 3.5, 4.5, 5.1  
**Description**: Generate and publish dataset registry.

**Acceptance Criteria**:
- [ ] `CATALOG.md` created with all datasets
- [ ] Includes: name, description, row count, schema link, download link
- [ ] Includes: created date, version, license
- [ ] Human-readable format
- [ ] `DATASETS.json` generated (machine-readable registry)
- [ ] Registry updated with download URLs

---

## Phase 9: Final Testing & Release

### 9.1 Full Integration Test
**Effort**: Medium  
**Dependencies**: 1.5.5, 3.5, 4.5  
**Description**: Run full end-to-end pipeline on all datasets.

**Acceptance Criteria**:
- [ ] Orchestrator runs from start to finish without errors
- [ ] All 3 datasets processed successfully
- [ ] All validation checks pass
- [ ] Output datasets validated against schemas
- [ ] Datasets exported to CSV/JSON correctly

### 9.2 Test Coverage Verification
**Effort**: Small  
**Dependencies**: 1.4  
**Description**: Verify test coverage meets targets.

**Acceptance Criteria**:
- [ ] Run `pytest --cov=pipeline tests/`
- [ ] Coverage >= 80% for pipeline module
- [ ] All core functions have unit tests
- [ ] Integration tests cover happy path and error cases
- [ ] Test execution time < 10 seconds

### 9.3 Documentation Review
**Effort**: Small  
**Dependencies**: 7.1 through 7.7  
**Description**: Review and finalize all documentation.

**Acceptance Criteria**:
- [ ] All guides are readable and complete
- [ ] Code examples are runnable (copy-paste friendly)
- [ ] Links are valid (README → guides, guides → code)
- [ ] Markdown syntax is valid
- [ ] Tone is welcoming and accessible

### 9.4 Create Initial Release
**Effort**: Small  
**Dependencies**: 9.1, 9.2, 9.3  
**Description**: Create v1.0.0 release on GitHub.

**Acceptance Criteria**:
- [ ] Git tag created: `v1.0.0`
- [ ] GitHub Release created with changelog
- [ ] Release notes document MVP datasets
- [ ] Datasets packaged and attached to release
- [ ] Registry file attached to release
- [ ] Release is published

---

## Task Dependencies Graph

```
1.1 → 1.2 → 1.4 → 1.5.1, 1.5.2, 1.5.3, 1.5.4
            ↓
1.1 → 1.3 (parallel with 1.2)

1.5.1 + 1.5.2 + 1.5.3 + 1.5.4 → 1.5.5

2.1 → 3.1, 4.1
2.2 → 3.2, 4.2
2.3, 2.4 (parallel with 2.1)

3.1 → 3.3 → 3.5, 3.4
4.1 → 4.3 → 4.5, 4.4
5.1 → 5.2

1.5.1 + 1.5.2 + 1.5.5 → 6.1, 6.3
1.5.4 + 1.5.5 → 6.2

7.1, 7.2, 7.3, 7.4, 7.5, 7.6 (parallel)
3.5 + 4.5 + 5.1 → 7.7, 8.1

3.5 + 4.5 + 1.5.5 → 9.1
1.4 → 9.2
7.1-7.7 → 9.3
9.1 + 9.2 + 9.3 → 9.4
```

---

## Execution Strategy

### Recommended Order (Sequential for Single Maintainer)

1. **Phase 1** (Days 1-2): Foundation
   - Setup repository, Python project, testing
   - This enables all subsequent work

2. **Phase 1.5** (Days 2-4): Core Pipeline
   - Implement validators, transformers, collectors, exporters, orchestrator
   - These are used by all datasets

3. **Phases 2-3** (Days 4-7): Transaction Dataset
   - Create schemas, metadata, collection script, process data
   - Good template for subsequent datasets

4. **Phase 4** (Days 7-9): Wallet Dataset
   - Reuse transaction templates and patterns
   - Faster than transactions

5. **Phase 5** (Day 9): Reference Data
   - Quick win, establishes dataset catalog

6. **Phase 6** (Days 9-10): CI/CD
   - Automate validation and publishing
   - Enables future updates

7. **Phase 7** (Days 10-11): Documentation
   - Write guides while implementation is fresh
   - Parallelize with testing

8. **Phase 8-9** (Days 11-12): Testing & Release
   - Final verification and v1.0.0 release

**Total: 2-3 weeks for single maintainer**

---

## Parallel Work Opportunities

For multiple contributors:

- **Phase 1** tasks (setup) must be sequential
- **Phase 1.5** core modules can be worked in parallel (validators, transformers, exporters)
- **Phases 3-4** (transaction and wallet datasets) can be worked in parallel
- **Phase 6** (CI/CD) can start after Phase 1.5
- **Phase 7** (documentation) can be started after Phase 1.5 (write as you implement)

---

## Success Criteria

MVP is complete when:

1. ✓ All Phase 1 tasks completed (foundation)
2. ✓ All Phase 1.5 tasks completed (pipeline)
3. ✓ All Phases 2-5 tasks completed (datasets)
4. ✓ All Phase 6 tasks completed (CI/CD)
5. ✓ All Phase 7 tasks completed (documentation)
6. ✓ Phase 9.1 integration test passes
7. ✓ Phase 9.2 coverage verified (≥80%)
8. ✓ Phase 9.3 documentation complete
9. ✓ Phase 9.4 v1.0.0 released on GitHub

**When all criteria met: MVP is production-ready for Phase 2 expansion.**
