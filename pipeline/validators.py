"""
Dataset validation module.

Implements schema validation, integrity checks, semantic validation, and quality metrics.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple

import jsonschema
import pandas as pd
import yaml

logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of a validation check."""

    def __init__(self, is_valid: bool, errors: Optional[List[str]] = None, warnings: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

    def __repr__(self) -> str:
        status = "✓ VALID" if self.is_valid else "✗ INVALID"
        return f"ValidationResult({status}, {len(self.errors)} errors, {len(self.warnings)} warnings)"


def validate_schema(row: Dict[str, Any], schema_obj: Dict[str, Any]) -> ValidationResult:
    """
    Validate a single row against a JSON Schema.

    Args:
        row: Dictionary representing a data row
        schema_obj: JSON Schema dictionary

    Returns:
        ValidationResult with is_valid flag and errors list
    """
    errors = []
    try:
        jsonschema.validate(instance=row, schema=schema_obj)
    except jsonschema.ValidationError as e:
        errors.append(f"Schema validation failed: {e.message} at path {list(e.absolute_path)}")
    except jsonschema.SchemaError as e:
        errors.append(f"Schema error: {e.message}")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


def validate_dataframe_schema(data: pd.DataFrame, schema_obj: Dict[str, Any]) -> ValidationResult:
    """
    Validate all rows in a DataFrame against a JSON Schema.

    Args:
        data: DataFrame to validate
        schema_obj: JSON Schema dictionary

    Returns:
        ValidationResult with summary and row-level errors
    """
    errors = []
    invalid_rows = []

    for idx, row in data.iterrows():
        row_dict = row.to_dict()
        result = validate_schema(row_dict, schema_obj)
        if not result.is_valid:
            invalid_rows.append(idx)
            for error in result.errors:
                errors.append(f"Row {idx}: {error}")

    if invalid_rows:
        logger.warning(f"Schema validation failed for {len(invalid_rows)} rows out of {len(data)}")
        summary = f"Schema validation failed for {len(invalid_rows)}/{len(data)} rows"
        errors.insert(0, summary)

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


def check_integrity(
    data: pd.DataFrame,
    duplicate_key: Optional[List[str]] = None,
    required_fields: Optional[List[str]] = None,
    reject_nulls: bool = True,
) -> ValidationResult:
    """
    Check data integrity: duplicates, nulls, required fields.

    Args:
        data: DataFrame to check
        duplicate_key: Column(s) to check for duplicates
        required_fields: Columns that must not be null
        reject_nulls: If True, treat nulls as errors; if False, as warnings

    Returns:
        ValidationResult with integrity issues
    """
    warnings = []
    errors = []

    # Check duplicates
    if duplicate_key:
        duplicates = data.duplicated(subset=duplicate_key, keep=False)
        n_duplicates = duplicates.sum()
        if n_duplicates > 0:
            dup_rows = data[duplicates].index.tolist()
            logger.warning(f"Found {n_duplicates} duplicate rows on key {duplicate_key}")
            warnings.append(f"Found {n_duplicates} duplicates on {duplicate_key}. Affected rows: {dup_rows[:10]}")

    # Check required fields
    if required_fields:
        for field in required_fields:
            if field not in data.columns:
                errors.append(f"Required field '{field}' not found in data")
                continue

            null_count = data[field].isnull().sum()
            if null_count > 0:
                null_pct = 100.0 * null_count / len(data)
                msg = f"Field '{field}' has {null_count} nulls ({null_pct:.2f}%)"
                if reject_nulls:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


def validate_semantic_rules(data: pd.DataFrame, rules: Dict[str, Any]) -> ValidationResult:
    """
    Validate semantic/domain-specific rules.

    Args:
        data: DataFrame to validate
        rules: Dictionary with rule definitions

    Returns:
        ValidationResult with semantic validation errors
    """
    errors = []
    warnings = []

    if not rules or "rules" not in rules:
        return ValidationResult(is_valid=True, errors=[], warnings=[])

    for rule in rules.get("rules", []):
        rule_name = rule.get("name", "unnamed")
        rule_type = rule.get("type", "custom")

        try:
            # Address validation example
            if rule_type == "valid_addresses":
                invalid_rows = []
                for field in rule.get("fields", []):
                    if field in data.columns:
                        # Simple check: Stellar addresses start with 'G' and are 56 chars
                        invalid = data[~data[field].astype(str).str.match(r"^G[A-Z2-7]{55}$", na=False)].index
                        invalid_rows.extend(invalid)

                if invalid_rows:
                    msg = f"Rule '{rule_name}': {len(invalid_rows)} invalid addresses"
                    errors.append(msg)

            # Date range validation
            elif rule_type == "date_range":
                for field in rule.get("fields", []):
                    if field in data.columns:
                        try:
                            dates = pd.to_datetime(data[field])
                            if rule.get("min_date"):
                                min_date = pd.to_datetime(rule["min_date"])
                                before_min = (dates < min_date).sum()
                                if before_min > 0:
                                    warnings.append(f"Rule '{rule_name}': {before_min} dates before {rule['min_date']}")

                            if rule.get("max_date"):
                                max_date = pd.to_datetime(rule["max_date"])
                                after_max = (dates > max_date).sum()
                                if after_max > 0:
                                    warnings.append(f"Rule '{rule_name}': {after_max} dates after {rule['max_date']}")
                        except Exception as e:
                            errors.append(f"Rule '{rule_name}': Failed to parse dates - {str(e)}")

        except Exception as e:
            errors.append(f"Rule '{rule_name}' execution failed: {str(e)}")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors, warnings=warnings)


def compute_quality_metrics(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute data quality metrics and statistics.

    Args:
        data: DataFrame to analyze

    Returns:
        Dictionary with quality metrics
    """
    metrics = {
        "row_count": len(data),
        "column_count": len(data.columns),
        "columns": list(data.columns),
        "null_counts": data.isnull().sum().to_dict(),
        "null_percentages": (100 * data.isnull().sum() / len(data)).to_dict(),
        "duplicate_count": data.duplicated().sum(),
        "memory_usage_mb": data.memory_usage(deep=True).sum() / 1024 / 1024,
    }

    # Add statistics for numeric columns
    numeric_stats = {}
    for col in data.select_dtypes(include=["number"]).columns:
        numeric_stats[col] = {
            "min": float(data[col].min()),
            "max": float(data[col].max()),
            "mean": float(data[col].mean()),
            "std": float(data[col].std()),
            "distinct_count": int(data[col].nunique()),
        }

    metrics["numeric_columns"] = numeric_stats

    # Distinct values for categorical columns (up to 100)
    categorical_stats = {}
    for col in data.select_dtypes(include=["object"]).columns:
        distinct = data[col].nunique()
        categorical_stats[col] = {
            "distinct_count": distinct,
            "top_values": data[col].value_counts().head(10).to_dict() if distinct <= 100 else None,
        }

    metrics["categorical_columns"] = categorical_stats

    return metrics


def generate_quality_report(data: pd.DataFrame, dataset_name: str = "Unknown") -> str:
    """
    Generate human-readable quality report.

    Args:
        data: DataFrame to analyze
        dataset_name: Name of the dataset

    Returns:
        Formatted quality report
    """
    metrics = compute_quality_metrics(data)

    report = f"\n{'='*60}\n"
    report += f"Quality Report: {dataset_name}\n"
    report += f"{'='*60}\n"
    report += f"Rows: {metrics['row_count']:,}\n"
    report += f"Columns: {metrics['column_count']}\n"
    report += f"Memory: {metrics['memory_usage_mb']:.2f} MB\n"
    report += f"Duplicates: {metrics['duplicate_count']}\n"
    report += f"\nNull Statistics:\n"

    for col, null_count in metrics["null_counts"].items():
        null_pct = metrics["null_percentages"][col]
        report += f"  {col}: {null_count} ({null_pct:.2f}%)\n"

    if metrics["numeric_columns"]:
        report += f"\nNumeric Columns:\n"
        for col, stats in metrics["numeric_columns"].items():
            report += f"  {col}: min={stats['min']:.2f}, max={stats['max']:.2f}, mean={stats['mean']:.2f}\n"

    report += f"{'='*60}\n"
    return report
