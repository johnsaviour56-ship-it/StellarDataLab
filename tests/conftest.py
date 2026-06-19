"""Pytest configuration and fixtures."""

import json
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_transaction():
    """Sample valid transaction for testing."""
    return {
        "tx_id": "abc123def456abc123def456abc123def456abc123def456abc123def456abc1",
        "timestamp": "2024-01-01T12:00:00Z",
        "sender": "gbrpyhil2ci3xq4k5f7ekz7ai4f6eya7v5ueyfbu72u4a3zvp2wy3dz",
        "receiver": "gbbd47qwpiogksm4v256g33a3mhsbq7t5vc3ahdvwgqy5jxqm74wcgbc",
        "amount": 100.5,
        "operation_type": "payment",
    }


@pytest.fixture
def sample_wallet():
    """Sample valid wallet for testing."""
    return {
        "account": "gbrpyhil2ci3xq4k5f7ekz7ai4f6eya7v5ueyfbu72u4a3zvp2wy3dz",
        "created_date": "2024-01-01T00:00:00Z",
        "balance": 1000.0,
        "signer_count": 1,
        "updated_date": "2024-01-15T00:00:00Z",
    }


@pytest.fixture
def sample_transactions_df():
    """Sample DataFrame of transactions."""
    data = [
        {
            "tx_id": f"tx_{i:064d}",
            "timestamp": "2024-01-01T12:00:00Z",
            "sender": "gbrpyhil2ci3xq4k5f7ekz7ai4f6eya7v5ueyfbu72u4a3zvp2wy3dz",
            "receiver": "gbbd47qwpiogksm4v256g33a3mhsbq7t5vc3ahdvwgqy5jxqm74wcgbc",
            "amount": 100.0 + i,
            "operation_type": "payment",
        }
        for i in range(10)
    ]
    return pd.DataFrame(data)


@pytest.fixture
def sample_wallets_df():
    """Sample DataFrame of wallets."""
    data = [
        {
            "account": f"gacc{i:056d}",
            "created_date": "2024-01-01T00:00:00Z",
            "balance": 1000.0 + i * 100,
            "signer_count": 1,
            "updated_date": "2024-01-15T00:00:00Z",
        }
        for i in range(5)
    ]
    return pd.DataFrame(data)


@pytest.fixture
def transaction_schema():
    """JSON Schema for transactions."""
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Transaction",
        "type": "object",
        "required": ["tx_id", "timestamp", "sender", "receiver", "amount"],
        "properties": {
            "tx_id": {"type": "string", "minLength": 64},
            "timestamp": {"type": "string", "format": "date-time"},
            "sender": {"type": "string", "pattern": "^g[a-z2-7]{54}$"},
            "receiver": {"type": "string", "pattern": "^g[a-z2-7]{54}$"},
            "amount": {"type": "number", "minimum": 0},
            "operation_type": {"type": "string"},
        },
    }


@pytest.fixture
def wallet_schema():
    """JSON Schema for wallets."""
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Wallet",
        "type": "object",
        "required": ["account", "created_date", "balance", "signer_count"],
        "properties": {
            "account": {"type": "string", "pattern": "^g[a-z2-7]{54}$"},
            "created_date": {"type": "string", "format": "date-time"},
            "balance": {"type": "number", "minimum": 0},
            "signer_count": {"type": "integer", "minimum": 0},
            "updated_date": {"type": "string", "format": "date-time"},
        },
    }


@pytest.fixture
def tmp_dataset_dir(tmp_path):
    """Create temporary directory structure for datasets."""
    raw_dir = tmp_path / "raw"
    curated_dir = tmp_path / "curated"
    metadata_dir = tmp_path / "metadata"

    raw_dir.mkdir()
    curated_dir.mkdir()
    metadata_dir.mkdir()

    return {
        "root": tmp_path,
        "raw": raw_dir,
        "curated": curated_dir,
        "metadata": metadata_dir,
    }
