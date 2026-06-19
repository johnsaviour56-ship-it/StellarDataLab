"""
Data export module.

Handles exporting datasets to various formats (CSV, JSON) and generating registries.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def export_to_csv(data: pd.DataFrame, filepath: str, index: bool = False) -> str:
    """
    Export DataFrame to CSV file.

    Args:
        data: DataFrame to export
        filepath: Output file path
        index: Whether to include index in CSV

    Returns:
        Path to created file
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(filepath, index=index)
    logger.info(f"Exported {len(data)} rows to {filepath}")
    return filepath


def export_to_json(data: pd.DataFrame, filepath: str, orient: str = "records") -> str:
    """
    Export DataFrame to JSON file.

    Args:
        data: DataFrame to export
        filepath: Output file path
        orient: JSON format ('records' for line-delimited, 'split', etc.)

    Returns:
        Path to created file
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    if orient == "records":
        # Line-delimited JSON
        with open(filepath, "w") as f:
            for _, row in data.iterrows():
                json.dump(row.to_dict(), f)
                f.write("\n")
    else:
        # Standard JSON
        data.to_json(filepath, orient=orient)

    logger.info(f"Exported {len(data)} rows to {filepath}")
    return filepath


def generate_registry(datasets_dir: str, output_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate dataset registry from metadata files.

    Args:
        datasets_dir: Path to datasets directory
        output_file: Optional path to write registry JSON

    Returns:
        Registry dictionary
    """
    registry = {
        "version": "1.0",
        "generated_date": datetime.now().isoformat(),
        "datasets": [],
    }

    datasets_path = Path(datasets_dir)
    metadata_path = datasets_path / "metadata"

    if not metadata_path.exists():
        logger.warning(f"Metadata directory not found: {metadata_path}")
        return registry

    # Find all curated datasets
    curated_path = datasets_path / "curated"
    if curated_path.exists():
        for dataset_file in curated_path.glob("*.csv"):
            dataset_name = dataset_file.stem
            metadata_file = metadata_path / f"{dataset_name}.metadata.yml"

            dataset_info = {
                "name": dataset_name,
                "file": str(dataset_file),
                "format": "csv",
                "size_bytes": dataset_file.stat().st_size,
                "rows": len(pd.read_csv(dataset_file)),
            }

            if metadata_file.exists():
                # Try to read metadata
                try:
                    import yaml

                    with open(metadata_file) as f:
                        metadata = yaml.safe_load(f)
                        if metadata:
                            dataset_info["metadata"] = metadata

                except Exception as e:
                    logger.warning(f"Could not read metadata for {dataset_name}: {str(e)}")

            registry["datasets"].append(dataset_info)

        for dataset_file in curated_path.glob("*.json"):
            dataset_name = dataset_file.stem
            dataset_info = {
                "name": dataset_name,
                "file": str(dataset_file),
                "format": "json",
                "size_bytes": dataset_file.stat().st_size,
            }
            registry["datasets"].append(dataset_info)

    # Write registry if output file specified
    if output_file:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(registry, f, indent=2)
        logger.info(f"Generated registry with {len(registry['datasets'])} datasets: {output_file}")

    return registry
