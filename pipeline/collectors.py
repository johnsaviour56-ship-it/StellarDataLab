"""
Data collection module.

Provides interface for collection scripts and handles common operations like retries.
"""

import importlib.util
import logging
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


def run_collection_script(
    script_path: str,
    function_name: str = "collect",
    config: Optional[Dict[str, Any]] = None,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
) -> Any:
    """
    Run a collection script with retry logic.

    Args:
        script_path: Path to collection script (.py file)
        function_name: Name of function to call (default: 'collect')
        config: Configuration dict to pass to function
        max_retries: Maximum number of retries
        backoff_factor: Backoff multiplier for exponential backoff

    Returns:
        Result from collection function
    """
    config = config or {}

    # Load module from file
    script_name = Path(script_path).stem
    spec = importlib.util.spec_from_file_location(script_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {script_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[script_name] = module
    spec.loader.exec_module(module)

    # Get collection function
    if not hasattr(module, function_name):
        raise RuntimeError(f"Function '{function_name}' not found in {script_path}")

    collect_func = getattr(module, function_name)

    # Execute with retries
    attempt = 0
    last_error = None

    while attempt <= max_retries:
        try:
            logger.info(f"Executing collection (attempt {attempt + 1}/{max_retries + 1})")
            result = collect_func(**config)
            logger.info(f"Collection succeeded on attempt {attempt + 1}")
            return result

        except Exception as e:
            last_error = e
            attempt += 1

            if attempt <= max_retries:
                wait_time = backoff_factor ** (attempt - 1)
                logger.warning(f"Collection failed (attempt {attempt}): {str(e)}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Collection failed after {max_retries + 1} attempts")

    raise RuntimeError(f"Collection failed after {max_retries + 1} attempts: {str(last_error)}")


def validate_collection_script(script_path: str, function_name: str = "collect") -> bool:
    """
    Validate that a collection script has required interface.

    Args:
        script_path: Path to collection script
        function_name: Expected function name

    Returns:
        True if valid, raises exception otherwise
    """
    try:
        spec = importlib.util.spec_from_file_location("test_module", script_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load module from {script_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, function_name):
            raise RuntimeError(f"Function '{function_name}' not found in {script_path}")

        return True
    except Exception as e:
        logger.error(f"Script validation failed: {str(e)}")
        raise
