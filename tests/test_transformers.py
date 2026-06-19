"""Tests for transformers module."""

import pytest

from pipeline.transformers import (
    normalize_addresses,
    normalize_timestamps,
    deduplicate,
)


class TestNormalizeAddresses:
    """Tests for address normalization."""

    def test_normalize_addresses_lowercase(self, sample_transactions_df):
        result = normalize_addresses(sample_transactions_df, ["sender", "receiver"])
        assert result["sender"].iloc[0].islower()
        assert result["receiver"].iloc[0].islower()

    def test_normalize_preserves_data(self, sample_transactions_df):
        original_len = len(sample_transactions_df)
        result = normalize_addresses(sample_transactions_df)
        assert len(result) == original_len


class TestNormalizeTimestamps:
    """Tests for timestamp normalization."""

    def test_normalize_timestamps(self, sample_transactions_df):
        result = normalize_timestamps(sample_transactions_df, ["timestamp"])
        # Check that temporal components were added
        assert "timestamp_year" in result.columns
        assert "timestamp_month" in result.columns
        assert "timestamp_day" in result.columns


class TestDeduplicate:
    """Tests for deduplication."""

    def test_deduplicate_removes_duplicates(self, sample_transactions_df):
        # Add a duplicate
        dup_df = sample_transactions_df.append(sample_transactions_df.iloc[0], ignore_index=True)
        assert len(dup_df) == len(sample_transactions_df) + 1
        
        # Deduplicate
        result = deduplicate(dup_df, key=["tx_id"])
        assert len(result) == len(sample_transactions_df)

    def test_deduplicate_preserves_data(self, sample_transactions_df):
        result = deduplicate(sample_transactions_df, key=["tx_id"])
        assert len(result) == len(sample_transactions_df)
