"""Tests for validation module."""

import pytest

from pipeline.validators import (
    ValidationResult,
    check_integrity,
    compute_quality_metrics,
    validate_dataframe_schema,
    validate_schema,
)


class TestValidationResult:
    """Tests for ValidationResult class."""

    def test_valid_result(self):
        result = ValidationResult(is_valid=True)
        assert result.is_valid
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_invalid_result(self):
        result = ValidationResult(is_valid=False, errors=["Error 1"])
        assert not result.is_valid
        assert len(result.errors) == 1


class TestSchemaValidation:
    """Tests for schema validation."""

    def test_validate_valid_row(self, sample_transaction, transaction_schema):
        result = validate_schema(sample_transaction, transaction_schema)
        assert result.is_valid
        assert len(result.errors) == 0

    def test_validate_missing_required_field(self, sample_transaction, transaction_schema):
        invalid_row = {k: v for k, v in sample_transaction.items() if k != "tx_id"}
        result = validate_schema(invalid_row, transaction_schema)
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_validate_invalid_type(self, sample_transaction, transaction_schema):
        invalid_row = sample_transaction.copy()
        invalid_row["amount"] = "not_a_number"
        result = validate_schema(invalid_row, transaction_schema)
        assert not result.is_valid


class TestDataFrameValidation:
    """Tests for DataFrame validation."""

    def test_validate_all_valid_rows(self, sample_transactions_df, transaction_schema):
        result = validate_dataframe_schema(sample_transactions_df, transaction_schema)
        assert result.is_valid

    def test_compute_quality_metrics(self, sample_transactions_df):
        metrics = compute_quality_metrics(sample_transactions_df)
        assert metrics["row_count"] == 10
        assert metrics["column_count"] == 6
        assert metrics["duplicate_count"] == 0


class TestIntegrityChecks:
    """Tests for integrity checks."""

    def test_check_duplicates(self, sample_transactions_df):
        result = check_integrity(sample_transactions_df, duplicate_key=["tx_id"])
        assert result.is_valid
        assert len(result.warnings) == 0

    def test_check_required_fields(self, sample_transactions_df):
        result = check_integrity(
            sample_transactions_df,
            required_fields=["tx_id", "timestamp"],
            reject_nulls=True,
        )
        assert result.is_valid

    def test_check_missing_column(self, sample_transactions_df):
        result = check_integrity(
            sample_transactions_df,
            required_fields=["nonexistent_field"],
            reject_nulls=True,
        )
        assert not result.is_valid
        assert len(result.errors) > 0
