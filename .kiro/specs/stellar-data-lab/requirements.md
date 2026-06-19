# Requirements Document: StellarDataLab

## Overview

This document specifies the requirements for StellarDataLab, an open-source research and data repository for the Stellar ecosystem. Requirements are derived from the design document and organized by category. Each requirement is testable and includes acceptance criteria.

---

## 1. Architecture & Repository Setup

### REQ-ARCH-001: File-Based Storage System
**Category**: Architecture  
**Priority**: P0 (Critical)  
**Effort**: Small  

The repository must use Git and file-based storage (CSV, JSON) exclusively for all datasets and configurations.

**Acceptance Criteria**:
- No database server is deployed or referenced
- All data is stored in CSV or JSON format
- All data is committed to Git history
- No cloud storage services (S3, BigQuery, etc.) are referenced

**Rationale**: Ensures immutability, auditability, and eliminates operational overhead.

### REQ-ARCH-002: Python Single-Pipeline Orchestration
**Category**: Architecture  
**Priority**: P0 (Critical)  
**Effort**: Medium  

A single Python module (`pipeline/orchestrator.py`) must orchestrate all data collection, transformation, validation, and export operations.

**Acceptance Criteria**:
- `pipeline/orchestrator.py` exists and is importable
- Orchestrator exposes `orchestrate_pipeline(config)` function
- Orchestrator runs all phases: collection → transformation → validation → export
- Orchestrator can be invoked locally or via GitHub Actions

**Rationale**: Single entry point simplifies maintenance and testing.

### REQ-ARCH-003: Directory Structure Compliance
**Category**: Architecture  
**Priority**: P0 (Critical)  
**Effort**: Small  

Repository must follow the specified directory structure with clear separation of concerns.

**Acceptance Criteria**:
- `/pipeline/` contains core Python modules
- `/schemas/` contains JSON Schema definitions
- `/datasets/raw/` contains unmodified raw data
- `/datasets/curated/` contains processed, validated data
- `/datasets/metadata/` contains YAML sidecar files
- `/scripts/` contains collection scripts
- `/tests/` contains unit and integration tests
- All directories have README.md with purpose and contents

**Rationale**: Clear organization enables contributor onboarding and maintainability.

---

## 2. Data Collection Pipeline

### REQ-COLL-001: Collection Script Framework
**Category**: Collection  
**Priority**: P1 (High)  
**Effort**: Medium  

Collection scripts must follow a standard interface and be independently runnable.

**Acceptance Criteria**:
- Each collection script has `collect_[dataset_name]()` function
- Scripts accept configuration via function parameters and environment variables
- Scripts log collection progress and errors
- Scripts write output to specified file path
- Scripts handle API rate limiting and retries gracefully
- Scripts document error handling behavior

**Rationale**: Standard interface enables easy addition of new data sources.

### REQ-COLL-002: Transaction Collection Implementation
**Category**: Collection  
**Priority**: P1 (High)  
**Effort**: Medium  

Implement collection script for Stellar transactions from the Stellar Horizon API.

**Acceptance Criteria**:
- `scripts/collect_transactions.py` fetches transactions from Stellar API
- Collects transactions for specified date range
- Writes output to `datasets/raw/transactions_YYYY_raw.csv`
- Handles API pagination
- Logs number of transactions collected
- Retry logic for failed requests (3 attempts, exponential backoff)
- Documentation includes API endpoint, rate limits, authentication

**Rationale**: Foundation dataset for network monitoring.

### REQ-COLL-003: Wallet Snapshot Collection Implementation
**Category**: Collection  
**Priority**: P1 (High)  
**Effort**: Medium  

Implement collection script for Stellar wallet snapshot.

**Acceptance Criteria**:
- `scripts/collect_wallets.py` fetches list of active accounts from Stellar API
- Includes account age, balance, signer count
- Writes output to `datasets/raw/wallets_snapshot_raw.csv`
- Handles large result sets (pagination or streaming)
- Logs number of accounts collected and any skipped records
- Includes timestamp of snapshot

**Rationale**: Foundation for network statistics and wallet analysis.

### REQ-COLL-004: Static Reference Data
**Category**: Collection  
**Priority**: P0 (Critical)  
**Effort**: Small  

Operation types reference data must be curated statically (no API collection needed).

**Acceptance Criteria**:
- `datasets/curated/operation_types.json` exists
- Contains all 13 Stellar operation types
- Includes name, type code, description, example
- Valid JSON format per schema

**Rationale**: Reference data, curated once; no need for dynamic collection.

---

## 3. Data Schemas

### REQ-SCHEMA-001: JSON Schema Standard
**Category**: Schema  
**Priority**: P0 (Critical)  
**Effort**: Small  

All datasets must have JSON Schema (Draft 7) definitions.

**Acceptance Criteria**:
- `schemas/transaction.schema.json` exists and is valid JSON Schema
- `schemas/wallet.schema.json` exists and is valid JSON Schema
- `schemas/operation_types.schema.json` exists and is valid JSON Schema
- Each schema validates with jsonschema library
- Each schema includes title, description, required fields, properties, and constraints

**Rationale**: Machine-readable validation contracts.

### REQ-SCHEMA-002: Transaction Schema Definition
**Category**: Schema  
**Priority**: P1 (High)  
**Effort**: Small  

Transaction schema must define all required fields and validation rules.

**Acceptance Criteria**:
- Required fields: tx_id, timestamp, sender, receiver, amount, operation_type
- tx_id: string, 64-char hex
- timestamp: ISO 8601 format
- sender/receiver: Stellar address pattern validation
- amount: positive number
- operation_type: enum of valid operations

**Rationale**: Ensures collected transaction data is consistent.

### REQ-SCHEMA-003: Wallet Schema Definition
**Category**: Schema  
**Priority**: P1 (High)  
**Effort**: Small  

Wallet schema must define all required fields and validation rules.

**Acceptance Criteria**:
- Required fields: account, created_date, balance, signer_count, updated_date
- account: Stellar address pattern validation
- created_date/updated_date: ISO 8601 format
- created_date ≤ updated_date (validated via constraint)
- balance: non-negative number
- signer_count: non-negative integer

**Rationale**: Ensures wallet snapshots are consistent and valid.

---

## 4. Dataset Metadata

### REQ-META-001: YAML Metadata Sidecar Format
**Category**: Metadata  
**Priority**: P1 (High)  
**Effort**: Small  

Each dataset must have a YAML metadata sidecar documenting lineage, methodology, and validation rules.

**Acceptance Criteria**:
- Metadata file: `datasets/metadata/[dataset_name].metadata.yml`
- Required fields: name, version, created_date, description, source, collection, schema, transformations, quality_checks
- Metadata is valid YAML and parseable by PyYAML
- Metadata documents data lineage and reproducibility

**Rationale**: Ensures transparency and reproducibility of datasets.

### REQ-META-002: Transaction Metadata
**Category**: Metadata  
**Priority**: P1 (High)  
**Effort**: Small  

Transaction dataset must have complete metadata documenting source, collection method, and validation rules.

**Acceptance Criteria**:
- `datasets/metadata/transactions_2024.metadata.yml` exists
- Documents source: Stellar Horizon API
- Documents collection method: daily pagination with rate limiting
- Documents transformations: normalization, deduplication
- Documents quality checks: duplicates by tx_id, no nulls in required fields

**Rationale**: Ensures researchers understand data provenance.

### REQ-META-003: Wallet Metadata
**Category**: Metadata  
**Priority**: P1 (High)  
**Effort**: Small  

Wallet dataset must have complete metadata documenting snapshot methodology and validation.

**Acceptance Criteria**:
- `datasets/metadata/wallets_snapshot.metadata.yml` exists
- Documents source: Stellar Horizon API snapshot
- Documents collection method: full ledger enumeration
- Documents snapshot timestamp and date range coverage
- Documents quality checks: address validation, date range validation

**Rationale**: Ensures wallet data is properly documented.

---

## 5. Data Transformation & Normalization

### REQ-TRANS-001: Transformation Pipeline Module
**Category**: Transformation  
**Priority**: P1 (High)  
**Effort**: Medium  

`pipeline/transformers.py` must implement transformations as composable, reusable functions.

**Acceptance Criteria**:
- Module exports transformation functions for normalization, labeling, aggregation
- Each transformation function has signature: `transform(dataframe, config) -> dataframe`
- Transformations are deterministic (same input → same output)
- Transformations log progress and row counts
- Transformations include pre/post validation

**Rationale**: Enables reproducible data processing.

### REQ-TRANS-002: Address Normalization
**Category**: Transformation  
**Priority**: P1 (High)  
**Effort**: Small  

Addresses must be normalized to lowercase and validated.

**Acceptance Criteria**:
- `transformers.normalize_addresses()` converts all addresses to lowercase
- Validates format: Stellar address pattern (G followed by 55 alphanumeric chars)
- Raises error if address is malformed (not auto-corrected)
- Logs count of normalized addresses

**Rationale**: Ensures consistent address format across datasets.

### REQ-TRANS-003: Timestamp Normalization
**Category**: Transformation  
**Priority**: P1 (High)  
**Effort**: Small  

Timestamps must be normalized to ISO 8601 format.

**Acceptance Criteria**:
- `transformers.normalize_timestamps()` converts timestamps to ISO 8601
- Extracts temporal components (year, month, day, hour, day_of_week)
- Validates that timestamps are in valid range (e.g., not future dates)
- Logs count of normalized timestamps

**Rationale**: Enables temporal analysis and consistency.

### REQ-TRANS-004: Deduplication
**Category**: Transformation  
**Priority**: P1 (High)  
**Effort**: Small  

Datasets must be deduplicated by primary key.

**Acceptance Criteria**:
- `transformers.deduplicate()` removes duplicate rows by specified key
- For transactions: dedup by (tx_id)
- For wallets: dedup by (account)
- Logs count of duplicates removed
- Preserves first occurrence (stable sort)

**Rationale**: Prevents duplicate data in research datasets.

---

## 6. Data Validation

### REQ-VAL-001: Schema Validator
**Category**: Validation  
**Priority**: P0 (Critical)  
**Effort**: Medium  

`pipeline/validators.py` must implement schema validation against JSON Schema.

**Acceptance Criteria**:
- Module exports `validate_schema(row, schema_obj)` function
- Uses jsonschema library for validation
- Returns result object with `is_valid: bool` and `errors: list`
- Validates all rows in dataset against schema
- Reports schema violations with row number and field details

**Rationale**: Catches data quality issues early.

### REQ-VAL-002: Integrity Checks
**Category**: Validation  
**Priority**: P1 (High)  
**Effort**: Medium  

Validator must check for duplicates and null values.

**Acceptance Criteria**:
- `validators.check_integrity()` detects duplicate rows
- Detects null values in required fields
- Returns result with duplicate count, null count, affected rows
- Allows configuring which fields are required vs. optional

**Rationale**: Ensures data quality and completeness.

### REQ-VAL-003: Semantic Validation
**Category**: Validation  
**Priority**: P1 (High)  
**Effort**: Medium  

Validator must check domain-specific logic (semantic rules).

**Acceptance Criteria**:
- `validators.validate_semantic_rules()` evaluates custom validation rules
- Rules defined in YAML (metadata file)
- Supports predicates: address validation, amount ranges, date ordering, etc.
- Reports which semantic rules failed and why

**Rationale**: Catches domain-specific errors (e.g., invalid addresses).

### REQ-VAL-004: Quality Metrics
**Category**: Validation  
**Priority**: P2 (Medium)  
**Effort**: Medium  

Validator must compute and report quality metrics.

**Acceptance Criteria**:
- `validators.compute_quality_metrics()` returns statistics
- Metrics: row count, null percentage, duplicate percentage, value distributions
- Detects outliers using IQR method
- Reports distinct value counts per column
- Generates human-readable quality report

**Rationale**: Enables data quality monitoring and trending.

### REQ-VAL-005: Validation Rules Configuration
**Category**: Validation  
**Priority**: P1 (High)  
**Effort**: Small  

Validation rules must be configurable via YAML.

**Acceptance Criteria**:
- Validation rules in metadata YAML files
- Rules include: duplicate keys, required fields, semantic checks, quality thresholds
- Rules are declarative (not hardcoded in Python)
- Validators load rules from YAML at runtime

**Rationale**: Non-programmers can configure validation without code changes.

---

## 7. Labeling Framework

### REQ-LABEL-001: Labeling Engine
**Category**: Labeling  
**Priority**: P2 (Medium)  
**Effort**: Medium  

`pipeline/transformers.py` must include labeling functionality.

**Acceptance Criteria**:
- `apply_labels(dataframe, labeling_config)` function exists
- Labeling config loaded from YAML (metadata file)
- Rules applied in order (first match wins)
- Default label assigned to unmatched rows
- Logs label distribution (value counts)
- Validates that all output labels are in allowed set

**Rationale**: Enables classification and downstream ML applications.

### REQ-LABEL-002: Labeling Rules Configuration
**Category**: Labeling  
**Priority**: P2 (Medium)  
**Effort**: Small  

Labeling rules must be declarative and configurable.

**Acceptance Criteria**:
- Rules defined in YAML within metadata file
- Each rule has: condition, value, confidence, reasoning
- Conditions are Python-like expressions (evaluated safely)
- Rules document methodology and confidence level
- Quality checks: label coverage, class imbalance thresholds

**Rationale**: Lowers barrier for contributors to add labeling logic.

---

## 8. Testing Strategy

### REQ-TEST-001: Unit Test Suite
**Category**: Testing  
**Priority**: P1 (High)  
**Effort**: Medium  

Unit tests must cover core pipeline components.

**Acceptance Criteria**:
- `tests/test_validators.py`: Tests schema validation, integrity checks, semantic rules
- `tests/test_transformers.py`: Tests normalization, deduplication, labeling
- `tests/test_collectors.py`: Tests collection script interfaces and error handling
- Minimum 80% code coverage for pipeline module
- Tests use fixtures from `tests/fixtures/`
- All tests pass with `pytest tests/ -v`

**Rationale**: Ensures reliability and prevents regressions.

### REQ-TEST-002: Integration Tests
**Category**: Testing  
**Priority**: P1 (High)  
**Effort**: Medium  

Integration tests must verify end-to-end pipeline.

**Acceptance Criteria**:
- `tests/test_integration.py`: Tests full orchestrator pipeline
- Uses test datasets (small, known-good data)
- Verifies output data is valid against schema
- Verifies row counts correct after transformations
- Verifies validation passes for good data, fails for bad data

**Rationale**: Catches integration issues that unit tests miss.

### REQ-TEST-003: Test Fixtures
**Category**: Testing  
**Priority**: P1 (High)  
**Effort**: Small  

Test fixtures must provide sample data for reproducible testing.

**Acceptance Criteria**:
- `tests/fixtures/sample_transaction.json` - Valid transaction
- `tests/fixtures/sample_wallet.json` - Valid wallet
- `tests/fixtures/invalid_transaction.json` - Invalid transaction (schema violation)
- `tests/fixtures/transactions_batch.csv` - Small batch of transactions (5-10 rows)
- All fixtures are version-controlled and immutable

**Rationale**: Enables reproducible testing without external dependencies.

---

## 9. GitHub Actions CI/CD

### REQ-CI-001: Validate on Push Workflow
**Category**: CI/CD  
**Priority**: P1 (High)  
**Effort**: Medium  

GitHub Actions must validate datasets on every push.

**Acceptance Criteria**:
- `.github/workflows/validate-datasets.yml` exists
- Triggered on push to main and develop branches
- Runs schema validation on all datasets
- Runs integrity checks (duplicates, nulls)
- Runs quality checks
- Generates and uploads validation report as artifact
- Fails CI if validation fails (blocks merge)

**Rationale**: Catches data quality issues before publication.

### REQ-CI-002: Publish Release Workflow
**Category**: CI/CD  
**Priority**: P1 (High)  
**Effort**: Medium  

GitHub Actions must publish releases with packaged datasets.

**Acceptance Criteria**:
- `.github/workflows/publish-release.yml` exists
- Triggered on push to main with tag
- Runs full validation before publishing
- Generates dataset registry (JSON)
- Packages datasets as tar.gz
- Creates GitHub Release with artifacts
- Release includes version, changelog, dataset links

**Rationale**: Enables reproducible, versioned dataset distribution.

### REQ-CI-003: Code Quality Workflow
**Category**: CI/CD  
**Priority**: P2 (Medium)  
**Effort**: Medium  

GitHub Actions must check code quality.

**Acceptance Criteria**:
- `.github/workflows/check-quality.yml` exists
- Runs flake8 linting on Python code
- Runs black formatting check
- Runs full test suite with coverage
- Checks Markdown syntax in README, CONTRIBUTING
- Fails CI if tests fail or coverage drops

**Rationale**: Maintains code quality and consistency.

---

## 10. Dataset Export

### REQ-EXPORT-001: Export Functions
**Category**: Export  
**Priority**: P1 (High)  
**Effort**: Medium  

`pipeline/exporters.py` must handle dataset export formats.

**Acceptance Criteria**:
- `export_to_csv()` writes dataset to CSV with proper formatting
- `export_to_json()` writes dataset to JSON (line-delimited JSON format)
- `export_to_parquet()` optional (for future ML use)
- Exports include proper headers and metadata
- All exports are deterministic (same input → same file)

**Rationale**: Enables flexible dataset consumption.

### REQ-EXPORT-002: Dataset Registry Generation
**Category**: Export  
**Priority**: P1 (High)  
**Effort**: Small  

System must generate searchable dataset registry.

**Acceptance Criteria**:
- `exporters.generate_registry()` creates JSON registry of all datasets
- Registry includes: name, version, description, size, schema, url, date_added
- Registry is sortable by name, date, size
- Registry includes download links to GitHub Releases
- Human-readable CATALOG.md generated from registry

**Rationale**: Enables researchers to discover datasets.

---

## 11. Documentation & Onboarding

### REQ-DOC-001: README
**Category**: Documentation  
**Priority**: P0 (Critical)  
**Effort**: Small  

README must provide project overview and quick start.

**Acceptance Criteria**:
- README.md exists in repository root
- Includes project vision and goals
- Includes quick start (clone, setup, run pipeline)
- Includes dataset catalog with descriptions
- Includes links to CONTRIBUTING, RESEARCH guides
- Includes license information

**Rationale**: First impression for new users.

### REQ-DOC-002: Contributing Guide
**Category**: Documentation  
**Priority**: P1 (High)  
**Effort**: Small  

Contributing guide must enable new contributors.

**Acceptance Criteria**:
- CONTRIBUTING.md exists
- Includes step-by-step guide to add new dataset (in 30 minutes)
- Includes metadata template (copy-paste starting point)
- Includes schema template
- Includes collection script template
- Includes submission checklist
- Includes code style guidelines (Python, tests)

**Rationale**: Lowers barrier to contribution.

### REQ-DOC-003: Research Methodology Guide
**Category**: Documentation  
**Priority**: P1 (High)  
**Effort**: Small  

Research guide must document data quality and reproducibility standards.

**Acceptance Criteria**:
- RESEARCH.md exists
- Documents reproducibility principles
- Documents how to include methodology in metadata
- Documents statistical validation approach
- Documents handling of sensitive data
- Includes examples of good metadata and methodology documentation

**Rationale**: Ensures research integrity and reproducibility.

### REQ-DOC-004: Pipeline Guide
**Category**: Documentation  
**Priority**: P2 (Medium)  
**Effort**: Small  

Documentation must explain how to use and extend the pipeline.

**Acceptance Criteria**:
- `docs/pipeline-guide.md` exists
- Explains orchestrator, collectors, transformers, validators, exporters
- Includes code examples
- Explains how to add new collection script
- Explains how to add new transformation
- Includes troubleshooting section

**Rationale**: Enables contributors to modify and extend pipeline.

### REQ-DOC-005: Schema Guide
**Category**: Documentation  
**Priority**: P2 (Medium)  
**Effort**: Small  

Documentation must explain JSON Schema and how to write one.

**Acceptance Criteria**:
- `docs/schema-guide.md` exists
- Explains JSON Schema basics
- Shows how to define fields, validation rules
- Includes examples from actual schemas
- Explains validation in context of pipeline
- Links to JSON Schema specification

**Rationale**: Enables contributors to define schemas for new datasets.

---

## 12. MVP Dataset Implementations

### REQ-DATA-001: Transaction Dataset Complete
**Category**: Dataset  
**Priority**: P1 (High)  
**Effort**: Large  

Complete implementation of Transactions 2024 dataset.

**Acceptance Criteria**:
- Collection script (`scripts/collect_transactions.py`) implemented and tested
- Schema defined (`schemas/transaction.schema.json`)
- Metadata file complete (`datasets/metadata/transactions_2024.metadata.yml`)
- Raw data downloaded and stored (`datasets/raw/transactions_2024_raw.csv`)
- Curated data processed and validated (`datasets/curated/transactions_2024_labeled.csv`)
- Passes all validation checks
- Documented in CATALOG.md

**Rationale**: Core foundation dataset.

### REQ-DATA-002: Wallet Dataset Complete
**Category**: Dataset  
**Priority**: P1 (High)  
**Effort**: Large  

Complete implementation of Wallet Snapshot dataset.

**Acceptance Criteria**:
- Collection script (`scripts/collect_wallets.py`) implemented and tested
- Schema defined (`schemas/wallet.schema.json`)
- Metadata file complete (`datasets/metadata/wallets_snapshot.metadata.yml`)
- Raw data downloaded and stored (`datasets/raw/wallets_snapshot_raw.csv`)
- Curated data processed and validated (`datasets/curated/wallets_snapshot_curated.csv`)
- Passes all validation checks
- Documented in CATALOG.md

**Rationale**: Foundation for network analysis and ML applications.

### REQ-DATA-003: Reference Data Complete
**Category**: Dataset  
**Priority**: P0 (Critical)  
**Effort**: Small  

Complete implementation of Operation Types reference data.

**Acceptance Criteria**:
- Schema defined (`schemas/operation_types.schema.json`)
- Reference data file created (`datasets/curated/operation_types.json`)
- Includes all 13 Stellar operation types with descriptions
- Valid against schema
- Documented in CATALOG.md

**Rationale**: Reference for labeling and documentation.

---

## 13. Project Setup & Configuration

### REQ-SETUP-001: Python Project Configuration
**Category**: Setup  
**Priority**: P0 (Critical)  
**Effort**: Small  

Project must be properly configured as Python package.

**Acceptance Criteria**:
- `pyproject.toml` exists with project metadata
- Dependencies listed: pandas, pydantic, jsonschema, pyyaml, requests, pytest, black, flake8
- Virtual environment setup documented in CONTRIBUTING
- `pip install -r requirements.txt` installs all dependencies

**Rationale**: Standard Python project setup.

### REQ-SETUP-002: Git Configuration
**Category**: Setup  
**Priority**: P0 (Critical)  
**Effort**: Small  

Repository must have proper Git configuration.

**Acceptance Criteria**:
- `.gitignore` excludes venv, __pycache__, .pyc, .DS_Store, test outputs
- LICENSE file present (MIT or Apache 2.0)
- All documentation checked into Git
- No secrets or credentials in Git history

**Rationale**: Ensures clean repository and security.

### REQ-SETUP-003: GitHub Configuration
**Category**: Setup  
**Priority**: P1 (High)  
**Effort**: Small  

GitHub repository must be properly configured.

**Acceptance Criteria**:
- Branch protection on main: require PR reviews, require CI checks to pass
- GitHub Issues enabled
- GitHub Discussions enabled for Q&A
- Code owners file specifies maintainers
- Repository description and topics set

**Rationale**: Enables collaboration and prevents accidental pushes.

---

## Summary

This requirements document specifies 40+ individual requirements organized into 13 categories. All requirements are:

- **SMART**: Specific and measurable
- **Testable**: Include acceptance criteria
- **Prioritized**: P0 (Critical), P1 (High), P2 (Medium)
- **Estimated**: Effort in Small/Medium/Large
- **Rationale-driven**: Explained why each is needed

The requirements focus on MVP scope with 3 core datasets and foundational infrastructure, avoiding feature creep and over-engineering. Implementation should follow tasks.md for concrete, sequenced work items.
