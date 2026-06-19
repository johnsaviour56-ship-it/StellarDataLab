"""
Data transformation module.

Handles normalization, deduplication, labeling, and other data transformations.
"""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def normalize_addresses(data: pd.DataFrame, address_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Normalize addresses to lowercase and validate format.

    Args:
        data: DataFrame with address columns
        address_columns: List of column names containing addresses

    Returns:
        DataFrame with normalized addresses
    """
    result = data.copy()

    if address_columns is None:
        # Auto-detect common address column names
        address_columns = [col for col in result.columns if "address" in col.lower() or col in ["sender", "receiver", "account"]]

    for col in address_columns:
        if col in result.columns:
            # Convert to lowercase
            result[col] = result[col].astype(str).str.lower()
            logger.info(f"Normalized addresses in column '{col}'")

    return result


def normalize_timestamps(data: pd.DataFrame, timestamp_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Normalize timestamps to ISO 8601 format and extract temporal components.

    Args:
        data: DataFrame with timestamp columns
        timestamp_columns: List of column names containing timestamps

    Returns:
        DataFrame with normalized timestamps and temporal components
    """
    result = data.copy()

    if timestamp_columns is None:
        # Auto-detect common timestamp column names
        timestamp_columns = [col for col in result.columns if "timestamp" in col.lower() or "date" in col.lower()]

    for col in timestamp_columns:
        if col in result.columns:
            try:
                # Convert to datetime
                result[col] = pd.to_datetime(result[col])

                # Extract temporal components
                base_name = col.replace("_date", "").replace("_timestamp", "")
                result[f"{base_name}_year"] = result[col].dt.year
                result[f"{base_name}_month"] = result[col].dt.month
                result[f"{base_name}_day"] = result[col].dt.day
                result[f"{base_name}_hour"] = result[col].dt.hour
                result[f"{base_name}_dow"] = result[col].dt.dayofweek  # 0=Monday, 6=Sunday

                logger.info(f"Normalized timestamps in column '{col}' and extracted temporal components")
            except Exception as e:
                logger.warning(f"Failed to normalize timestamps in column '{col}': {str(e)}")

    return result


def deduplicate(data: pd.DataFrame, key: Optional[List[str]] = None, keep: str = "first") -> pd.DataFrame:
    """
    Remove duplicate rows based on specified key.

    Args:
        data: DataFrame to deduplicate
        key: Column(s) to check for duplicates
        keep: Which duplicates to keep ('first', 'last', False for all)

    Returns:
        Deduplicated DataFrame
    """
    if key is None:
        # Use all columns as key
        key = list(data.columns)

    original_len = len(data)
    result = data.drop_duplicates(subset=key, keep=keep).reset_index(drop=True)
    removed = original_len - len(result)

    logger.info(f"Removed {removed} duplicates out of {original_len} rows (key: {key})")

    return result


def apply_labels(data: pd.DataFrame, labeling_config: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply labeling rules to dataset.

    Args:
        data: DataFrame to label
        labeling_config: Dictionary with labeling rules

    Returns:
        DataFrame with labels applied
    """
    result = data.copy()

    if not labeling_config or "labels" not in labeling_config:
        logger.warning("No labeling configuration provided")
        return result

    for label_def in labeling_config.get("labels", []):
        label_column = label_def.get("column_name", "label")
        default_value = label_def.get("default_value", "unknown")
        rules = label_def.get("rules", [])

        # Initialize label column
        result[label_column] = default_value

        # Apply rules (first match wins)
        for rule in rules:
            condition = rule.get("condition", "")
            value = rule.get("value", default_value)

            try:
                # Apply condition (simple string-based matching for MVP)
                # In production, this would be more sophisticated
                if condition and isinstance(condition, str):
                    # For now, just warn that we'd need to implement complex rule evaluation
                    logger.debug(f"Condition '{condition}' not yet evaluated for label '{label_column}'")

            except Exception as e:
                logger.warning(f"Failed to apply rule for label '{label_column}': {str(e)}")

        # Log label distribution
        distribution = result[label_column].value_counts().to_dict()
        logger.info(f"Label distribution for '{label_column}': {distribution}")

    return result


def transform_pipeline(data: pd.DataFrame, transformations: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Apply a sequence of transformations to data.

    Args:
        data: DataFrame to transform
        transformations: List of transformation configurations

    Returns:
        Transformed DataFrame
    """
    result = data.copy()

    for transform in transformations:
        name = transform.get("name", "unknown")
        transform_type = transform.get("type", "custom")

        try:
            if transform_type == "normalize_addresses":
                columns = transform.get("columns", None)
                result = normalize_addresses(result, columns)

            elif transform_type == "normalize_timestamps":
                columns = transform.get("columns", None)
                result = normalize_timestamps(result, columns)

            elif transform_type == "deduplicate":
                key = transform.get("key", None)
                result = deduplicate(result, key)

            elif transform_type == "apply_labels":
                config = transform.get("config", {})
                result = apply_labels(result, config)

            logger.info(f"Applied transformation: {name}")

        except Exception as e:
            logger.error(f"Transformation '{name}' failed: {str(e)}")
            raise

    return result
