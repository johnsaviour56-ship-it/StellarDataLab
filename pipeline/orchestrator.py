"""
Pipeline orchestrator module.

Orchestrates data collection, transformation, validation, and export.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import yaml

from pipeline.collectors import run_collection_script
from pipeline.exporters import export_to_csv, export_to_json, generate_registry
from pipeline.transformers import transform_pipeline
from pipeline.validators import validate_dataframe_schema, check_integrity, compute_quality_metrics

logger = logging.getLogger(__name__)


class Orchestrator:
    """Pipeline orchestrator."""

    def __init__(self, config_file: Optional[str] = None):
        self.config = {}
        if config_file and Path(config_file).exists():
            with open(config_file) as f:
                self.config = yaml.safe_load(f) or {}

    def process_dataset(
        self,
        dataset_config: Dict[str, Any],
        raw_path: str,
        curated_path: str,
    ) -> Dict[str, Any]:
        """
        Process a single dataset through the pipeline.

        Args:
            dataset_config: Dataset configuration
            raw_path: Path to raw dataset
            curated_path: Path to curated dataset

        Returns:
            Result dictionary with status and metrics
        """
        dataset_name = dataset_config.get("name", "unknown")
        logger.info(f"Processing dataset: {dataset_name}")

        result = {
            "name": dataset_name,
            "status": "pending",
            "errors": [],
            "warnings": [],
            "metrics": {},
        }

        try:
            # Load raw data
            if not Path(raw_path).exists():
                raise FileNotFoundError(f"Raw data not found: {raw_path}")

            if raw_path.endswith(".csv"):
                data = pd.read_csv(raw_path)
            elif raw_path.endswith(".json"):
                data = pd.read_json(raw_path)
            else:
                raise ValueError(f"Unsupported file format: {raw_path}")

            logger.info(f"Loaded {len(data)} rows from {raw_path}")

            # Apply transformations
            if "transformations" in dataset_config:
                data = transform_pipeline(data, dataset_config["transformations"])
                logger.info(f"Transformations applied. Data now has {len(data)} rows")

            # Validate schema
            if "schema" in dataset_config:
                schema_file = dataset_config["schema"]
                if Path(schema_file).exists():
                    with open(schema_file) as f:
                        import json

                        schema = json.load(f)
                    validation_result = validate_dataframe_schema(data, schema)
                    if not validation_result.is_valid:
                        result["errors"].extend(validation_result.errors)
                    result["warnings"].extend(validation_result.warnings)
                    logger.info(f"Schema validation: {'✓' if validation_result.is_valid else '✗'}")

            # Check integrity
            if "integrity_rules" in dataset_config:
                rules = dataset_config["integrity_rules"]
                integrity_result = check_integrity(
                    data,
                    duplicate_key=rules.get("duplicate_key"),
                    required_fields=rules.get("required_fields"),
                    reject_nulls=rules.get("reject_nulls", True),
                )
                if not integrity_result.is_valid:
                    result["errors"].extend(integrity_result.errors)
                result["warnings"].extend(integrity_result.warnings)

            # Compute quality metrics
            metrics = compute_quality_metrics(data)
            result["metrics"] = metrics
            logger.info(f"Quality metrics: {metrics['row_count']} rows, {metrics['duplicate_count']} duplicates")

            # Export curated data
            Path(curated_path).parent.mkdir(parents=True, exist_ok=True)
            if curated_path.endswith(".csv"):
                export_to_csv(data, curated_path)
            elif curated_path.endswith(".json"):
                export_to_json(data, curated_path)

            result["status"] = "success" if not result["errors"] else "completed_with_errors"
            logger.info(f"Dataset '{dataset_name}' processed: {result['status']}")

        except Exception as e:
            result["status"] = "failed"
            result["errors"].append(str(e))
            logger.error(f"Dataset processing failed: {str(e)}")

        return result

    def process_all_datasets(self) -> Dict[str, Any]:
        """
        Process all configured datasets.

        Returns:
            Summary of all dataset processing
        """
        results = {
            "total": 0,
            "succeeded": 0,
            "failed": 0,
            "datasets": [],
        }

        datasets = self.config.get("datasets", [])
        for dataset_config in datasets:
            raw_path = dataset_config.get("raw_path")
            curated_path = dataset_config.get("curated_path")

            if not raw_path or not curated_path:
                logger.warning(f"Dataset missing raw_path or curated_path: {dataset_config.get('name')}")
                continue

            result = self.process_dataset(dataset_config, raw_path, curated_path)
            results["datasets"].append(result)
            results["total"] += 1

            if result["status"] == "success":
                results["succeeded"] += 1
            else:
                results["failed"] += 1

        logger.info(f"Pipeline complete: {results['succeeded']}/{results['total']} datasets succeeded")
        return results


def orchestrate_pipeline(config_file: str) -> Dict[str, Any]:
    """
    Main entry point for orchestrator.

    Args:
        config_file: Path to YAML config file

    Returns:
        Pipeline execution result
    """
    logger.info(f"Starting pipeline orchestration from {config_file}")
    orchestrator = Orchestrator(config_file)
    return orchestrator.process_all_datasets()
